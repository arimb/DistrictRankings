import requests

def getdata(url):
    try:
        return requests.get(url, "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
    except:
        print("oops " + url)
        getdata(url)

file = open("regional_DP_placement_aw.csv", "w+")
file.write("Event,Team,Rank,Qual,Alliance #,Alliance Pick,Playoff Level,Awards\n")
events = getdata("https://www.thebluealliance.com/api/v3/events/2018/simple")
for event in events:
    if event["event_type"] == 0:
        print(event)
        DPs = getdata("https://www.thebluealliance.com/api/v3/event/"+event["key"]+"/district_points")["points"]
        ranking = []
        for teamKey in DPs:
            print(DPs[teamKey])
            team = getdata("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/"+event["key"]+"/status")
            try:
                alliance = {"alliance":team["alliance"]["number"], "pick":team["alliance"]["pick"]+1}
            except:
                alliance = {"alliance":-1, "pick":-1}
            if DPs[teamKey]["award_points"]<10:
                ranking.append({"key":teamKey, "DP":DPs[teamKey], "qual":team["qual"]["ranking"]["rank"], "alliance":alliance})
        ranking.sort(key=lambda x:x["DP"]["qual_points"], reverse=True)
        ranking.sort(key=lambda x:x["DP"]["alliance_points"],reverse=True)
        ranking.sort(key=lambda x:x["DP"]["elim_points"], reverse=True)
        ranking.sort(key=lambda x:x["DP"]["total"],reverse=True)
        for team in ranking:
            file.write(event["event_code"]+"," + team["key"] + "," + str(ranking.index(team)+1) + "," + str(team["qual"]) + "," +
                       str(team["alliance"]["alliance"]) + "," + str(team["alliance"]["pick"]) + "," + str(team["DP"]["elim_points"]) + "," +
                       str(team["DP"]["award_points"]) + "\n")
