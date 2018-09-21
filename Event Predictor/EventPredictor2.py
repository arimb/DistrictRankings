# import re
import random
import tkinter as tk
from tkinter import filedialog
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
tk.Tk().withdraw()
with open(filedialog.askopenfilename()) as file:
    allteams = file.readlines()
titles = allteams[0].strip().split(",")
for team in allteams[1:]:
    team = team.strip().split(",")
    key = ("frc" if team[0][:2]=="frc" else "") + team[0]
    DPs[key] = {}
    for i, element in enumerate(team[1:], start=1):
        DPs[key][titles[i]] = float(element)

# teams = [tmp if tmp[:3]=="frc" else ("frc"+tmp) for tmp in (re.split(' ', input("Teams: ")))]
teams = getdata("event/"+input("event: ")+"/teams/keys")
matches = int(input("Matches per Team: "))
runs = int(input("Iterations: "))

results = {team:0 for team in teams}
for i in range(runs):
    print(i)
    ev = {team:[0,0] for team in teams}
    while True:
        try:
            for j in range(int(len(teams)*matches/6)):
                random.shuffle(teams)
                redwins = sum([DPs[team]["Avg Win RP"] for team in teams[0:3]]) > sum([DPs[team]["Avg Win RP"] for team in teams[3:6]])
                for team in teams[0:6]:
                    ev[team][1] += 1
                for team in teams[0:3] if redwins else teams[3:6]:
                    ev[team][0] += 2
                if 3*random.random() <= sum([DPs[team]["Avg Auto RP"] for team in teams[0:3]]):
                    for team in teams[0:3]:
                        ev[team][0] += 1
                if 3*random.random() <= sum([DPs[team]["Avg Climb RP"] for team in teams[0:3]]):
                    for team in teams[0:3]:
                        ev[team][0] += 1
                if 3*random.random() <= sum([DPs[team]["Avg Auto RP"] for team in teams[3:6]]):
                    for team in teams[3:6]:
                        ev[team][0] += 1
                if 3*random.random() <= sum([DPs[team]["Avg Climb RP"] for team in teams[3:6]]):
                    for team in teams[3:6]:
                        ev[team][0] += 1
            ev = sorted([(ev[tmp][0]/ev[tmp][1], tmp) for tmp in ev], reverse=True)
            break
        except:
            pass
    for rank, team in enumerate(ev, start=1):
        results[team[1]] += rank

for team in results:
    results[team] /= runs

with open("2018cc.csv", "w+") as file:
    file.write("Team,Avg Rank\n")
    for team in results:
        file.write(team[3:] + "," + str(results[team]) + "\n")