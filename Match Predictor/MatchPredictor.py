import requests
import tkinter as tk
from tkinter import filedialog

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
def gmean(numbers):
    mean = 1
    for x in numbers:
        mean *= x
    return pow(mean, 1/len(numbers))

def predict(event):
    print(event)
    matches = getdata("event/" + event + "/matches")
    try:
        matches = sorted(matches, key=lambda x: x["predicted_time"])
    except:
        try:
            matches = sorted(matches, key=lambda x: x["actual_time"])
        except:
            pass
    results = []
    teams = {}
    for match in matches:
        redteams = match["alliances"]["red"]["team_keys"]
        blueteams = match["alliances"]["blue"]["team_keys"]
        red = gmean([float(DPs[team]["Adj DP"]) if team in DPs else 25 for team in redteams]) if ver == 1 \
            else sum([float(DPs[team]["Adj Qual DP"]) if team in DPs else 25 for team in redteams]) if ver == 2 \
            else sum([float(DPs[team]["Adj DP"]) if team in DPs else 25 for team in redteams])
        blue = gmean([float(DPs[team]["Adj DP"]) if team in DPs else 25 for team in blueteams]) if ver == 1 \
            else sum([float(DPs[team]["Adj Qual DP"]) if team in DPs else 25 for team in blueteams]) if ver == 2 \
            else sum([float(DPs[team]["Adj DP"]) if team in DPs else 25 for team in blueteams])
        predict = "RED" if red > blue else "BLUE"
        prob = 1 / (1 + pow(10, ((red - blue) / (23 if ver == 1 else 20 if ver == 2 else 80))))
        if -1 in [match["alliances"]["red"]["score"], match["alliances"]["blue"]["score"]]:
            winner = "N/A"
            correct = "N/A"
            brier = "N/A"
        else:
            winner = match["winning_alliance"].upper()
            correct = (predict == winner)
            brier = pow(prob - int(winner == "BLUE"), 2)
        results.append((match["key"], redteams, blueteams, red, blue, predict, prob, winner, correct, brier))
        for team in redteams:
            if team not in teams:
                teams[team] = {"wins": 0, "losses": 0, "played": 0}
            if team not in match["alliances"]["red"]["surrogate_team_keys"]:
                teams[team]["played"] += 1
                if red > blue:
                    teams[team]["wins"] += 1
                else:
                    teams[team]["losses"] += 1
        for team in blueteams:
            if team not in teams:
                teams[team] = {"wins": 0, "losses": 0, "played": 0}
            if team not in match["alliances"]["blue"]["surrogate_team_keys"]:
                teams[team]["played"] += 1
                if red < blue:
                    teams[team]["wins"] += 1
                else:
                    teams[team]["losses"] += 1

    brier = 0
    avg = 0
    num_matches = 0
    for result in results:
        if isinstance(result[9], float):
            brier += result[9]
            avg += int(result[8])
            num_matches += 1
    if num_matches == 0:
        brier = "N/A"
        avg = "N/A"
        print("No matches played")
    else:
        brier /= num_matches
        avg /= num_matches
        print(("%.2f" % (avg*100)) + "% correctly predicted")
        print("Brier Score: " + ("%.3f" % brier))

    teams = list(teams.items())
    teams = sorted(teams, key=lambda x: x[0])
    teams = sorted(teams, key=lambda x: x[1]["losses"])
    teams = sorted(teams, key=lambda x: x[1]["wins"], reverse=True)

    rankings = getdata("event/"+event+"/rankings")["rankings"]
    try:
        rankings = [(x["team_key"], (x["record"], x["matches_played"])) for x in rankings]
        rankings = dict(rankings)
    except:
        rankings = {}

    with open(event + "_results" + ("_geom" if ver == 1 else "_qual" if ver == 2 else "_adj") + ".csv", "w+") as file:
        file.write(
            event + "\nMatch Key,Red 1,Red 2,Red 3,Blue 1,Blue 2,Blue 3,Red DP,Blue DP,Prediction,Blue Win %,Winner,Correct,Component Brier Score\n")
        for result in results:
            file.write(result[0] + "," +
                       result[1][0][3:] + "," + result[1][1][3:] + "," + result[1][2][3:] + "," +
                       result[2][0][3:] + "," + result[2][1][3:] + "," + result[2][2][3:] + "," +
                       str(result[3]) + "," + str(result[4]) + "," +
                       result[5] + "," + str(result[6]) + "," +
                       result[7] + "," + str(result[8]) + "," + str(result[9]) + "\n")
        file.write("Average,,,,,,,,,,,% Correct->," + str(avg) + "," + str(brier) + ",<-Brier Score\n")
        file.write("\nPredicted Rankings\nRank,Team,Proj. Wins,Proj. Losses,Proj Win %" + (",Real Wins,Real Losses,Real Ties,Real Win %" if len(rankings)>0 else "") + "\n")
        for i, team in enumerate(teams, start=1):
            file.write(str(i) + "," + team[0] + "," + str(team[1]["wins"]) + "," + str(team[1]["losses"]) + "," +
                       str(team[1]["wins"]/team[1]["played"]))
            try:
                file.write("," + (str(rankings[team[0]][0]["wins"]) + "," + str(rankings[team[0]][0]["losses"]) + "," +
                            str(rankings[team[0]][0]["ties"])) + "," + str(rankings[team[0]][0]["wins"]/rankings[team[0]][1]) + "\n")
            except:
                file.write("\n")

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

events = input("Event Key: ")
for event in events.split(" "):
    for ver in range(0,3):
        predict(event)