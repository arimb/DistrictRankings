import random
import math
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

event = input("event: ")
teams = getTBAdata("event/"+event+"/teams/keys")
matches = getTBAdata("event/"+event+"/matches/simple")
runs = int(input("Iterations: "))

results = {team:[0]*len(teams) for team in teams}
avg = {team:0 for team in teams}
match_results = [0]*len(matches)
auto_results = [[0,0] for i in matches]
climb_results = [[0,0] for i in matches]
for i in range(runs):
    print(i)
    ev = {team:[0,0] for team in teams}
    for match in matches:
        if match["comp_level"]!= "qm": continue
        playing = match["alliances"]["red"]["team_keys"] + match["alliances"]["blue"]["team_keys"]
        redwins = random.random() <= 1/(1+math.exp(-3.5*(sum([DPs[team]["Avg Win RP"] for team in playing[:3]])-sum([DPs[team]["Avg Win RP"] for team in playing[3:]]))))
        match_results[match["match_number"]-1] += redwins
        for team in playing:
            ev[team][1] += 1
        for team in playing[:3] if redwins else playing[3:]:
            ev[team][0] += 2
        for x, alliance in enumerate([playing[:3], playing[3:]]):
            if random.random() <= .95: # sum([DPs[team]["Avg Auto RP"] for team in alliance]):
                auto_results[match["match_number"]-1][x] += 1
                for team in alliance:
                    ev[team][0] += 1
            if 3*random.random() <= sum([DPs[team]["Avg Climb RP"] for team in alliance]):
                climb_results[match["match_number"]-1][x] += 1
                for team in alliance:
                    ev[team][0] += 1
    ev = sorted([(ev[tmp][0]/ev[tmp][1], tmp) for tmp in ev], reverse=True)
    for rank, team in enumerate(ev, start=1):
        results[team[1]][rank-1] += 1
        avg[team[1]] += rank

with open("DistrictRankings/Match Predictor/"+event+".csv", "w+") as file:
    file.write("Team,Avg Rank,")
    for i in range(len(teams)):
        file.write(str(i+1) + ",")
    file.write("\n")
    for team in avg:
        file.write(team[3:] + "," + str(avg[team]/runs) + ",")
        for x in results[team]:
            file.write(str(x/runs) + ",")
        file.write("\n")

with open("DistrictRankings/Match Predictor/"+event+"_matches.csv", "w+") as file:
    file.write("Match,Red Win %,Red Auto,Red Climb,Blue Auto,Blue Climb\n")
    for num, (match, auto, climb) in enumerate(zip(match_results, auto_results, climb_results), start=1):
        file.write(str(num) + "," + str(match/runs) + "," + str(auto[0]/runs) + "," + str(climb[0]/runs) + "," +
                   str(auto[1]/runs) + "," + str(climb[1]/runs) + "\n")
