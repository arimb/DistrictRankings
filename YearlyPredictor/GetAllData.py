from functions import getTBAdata
from scipy.special import erfinv
from math import ceil, exp

awarddp = {
    0: 60,
    3: 10,
    6: 5,
    7: 5,
    8: 5,
    9: 45,
    10: 25,
    11: 5,
    12: 5,
    13: 5,
    15: 5,
    16: 20,
    17: 20,
    18: 5,
    19: 5,
    20: 20,
    21: 20,
    22: 5,
    23: 20,
    26: 20,
    27: 5,
    28: 5,
    29: 20,
    30: 5,
    31: 5,
    64: 5,
    69: 45,
    71: 20
}

def eventDP(event):
    teams = {}
    statuses = getTBAdata("event/" + event + "/teams/statuses")
    num = len(getTBAdata("event/" + event + "/teams/keys"))
    matches = getTBAdata("event/" + event + "/matches/simple")
    awards = getTBAdata("event/" + event + "/awards")
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
    for a in awards:
        if a["award_type"] not in awarddp: continue
        for t in a["recipient_list"]:
            if t["team_key"] is None: continue
            if t["team_key"] not in teams:
                print("^^^^ " + t["team_key"])
                continue
            teams[t["team_key"]] += awarddp[a["award_type"]]
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

with open("DistrictRankings/YearlyPredictor/data_award.csv", "w+") as file:
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
                avg += a*1.7*exp(-0.9933*(2018-year+1))
            else: file.write(",")
        file.write(str(avg) + "\n")