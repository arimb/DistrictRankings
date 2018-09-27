from functions import getTBAdata

file = open("champs_ranking.csv", "w+")
file.write("Team #,DP,DivDP,OPR,CCWM,Region\n")
for i in range(0,12):
    print(["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i])
    teams = getTBAdata("event/2018"+["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i]+"/district_points")["points"]
    metrics = getTBAdata("2018"+["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i]+"/oprs")
    for teamKey in teams:
        DP = teams[teamKey]["total"]
        try:
            if getTBAdata("team/"+teamKey+"/event/2018"+["carv","gal","hop","new","roe","tur","arc","cars","cur","dal","dar","tes"][i]+"/status")["playoff"]["status"] == "won":
                print("einstein! "+str(DP))
                einstein_matches = getTBAdata("team/"+teamKey+"/event/2018cmp"+["tx","tx","tx","tx","tx","tx","mi","mi","mi","mi","mi","mi"][i]+"/matches")
                for match in einstein_matches:
                    DP += 5 if (teamKey in match["alliances"]["blue"]["team_keys"]) != (match['winning_alliance'] == "red") else 0
                einstein_awards = getTBAdata("team/"+teamKey+"/event/2018cmp"+["tx","tx","tx","tx","tx","tx","mi","mi","mi","mi","mi","mi"][i]+"/awards")
                for award in einstein_awards:
                    DP += 12 if award["award_type"] == 0 else 10 if award["award_type"] == 69 else 0
        except:
            pass
        district = getTBAdata("team/"+teamKey+"/districts")
        if len(district)!=0:
            region = (district[len(district)-1]["abbreviation"]).upper()
        else:
            team = getTBAdata("team/" + teamKey + "/simple")
            if team["country"] == "USA":
                region = team["state_prov"]
            else:
                region = team["country"]
        print(teamKey[3:]+"  "+str(DP)+"  "+str(teams[teamKey]["total"])+"  "+str(metrics["oprs"][teamKey])+"  "+str(metrics["ccwms"][teamKey])+"  "+region)
        file.write(teamKey[3:]+","+str(DP)+","+str(teams[teamKey]["total"])+","+str(metrics["oprs"][teamKey])+","+str(metrics["ccwms"][teamKey])+","+region+"\n")