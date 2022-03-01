import pandas as pd
import numpy as np
import operator
from cfbFcns import standardizeTeamName
import cfbd
from cfbd.rest import ApiException

week = 13

bets = pd.read_csv('./new_csv_Data/2021/predictionsWeek' + str(week) + '.csv', encoding = "ISO-8859-1")
spreadSum = 0
ouSum = 0
spreadNum = 0
ouNum = 0
spreadVol = 0
ouVol = 0

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'XBWTTfw3Jo8o/r/jmDnRA6SsnoHp0MKKPBEE0UGID/hPKqzKLV/+0Ljn06dCbQRS'
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 2021
api_response = api_instance.get_games(year=year, week=week, season_type="regular")
for index, row in bets.iterrows():
    for x in api_response:
        if (standardizeTeamName(x.home_team, False) == standardizeTeamName(row["Home Team"], False) and standardizeTeamName(x.away_team, False) == standardizeTeamName(row["Road Team"], False)):
            try:
                if (not pd.isnull(row["Spread Bet"])):
                    spreadNum += 1
                    spreadVol += float(row["Spread Amt"])
                    if ('+' in row["Spread Bet"]):
                        team = row["Spread Bet"].split(" +")[0]
                        points = float(row["Spread Bet"].split(" +")[1])
                        if (team == standardizeTeamName(x.home_team, False)):
                            if (float(x.home_points) + points > float(x.away_points)):
                                spreadSum += float(row["Spread Amt"]) * (float(row["Spread Odds"]) - 1)
                            elif (float(x.home_points) + points < float(x.away_points)):
                                spreadSum -= float(row["Spread Amt"])
                        else:
                            if (float(x.away_points) + points > float(x.home_points)):
                                spreadSum += float(row["Spread Amt"]) * (float(row["Spread Odds"]) - 1)
                            elif (float(x.away_points) + points < float(x.home_points)):
                                spreadSum -= float(row["Spread Amt"])
                    else:
                        team = row["Spread Bet"].split(" -")[0]
                        points = float(row["Spread Bet"].split(" -")[1])
                        if (team == standardizeTeamName(x.home_team, False)):
                            if (float(x.home_points) - points > float(x.away_points)):
                                spreadSum += float(row["Spread Amt"]) * (float(row["Spread Odds"]) - 1)
                            elif (float(x.home_points) - points < float(x.away_points)):
                                spreadSum -= float(row["Spread Amt"])
                        else:
                            if (float(x.away_points) - points > float(x.home_points)):
                                spreadSum += float(row["Spread Amt"]) * (float(row["Spread Odds"]) - 1)
                            elif (float(x.away_points) - points < float(x.home_points)):
                                spreadSum -= float(row["Spread Amt"])
            except:
                pass
            try:
                if (not pd.isnull(row["O/U Bet"])):
                    ouNum += 1
                    ouVol += float(row["O/U Amt"])
                    if ("Under" in row["O/U Bet"]):
                        if (int(x.home_points) + int(x.away_points) < float(row["O/U Bet"].split("Under ")[1])):
                            ouSum += float(row["O/U Amt"]) * (float(row["O/U Odds"]) - 1)
                        elif (int(x.home_points) + int(x.away_points) > float(row["O/U Bet"].split("Under ")[1])):
                            ouSum -= float(row["O/U Amt"])
                    else:
                        if (int(x.home_points) + int(x.away_points) > float(row["O/U Bet"].split("Over ")[1])):
                            ouSum += float(row["O/U Amt"]) * (float(row["O/U Odds"]) - 1)
                        elif (int(x.home_points) + int(x.away_points) < float(row["O/U Bet"].split("Over ")[1])):
                            ouSum -= float(row["O/U Amt"])
            except:
                pass

dict = {"Week":[week],"Total Net Win":[spreadSum + ouSum],"Ending Bankroll":[spreadSum + ouSum + spreadVol + ouVol],"Total Bets":[spreadNum + ouNum],"Total Volume":[spreadVol + ouVol],"Spread Bets":[spreadNum],"Spread Volume":[spreadVol],"Spread Net Win":[spreadSum],"O/U Bets":[ouNum],"O/U Volume":[ouVol],"O/U Net Win":[ouSum],"Manual Adjustment":[0]}
dfFinal = pd.DataFrame.from_dict(dict)

try:
    res = pd.read_csv('./new_csv_Data/2021/RESULTS.csv', encoding = "ISO-8859-1")
    res = res.append(dfFinal)
    res.to_csv('./new_csv_Data/2021/RESULTS.csv', index = False)
except:
    dfFinal.to_csv('./new_csv_Data/2021/RESULTS.csv', index = False)
