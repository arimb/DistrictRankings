import csv

def generate(current, currentsum, currentprice, lst, shekels, i):
    global best
    newlst = dict(lst)
    for team in lst:
        del newlst[team]
        if i==2:print(current+[team])
        if currentprice + teams[team][1] <= shekels:
            if currentsum + teams[team][0] > best[0]:
                best = (currentsum + teams[team][0], current+[team])
                print(best)
            if len(lst)>1:
                generate(current+[team], currentsum+teams[team][0], currentprice+teams[team][1], newlst, shekels, i+1)
                # {key: val for key, val in lst.items() if key < team}
    return best

with open("2019_world_DP.csv") as dpfile, open("input.csv") as pricefile:
    allteams = {}
    dpreader = csv.DictReader(dpfile)
    for row in dpreader:
        allteams[int(row["Team"][3:])] = float(row["Adj Alliance DP"])+float(row["Adj Playoff DP"])

    teams = {}
    pricereader = csv.DictReader(pricefile)
    for row in pricereader:
        teams[int(row["Team"])] = (allteams[int(row["Team"])], int(row["Price"]))
    del allteams
    # for t,x in sorted(teams.items(), key=lambda y:y[1][0][1], reverse=True)[32:]:
    #     teams[t][0][0] -= teams[t][0][1]*0.75
    # teams = {key:(val[0][0], val[1]) for key,val in teams.items()}

    # min_play = min([x[0][1] for key,x in teams.items()])
    # teams = {key:(val[0][0]-min_play*0.75, val[1]) for key, val in teams.items()}

best = (0, [])
print(generate([], 0, 0, teams, 200, 0))