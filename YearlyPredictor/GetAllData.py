from functions import getTBAdata
from scipy.special import erfinv
from math import ceil, exp

def eventDP(event):
    teams = {}
    statuses = getTBAdata("event/" + event + "/teams/statuses")
    num = len(getTBAdata("event/" + event + "/teams/keys"))
    matches = getTBAdata("event/" + event + "/matches/simple")
    for key, t in statuses.items():
        if t is None: continue
        if t["qual"] is None: teams[key] = 0
        else: teams[key] = ceil(7.676 * erfinv(0.934579 + 1.86916 * (1 - t["qual"]["ranking"]["rank"]) / num) + 12)
        if t["alliance"] is not None and t["qual"] is not None:
            teams[key] += ((17-t["alliance"]["number"]) if t["alliance"]["pick"]<2 else t["alliance"]["number"]) if t["alliance"]["pick"]<3 else 0
        if t["playoff"] is not None:
            cnt = 0
            for lvl in ["qf", "sf", "f"]:
                if [0,0,10,20][["ef","qf","sf","f"].index(lvl)] < ([0,0,10,20][["ef","qf","sf","f"].index(t["playoff"]["level"])] if t["playoff"]["status"] == "eliminated" else 30):
                    for m in matches:
                        if m["comp_level"] != lvl: continue
                        if key in m["alliances"]["blue"]["team_keys"] and m["winning_alliance"] == "blue": cnt += 5
                        if key in m["alliances"]["red"]["team_keys"] and m["winning_alliance"] == "red": cnt += 5
            teams[key] += cnt
    return teams

data = {}
years = range(2011,2019)
for year in years:
    yeardp = {}
    events = getTBAdata("events/" + str(year))
    for event in events:
        if event["event_type"] > 5 or len(event["division_keys"]) > 0: continue
        print(event["key"])
        eventdp = eventDP(event["key"])
        for key, dp in eventdp.items():
            if key not in yeardp: yeardp[key] = [0, 0]
            yeardp[key][0] += dp * [1,1,1.1,1.2,1,1.1][event["event_type"]]
            yeardp[key][1] += 1 if event["event_type"] != 4 else 0
    for key, t in yeardp.items():
        if key not in data: data[key] = {}
        data[key][year] = t

with open("DistrictRankings/YearlyPredictor/data.csv", "w+") as file:
    file.write("Team,")
    for y in years:
        file.write(str(y) + ",")
    file.write("Avg\n")
    for key, t in data.items():
        file.write(key + ",")
        avg = 0
        for year in years:
            if year in t:
                a = t[year][0] / t[year][1]**0.7
                file.write(str(a) + ",")
                avg += a*exp(-1.053*(2018-year+1))
            else: file.write(",")
        file.write(str(avg) + "\n")