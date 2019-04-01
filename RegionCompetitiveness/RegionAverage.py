from functions import getTBAdata

avgs = {}
events = getTBAdata("events/2018")
for event in events:
    if event["event_type"]>1 : continue
    print(event["key"])
    dps = getTBAdata("event/" + event["key"] + "/district_points")["points"]
    avgs[event["key"]] = (sum([dps[t]["total"] for t in dps.keys()])/len(dps), len(dps))

with open("avgs.csv", "w+") as file:
    file.write("Event,AvgDP,# Teams\n")
    for event, avg in avgs.items():
        file.write(event + "," + str(avg[0]) + "," + str(avg[1]) + "\n")