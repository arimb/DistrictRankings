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
    DPs["frc" + team[0]] = {}
    for i, element in enumerate(team[1:], start=1):
        DPs["frc" + team[0]][titles[i]] = float(element)

# teams = [tmp if tmp[:3]=="frc" else ("frc"+tmp) for tmp in (re.split(' ', input("Teams: ")))]
teams = getdata("event/"+input("event: ")+"/teams/keys")
matches = int(input("Matches per Team: "))
runs = int(input("Iterations: "))

results = {team:[0,0] for team in teams}
for i in range(runs):
    print(i)
    ev = {team:[0,0] for team in teams}
    for j in range(int(len(teams)*matches/6)):
        random.shuffle(teams)
        winner = sum([DPs[team]["Adj Qual DP"] for team in teams[0:3]]) > sum([DPs[team]["Adj Qual DP"] for team in teams[3:6]])
        for team in teams[0:6]:
            ev[team][1] += 1
        for team in teams[0:3] if winner else teams[3:6]:
            ev[team][0] += 1
    ev = sorted([(ev[tmp][0]/ev[tmp][1], tmp) for tmp in ev])
    for rank, team in enumerate(ev, start=1):
        print(type(team[1]))
        print(team[1])
        results[team[1]] += rank

for team in results:
    results[team] /= runs

with open("cc.csv", "w+") as file:
    file.write("Team,Wins,Plays,Avg\n")
    for team in results:
        file.write(team + "," + str(results[team][0]) + "," + str(results[team][1]) + "," + str(results[team][0]/results[team][1]) + "\n")