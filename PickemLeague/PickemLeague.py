import csv
import numpy as np
from keras.models import load_model
from heapq import nlargest

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
    return best

def nth_largest(n, iter):
    return nlargest(n, iter)[-1]

with open("2019_world_DP.csv") as dpfile, open("input.csv") as pricefile:
    teams = {}
    pricereader = csv.DictReader(pricefile)
    for row in pricereader:
        teams[int(row['Team'])] = int(row['Price'])

    allteams = {}
    dpreader = csv.DictReader(dpfile)
    for row in dpreader:
        allteams[int(row['Team'][3:])] = [float(row['Adj Qual DP']), float(row['Adj Alliance DP']), float(row['Adj Playoff DP'])]

model = load_model('model.h5')
teams = {key: [model.predict(np.array([allteams[key]])), price] for key,price in teams.items()}

max_q = max([x[0][0][0] for x in teams.values()])
min_q = min([x[0][0][0] for x in teams.values()])
min_a = nth_largest(32, [x[0][0][1] for x in teams.values()])
print([max_q, min_q, min_a])
for key,val in teams.items():
    val[0][0][0] = 22*(val[0][0][0]-min_q)/(max_q-min_q)
    if val[0][0][1] < min_a:
        val[0][0][1] = 0
        val[0][0][2] = 0
    val[0] = np.sum(val[0])

# maxs = np.amax([x[0] for x in teams.values()], axis=0)
# mins = np.amin([x[0] for x in teams.values()], axis=0)
# print(maxs)
# print(mins)
# teams = {key: [np.multiply([[22,16,30]],np.divide(np.subtract(val[0],mins), np.subtract(maxs, mins))), val[1]] for key,val in teams.items()}

print(teams)
best = (0, [])
print(generate([], 0, 0, teams, 200, 0))