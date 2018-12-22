import random
import math
from functions import getTBAdata
import csv

DPs = {}
with open("DistrictRankings/SingleYearDP/2018_world_DP.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        DPs[row["Team"]] = float(row["Adj DP"])

event = input("event: ")
teams = getTBAdata("event/"+event+"/teams/keys")
num_matches = int(input("Matches per Team: "))
with open("DistrictRankings/Event Predictor/schedules/"+str(len(teams))+"_"+str(num_matches)+".csv") as file:
    matches = file.readlines()
matches = [[int(x) for x in match.strip().split(",")[0::2]] for match in matches]
runs = int(input("Iterations: "))

results = {team:[0]*len(teams) for team in teams}
avg = {team:0 for team in teams}
for i in range(runs):
    print(i)
    random.shuffle(teams)
    ev = {team:[0,0] for team in teams}
    for match in matches:
        playing = [teams[x-1] for x in match]
        redwins = random.random() <= 1/(1+math.exp(-(sum([DPs[team] for team in playing[:3]])-sum([DPs[team] for team in playing[3:]]))/38))
        for team in playing:
            ev[team][1] += 1
        for team in playing[:3] if redwins else playing[3:]:
            ev[team][0] += 1
    ev = sorted([(ev[tmp][0]/ev[tmp][1], tmp) for tmp in ev], reverse=True)
    for rank, team in enumerate(ev, start=1):
        results[team[1]][rank-1] += 1
        avg[team[1]] += rank

with open("DistrictRankings/Event Predictor/"+event+".csv", "w+") as file:
    file.write("Team,Avg Rank,")
    for i in range(len(teams)):
        file.write(str(i+1) + ",")
    file.write("\n")
    for team in avg:
        file.write(team[3:] + "," + str(avg[team]/runs) + ",")
        for x in results[team]:
            file.write(str(x/runs) + ",")
        file.write("\n")