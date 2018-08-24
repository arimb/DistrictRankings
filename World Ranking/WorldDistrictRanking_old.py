import requests
from math import ceil
from scipy.special import erfinv

def getdata(url):
    try:
        return requests.get(url, "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
    except:
        print("oops " + url)
        getdata(url)

file = open("prechamps_rankings.csv", "w+")
file.write("Team #,Avg DP,Avg Playoff DP (Tie 1),Best Playoff DP (Tie 2),Avg Alliance DP (Tie 3),Best Alliance DP (Tie 4),Avg Qual DP (Tie 5),Avg No Awards DP, Total DP, # of Events, Champs Registration\n")
for i in range(0, 15):
    teams = getdata("https://www.thebluealliance.com/api/v3/teams/2018/"+str(i))
    for team in teams:
        qualDP = 0
        allianceDP = 0
        playoffDP = 0
        awardDP = 0
        bestAlliance = 0
        bestPlayoff = 0
        num_events = 0
        champs = ""
        eventKeys = getdata("https://www.thebluealliance.com/api/v3/team/"+team["key"]+"/events/2018/keys")
        for eventKey in eventKeys:
            event = getdata("https://www.thebluealliance.com/api/v3/event/"+eventKey+"/simple")
            if event["event_type"] == 3:
                champs = event["name"]
            elif 0 <= event["event_type"] <= 2 or event["event_type"] == 5:
                teamEvent = getdata("https://www.thebluealliance.com/api/v3/team/" + team["key"] + "/event/"+eventKey+"/status")
                if teamEvent is not None:
                    if teamEvent["qual"] is not None:
                        print(teamEvent)
                        qualDP += ceil(erfinv((teamEvent["qual"]["num_teams"]-2*teamEvent["qual"]["ranking"]["rank"]+2)/(1.07*teamEvent["qual"]["num_teams"]))*7.676+12)
                        if teamEvent["alliance"] is not None:
                            allianceDP_ = 17-teamEvent["alliance"]["number"] if teamEvent["alliance"]["pick"] < 2 else teamEvent["alliance"]["number"]
                            allianceDP += allianceDP_
                            if allianceDP_ > bestAlliance:
                                bestAlliance = allianceDP_
                            playoffDP_ = 0 if teamEvent["playoff"]["level"] == "qf" else 10 if teamEvent["playoff"]["level"] == "sf" else 30 if teamEvent["playoff"]["status"] == "won" else 20
                            playoffDP += playoffDP_
                            if playoffDP_ > bestPlayoff:
                                bestPlayoff = playoffDP_
                        num_events += 1
        awards = getdata("https://www.thebluealliance.com/api/v3/team/" + team["key"] + "/awards/2018")
        for award in awards:
            try:
                awardDP += [10, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5][award["award_type"]]
            except IndexError:
                pass
        print(team["team_number"])
        if num_events > 0:
            file.write(str(team["team_number"]) + "," + str((qualDP+allianceDP+playoffDP+awardDP)/num_events) + "," + str(playoffDP/num_events) + "," + str(bestPlayoff) + "," + str(allianceDP/num_events) + "," + str(bestAlliance) + "," + str(qualDP/num_events) + "," + str((qualDP+allianceDP+playoffDP)/num_events) + "," + str(qualDP+allianceDP+playoffDP+awardDP) + "," + str(num_events) + "," + champs + "\n")
        else:
            file.write(str(team["team_number"]) + ",NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN\n")
file.close()