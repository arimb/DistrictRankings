from functions import get_tba_data, get_data
import csv

prcnt = brier = 0

DPs = {}
with open("../SingleYearDP/2019_precmp_DP_.csv") as dp_file:
    reader = csv.DictReader(dp_file)
    for row in reader:
        DPs[row["Team"]] = float(row["Adj DP"])

events = ["2019carv", "2019gal", "2019hop", "2019new", "2019roe", "2019tur"  ]#, "2019arc", "2019cars", "2019cur", "2019dal", "2019dar", "2019tes"]
# file = open("2019cmp.csv", "w+")
for event in events:
    print(event)
    file = open(event + ".csv", "w+")
    file.write("Match,Red1,Red2,Red3,RedDP,Blue1,Blue2,Blue3,BlueDP,Pred,Result,Correct?,Brier\n")
    # matches = get_tba_data("event/" + event + "/matches")
    matches = get_data("http://arimb.ddns.net/cmp_prelim_sched/" + event + ".json")
    if None not in [m["predicted_time"] for m in matches]: matches.sort(key=lambda x:x["predicted_time"])
    if None not in [m["actual_time"] for m in matches]: matches.sort(key=lambda x: x["actual_time"])

    for match in matches:
        if not match["comp_level"] == 'qm': continue
        file.write(match["key"] + ",")
        teams = []
        points = []
        for alliance in ["red", "blue"]:
            teams.append(match["alliances"][alliance]["team_keys"])
            points.append(sum([DPs[t] for t in teams[-1]]))
            for t in teams[-1]: file.write(t + ",")
            file.write(str(points[-1]) + ",")
        pred = 1/(1+pow(10, (points[0]-points[1])/86))
        file.write(str(pred) + ",")

        if -1 in [match["alliances"][x]["score"] for x in ['red','blue']]:
            file.write("\n")
        else:
            winner = match["winning_alliance"].upper()
            if winner == "": winner = "TIE"
            correct = ("BLUE" if pred>.5 else "RED") == winner
            prcnt += int(correct)
            comp_brier = (pred-{"BLUE":1, "RED":0, "TIE":0.5}[winner])**2
            brier += comp_brier
            file.write(winner + "," + str(correct) + "," + str(comp_brier) + "\n")

    prcnt /= len(matches)
    brier /= len(matches)
    file.write(",,,,,,,,,,," + str(prcnt) + "," + str(brier))
    print(str(prcnt) + "% Predicted")
    print(brier)
    file.close()