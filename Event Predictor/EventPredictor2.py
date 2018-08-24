import re
import random
import tkinter as tk
from tkinter import filedialog

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

teams = [tmp if tmp[:3]=="frc" else ("frc"+tmp) for tmp in (re.split(' ', input("Teams: ")))]
runs = int(input("Iterations: "))

results = {team:[0,0] for team in teams}
for i in range(0, runs):
    print(i)
    random.shuffle(teams)
    winner = sum([DPs[team]["Adj DP"] for team in teams[0:3]]) > sum([DPs[team]["Adj Qual DP"] if team in DPs else 25 for team in teams[3:6]])
    for team in teams[0:6]:
        results[team][1] += 1
    for team in teams[0:3] if winner else teams[3:6]:
        results[team][0] += 1

with open("results.csv", "w+") as file:
    file.write("Team,Wins,Plays,Avg\n")
    for team in results:
        file.write(team + "," + str(results[team][0]) + "," + str(results[team][1]) + "," + str(results[team][0]/results[team][1]) + "\n")