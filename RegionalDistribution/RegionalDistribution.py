from functions import getTBAdata

with open("DistrictRankings/RegionalDistribution/regional_DP_distr.csv", "w+") as file:
    file.write("Event,Team,Rank,Qual,Alliance #,Alliance Pick,Playoff Level,Awards\n")
    events = getTBAdata("events/2018/simple")
    for event in events:
        if event["event_type"] > 0: continue
        print(event)
        DPs = getTBAdata("event/"+event["key"]+"/district_points")["points"]
        ranking = []
        for teamKey in DPs:
            team = getTBAdata("team/"+teamKey+"/event/"+event["key"]+"/status")
            try:
                alliance = {"alliance":team["alliance"]["number"], "pick":team["alliance"]["pick"]+1}
            except:
                alliance = {"alliance":-1, "pick":-1}
            if DPs[teamKey]["award_points"]<10:
                ranking.append({"key":teamKey, "DP":DPs[teamKey], "qual":team["qual"]["ranking"]["rank"], "alliance":alliance})
        ranking.sort(key=lambda x:(x["DP"]["total"],
                                   x["DP"]["elim_points"],
                                   x["DP"]["alliance_points"],
                                   x["DP"]["qual_points"]),reverse=True)
        for team in ranking:
            file.write(event["event_code"] + "," +
                       team["key"] + "," +
                       str(ranking.index(team)+1) + "," +
                       str(team["qual"]) + "," +
                       str(team["alliance"]["alliance"]) + "," +
                       str(team["alliance"]["pick"]) + "," +
                       str(team["DP"]["elim_points"]) + "," +
                       str(team["DP"]["award_points"]) + "\n")
