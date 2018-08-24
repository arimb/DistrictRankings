import requests

def getdata(url):
    try:
        return requests.get(url, "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
    except:
        print("oops " + url)
        getdata(url)

class Team:
    def __init__(self, event, DP):
        if event["event_type"] == 2 or event["event_type"] == 5:
            factor = 0.37
        else:
            factor = 1
        self.qual = DP["qual_points"]*factor
        self.alliance = DP["alliance_points"]*factor
        self.playoff = DP["elim_points"]*factor
        self.awards = DP["award_points"]*factor
        self.bestPlayoff = DP["elim_points"]
        self.bestAlliance = DP["alliance_points"]
        self.num_events = 1
    def add_event(self, event, DP):
        if event["event_type"] == 2 or event["event_type"] == 5:
            factor = 0.37
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

teams = {}
year = 2018

file = open("2018_champs_predictions.csv", "w+")
file.write("Match Key,Red 1,Red 2,Red 3,Blue 1,Blue 2,Blue 3,Red DP,Blue DP,Prediction,Actual,Good?\n")
events = getdata("https://www.thebluealliance.com/api/v3/events/"+str(year))
for event in events:
    if 0 <= event["event_type"] <= 2 or event["event_type"] == 5:
        if len(event["division_keys"]) == 0:
            print(event["key"])
            DPs = getdata("https://www.thebluealliance.com/api/v3/event/"+event["key"]+"/district_points")["points"]
            for teamKey in DPs:
                if teamKey in teams:
                    teams[teamKey].add_event(event, DPs[teamKey])
                else:
                    teams[teamKey] = Team(event, DPs[teamKey])

for event in ["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"]:
    print(event)
    matches = getdata("https://www.thebluealliance.com/api/v3/event/"+str(year)+event+"/matches/simple")
    num = total = 0
    for match in matches:
        if match["comp_level"]=="qm":
            red1 = match["alliances"]["red"]["team_keys"][0]
            red2 = match["alliances"]["red"]["team_keys"][1]
            red3 = match["alliances"]["red"]["team_keys"][2]
            blue1 = match["alliances"]["blue"]["team_keys"][0]
            blue2 = match["alliances"]["blue"]["team_keys"][1]
            blue3 = match["alliances"]["blue"]["team_keys"][2]
            red = teams[red1].adj() + teams[red2].adj() + teams[red3].adj()
            blue = teams[blue1].adj() + teams[blue2].adj() + teams[blue3].adj()
            prediction = "red" if red>blue else "blue" if blue>red else "tie"
            good = prediction == match["winning_alliance"]
            if good:
                num +=1
            total +=1

            file.write(match["key"] + "," + red1 + "," + red2 + "," + red3 + "," + blue1 + "," + blue2 + "," + blue3 + "," +
                       str(red) + "," + str(blue) + "," + prediction + "," +
                       ("tie" if match["winning_alliance"]=="" else match["winning_alliance"]) + "," +
                       ("True" if good else "False") + "\n")
    file.write(str(num) + "," + str(num/total) + "\n")
