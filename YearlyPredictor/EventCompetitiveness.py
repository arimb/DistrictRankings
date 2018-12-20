from functions import getTBAdata
import csv
from scipy.stats.mstats import gmean
from numpy import std

dps = {}
with open("DistrictRankings/YearlyPredictor/data_award.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        dps[row["Team"]] = float(row["Avg"])

scores = []
events = getTBAdata("events/2019/keys")
for event in events:
    print(event)
    teams = getTBAdata("event/" + event + "/teams/keys")
    if len(teams) < 2: continue
    localdps = [dps[t] if t in dps and dps[t]!=0 else 1 for t in teams]
    scores.append((event, gmean(localdps), std(localdps)))

scores = sorted(scores, key=lambda x:x[1]/x[2], reverse=True)

with open("DistrictRankings/YearlyPredictor/ranked_events.csv", "w+") as file:
    file.write("Event,Mean,StDev,Score\n")
    for e in scores:
        file.write(e[0] + "," + str(e[1]) + "," + str(e[2]) + "," + str(e[1]/e[2]) + "\n")
