import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

years = []
start = 2014
while (start != 2020):
    years.append(start)
    start += 1
dict = {}
d1Teams = []
teamDf = pd.read_csv('./csv_Data/majorDivTeams.csv', encoding = "ISO-8859-1")
for index, row in teamDf.iterrows():
    d1Teams.append(standardizeTeamName(row["school"],True))
#Adding Idaho Manually since they are no longer FBS
d1Teams.append("Idaho")

stats = pd.read_csv('./csv_Data/combinedFwdLookingStats/2003.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
games = pd.read_csv('./csv_Data/BettingResults+Elo/2003.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])

dict["Year"] = []
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
dict["Actual Spread"] = []
dict["Actual Total"] = []


for year in years:
    stats = pd.read_csv('./new_csv_Data/combinedFwdLookingStats/' + str(year) + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
    games = pd.read_csv('./csv_Data/BettingResults+Elo/' + str(year) + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])

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
        dict["Year"].append(year)
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
        if (int(dict["Homefield"][-1]) == 1):
            dict["Actual Spread"].append(float(dict["Road Score"][-1]) - float(dict["Home Score"][-1]))
        else:
            dict["Actual Spread"].append(float(dict["Home Score"][-1]) - float(dict["Road Score"][-1]))
        dict["Actual Total"].append(float(dict["Road Score"][-1]) + float(dict["Home Score"][-1]))
        #road team:
        dict["Year"].append(year)
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
        if (int(dict["Homefield"][-1]) == 1):
            dict["Actual Spread"].append(float(dict["Road Score"][-1]) - float(dict["Home Score"][-1]))
        else:
            dict["Actual Spread"].append(float(dict["Home Score"][-1]) - float(dict["Road Score"][-1]))
        dict["Actual Total"].append(float(dict["Road Score"][-1]) + float(dict["Home Score"][-1]))

    print (year)
dfFinal = pd.DataFrame.from_dict(dict)
print (dfFinal)
dfFinal.to_csv("./new_csv_Data/bigboy.csv")
