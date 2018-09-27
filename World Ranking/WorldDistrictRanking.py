from functions import getTBAdata

class Team:
    def __init__(self, key, event, DP):
        self.key = key
        self.qual = 0
        self.alliance = 0
        self.playoff = 0
        self.awards = 0
        self.bestPlayoff = 0
        self.bestAlliance = 0
        self.num_events = 0
        self.add_event(event, DP)
    def add_event(self, event, DP):
        if event["event_type"] == 2 or event["event_type"] == 5:
            factor = 0.37
        elif event["event_type"] == 3:
            factor = 1.2
        else:
            factor = 1
        self.qual += DP["qual_points"]*factor
        self.alliance += DP["alliance_points"]*factor
        self.playoff += DP["elim_points"]*factor
        self.awards += DP["award_points"]*factor
        if self.bestPlayoff < DP["elim_points"]:
            self.bestPlayoff = DP["elim_points"]
        if self.bestAlliance < DP["alliance_points"]:
            self.bestAlliance = DP["alliance_points"]
        self.num_events += 1
    def adj(self):
        return (self.qual + self.alliance + self.playoff) * (self.num_events ** -0.7)
    def adjawards(self):
        return (self.qual + self.alliance + self.playoff + self.awards) * (self.num_events ** -0.7)
    def valadj(self, value):
        return value * (self.num_events ** -0.7)

teams = {}
year = 2018

file = open("2018_predcmp_world_DP.csv", "w+")
file.write("Team,# Events,Adj Qual DP,Adj Alliance DP,Adj Playoff DP,Adj Awards DP,Best Alliance,Best Playoff,Adj DP,Adj DP w/Awards\n")
events = getTBAdata("events/"+str(year))
for event in events:
    if 0 <= event["event_type"] <= 1:# or event["event_type"] == 5:
        if len(event["division_keys"]) == 0:
            print(event["key"])
            DPs = getTBAdata("event/"+event["key"]+"/district_points")["points"]
            for teamKey in DPs:
                if teamKey in teams:
                    teams[teamKey].add_event(event, DPs[teamKey])
                else:
                    teams[teamKey] = Team(teamKey, event, DPs[teamKey])

teamlist = sorted(teams, key=lambda key:(teams[key].adjawards(),teams[key].adj(),teams[key].valadj(teams[key].playoff),teams[key].bestPlayoff,
                                         teams[key].valadj(teams[key].alliance),teams[key].valadj(teams[key].alliance),teams[key].bestAlliance,
                                         teams[key].valadj(teams[key].qual)), reverse=True)

for team in teamlist:
    file.write(teams[team].key[3:]+","+str(teams[team].num_events)+","+str(teams[team].valadj(teams[team].qual))+","+
               str(teams[team].valadj(teams[team].alliance))+","+str(teams[team].valadj(teams[team].playoff))+","+
               str(teams[team].valadj(teams[team].awards))+","+str(teams[team].bestAlliance)+","+
               str(teams[team].bestPlayoff)+","+str(teams[team].adj())+","+str(teams[team].adjawards())+"\n")
