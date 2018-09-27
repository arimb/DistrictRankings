from functions import getTBAdata

DPs = {}
with open("DistrictRankings/Ranking Points/world_RP.csv") as file:
    allteams = file.readlines()
titles = allteams[0].strip().split(",")
for team in allteams[1:]:
    team = team.strip().split(",")
    key = ("frc" if team[0][:2]=="frc" else "") + team[0]
    DPs[key] = {}
    for i, element in enumerate(team[1:], start=1):
        DPs[key][titles[i]] = float(element)

data = {}

events = getTBAdata("events/2018/simple")
for event in events:
    if event["event_type"]<=5:
        print(event["key"])
        matches = getTBAdata("event/"+event["key"]+"/matches/simple")
        for match in matches:
            if match["comp_level"]=="qm":
                diffRP = round(sum([DPs[team]["Avg Win RP"] for team in match["alliances"]["red"]["team_keys"]]) - sum([DPs[team]["Avg Win RP"] for team in match["alliances"]["blue"]["team_keys"]]), 1)
                if diffRP not in data: data[diffRP] = [0,0]
                data[diffRP][0] += 1 if match["winning_alliance"]=="red" else 0
                data[diffRP][1] += 1

with open("DistrictRankings/Ranking Points/scaling.csv", "w+") as file:
    file.write("RP Difference,Red Win %\n")
    for diffRP in data:
        file.write(str(diffRP) + "," + str(data[diffRP][0]/data[diffRP][1]) + "\n")