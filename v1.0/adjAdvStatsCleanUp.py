import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

stats = pd.read_csv('./csv_Data/advStatsgame/' + '2013' + '.csv', encoding = "ISO-8859-1")
final = {}
final["Week"] = []
final["Team"] = []
masterDict = {}
cats = []
d1Teams = []
for col in stats.columns:
    if (col != "gameId" and col != "week" and col != "team" and col != "opponent"):
        cats.append(col)
        final["adj_" + col] = []
teamDf = pd.read_csv('./csv_Data/majorDivTeams.csv', encoding = "ISO-8859-1")
for index, row in teamDf.iterrows():
    d1Teams.append(standardizeTeamName(row["school"],True))
#Adding Idaho Manually since they are no longer FBS
d1Teams.append("Idaho")
years = []
start = 2014
while (start != 2020):
    years.append(start)
    start += 1

for year in years:
    for d1 in d1Teams:
        masterDict[standardizeTeamName(d1,True)] = {}
        for col in stats.columns:
            if (col != "gameId" and col != "week" and col != "team" and col != "opponent"):
                masterDict[standardizeTeamName(d1,True)][col] = []
    stats = pd.read_csv('./new_csv_Data/advStatsgame/' + str(year) + '.csv', encoding = "ISO-8859-1")
    betting = pd.read_csv('./csv_Data/BettingResults+Elo/' + str(year) + '.csv', encoding = "ISO-8859-1")
    for index1, row1 in stats.iterrows():
        print (index1)
        #print (row1["team"], standardizeTeamName(row1["team"], True))
        if (row1["week"] == 99):
            break
        if (standardizeTeamName(row1["team"],False) not in d1Teams):
            continue
        if (standardizeTeamName(row1["opponent"],False) not in d1Teams):
            oppElo = 500
        else:
            #need to test to make sure opp elos are always found if they are d1
            for index, row in betting.iterrows():
                if (row["Week"] == "Bowl"):
                    continue
                if (standardizeTeamName(row1["opponent"],False) == standardizeTeamName(row["Home Team"],False) and int(row1["week"]) == int(row["Week"])):
                    if (np.isnan(row["Home Incoming Elo"])):
                        print ("ERROR FINDING ELO:", row["Home Team"])
                    oppElo = float(row["Home Incoming Elo"])
                    break
                elif (standardizeTeamName(row1["opponent"],False) == standardizeTeamName(row["Road Team"],False) and int(row1["week"]) == int(row["Week"])):
                    if (np.isnan(row["Road Incoming Elo"])):
                        print ("ERROR FINDING ELO:", row["Road Team"])
                    oppElo = float(row["Road Incoming Elo"])
                    break
        if (standardizeTeamName(row1["team"],False) in d1Teams):
            final["Week"].append(int(row1["week"]) + 1)
            final["Team"].append(standardizeTeamName(row1["team"],False))
        for col in cats:
            if (standardizeTeamName(row1["team"],False) in d1Teams):
                #HERE IS THE ADJUSTMENT
                #if (float(row1[col]) >= 0):
                #    masterDict[row1["team"]][col].append(float(row1[col])*oppElo)
                #else:
            #        masterDict[row1["team"]][col].append(float(row1[col])/oppElo)
                if (not np.isnan(row1[col])):
                    masterDict[standardizeTeamName(row1["team"],False)][col].append((1.5**float(row1[col]))*oppElo)
                if (len(masterDict[standardizeTeamName(row1["team"],False)][col]) >= 1):
                    final["adj_" + col].append(np.average(masterDict[standardizeTeamName(row1["team"],False)][col]))
                else:
                    final["adj_" + col].append(np.nan)


    dfFinal = pd.DataFrame.from_dict(final)
    dfFinal.to_csv("./new_csv_Data/adjAdvStatsFwdLooking/" + str(year) + ".csv")
    for key in final:
        final[key] = []
    print (year)
