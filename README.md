# District Points Statistics

Many unintended ways to use the FRC District Points system for statistical analyses and predictions.

## ChampsAnalysis

ChampsAnalysis looks at the strengths of the different champs sub-divisions, as well as the best/worse performing regions (i.e. states, districts, and countries). Also looks at the predictive power of using DP to predict Champs performance compared to OPR, CCWM, and EPR. ChiefDelphi post on the topic [here](https://www.chiefdelphi.com/forums/showthread.php?t=165298). This was one of the first experiments using District Points for more than in-district analysis, and much of what is done here has been re-done more efficiently, accurately, and generally in SingleYearDP, EventPredictor, and MatchPredictor.

## EventPredictor

EventPredictor predicts the final qualification ranking of an event before the match schedule has been released. This simulator is less effective than the [Ranking Points PreSchdulePredictor](https://github.com/arimb/EventPredictor/tree/master/PreSchedulePredictor), which only takes into account teams' previous probability of earning ranking points. Since the simulator needs a majority of teams' Adjusted District Points, it only works for late/post-season competitions. 

The simulator works thusly. Using the pre-constructed match schedules from [CheesyArena](https://github.com/Team254/cheesy-arena), the simulator creates a sample match schedule for the event. Then for each match, it finds the difference between the alliances' average Adjusted District Points and calculates a match win probability based on scaling data taken from earlier matches. Once all of the matches have been simulated, the teams are ranked based on how many matches they won. The simulator scrambles the teams, re-assigns teams to the pre-constructed match schedules, repeats the event simulation a pre-defined number of times, and averages the resulting ranks. 

## MatchPredictor

MatchPredictor predicts the final qualification ranking of an event once the event's match schedule has been released. It works similarly to EventPredictor, but without needing the CheesyArena schedules. In its current form MatchPredictor also needs a majority of teams' Adjusted District Points, so it only works for late/post-season competitions.

##OPR_Correlation

ORP_Correlation does exactly what it sounds like: it looks at the correlation between the district points model and the OPR and Qualification Rank models. It found DP/OPR correlations of 52%, 68%, 62%, 61%, 65%, 75%, 68%, 60%, and 66% for each year since 2010, respectively; the average of which is 64%.

## PickemLeague

This script was used to evaluate the best choices for the [IRI Pickem League competition](https://www.chiefdelphi.com/forums/showthread.php?t=165969). It evaluates every combination of teams satisfying the competition requirements to find which has the highest total Adj. District Points score. For the IRI competition with 70 teams, there are ~900 combinations of teams (compared to ~3x10^51 permutations of teams). The program worked decently, but in the future more care needs to be payed to the exact method of scoring, if that differs from the District Points model. 

## RegionalDistribution

