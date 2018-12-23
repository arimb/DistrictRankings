from functions import getTBAdata

data = {}
events = getTBAdata("events/2018/simple")
for event in events:
    if event["event_type"] > 0: continue
    print(event["key"])
    DPs = getTBAdata("event/" + event["key"] + "/district_points")["points"]
    statuses = getTBAdata("event/" + event["key"] + "/teams/statuses")
    ranking = []
    for teamKey, dp in DPs.items():
        try:
            alliance = {"alliance":statuses[teamKey]["alliance"]["number"], "pick":statuses[teamKey]["alliance"]["pick"]+1}
        except:
            alliance = {"alliance":-1, "pick":-1}
        if dp["award_points"]<10:
            ranking.append({"key":teamKey, "DP":dp, "qual":statuses[teamKey]["qual"]["ranking"]["rank"], "alliance":alliance})
    ranking.sort(key=lambda x:(x["DP"]["total"],
                               x["DP"]["elim_points"],
                               x["DP"]["alliance_points"],
                               x["DP"]["qual_points"]),reverse=True)
    data[event["key"]] = ranking

with open("DistrictRankings/RegionalDistribution/regionals.csv", "w+") as file:
    file.write("Event,Team,DP Rank,Qual Rank,Alliance #,Alliance Pick,Qual DP,Alliance DP,Playoff DP,Awards DP,Total DP\n")
    for event, ranking in data.items():
        for i, team in enumerate(ranking, start=1):
            file.write(event + "," +
                       team["key"] + "," +
                       str(i) + "," +
                       str(team["qual"]) + "," +
                       str(team["alliance"]["alliance"]) + "," +
                       str(team["alliance"]["pick"]) + "," +
                       str(team["DP"]["qual_points"]) + "," +
                       str(team["DP"]["alliance_points"]) + "," +
                       str(team["DP"]["elim_points"]) + "," +
                       str(team["DP"]["award_points"]) + "," +
                       str(team["DP"]["total"]) + "\n")
