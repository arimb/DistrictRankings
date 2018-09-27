from math import ceil
from scipy.special import erfinv
from functions import getTBAdata


class Team:
    def __init__(self, event, status, OPR):
        self.DPs = [0] * (2018-2010+1)
        self.OPRs = [0] * (2018-2010+1)
        self.ranks = [0] * (2018-2010+1)
        self.numevents = [0] * (2018-2010+1)
        self.add_event(event, status, OPR)

    def add_event(self, event, status, OPR):
        if event["event_type"] == 2 or event["event_type"] == 5:
            factor = 0.37
        elif event["event_type"] == 3:
            factor = 1.2
        else:
            factor = 1

        if status is not None:
            if status["qual"] is not None:
                if status["qual"]["ranking"] is not None:
                    if status["qual"]["ranking"]["rank"] is not None:
                        self.DPs[event["year"] - 2010] += ceil(erfinv((status["qual"]["num_teams"]-2*status["qual"]["ranking"]["rank"]+2)/(1.07*status["qual"]["num_teams"]))*7.676+12) * factor
                        self.numevents[event["year"] - 2010] += 1
                        if status["alliance"] is not None:
                            self.DPs[event["year"] - 2010] += (17-status["alliance"]["number"] if status["alliance"]["pick"] < 2 else status["alliance"]["number"]) * factor
                            self.DPs[event["year"] - 2010] += (0 if status["playoff"]["level"] == "qf" else 10 if status["playoff"]["level"] == "sf" else 30 if status["playoff"]["status"] == "won" else 20) * factor
                        self.OPRs[event["year"]-2010] = (self.OPRs[event["year"]-2010]*(self.numevents[event["year"]-2010]-1)+OPR)/self.numevents[event["year"]-2010]
                        self.ranks[event["year"] - 2010] = (self.ranks[event["year"] - 2010] * (self.numevents[event["year"] - 2010] - 1) + status["qual"]["ranking"]["rank"]) / self.numevents[event["year"] - 2010]

    def calc(self):
        tmp = ""
        for year in range(2018-2010+1):
            if self.numevents[year] > 0 and self.DPs[year] > 0:
                tmp+=str(self.DPs[year]/pow(self.numevents[year],0.7)) + "," + str(self.OPRs[year]) + "," + str(self.ranks[year]) + "," + str(self.numevents[year]) + ","
            else:
                tmp+=",,,,"
        return tmp

teams = {}

file = open("yearly_dp_.csv", "w+")
file.write("Team #,")

for year in range(2010, 2018+1):
    file.write(str(year) + " DP," + str(year) + " OPR," + str(year) + " Rank," + str(year) + " Num Events,")
    events = getTBAdata("events/" + str(year))
    for event in events:
        if 0 <= event["event_type"] <= 3 or event["event_type"] == 5:
            if len(event["division_keys"]) == 0:
                print(event["key"])
                statuses = getTBAdata("event/" + event["key"] + "/teams/statuses")
                oprs = getTBAdata("event/" + event["key"] + "/oprs")["oprs"]
                for teamKey in statuses:
                    print(statuses[teamKey])
                    if teamKey in oprs:
                        if teamKey in teams:
                            teams[teamKey].add_event(event, statuses[teamKey], oprs[teamKey])
                        else:
                            teams[teamKey] = Team(event, statuses[teamKey], oprs[teamKey])

file.write("\n")
for team in teams:
    file.write(team[3:] + "," + teams[team].calc() + "\n")