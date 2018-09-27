from functions import getTBAdata

teams = {}

events = getTBAdata("events/2018/simple")
for event in events:
    if event["event_type"]<=5:
        print(event["key"])
        matches = getTBAdata("event/"+event["key"]+"/matches")
        for match in matches:
            if match["comp_level"]=="qm":
                for alliance in ["blue","red"]:
                    for team in match["alliances"][alliance]["team_keys"]:
                        if team not in teams: teams[team] = [0,0,0,0]
                        teams[team][0] += 1
                        teams[team][1] += 2 if match["winning_alliance"]==alliance else 0
                        teams[team][2] += 1 if match["score_breakdown"][alliance]["autoQuestRankingPoint"] else 0
                        teams[team][3] += 1 if match["score_breakdown"][alliance]["faceTheBossRankingPoint"] else 0

with open("world_RP.csv", "w+") as file:
    file.write("Team,Avg Win RP,Adj Auto RP,Avg Climb RP\n")
    for team in teams:
        file.write(team + "," + str(teams[team][1]/teams[team][0]) + "," + str(teams[team][2]/teams[team][0]) + "," + str(teams[team][3]/teams[team][0]) + "\n")