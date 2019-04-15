from functions import get_tba_data
import csv

prcnt = brier = 0

DPs = {}
with open("../SingleYearDP/2018_precmp_DP_.csv") as dp_file:
    reader = csv.DictReader(dp_file)
    for row in reader:
        DPs[row["Team"]] = float(row["Adj DP"])

events = ["2018carv", "2018gal", "2018hop", "2018new", "2018roe", "2018tur", "2018arc", "2018cars", "2018cur", "2018dal", "2018dar", "2018tes"]
for event in events:
    print(event)
    file = open(event + ".csv", "w+")
    file.write("Match,Blue1,Blue2,Blue3,BlueDP,Red1,Red2,Red3,RedDP,Pred,Result,Correct?,Brier\n")
    matches = get_tba_data("event/" + event + "/matches")
    if None not in [m["predicted_time"] for m in matches]: matches.sort(key=lambda x:x["predicted_time"])
    if None not in [m["actual_time"] for m in matches]: matches.sort(key=lambda x: x["actual_time"])

    for match in matches:
        teams = []
        points = []
        for alliance in ["blue", "red"]:
            teams.append(match["alliances"][alliance]["team_keys"])
            points.append(sum([DPs[t] for t in teams[-1]]))
            for t in teams[-1]: file.write(t + ",")
            file.write(str(points[-1]) + ",")
        pred = 1/(1+pow(10, (points[0]-points[1])/23))
        file.write(str(pred) + ",")

        print(match["alliances"])
        if -1 in match["alliances"]["blue","red"]["score"]:
            file.write("\n")
        else:
            winner = match["winning_alliance"].upper()
            if winner == "": winner = "TIE"
            correct = ("BLUE" if pred>.5 else "RED") == winner
            prcnt += int(correct)
            comp_brier = (pred-{"BLUE":1, "RED":0, "TIE":0.5}[winner])
            brier += comp_brier
            file.write(winner + "," + str(correct) + "," + str(comp_brier) + "\n")
    file.close()