# Combination of Snoozle and collegefootballdata.com data since txt spreads only cover 2001-2017
# Use this for 2018- lines
import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

year = "2018"

bets = pd.read_csv('./csv_Data/rawBettingLines/' + year + '/Betting.csv', encoding = "ISO-8859-1")
games = pd.read_csv('./csv_Data/rawBettingLines/' + year + '/Games.csv', encoding = "ISO-8859-1")

dict = {"Week":[],"Date":[],"Home Team":[],"Road Team":[],"Neutral Field":[],"Night Game":[],"Postseason Game":[],"Favorite":[],"Spread":[],"O/U":[],"Home Score":[],"Road Score":[],"Spread Winner":[],"O/U Outcome":[]}
idsUsed = []

for index, row in bets.iterrows():
    if (row["id"] not in idsUsed):
        dict["Home Team"].append(standardizeTeamName((row["homeTeam"]),False))
        dict["Road Team"].append(standardizeTeamName((row["awayTeam"]),False))
        dict["Home Score"].append(row["homeScore"])
        dict["Road Score"].append(row["awayScore"])
        k = 0
        curGame = row["id"]
        consensusFound = False
        while (k+index < len(bets.index) and bets.iat[k+index,0] == curGame):
            if (bets.iat[k+index,5] == "consensus"):
                consensusFound = True
                dict["O/U"].append(bets.iat[k+index,6])
                if (int(bets.iat[k+index,2]) + int(bets.iat[k+index,4]) > float(bets.iat[k+index,6])):
                    dict["O/U Outcome"].append("Over")
                elif (int(bets.iat[k+index,2]) + int(bets.iat[k+index,4]) == float(bets.iat[k+index,6])):
                    dict["O/U Outcome"].append("Push")
                else:
                    dict["O/U Outcome"].append("Under")
                dict["Spread"].append(abs(float(bets.iat[k+index,7])))
                if (float(bets.iat[k+index,7]) < 0):
                    dict["Favorite"].append(standardizeTeamName((row["homeTeam"]),False))
                    if (int(bets.iat[k+index,2]) - int(bets.iat[k+index,4]) > abs(float(bets.iat[k+index,7]))):
                        dict["Spread Winner"].append(standardizeTeamName((row["homeTeam"]),False))
                    elif (int(bets.iat[k+index,2]) - int(bets.iat[k+index,4]) == abs(float(bets.iat[k+index,7]))):
                        dict["Spread Winner"].append("Push")
                    else:
                        dict["Spread Winner"].append(standardizeTeamName((row["awayTeam"]),False))
                else:
                    dict["Favorite"].append(standardizeTeamName(row["awayTeam"],False))
                    if (int(bets.iat[k+index,4]) - int(bets.iat[k+index,2]) > abs(float(bets.iat[k+index,7]))):
                        dict["Spread Winner"].append(standardizeTeamName((row["awayTeam"]),False))
                    elif (int(bets.iat[k+index,4]) - int(bets.iat[k+index,2]) == abs(float(bets.iat[k+index,7]))):
                        dict["Spread Winner"].append("Push")
                    else:
                        dict["Spread Winner"].append(standardizeTeamName((row["homeTeam"]),False))
                break
            k += 1
        if (not consensusFound):
            dict["O/U"].append(row["overUnder"])
            if (int(row["homeScore"]) + int(row["awayScore"]) > float(row["overUnder"])):
                dict["O/U Outcome"].append("Over")
            elif (int(row["homeScore"]) + int(row["awayScore"]) == float(row["overUnder"])):
                dict["O/U Outcome"].append("Push")
            else:
                dict["O/U Outcome"].append("Under")
            dict["Spread"].append(abs(float(row["spread"])))
            if (float(row["spread"]) < 0):
                dict["Favorite"].append(standardizeTeamName((row["homeTeam"]),False))
                if (int(row["homeScore"]) - int(row["awayScore"]) > abs(float(row["spread"]))):
                    dict["Spread Winner"].append(standardizeTeamName((row["homeTeam"]),False))
                elif (int(row["homeScore"]) - int(row["awayScore"]) == abs(float(row["spread"]))):
                    dict["Spread Winner"].append("Push")
                else:
                    dict["Spread Winner"].append(standardizeTeamName((row["awayTeam"]),False))
            else:
                dict["Favorite"].append(standardizeTeamName(row["awayTeam"],False))
                if (int(row["awayScore"]) - int(row["homeScore"]) > abs(float(row["spread"]))):
                    dict["Spread Winner"].append(standardizeTeamName((row["awayTeam"]),False))
                elif (int(row["awayScore"]) - int(row["homeScore"]) == abs(float(row["spread"]))):
                    dict["Spread Winner"].append("Push")
                else:
                    dict["Spread Winner"].append(standardizeTeamName((row["homeTeam"]),False))
        for indexx, roww in games.iterrows():
            if (row["id"] == roww["id"]):
                dict["Date"].append(roww["start_date"])
                dict["Night Game"].append(np.nan)
                if (roww["neutral_site"] == True):
                    dict["Neutral Field"].append(1)
                else:
                    dict["Neutral Field"].append(0)
                if (roww["season_type"] == "postseason"):
                    dict["Week"].append("Bowl")
                    dict["Postseason Game"].append(1)
                else:
                    dict["Week"].append(roww["week"])
                    dict["Postseason Game"].append(0)
                break
        idsUsed.append(curGame)
df = pd.DataFrame.from_dict(dict)
print (df)
print ("Copied to file.")
df.to_csv("./csv_Data/BettingResults/" + year + ".csv")
