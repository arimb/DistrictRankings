import requests

def getdata(url):
    try:
        return requests.get(url, "accept=application%2Fjson&X-TBA-Auth-Key=gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ").json()
    except:
        print("oops " + url)
        getdata(url)

file = open("champs_ranking.csv", "w+")
file.write("Team #,DP,DivDP,OPR,CCWM,Region\n")
for i in range(0,12):
    print(["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i])
    teams = getdata("https://www.thebluealliance.com/api/v3/event/2018"+["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i]+"/district_points")["points"]
    metrics = getdata("https://www.thebluealliance.com/api/v3/event/2018"+["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i]+"/oprs")
    for teamKey in teams:
        DP = teams[teamKey]["total"]
        try:
            if getdata("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/2018"+["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i]+"/status")["playoff"]["status"] == "won":
                print("einstein! "+str(DP))
                einstein_matches = getdata("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/2018cmp"+["tx","tx","tx","tx","tx","tx","mi","mi","mi","mi","mi","mi"][i]+"/matches")
                for match in einstein_matches:
                    DP += 5 if (teamKey in match["alliances"]["blue"]["team_keys"]) != (match['winning_alliance'] == "red") else 0
                einstein_awards = getdata("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/2018cmp"+["tx","tx","tx","tx","tx","tx","mi","mi","mi","mi","mi","mi"][i]+"/awards")
                for award in einstein_awards:
                    DP += 12 if award["award_type"] == 0 else 10 if award["award_type"] == 69 else 0
        except:
            pass
        district = getdata("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/districts")
        if len(district)!=0:
            region = (district[len(district)-1]["abbreviation"]).upper()
        else:
            team = getdata("https://www.thebluealliance.com/api/v3/team/" + teamKey + "/simple")
            if team["country"] == "USA":
                region = team["state_prov"]
            else:
                region = team["country"]
        print(teamKey[3:]+"  "+str(DP)+"  "+str(teams[teamKey]["total"])+"  "+str(metrics["oprs"][teamKey])+"  "+str(metrics["ccwms"][teamKey])+"  "+region)
        file.write(teamKey[3:]+","+str(DP)+","+str(teams[teamKey]["total"])+","+str(metrics["oprs"][teamKey])+","+str(metrics["ccwms"][teamKey])+","+region+"\n")