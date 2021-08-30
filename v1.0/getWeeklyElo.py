import pandas as pd
import numpy as np
import operator
from cfbFcns import standardizeTeamName

curElo = {}
teamDf = pd.read_csv('./csv_Data/majorDivTeams.csv', encoding = "ISO-8859-1")
for index, row in teamDf.iterrows():
    curElo[standardizeTeamName(row["school"],False)] = {"Elo":1500,"G":0}
#Adding Idaho Manually since they are no longer FBS
curElo["Idaho"] = {"Elo":1500,"G":0}
#{Spread : Prob of Fav winning that spread}
pDict = {}
pChart = pd.read_csv('./csv_data/spreadProbChart.csv', encoding = "ISO-8859-1")
for index, row in pChart.iterrows():
    pDict[float(row["spread"])] = float(row["fav win"].split("%")[0])/100

#k function is a complete gut call
years = []
zzz = 1999
while (zzz <= 2020):
    years.append(zzz)
    zzz += 1
for year in years:
    eloLoss = 0
    if (year >= 2002 and year <= 2019):
        curYearDf = pd.read_csv('./csv_Data/BettingResults/' + str(year) + '.csv', encoding = "ISO-8859-1")
        for index, row in curYearDf.iterrows():
            #Case 1: Home Team is FCS (Home and Road cannot both be FCS) - win prob based on game spreads
            if (len(standardizeTeamName(standardizeTeamName(row["Home Team"], False),True).split("Error: ")) > 1):
                if (standardizeTeamName(row["Road Team"], False) == row["Favorite"]):
                    if (float(row["Spread"]) >= 20):
                        eR = 1
                        eH = 0
                    else:
                        eR = pDict[float(row["Spread"])]
                        eH = 1 - eR
                else:
                    if (float(row["Spread"]) >= 20):
                        eR = 0
                        eH = 1
                    else:
                        eH = pDict[float(row["Spread"])]
                        eR = 1 - eH
                kR = 150**(50/(curElo[standardizeTeamName(row["Road Team"], False)]["G"]+50))
                if (int(row["Road Score"]) > int(row["Home Score"])):
                    curElo[standardizeTeamName(row["Road Team"], False)]["Elo"] += kR*(1-eR)
                    eloLoss -= kR*(1-eR)
                else:
                    curElo[standardizeTeamName(row["Road Team"], False)]["Elo"] += kR*(0-eR)
                    eloLoss += kR*(0-eR)
                curElo[standardizeTeamName(row["Road Team"], False)]["G"] += min(eH,eR)/max(eH,eR)
            #Case 2: Road Team is FCS - win prob based on game spreads
            elif (len(standardizeTeamName(standardizeTeamName(row["Road Team"], False),True).split("Error: ")) > 1):
                if (standardizeTeamName(row["Home Team"], False) == row["Favorite"]):
                    if (float(row["Spread"]) >= 20):
                        eH = 1
                        eR = 0
                    else:
                        eH = pDict[float(row["Spread"])]
                        eR = 1 - eH
                else:
                    if (float(row["Spread"]) >= 20):
                        eR = 1
                        eH = 0
                    else:
                        eR = pDict[float(row["Spread"])]
                        eH = 1 - eR
                kH = 150**(50/(curElo[standardizeTeamName(row["Home Team"], False)]["G"]+50))
                if (int(row["Home Score"]) > int(row["Road Score"])):
                    curElo[standardizeTeamName(row["Home Team"], False)]["Elo"] += kH*(1-eH)
                    eloLoss -= kH*(1-eH)
                else:
                    curElo[standardizeTeamName(row["Home Team"], False)]["Elo"] += kH*(0-eH)
                    eloLoss += kH*(0-eH)
                curElo[standardizeTeamName(row["Home Team"], False)]["G"] += min(eH,eR)/max(eH,eR)
            #Case 3: Both teams are FBS
            else:
                # 0.05 to compensate for home field
                eH = min(1, 1/(1+10**((curElo[standardizeTeamName(row["Road Team"], False)]["Elo"] - curElo[standardizeTeamName(row["Home Team"], False)]["Elo"])/400)) + 0.05)
                eR = 1 - eH
                kH = 150**(50/(curElo[standardizeTeamName(row["Home Team"], False)]["G"]+50))
                kR = 150**(50/(curElo[standardizeTeamName(row["Road Team"], False)]["G"]+50))
                if (int(row["Home Score"]) > int(row["Road Score"])):
                    curElo[standardizeTeamName(row["Home Team"], False)]["Elo"] += kH*(1-eH)
                    curElo[standardizeTeamName(row["Road Team"], False)]["Elo"] += kR*(0-eR)
                else:
                    curElo[standardizeTeamName(row["Home Team"], False)]["Elo"] += kH*(0-eH)
                    curElo[standardizeTeamName(row["Road Team"], False)]["Elo"] += kR*(1-eR)
                curElo[standardizeTeamName(row["Road Team"], False)]["G"] += min(eH,eR)/max(eH,eR)
                curElo[standardizeTeamName(row["Home Team"], False)]["G"] += min(eH,eR)/max(eH,eR)
        set = []
        zSum = 0
        for teams in curElo:
            curElo[teams]["G"] = 0
            set.append(curElo[teams]["Elo"])
        for teams in curElo:
            curElo[teams]["Elo"] -= eloLoss/131
    else:
        curYearDf = pd.read_csv('./csv_Data/GameResults/' + str(year) + '.csv', encoding = "ISO-8859-1")
        for index, row in curYearDf.iterrows():
            if (len(standardizeTeamName(standardizeTeamName(row["home_team"], False),True).split("Error: ")) > 1):
                eR = 1
                eH = 0
                kR = 150**(50/(curElo[standardizeTeamName(row["away_team"], False)]["G"]+50))
                if (int(row["away_points"]) > int(row["home_points"])):
                    curElo[standardizeTeamName(row["away_team"], False)]["Elo"] += kR*(1-eR)
                    eloLoss -= kR*(1-eR)
                else:
                    curElo[standardizeTeamName(row["away_team"], False)]["Elo"] += kR*(0-eR)
                    eloLoss += kR*(1-eR)
                curElo[standardizeTeamName(row["away_team"], False)]["G"] += min(eH,eR)/max(eH,eR)
            elif (len(standardizeTeamName(standardizeTeamName(row["away_team"], False),True).split("Error: ")) > 1):
                eR = 0
                eH = 1
                kH = 150**(50/(curElo[standardizeTeamName(row["home_team"], False)]["G"]+50))
                if (int(row["home_points"]) > int(row["away_points"])):
                    curElo[standardizeTeamName(row["home_team"], False)]["Elo"] += kH*(1-eH)
                    eloLoss -= kH*(1-eH)
                else:
                    curElo[standardizeTeamName(row["home_team"], False)]["Elo"] += kH*(0-eH)
                    eloLoss += kH*(0-eH)
                curElo[standardizeTeamName(row["home_team"], False)]["G"] += min(eH,eR)/max(eH,eR)
            else:
                eH = min(1, 1/(1+10**((curElo[standardizeTeamName(row["away_team"], False)]["Elo"] - curElo[standardizeTeamName(row["home_team"], False)]["Elo"])/400)) + 0.05)
                eR = 1 - eH
                kH = 150**(50/(curElo[standardizeTeamName(row["home_team"], False)]["G"]+50))
                kR = 150**(50/(curElo[standardizeTeamName(row["away_team"], False)]["G"]+50))
                if (int(row["home_points"]) > int(row["away_points"])):
                    curElo[standardizeTeamName(row["home_team"], False)]["Elo"] += kH*(1-eH)
                    curElo[standardizeTeamName(row["away_team"], False)]["Elo"] += kR*(0-eR)
                else:
                    curElo[standardizeTeamName(row["home_team"], False)]["Elo"] += kH*(0-eH)
                    curElo[standardizeTeamName(row["away_team"], False)]["Elo"] += kR*(1-eR)
                curElo[standardizeTeamName(row["away_team"], False)]["G"] += min(eH,eR)/max(eH,eR)
                curElo[standardizeTeamName(row["home_team"], False)]["G"] += min(eH,eR)/max(eH,eR)
        set = []
        for teams in curElo:
            curElo[teams]["G"] = 0
            set.append(curElo[teams]["Elo"])
        for teams in curElo:
            curElo[teams]["Elo"] -= eloLoss/131

#all the 2021 stuff now
