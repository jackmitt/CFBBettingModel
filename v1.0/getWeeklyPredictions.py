from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from cfbFcns import getBin
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import StandardScaler
from evalPredictions import testClassification
from sklearn.utils import shuffle
import random

weekMain = 3


#advStatsCleanUp
def avg(arr):
    if (len(arr) > 0):
        return sum(arr)/len(arr)
    return np.nan

df = pd.read_csv('./new_csv_data/currentSeason/week1.csv', encoding = "ISO-8859-1")
for w in range(2, weekMain):
    df = df.append(pd.read_csv('./new_csv_data/currentSeason/week' + str(w) + '.csv', encoding = "ISO-8859-1"), ignore_index=True)


dropRows = []
for index, row in df.iterrows():
    if (index > 0 and row["gameId"] == df.at[index-1,"gameId"]):
        dropRows.append(index)
df = df.drop(dropRows)
dict = {"Week":[],"Team":[],"Offense":{},"Defense":{}}
subDictOff = {"Ppa":[],"Sr":[],"Exp":[],"PwrS":[],"Stuff":[],"SecLevel":[],"OpenField":[],"StDownPpa":[],"StDownSr":[],"StDownExp":[],"PassDownPpa":[],"PassDownSr":[],"PassDownExp":[],"RushPpa":[],"RushSr":[],"RushExp":[],"PassPpa":[],"PassSr":[],"PassExp":[]}
subDictDef = {"Ppa":[],"Sr":[],"Exp":[],"PwrS":[],"Stuff":[],"SecLevel":[],"OpenField":[],"StDownPpa":[],"StDownSr":[],"StDownExp":[],"PassDownPpa":[],"PassDownSr":[],"PassDownExp":[],"RushPpa":[],"RushSr":[],"RushExp":[],"PassPpa":[],"PassSr":[],"PassExp":[]}
for index, row in df.iterrows():
    dict["Week"].append(row["week"])
    dict["Team"].append(standardizeTeamName(row["team"], False))
    dict["Week"].append(row["week"])
    dict["Team"].append(standardizeTeamName(row["opponent"], False))
    #Offense
    subDictOff["Ppa"].append(row["offense.ppa"])
    subDictDef["Ppa"].append(row["defense.ppa"])
    subDictOff["Ppa"].append(row["defense.ppa"])
    subDictDef["Ppa"].append(row["offense.ppa"])

    subDictOff["Sr"].append(row["offense.successRate"])
    subDictDef["Sr"].append(row["defense.successRate"])
    subDictOff["Sr"].append(row["defense.successRate"])
    subDictDef["Sr"].append(row["offense.successRate"])

    subDictOff["Exp"].append(row["offense.explosiveness"])
    subDictDef["Exp"].append(row["defense.explosiveness"])
    subDictOff["Exp"].append(row["defense.explosiveness"])
    subDictDef["Exp"].append(row["offense.explosiveness"])

    subDictOff["PwrS"].append(row["offense.powerSuccess"])
    subDictDef["PwrS"].append(row["defense.powerSuccess"])
    subDictOff["PwrS"].append(row["defense.powerSuccess"])
    subDictDef["PwrS"].append(row["offense.powerSuccess"])

    subDictOff["Stuff"].append(row["offense.stuffRate"])
    subDictDef["Stuff"].append(row["defense.stuffRate"])
    subDictOff["Stuff"].append(row["defense.stuffRate"])
    subDictDef["Stuff"].append(row["offense.stuffRate"])

    subDictOff["SecLevel"].append(row["offense.secondLevelYards"])
    subDictDef["SecLevel"].append(row["defense.secondLevelYards"])
    subDictOff["SecLevel"].append(row["defense.secondLevelYards"])
    subDictDef["SecLevel"].append(row["offense.secondLevelYards"])

    subDictOff["OpenField"].append(row["offense.openFieldYards"])
    subDictDef["OpenField"].append(row["defense.openFieldYards"])
    subDictOff["OpenField"].append(row["defense.openFieldYards"])
    subDictDef["OpenField"].append(row["offense.openFieldYards"])

    subDictOff["StDownPpa"].append(row["offense.standardDowns.ppa"])
    subDictDef["StDownPpa"].append(row["defense.standardDowns.ppa"])
    subDictOff["StDownPpa"].append(row["defense.standardDowns.ppa"])
    subDictDef["StDownPpa"].append(row["offense.standardDowns.ppa"])

    subDictOff["StDownSr"].append(row["offense.standardDowns.successRate"])
    subDictDef["StDownSr"].append(row["defense.standardDowns.successRate"])
    subDictOff["StDownSr"].append(row["defense.standardDowns.successRate"])
    subDictDef["StDownSr"].append(row["offense.standardDowns.successRate"])

    subDictOff["StDownExp"].append(row["offense.standardDowns.explosiveness"])
    subDictDef["StDownExp"].append(row["defense.standardDowns.explosiveness"])
    subDictOff["StDownExp"].append(row["defense.standardDowns.explosiveness"])
    subDictDef["StDownExp"].append(row["offense.standardDowns.explosiveness"])

    subDictOff["PassDownPpa"].append(row["offense.passingDowns.ppa"])
    subDictDef["PassDownPpa"].append(row["defense.passingDowns.ppa"])
    subDictOff["PassDownPpa"].append(row["defense.passingDowns.ppa"])
    subDictDef["PassDownPpa"].append(row["offense.passingDowns.ppa"])

    subDictOff["PassDownSr"].append(row["offense.passingDowns.successRate"])
    subDictDef["PassDownSr"].append(row["defense.passingDowns.successRate"])
    subDictOff["PassDownSr"].append(row["defense.passingDowns.successRate"])
    subDictDef["PassDownSr"].append(row["offense.passingDowns.successRate"])

    subDictOff["PassDownExp"].append(row["offense.passingDowns.explosiveness"])
    subDictDef["PassDownExp"].append(row["defense.passingDowns.explosiveness"])
    subDictOff["PassDownExp"].append(row["defense.passingDowns.explosiveness"])
    subDictDef["PassDownExp"].append(row["offense.passingDowns.explosiveness"])

    subDictOff["RushPpa"].append(row["offense.rushingPlays.ppa"])
    subDictDef["RushPpa"].append(row["defense.rushingPlays.ppa"])
    subDictOff["RushPpa"].append(row["defense.rushingPlays.ppa"])
    subDictDef["RushPpa"].append(row["offense.rushingPlays.ppa"])

    subDictOff["RushSr"].append(row["offense.rushingPlays.successRate"])
    subDictDef["RushSr"].append(row["defense.rushingPlays.successRate"])
    subDictOff["RushSr"].append(row["defense.rushingPlays.successRate"])
    subDictDef["RushSr"].append(row["offense.rushingPlays.successRate"])

    subDictOff["RushExp"].append(row["offense.rushingPlays.explosiveness"])
    subDictDef["RushExp"].append(row["defense.rushingPlays.explosiveness"])
    subDictOff["RushExp"].append(row["defense.rushingPlays.explosiveness"])
    subDictDef["RushExp"].append(row["offense.rushingPlays.explosiveness"])

    subDictOff["PassPpa"].append(row["offense.passingPlays.ppa"])
    subDictDef["PassPpa"].append(row["defense.passingPlays.ppa"])
    subDictOff["PassPpa"].append(row["defense.passingPlays.ppa"])
    subDictDef["PassPpa"].append(row["offense.passingPlays.ppa"])

    subDictOff["PassSr"].append(row["offense.passingPlays.successRate"])
    subDictDef["PassSr"].append(row["defense.passingPlays.successRate"])
    subDictOff["PassSr"].append(row["defense.passingPlays.successRate"])
    subDictDef["PassSr"].append(row["offense.passingPlays.successRate"])

    subDictOff["PassExp"].append(row["offense.passingPlays.explosiveness"])
    subDictDef["PassExp"].append(row["defense.passingPlays.explosiveness"])
    subDictOff["PassExp"].append(row["defense.passingPlays.explosiveness"])
    subDictDef["PassExp"].append(row["offense.passingPlays.explosiveness"])
dict["Offense"] = subDictOff
dict["Defense"] = subDictDef
#Forward looking week - week 1 stats are entered as week 2, week 1 and 2 stats averaged for week 3 and so on so that week matches up with predicting spreads
final = {"Week":[],"Team":[],"oPpa":[],"oSr":[],"oExp":[],"oPwrS":[],"oStuff":[],"oSecLevel":[],"oOpenField":[],"oStDownPpa":[],"oStDownSr":[],"oStDownExp":[],"oPassDownPpa":[],"oPassDownSr":[],"oPassDownExp":[],"oRushPpa":[],"oRushSr":[],"oRushExp":[],"oPassPpa":[],"oPassSr":[],"oPassExp":[],"dPpa":[],"dSr":[],"dExp":[],"dPwrS":[],"dStuff":[],"dSecLevel":[],"dOpenField":[],"dStDownPpa":[],"dStDownSr":[],"dStDownExp":[],"dPassDownPpa":[],"dPassDownSr":[],"dPassDownExp":[],"dRushPpa":[],"dRushSr":[],"dRushExp":[],"dPassPpa":[],"dPassSr":[],"dPassExp":[]}
for i in range(len(dict["Team"])):
    week = int(dict["Week"][i])
    team = dict["Team"][i]
    if (week != 99):
        final["Week"].append(week+1)
    else:
        final["Week"].append("Year End")
    final["Team"].append(team)
    dPpa = []
    dSr = []
    dExp = []
    dPwrS = []
    dStuff = []
    dSecLevel = []
    dOpenField = []
    dStDownPpa = []
    dStDownSr = []
    dStDownExp = []
    dPassDownPpa = []
    dPassDownSr = []
    dPassDownExp = []
    dRushPpa = []
    dRushSr = []
    dRushExp = []
    dPassPpa = []
    dPassSr = []
    dPassExp = []
    oPpa = []
    oSr = []
    oExp = []
    oPwrS = []
    oStuff = []
    oSecLevel = []
    oOpenField = []
    oStDownPpa = []
    oStDownSr = []
    oStDownExp = []
    oPassDownPpa = []
    oPassDownSr = []
    oPassDownExp = []
    oRushPpa = []
    oRushSr = []
    oRushExp = []
    oPassPpa = []
    oPassSr = []
    oPassExp = []
    k = 0
    while (k < len(dict["Week"]) and int(dict["Week"][k]) <= week):
        if (team == dict["Team"][k]):
            oPpa.append(float(dict["Offense"]["Ppa"][k]))
            oSr.append(float(dict["Offense"]["Sr"][k]))
            oExp.append(float(dict["Offense"]["Exp"][k]))
            oPwrS.append(float(dict["Offense"]["PwrS"][k]))
            oStuff.append(float(dict["Offense"]["Stuff"][k]))
            oSecLevel.append(float(dict["Offense"]["SecLevel"][k]))
            oOpenField.append(float(dict["Offense"]["OpenField"][k]))
            oStDownPpa.append(float(dict["Offense"]["StDownPpa"][k]))
            oStDownSr.append(float(dict["Offense"]["StDownSr"][k]))
            oStDownExp.append(float(dict["Offense"]["StDownExp"][k]))
            oPassDownPpa.append(float(dict["Offense"]["PassDownPpa"][k]))
            oPassDownSr.append(float(dict["Offense"]["PassDownSr"][k]))
            oPassDownExp.append(float(dict["Offense"]["PassDownExp"][k]))
            oRushPpa.append(float(dict["Offense"]["RushPpa"][k]))
            oRushSr.append(float(dict["Offense"]["RushSr"][k]))
            oRushExp.append(float(dict["Offense"]["RushExp"][k]))
            oPassPpa.append(float(dict["Offense"]["PassPpa"][k]))
            oPassSr.append(float(dict["Offense"]["PassSr"][k]))
            oPassExp.append(float(dict["Offense"]["PassExp"][k]))
            dPpa.append(float(dict["Defense"]["Ppa"][k]))
            dSr.append(float(dict["Defense"]["Sr"][k]))
            dExp.append(float(dict["Defense"]["Exp"][k]))
            dPwrS.append(float(dict["Defense"]["PwrS"][k]))
            dStuff.append(float(dict["Defense"]["Stuff"][k]))
            dSecLevel.append(float(dict["Defense"]["SecLevel"][k]))
            dOpenField.append(float(dict["Defense"]["OpenField"][k]))
            dStDownPpa.append(float(dict["Defense"]["StDownPpa"][k]))
            dStDownSr.append(float(dict["Defense"]["StDownSr"][k]))
            dStDownExp.append(float(dict["Defense"]["StDownExp"][k]))
            dPassDownPpa.append(float(dict["Defense"]["PassDownPpa"][k]))
            dPassDownSr.append(float(dict["Defense"]["PassDownSr"][k]))
            dPassDownExp.append(float(dict["Defense"]["PassDownExp"][k]))
            dRushPpa.append(float(dict["Defense"]["RushPpa"][k]))
            dRushSr.append(float(dict["Defense"]["RushSr"][k]))
            dRushExp.append(float(dict["Defense"]["RushExp"][k]))
            dPassPpa.append(float(dict["Defense"]["PassPpa"][k]))
            dPassSr.append(float(dict["Defense"]["PassSr"][k]))
            dPassExp.append(float(dict["Defense"]["PassExp"][k]))
        k += 1
    copy = oPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPpa"].append(avg(adj))
    copy = oSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oSr"].append(avg(adj))
    copy = oExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oExp"].append(avg(adj))
    copy = oPwrS
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPwrS"].append(avg(adj))
    copy = oStuff
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oStuff"].append(avg(adj))
    copy = oSecLevel
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oSecLevel"].append(avg(adj))
    copy = oOpenField
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oOpenField"].append(avg(adj))
    copy = oStDownPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oStDownPpa"].append(avg(adj))
    copy = oStDownSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oStDownSr"].append(avg(adj))
    copy = oStDownExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oStDownExp"].append(avg(adj))
    copy = oPassDownPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPassDownPpa"].append(avg(adj))
    copy = oPassDownSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPassDownSr"].append(avg(adj))
    copy = oPassDownExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPassDownExp"].append(avg(adj))
    copy = oRushPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oRushPpa"].append(avg(adj))
    copy = oRushSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oRushSr"].append(avg(adj))
    copy = oRushExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oRushExp"].append(avg(adj))
    copy = oPassPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPassPpa"].append(avg(adj))
    copy = oPassSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPassSr"].append(avg(adj))
    copy = oPassExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["oPassExp"].append(avg(adj))
    copy = dPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPpa"].append(avg(adj))
    copy = dSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dSr"].append(avg(adj))
    copy = dExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dExp"].append(avg(adj))
    copy = dPwrS
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPwrS"].append(avg(adj))
    copy = dStuff
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dStuff"].append(avg(adj))
    copy = dSecLevel
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dSecLevel"].append(avg(adj))
    copy = dOpenField
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dOpenField"].append(avg(adj))
    copy = dStDownPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dStDownPpa"].append(avg(adj))
    copy = dStDownSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dStDownSr"].append(avg(adj))
    copy = dStDownExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dStDownExp"].append(avg(adj))
    copy = dPassDownPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPassDownPpa"].append(avg(adj))
    copy = dPassDownSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPassDownSr"].append(avg(adj))
    copy = dPassDownExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPassDownExp"].append(avg(adj))
    copy = dRushPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dRushPpa"].append(avg(adj))
    copy = dRushSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dRushSr"].append(avg(adj))
    copy = dRushExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dRushExp"].append(avg(adj))
    copy = dPassPpa
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPassPpa"].append(avg(adj))
    copy = dPassSr
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPassSr"].append(avg(adj))
    copy = dPassExp
    adj = []
    for z in range(len(copy)):
        if (not np.isnan(copy[z])):
            adj.append(copy[z])
    final["dPassExp"].append(avg(adj))
stats = pd.DataFrame.from_dict(final)

###################################################################################################ELO UPDATE CODE NEEDED**************************************************************************************

#adjAdvStatesCleanUp
statsTemp = pd.read_csv('./new_csv_data/currentSeason/week1.csv', encoding = "ISO-8859-1")
for w in range(2, weekMain):
    statsTemp = statsTemp.append(pd.read_csv('./new_csv_data/currentSeason/week' + str(w) + '.csv', encoding = "ISO-8859-1"), ignore_index=True)

final = {}
final["Week"] = []
final["Team"] = []
masterDict = {}
cats = []
d1Teams = []
for col in statsTemp.columns:
    if (col != "gameId" and col != "week" and col != "team" and col != "opponent"):
        cats.append(col)
        final["adj_" + col] = []
teamDf = pd.read_csv('./csv_Data/majorDivTeams.csv', encoding = "ISO-8859-1")
for index, row in teamDf.iterrows():
    d1Teams.append(standardizeTeamName(row["school"],True))

for d1 in d1Teams:
    masterDict[standardizeTeamName(d1,True)] = {}
    for col in statsTemp.columns:
        if (col != "gameId" and col != "week" and col != "team" and col != "opponent"):
            masterDict[standardizeTeamName(d1,True)][col] = []
betting = pd.read_csv('./new_csv_Data/currentSeason/BettingLines.csv', encoding = "ISO-8859-1")
for index1, row1 in statsTemp.iterrows():
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


adjStats = pd.DataFrame.from_dict(final)

#combineFwdLookingStats.py

dict = {}
match = False

for col in stats.columns:
    dict[col] = []
for col in adjStats.columns:
    if (col != "Week" or col != "Team"):
        dict[col] = []

for index, row in adjStats.iterrows():
    match = False
    for i, r in stats.iterrows():
        if (row["Team"] == r["Team"] and int(row["Week"]) == int(r["Week"])):
            match = True
            for col in stats.columns:
                if (col != "Week" and col != "Team"):
                    dict[col].append(r[col])
            break
    if (match):
        for col in adjStats.columns:
            dict[col].append(row[col])

stats = pd.DataFrame.from_dict(dict)


#finalData.py
dict = {}
d1Teams = []
teamDf = pd.read_csv('./csv_Data/majorDivTeams.csv', encoding = "ISO-8859-1")
for index, row in teamDf.iterrows():
    d1Teams.append(standardizeTeamName(row["school"],True))

games = pd.read_csv('./new_csv_Data/currentSeason/BettingLines.csv', encoding = "ISO-8859-1")

for col in stats.columns:
    dict[col] = []
dict["Opponent"] = []
dict["Homefield"] = []
for col in stats.columns:
    if (col != "Week" and col != "Team"):
        dict["X" + col] = []
dict["Elo"] = []
dict["XElo"] = []
for col in games.columns:
    if (col != "Week" and col != "Date" and col != "Home Team" and col != "Road Team" and col != "Night Game" and col != "Postseason Game" and col != "Home Incoming Elo" and col != "Road Incoming Elo" and col != "Home Resulting Elo" and col != "Road Resulting Elo"):
        dict[col] = []
dict["TrueHF"] = []
dict["alt_spread"] = []

for index, row in games.iterrows():
    hI = -999
    rI = -999
    if (standardizeTeamName(row["Home Team"], False) not in d1Teams or standardizeTeamName(row["Road Team"], False) not in d1Teams):
        continue
    if (row["Week"] == "Bowl"):
        continue
    home = standardizeTeamName(row["Home Team"], False)
    road = standardizeTeamName(row["Road Team"], False)
    week = int(row["Week"])
    for i, r in stats.iterrows():
        if (r["Week"] > week):
            break
        if (r["Team"] == home):
            hI = i;
        elif (r["Team"] == road):
            rI = i;
    #home team:
    dict["Week"].append(week)
    dict["Team"].append(home)
    for col in stats.columns:
        if (col != "Week" and col != "Team"):
            if (hI != -999):
                dict[col].append(stats.loc[hI,col])
            else:
                dict[col].append(np.nan)
    dict["Opponent"].append(road)
    dict["Homefield"].append(1)
    for col in stats.columns:
        if (col != "Week" and col != "Team"):
            if (rI != -999):
                dict["X" + col].append(stats.loc[rI,col])
            else:
                dict["X" + col].append(np.nan)
    dict["Elo"].append(row["Home Incoming Elo"])
    dict["XElo"].append(row["Road Incoming Elo"])
    for col in games.columns:
        if (col != "Week" and col != "Date" and col != "Home Team" and col != "Road Team" and col != "Night Game" and col != "Postseason Game" and col != "Home Incoming Elo" and col != "Road Incoming Elo" and col != "Home Resulting Elo" and col != "Road Resulting Elo"):
            dict[col].append(row[col])
    if (int(dict["Homefield"][-1]) == 1 and int(dict["Neutral Field"][-1]) == 0):
        dict["TrueHF"].append(1)
    else:
        dict["TrueHF"].append(0)
    if (dict["Team"][-1] == dict["Favorite"][-1]):
        dict["alt_spread"].append(0-float(dict["Spread"][-1]))
    else:
        dict["alt_spread"].append(float(dict["Spread"][-1]))
    #road team:
    dict["Week"].append(week)
    dict["Team"].append(road)
    for col in stats.columns:
        if (col != "Week" and col != "Team"):
            if (rI != -999):
                dict[col].append(stats.loc[rI,col])
            else:
                dict[col].append(np.nan)
    dict["Opponent"].append(home)
    dict["Homefield"].append(0)
    for col in stats.columns:
        if (col != "Week" and col != "Team"):
            if (hI != -999):
                dict["X" + col].append(stats.loc[hI,col])
            else:
                dict["X" + col].append(np.nan)
    dict["Elo"].append(row["Road Incoming Elo"])
    dict["XElo"].append(row["Home Incoming Elo"])
    for col in games.columns:
        if (col != "Week" and col != "Date" and col != "Home Team" and col != "Road Team" and col != "Night Game" and col != "Postseason Game" and col != "Home Incoming Elo" and col != "Road Incoming Elo" and col != "Home Resulting Elo" and col != "Road Resulting Elo"):
            dict[col].append(row[col])
    if (int(dict["Homefield"][-1]) == 1 and int(dict["Neutral Field"][-1]) == 0):
        dict["TrueHF"].append(1)
    else:
        dict["TrueHF"].append(0)
    if (dict["Team"][-1] == dict["Favorite"][-1]):
        dict["alt_spread"].append(0-float(dict["Spread"][-1]))
    else:
        dict["alt_spread"].append(float(dict["Spread"][-1]))

bigboy = pd.DataFrame.from_dict(dict)
bigboy = bigboy[bigboy.Week == weekMain]

#bigboyConvert
newDict = {}
for col in bigboy.columns:
    if (col == "Year" or col == "Week" or col == "Favorite" or col == "Spread" or col == "O/U" or col == "Home Score" or col == "Road Score" or col == "Spread Winner" or col == "O/U Outcome" or col == "TrueHF" or col == "alt_spread" or col == "Actual Spread" or col == "Actual Total"):
        newDict[col] = []
    elif (col != "Opponent" and col != "Homefield" and col != "Neutral Field" and col[0] != "X"):
        newDict["H" + col] = []
        newDict["R" + col] = []
for index, row in bigboy.iterrows():
    try:
        if (index+1 == len(bigboy.index)):
            break
        if (row["Opponent"] == bigboy.at[index+1,"Team"]):
            #TEMP week thing
            for col in bigboy.columns:
                if (col == "Year" or col == "Week" or col == "Favorite" or col == "Spread" or col == "O/U" or col == "Home Score" or col == "Road Score" or col == "Spread Winner" or col == "O/U Outcome" or col == "TrueHF" or col == "alt_spread" or col == "Actual Spread" or col == "Actual Total"):
                    newDict[col].append(row[col])
                elif (col != "Opponent" and col != "Homefield" and col != "Neutral Field" and col[0] != "X"):
                    newDict["H" + col].append(row[col])
                    newDict["R" + col].append(bigboy.at[index+1,col])
    except:
        pass


a = pd.DataFrame.from_dict(newDict)


#binClassificationTransform
Drop = True
reg = pd.DataFrame()
#ignore 37 or greater spreads
rem = []
for col in a.columns:
    if ("totalPPA" in col):
        rem.append(col)
a = a.drop(columns=rem)
a = a.dropna()
if ("FavHF" not in a.columns):
    temp = []
    for index, row in a.iterrows():
        if (row["HTeam"] == row["Favorite"] and int(row["TrueHF"]) == 1):
            temp.append(1)
        elif (int(row["TrueHF"]) == 0):
            temp.append(0.5)
        else:
            temp.append(0)
    a["FavHF"] = temp
dict = {}
for index, row in a.iterrows():
    if (row["HTeam"] == row["Favorite"]):
        homeFav = True
    else:
        homeFav = False
    for col in a.columns:
        if ('H' == col[0] and 'o' == col[1] and "Score" not in col):
            if (homeFav):
                if ("FE_" + col.split("Ho")[1] not in dict):
                    dict["FE_" + col.split("Ho")[1]] = []
                dict["FE_" + col.split("Ho")[1]].append((float(row[col]) + float(row["Rd" + col.split("Ho")[1]])) / 2)
            else:
                if ("DE_" + col.split("Ho")[1] not in dict):
                    dict["DE_" + col.split("Ho")[1]] = []
                dict["DE_" + col.split("Ho")[1]].append((float(row[col]) + float(row["Rd" + col.split("Ho")[1]])) / 2)
        elif ('R' == col[0] and 'o' == col[1] and "Score" not in col):
            if (homeFav):
                if ("DE_" + col.split("Ro")[1] not in dict):
                    dict["DE_" + col.split("Ro")[1]] = []
                dict["DE_" + col.split("Ro")[1]].append((float(row[col]) + float(row["Hd" + col.split("Ro")[1]])) / 2)
            else:
                if ("FE_" + col.split("Ro")[1] not in dict):
                    dict["FE_" + col.split("Ro")[1]] = []
                dict["FE_" + col.split("Ro")[1]].append((float(row[col]) + float(row["Hd" + col.split("Ro")[1]])) / 2)
        elif ("Hadj_offense." in col):
            if (homeFav):
                if ("FE_adj_" + col.split("Hadj_offense.")[1] not in dict):
                    dict["FE_adj_" + col.split("Hadj_offense.")[1]] = []
                dict["FE_adj_" + col.split("Hadj_offense.")[1]].append((float(row[col]) + float(row["Radj_defense." + col.split("Hadj_offense.")[1]])) / 2)
            else:
                if ("DE_adj_" + col.split("Hadj_offense.")[1] not in dict):
                    dict["DE_adj_" + col.split("Hadj_offense.")[1]] = []
                dict["DE_adj_" + col.split("Hadj_offense.")[1]].append((float(row[col]) + float(row["Radj_defense." + col.split("Hadj_offense.")[1]])) / 2)
        elif ("Radj_offense." in col):
            if (homeFav):
                if ("DE_adj_" + col.split("Radj_offense.")[1] not in dict):
                    dict["DE_adj_" + col.split("Radj_offense.")[1]] = []
                dict["DE_adj_" + col.split("Radj_offense.")[1]].append((float(row[col]) + float(row["Hadj_defense." + col.split("Radj_offense.")[1]])) / 2)
            else:
                if ("FE_adj_" + col.split("Radj_offense.")[1] not in dict):
                    dict["FE_adj_" + col.split("Radj_offense.")[1]] = []
                dict["FE_adj_" + col.split("Radj_offense.")[1]].append((float(row[col]) + float(row["Hadj_defense." + col.split("Radj_offense.")[1]])) / 2)
        elif (col == "HElo"):
            if (homeFav):
                if ("Elo_diff" not in dict):
                    dict["Elo_diff"] = []
                dict["Elo_diff"].append(float(row[col]) - float(row["RElo"]))
            else:
                if ("Elo_diff" not in dict):
                    dict["Elo_diff"] = []
                dict["Elo_diff"].append(float(row["RElo"]) - float(row[col]))
for key in dict:
    a[key] = dict[key]
dict = {}
for index, row in a.iterrows():
    for col in a.columns:
        if ("FE_" in col):
            if (col.split("FE_")[1] + "_diff" not in dict):
                dict[col.split("FE_")[1] + "_diff"] = []
            dict[col.split("FE_")[1] + "_diff"].append(float(row[col]) - float(row["DE_" + col.split("FE_")[1]]))
for key in dict:
    a[key] = dict[key]
a = a.dropna()
aa = pd.read_csv('./new_csv_Data/bigboyBinClassification.csv', encoding = "ISO-8859-1")
reg["Spread"] = aa["Spread"]
for col in aa.columns:
    if ("_diff" in col or col == "FavHF"):
        reg[col] = aa[col]
dict = {}
temp = pd.DataFrame()
for index, row in a.iterrows():
    temp = reg.copy()
    for col in a.columns:
        if ("_diff" in col or col == "FavHF"):
            testSpread = a.at[index, "Spread"]
            if (col + "_aboveAvg" not in dict):
                dict[col + "_aboveAvg"] = []
            model = LinearRegression(fit_intercept = False)
            model.fit(X = temp["Spread"].to_numpy().reshape(-1,1), y = temp[col].to_numpy().reshape(-1,1))
            dict[col + "_aboveAvg"].append(a.at[index, col] - model.predict(testSpread.reshape(1,-1))[0][0])
    temp = pd.DataFrame()
for key in dict:
    a[key] = dict[key]
a = a.dropna()

#binClassificationTransformTotals
reg = pd.DataFrame()
dict = {}
for index, row in a.iterrows():
    for col in a.columns:
        if ("FE_" in col):
            if (col.split("FE_")[1] + "_total" not in dict):
                dict[col.split("FE_")[1] + "_total"] = []
            dict[col.split("FE_")[1] + "_total"].append(float(row[col]) + float(row["DE_" + col.split("FE_")[1]]))
for key in dict:
    a[key] = dict[key]
a = a.dropna()
aa = pd.read_csv('./new_csv_Data/bigboyBinClassificationTotals.csv', encoding = "ISO-8859-1")
reg["O/U"] = aa["O/U"]
for col in aa.columns:
    if ("_total" in col):
        reg[col] = aa[col]
dict = {}
temp = pd.DataFrame()
for index, row in a.iterrows():
    temp = reg.copy()
    for col in a.columns:
        if ("_total" in col):
            testSpread = a.at[index, "O/U"]
            if (col + "_aboveAvg" not in dict):
                dict[col + "_aboveAvg"] = []
            model = LinearRegression(fit_intercept = False)
            model.fit(X = temp["O/U"].to_numpy().reshape(-1,1), y = temp[col].to_numpy().reshape(-1,1))
            dict[col + "_aboveAvg"].append(a.at[index, col] - model.predict(testSpread.reshape(1,-1))[0][0])
for key in dict:
    a[key] = dict[key]
a = a.dropna()

#Logitic Regression Portion
predictions = []
allSums = []
x = []
y = []
z = []
allScores = []
train = pd.read_csv('./new_csv_Data/bigboyBinClassificationTrain2.csv', encoding = "ISO-8859-1")
y_train = train["binSpread"]
xCols = []
for col in train.columns:
    if ("aboveAvg" in col):
        xCols.append(col)
scaler = StandardScaler()
X_train = pd.DataFrame(train, columns = xCols)
X_train[xCols] = scaler.fit_transform(X_train[xCols])

X_test = pd.DataFrame(a, columns = xCols)
X_test[xCols] = scaler.transform(X_test[xCols])

model = LogisticRegression(max_iter = 100000, C = 0.1)
model.fit(X = X_train, y = y_train)
for p in model.predict_proba(X_test):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
    else:
        predictions.append(p[0])
a["Spread PFITS"] = predictions


predictions = []
allSums = []
x = []
y = []
z = []
allScores = []
train = pd.read_csv('./new_csv_Data/bigboyBinClassificationTotalsALTTrain.csv', encoding = "ISO-8859-1")
y_train = train["binTotal"]
xCols = []
for col in train.columns:
    if ("aboveAvg" in col):
        xCols.append(col)
scaler = StandardScaler()
X_train = pd.DataFrame(train, columns = xCols)
X_train[xCols] = scaler.fit_transform(X_train[xCols])
X_test = pd.DataFrame(a, columns = xCols)
X_test[xCols] = scaler.transform(X_test[xCols])

model = LogisticRegression(max_iter = 100000, C = 0.25)
model.fit(X = X_train, y = y_train)
for p in model.predict_proba(X_test):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
    else:
        predictions.append(p[0])
a["O/U PFITS"] = predictions


print(a)
