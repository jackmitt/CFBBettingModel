import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

years = []
start = 2003
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

for year in years:
    stats = pd.read_csv('./csv_Data/combinedFwdLookingStats/' + str(year) + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
    games = pd.read_csv('./csv_Data/BettingResults+Elo/' + str(year) + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])

    for index, row in games.iterrows():
        if (standardizeTeamName(row["Home Team"], False) not in d1Teams or standardizeTeamName(row["Road Team"], False) not in d1Teams):
            continue
        if (row["Week"] == "Bowl" or int(row["Week"]) == 1 or int(row["Week"]) == 2 or int(row["Week"]) == 3 or int(row["Week"]) == 4):
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
        for col in stats.columns:
            if (col != "Week"):
                dict[col].append(stats.loc[hI,col])
        dict["Opponent"].append(road)
        dict["Homefield"].append(1)
        for col in stats.columns:
            if (col != "Week" and col != "Team"):
                dict["X" + col].append(stats.loc[rI,col])
        dict["Elo"].append(row["Home Incoming Elo"])
        dict["XElo"].append(row["Road Incoming Elo"])
        for col in games.columns:
            if (col != "Week" and col != "Date" and col != "Home Team" and col != "Road Team" and col != "Night Game" and col != "Postseason Game" and col != "Home Incoming Elo" and col != "Road Incoming Elo" and col != "Home Resulting Elo" and col != "Road Resulting Elo"):
                dict[col].append(row[col])
        #road team:
        dict["Year"].append(year)
        dict["Week"].append(week)
        for col in stats.columns:
            if (col != "Week"):
                dict[col].append(stats.loc[rI,col])
        dict["Opponent"].append(home)
        dict["Homefield"].append(0)
        for col in stats.columns:
            if (col != "Week" and col != "Team"):
                dict["X" + col].append(stats.loc[hI,col])
        dict["Elo"].append(row["Road Incoming Elo"])
        dict["XElo"].append(row["Home Incoming Elo"])
        for col in games.columns:
            if (col != "Week" and col != "Date" and col != "Home Team" and col != "Road Team" and col != "Night Game" and col != "Postseason Game" and col != "Home Incoming Elo" and col != "Road Incoming Elo" and col != "Home Resulting Elo" and col != "Road Resulting Elo"):
                dict[col].append(row[col])

    print (year)
dfFinal = pd.DataFrame.from_dict(dict)
print (dfFinal)
dfFinal.to_csv("./csv_Data/bigboy.csv")
