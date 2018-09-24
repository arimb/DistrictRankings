import random
import math
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
teams = getdata("event/"+event+"/teams/keys")
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
        redwins = random.random() <= 1/(1+math.exp(-3.5*(sum([DPs[team]["Avg Win RP"] for team in playing[:3]])-sum([DPs[team]["Avg Win RP"] for team in playing[3:]]))))
        for team in playing:
            ev[team][1] += 1
        for team in playing[:3] if redwins else playing[3:]:
            ev[team][0] += 2
        for alliance in [playing[:3], playing[3:]]:
            if 3 * random.random() <= sum([DPs[team]["Avg Auto RP"] for team in alliance]):
                for team in alliance:
                    ev[team][0] += 1
            if 3 * random.random() <= sum([DPs[team]["Avg Climb RP"] for team in alliance]):
                for team in alliance:
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