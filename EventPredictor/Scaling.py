from functions import getTBAdata
import csv

DPs = {}
with open("DistrictRankings/SingleYearDP/2018_prechamps_world_DP.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        DPs[row["Team"]] = float(row["Adj DP"])

data = {}
events = getTBAdata("events/2018/simple")
for event in events:
    if event["event_type"] not in [3,4]: continue
    print(event["key"])
    matches = getTBAdata("event/" + event["key"] + "/matches/simple")
    for match in matches:
        diffDP = sum([DPs[t] for t in match["alliances"]["red"]["team_keys"]]) - sum([DPs[t] for t in match["alliances"]["blue"]["team_keys"]])
        bin = round(diffDP/10)*10
        if bin not in data: data[bin] = [0, 0]
        data[bin][0] += {"red":1, "blue":0, "":0.5}[match["winning_alliance"]]
        data[bin][1] += 1

with open("DistrictRankings/Event Predictor/scaling.csv", "w+") as file:
    file.write("DiffDP,Win\n")
    for bin, d in data.items():
        file.write(str(bin) + "," + str(d[0]/d[1]) + '\n')