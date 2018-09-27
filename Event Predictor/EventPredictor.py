import tkinter as tk
from tkinter import filedialog
from operator import itemgetter
from functions import getTBAdata

DPs = {}
tk.Tk().withdraw()
with open(filedialog.askopenfilename()) as file:
    allteams = file.readlines()
titles = allteams[0].strip().split(",")
for team in allteams[1:]:
    team = team.strip().split(",")
    DPs["frc" + team[0]] = {}
    for i, element in enumerate(team[1:], start=1):
        DPs["frc" + team[0]][titles[i]] = element

teams = []
competing = getTBAdata("event/" + input("Event Key: ") + "/teams/keys")
for team in competing:
    teams.append((team, float(DPs[team]["AdjDP"])))
teams = sorted(teams, key=itemgetter(1), reverse=True)
print(teams)