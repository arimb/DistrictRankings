from functions import get_tba_data
import csv
import pickle
from math import ceil
from scipy.special import erfinv

competitors = []

for year in range(2019, 2020):
    teams = {}
    with open(str(year)+"_world_DP.csv") as dpfile:
        dpreader = csv.DictReader(dpfile)
        for row in dpreader:
            teams[row["Team"]] = [float(row["Adj DP"]), float(row["Adj Qual DP"]), float(row["Adj Alliance DP"]), float(row["Adj Playoff DP"])]
    events = get_tba_data('events/'+str(year)+'/simple')
    for event in events:
        if event['key'] != '2019cc': continue
        if event['event_type'] != 99: continue
        matches = get_tba_data('event/'+event['key']+'/matches/simple')
        if len(matches) ==0: continue
        statuses = get_tba_data('event/'+event['key']+'/teams/statuses')
        if None in statuses.values(): continue
        print(event['key'])
        event_teams = {}
        for team, status in statuses.items():
            if team not in teams: continue
            if status['qual'] is None: continue
            if status['qual']['ranking'] is None: continue
            if status['qual']['ranking']['rank'] is None: continue
            event_teams[team] = [[], 0, 0, 0]
            event_teams[team][0] = teams[team]
            event_teams[team][1] = ceil(7.676*erfinv((status['qual']['num_teams']-2*status['qual']['ranking']['rank']+2)/(1.07*status['qual']['num_teams']))+12)
            if status['alliance'] is not None:
                if status['alliance']['pick'] <2: event_teams[team][2] = 17-status['alliance']['number']
                elif status['alliance']['pick'] ==2: event_teams[team][2] = status['alliance']['number']
        for match in matches:
            if match['comp_level'] == 'qm' or not match['winning_alliance']: continue
            for team in match['alliances'][match['winning_alliance']]['team_keys']:
                if team in event_teams: event_teams[team][3] += 5
        competitors += list(event_teams.items())

with open('cc.pkl', 'wb') as file:
    pickle.dump(competitors, file)

with open('cc.csv', 'w+') as file:
    file.write('Team,Adj DP,Qual DP,Alliance DP,Playoff DP,Qual Points,Alliance Points,Playoff Points,Total Points\n')
    for c in competitors:
        file.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(c[0],c[1][0][0],c[1][0][1],c[1][0][2],c[1][0][3],c[1][1],c[1][2],c[1][3],c[1][1]+c[1][2]+c[1][3]))