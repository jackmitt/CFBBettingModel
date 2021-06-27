import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

years = ["2013","2015","2016","2017","2018"]
weeks = [2,3,4]
statsDict = {}
appendedHome = False
appendedRoad = False

stats = pd.read_csv('./csv_Data/advStatsFwdLooking/2016.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
games = pd.read_csv('./csv_Data/BettingResults+Elo/2016.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])

for week in weeks:
    if (week == 2 or week == 3 or week == 4):
        continue
    else:
        for col in games.columns:
            statsDict[col] = []
        for col in stats.columns:
            if (col != "Week" and col != "Team"):
                statsDict["Home " + col] = []
                statsDict["Road " + col] = []
        for year in years:
            stats = pd.read_csv('./csv_Data/advStatsFwdLooking/' + year + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
            games = pd.read_csv('./csv_Data/BettingResults+Elo/' + year + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
            for gamesIndex, gamesRow in games.iterrows():
                if (gamesRow["Week"] == "Bowl" or int(gamesRow["Week"]) > week):
                    break
                #Case that aggregates later weeks in season
                if (week == 999):
                    if (int(gamesRow["Week"]) > 10):
                        for col in games.columns:
                            statsDict[col].append(gamesRow[col])
                        for statsIndex, statsRow in stats.iterrows():
                            if (statsRow["Week"] == "Year End" or int(statsRow["Week"]) > int(gamesRow["Week"])):
                                break
                            if (standardizeTeamName(gamesRow["Home Team"],False) == standardizeTeamName(statsRow["Team"],False)):
                                if (not appendedHome):
                                    for col in stats.columns:
                                        if (col != "Week" and col != "Team"):
                                            statsDict["Home " + col].append(statsRow[col])
                                    appendedHome = True
                                else:
                                    for col in stats.columns:
                                        if (col != "Week" and col != "Team"):
                                            del statsDict["Home " + col][-1]
                                            statsDict["Home " + col].append(statsRow[col])
                            if (standardizeTeamName(gamesRow["Road Team"],False) == standardizeTeamName(statsRow["Team"],False)):
                                if (not appendedRoad):
                                    for col in stats.columns:
                                        if (col != "Week" and col != "Team"):
                                            statsDict["Road " + col].append(statsRow[col])
                                    appendedRoad = True
                                else:
                                    for col in stats.columns:
                                        if (col != "Week" and col != "Team"):
                                            del statsDict["Road " + col][-1]
                                            statsDict["Road " + col].append(statsRow[col])
                        if (not appendedHome):
                            for col in stats.columns:
                                if (col != "Week" and col != "Team"):
                                    statsDict["Home " + col].append(np.nan)
                        if (not appendedRoad):
                            for col in stats.columns:
                                if (col != "Week" and col != "Team"):
                                    statsDict["Road " + col].append(np.nan)
                        appendedHome = False
                        appendedRoad = False
                #Case that aggregates specific weeks in the list
                elif (int(gamesRow["Week"]) == week):
                    for col in games.columns:
                        statsDict[col].append(gamesRow[col])
                    for statsIndex, statsRow in stats.iterrows():
                        if (int(statsRow["Week"]) > week):
                            break
                        if (standardizeTeamName(gamesRow["Home Team"],False) == standardizeTeamName(statsRow["Team"],False)):
                            if (not appendedHome):
                                for col in stats.columns:
                                    if (col != "Week" and col != "Team"):
                                        statsDict["Home " + col].append(statsRow[col])
                                appendedHome = True
                            else:
                                for col in stats.columns:
                                    if (col != "Week" and col != "Team"):
                                        del statsDict["Home " + col][-1]
                                        statsDict["Home " + col].append(statsRow[col])
                        if (standardizeTeamName(gamesRow["Road Team"],False) == standardizeTeamName(statsRow["Team"],False)):
                            if (not appendedRoad):
                                for col in stats.columns:
                                    if (col != "Week" and col != "Team"):
                                        statsDict["Road " + col].append(statsRow[col])
                                appendedRoad = True
                            else:
                                for col in stats.columns:
                                    if (col != "Week" and col != "Team"):
                                        del statsDict["Road " + col][-1]
                                        statsDict["Road " + col].append(statsRow[col])
                    if (not appendedHome):
                        for col in stats.columns:
                            if (col != "Week" and col != "Team"):
                                statsDict["Home " + col].append(np.nan)
                    if (not appendedRoad):
                        for col in stats.columns:
                            if (col != "Week" and col != "Team"):
                                statsDict["Road " + col].append(np.nan)
                    appendedHome = False
                    appendedRoad = False
    final = pd.DataFrame.from_dict(statsDict)
    print (final)
    final.to_csv("./csv_Data/TrainingDataByWeek/" + str(week) + ".csv")
