import requests
import csv
from math import exp

def getTBAdata(url, retry=True):
    try:
        ans = requests.get("https://www.thebluealliance.com/api/v3/" + url,
                           "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
        if ans is not None:
            return ans
        else:
            print("oops null " + url)
            return getTBAdata(url) if retry else None
    except:
        print("oops " + url)
        return getTBAdata(url) if retry else None

allteams = {}
with open("DistrictRankings/YearlyPredictor/data.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        allteams[row["Team"]] = float(row["Avg"])

picks = {}

regionals = input("Regionals:").split("|")
districts = input("Districts:").split("|")

for event in regionals:
    teams = getTBAdata("event/" + event + "/teams/keys")
    ranked = []
    for t in teams:
        try:
            ranked.append((t, allteams[t]))
        except:
            ranked.append((t, 0))
    ranked = sorted(ranked, key=lambda x:x[1], reverse=True)
    print(event)
    picks[event] = ranked

for district in districts:
    teams = getTBAdata("district/" + district + "/teams/keys")
    ranked = []
    for t in teams:
        try:
            ranked.append((t, allteams[t]))
        except:
            ranked.append((t, 0))
    ranked = sorted(ranked, key=lambda x: x[1], reverse=True)
    print(district)
    picks[district] = ranked

with open("DistrictRankings/YearlyPredictor/picks.csv", "w+") as file:
    for name, teams in picks.items():
        file.write(name + ",")
        for t in teams:
            file.write(t[0] + ",")
        file.write("\n")