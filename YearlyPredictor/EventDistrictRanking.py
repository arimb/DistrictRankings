from functions import getTBAdata
import csv

allteams = {}
with open("data_award.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        allteams[row["Team"]] = float(row["Avg"])

picks = {}

regionals = ["2019abca","2019casd","2019mnmi","2019nyut","2019alhu","2019casf","2019mnmi2","2019ohcl","2019arli","2019casj","2019mokc","2019ohmv","2019ausc","2019cave","2019mokc3","2019okok","2019ausp","2019code","2019mosl","2019azfl","2019flor","2019mxcm","2019azpx","2019flwp","2019mxmo","2019paca","2019bcvi","2019hiho","2019mxto","2019qcmo","2019caav","2019iacf","2019ndgf","2019qcqc","2019cada","2019idbo","2019nvlv","2019scmb","2019cadm","2019ilch","2019nyli","2019tnkn","2019cafr","2019ilpe","2019nyli2","2019tuis","2019cala","2019ksla","2019nyny","2019tuis2","2019caln","2019lake","2019nyro","2019utwv","2019camb","2019mndu","2019nysu","2019wila","2019caoc","2019mndu2","2019nytr","2019wimi"]
districts = ["2019chs","2019fim","2019fnc","2019in","2019isr","2019ne","2019pch","2019pnw","2019tx","2019ont","2019fma"]

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

with open("picks_award.csv", "w+") as file:
    for name, teams in picks.items():
        file.write(name + ",")
        for t in teams:
            file.write(t[0] + ",")
        file.write("\n")