import csv
import requests

def getdata(url):
    try:
        ans = requests.get("https://www.thebluealliance.com/api/v3/" + url,
                           "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
        if ans is not None:
            return ans
        else:
            print("oops null " + url)
            return getdata(url)
    except:
        print("oops " + url)
        return getdata(url)

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def generate(current, lst, shekels):
    global best
    currentprice = sum([teams[x][1] for x in current])
    for team in lst:
        if len(current)==4:print(current+[team])
        if currentprice + teams[team][1] <= shekels:
            if sum([teams[x][0] for x in current]) + teams[team][0] > best[0]:
                best = (sum([teams[x][0] for x in best[1]]) + teams[team][0], current+[team])
                print(best)
            if len(lst)>1:
                generate(current+[team], removekey(lst,team), shekels)

with open("DistrictRankings/World Ranking/2018_world_DP.csv") as dpfile, open("DistrictRankings/Pickem League/input.csv") as pricefile:
    allteams = {}
    dpreader = csv.DictReader(dpfile)
    for row in dpreader:
        allteams[row["Team"]] = row["Adj DP"]

    teams = {}
    pricereader = csv.DictReader(pricefile)
    for row in pricereader:
        teams[row["Team"]] = (float(allteams[row["Team"]]), int(row["Price"]))
    del allteams

best = (0, [])
generate([], teams, 200)
print(best)