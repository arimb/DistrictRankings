import requests

def getdata(url):
    try:
        ans = requests.get("https://www.thebluealliance.com/api/v3/" + url,
                           "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
        if ans is not None:
            return ans
        else:
            print("oops null " + url)
            getdata(url)
    except:
        print("oops " + url)
        getdata(url)

teams = {}

events = getdata("events/2018/simple")
for event in events:
    if event["event_type"]<=5:
        matches = getdata("event/"+event["key"]+"/matches")
        for match in matches:
            if match["comp_level"]=="qm":
                for alliance in ["blue","red"]:
                    for team in match["alliances"][alliance]["team_keys"]:
                        if team not in teams: teams[team] = [0,0]
                        teams[team][0] += match["score_breakdown"][alliance]["rp"]
                        teams[team][1] += 1

with open("world_RP.csv", "w+") as file:
    file.write("Team,Avg RP,Adj Avg RP\n")
    for team in teams:
        file.write(team + "," + str(teams[team][0]/teams[team][1]) + "," + str(teams[team][0]/teams[team][1]**0.7) + "\n")