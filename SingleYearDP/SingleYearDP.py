from functions import get_tba_data

class Team:
    def __init__(self, key):
        self.key = key
        self.qual = 0
        self.alliance = 0
        self.playoff = 0
        self.awards = 0
        self.bestPlayoff = 0
        self.bestAlliance = 0
        self.num_events = 0
    def add_event(self, event, DP):
        factor = [1, 1, 0.37, 1.2, 0, 0.37][event["event_type"]]
        self.qual += DP["qual_points"]*factor
        self.alliance += DP["alliance_points"]*factor
        self.playoff += DP["elim_points"]*factor
        self.awards += DP["award_points"]*factor
        self.bestPlayoff = max(self.bestPlayoff, DP["elim_points"]*factor)
        self.bestAlliance = max(self.bestAlliance, DP["alliance_points"]*factor)
        self.num_events += 1
    def adj(self):
        return (self.qual + self.alliance + self.playoff) / (self.num_events ** 0.7)
    def adjawards(self):
        return (self.qual + self.alliance + self.playoff + self.awards) / (self.num_events ** 0.7)
    def valadj(self, value):
        return value * (self.num_events ** -0.7)

teams = {}
year = 2019

events = get_tba_data("events/"+str(year))
for event in events:
    # if event["event_type"] == 4 or event["event_type"] > 5 or len(event["division_keys"]) > 0: continue     #All Events
    if event["event_type"] not in [0,1,2,5] or len(event["division_keys"]) > 0: continue     #Pre-Champs
    #if event["event_type"] > 1 or len(event["division_keys"]) > 0: continue     #Pre-DCMP
    print(event["key"])
    DPs = get_tba_data("event/"+event["key"]+"/district_points")["points"]
    for teamKey in DPs:
        if teamKey not in teams:
            teams[teamKey] = Team(teamKey)
        teams[teamKey].add_event(event, DPs[teamKey])

teamlist = sorted(teams, key=lambda key:(teams[key].adjawards(),
                                         teams[key].adj(),
                                         teams[key].valadj(teams[key].playoff),
                                         teams[key].bestPlayoff,
                                         teams[key].valadj(teams[key].alliance),
                                         teams[key].valadj(teams[key].alliance),
                                         teams[key].bestAlliance,
                                         teams[key].valadj(teams[key].qual)), reverse=True)

with open("2019_precmp_DP_.csv", "w+") as file:
    file.write("Team,# Events,Adj Qual DP,Adj Alliance DP,Adj Playoff DP,Adj Awards DP,Best Alliance,Best Playoff,Adj DP,Adj DP w/Awards\n")
    for team in teamlist:
        file.write(teams[team].key + "," +
                   str(teams[team].num_events) + "," +
                   str(teams[team].valadj(teams[team].qual)) + "," +
                   str(teams[team].valadj(teams[team].alliance)) + "," +
                   str(teams[team].valadj(teams[team].playoff)) + "," +
                   str(teams[team].valadj(teams[team].awards)) + "," +
                   str(teams[team].bestAlliance) + "," +
                   str(teams[team].bestPlayoff) + "," +
                   str(teams[team].adj()) + "," +
                   str(teams[team].adjawards()) + "\n")
