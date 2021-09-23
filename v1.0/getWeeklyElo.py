import pandas as pd
import numpy as np
import operator
from cfbFcns import standardizeTeamName
import cfbd
from cfbd.rest import ApiException

curWeek = 5

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

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'XBWTTfw3Jo8o/r/jmDnRA6SsnoHp0MKKPBEE0UGID/hPKqzKLV/+0Ljn06dCbQRS'
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 2021
for i in range(1, curWeek):
    api_response = api_instance.get_games(year=year, week=i, season_type="regular")
    for x in api_response:
        if (len(standardizeTeamName(standardizeTeamName(x.home_team, False),True).split("Error: ")) > 1):
            eR = 1
            eH = 0
            kR = 150**(50/(curElo[standardizeTeamName(x.away_team, False)]["G"]+50))
            if (int(x.away_points) > int(x.home_points)):
                curElo[standardizeTeamName(x.away_team, False)]["Elo"] += kR*(1-eR)
                eloLoss -= kR*(1-eR)
            else:
                curElo[standardizeTeamName(x.away_team, False)]["Elo"] += kR*(0-eR)
                eloLoss += kR*(1-eR)
            curElo[standardizeTeamName(x.away_team, False)]["G"] += min(eH,eR)/max(eH,eR)
        elif (len(standardizeTeamName(standardizeTeamName(x.away_team, False),True).split("Error: ")) > 1):
            eR = 0
            eH = 1
            kH = 150**(50/(curElo[standardizeTeamName(x.home_team, False)]["G"]+50))
            if (int(x.home_points) > int(x.away_points)):
                curElo[standardizeTeamName(x.home_team, False)]["Elo"] += kH*(1-eH)
                eloLoss -= kH*(1-eH)
            else:
                curElo[standardizeTeamName(x.home_team, False)]["Elo"] += kH*(0-eH)
                eloLoss += kH*(0-eH)
            curElo[standardizeTeamName(x.home_team, False)]["G"] += min(eH,eR)/max(eH,eR)
        else:
            eH = min(1, 1/(1+10**((curElo[standardizeTeamName(x.away_team, False)]["Elo"] - curElo[standardizeTeamName(x.home_team, False)]["Elo"])/400)) + 0.05)
            eR = 1 - eH
            kH = 150**(50/(curElo[standardizeTeamName(x.home_team, False)]["G"]+50))
            kR = 150**(50/(curElo[standardizeTeamName(x.away_team, False)]["G"]+50))
            if (int(x.home_points) > int(x.away_points)):
                curElo[standardizeTeamName(x.home_team, False)]["Elo"] += kH*(1-eH)
                curElo[standardizeTeamName(x.away_team, False)]["Elo"] += kR*(0-eR)
            else:
                curElo[standardizeTeamName(x.home_team, False)]["Elo"] += kH*(0-eH)
                curElo[standardizeTeamName(x.away_team, False)]["Elo"] += kR*(1-eR)
            curElo[standardizeTeamName(x.away_team, False)]["G"] += min(eH,eR)/max(eH,eR)
            curElo[standardizeTeamName(x.home_team, False)]["G"] += min(eH,eR)/max(eH,eR)

if (curWeek == 1):
    incElo = []
    lastWeek = pd.read_csv('./new_csv_Data/2021/BettingLinesWeek' + str(1) + '.csv', encoding = "ISO-8859-1")
    for index, row in lastWeek.iterrows():
        try:
            incElo.append(curElo[standardizeTeamName(row["team"], False)]["Elo"])
        except:
            incElo.append(np.nan)
    lastWeek["incElo"] = incElo
    lastWeek.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(1) + '.csv')
elif (curWeek <= 4):
    incElo = []
    resElo = []
    lastWeek = pd.read_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek - 1) + '.csv', encoding = "ISO-8859-1")
    for index, row in lastWeek.iterrows():
        try:
            resElo.append(curElo[standardizeTeamName(row["team"], False)]["Elo"])
        except:
            resElo.append(np.nan)
    lastWeek["resElo"] = resElo
    lastWeek.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek - 1) + '.csv')
    thisWeek = pd.read_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek) + '.csv', encoding = "ISO-8859-1")
    for index, row in thisWeek.iterrows():
        try:
            incElo.append(curElo[standardizeTeamName(row["team"], False)]["Elo"])
        except:
            incElo.append(np.nan)
    thisWeek["incElo"] = incElo
    thisWeek.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek) + '.csv')
elif (curWeek == 5):
    homeIncElo = []
    awayIncElo = []
    resElo = []
    lastWeek = pd.read_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek - 1) + '.csv', encoding = "ISO-8859-1")
    for index, row in lastWeek.iterrows():
        try:
            resElo.append(curElo[standardizeTeamName(row["team"], False)]["Elo"])
        except:
            resElo.append(np.nan)
    lastWeek["resElo"] = resElo
    lastWeek.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek - 1) + '.csv')
    thisWeek = pd.read_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek) + '.csv', encoding = "ISO-8859-1")
    for index, row in thisWeek.iterrows():
        try:
            homeIncElo.append(curElo[standardizeTeamName(row["Home Team"], False)]["Elo"])
        except:
            homeIncElo.append(np.nan)
        try:
            awayIncElo.append(curElo[standardizeTeamName(row["Road Team"], False)]["Elo"])
        except:
            awayIncElo.append(np.nan)
    thisWeek["Home Incoming Elo"] = homeIncElo
    thisWeek["Road Incoming Elo"] = awayIncElo
    thisWeek.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek) + '.csv')
else:
    homeIncElo = []
    awayIncElo = []
    homeResElo = []
    awayResElo = []
    lastWeek = pd.read_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek - 1) + '.csv', encoding = "ISO-8859-1")
    for index, row in lastWeek.iterrows():
        try:
            homeResElo.append(curElo[standardizeTeamName(row["Home Team"], False)]["Elo"])
        except:
            homeResElo.append(np.nan)
        try:
            awayResElo.append(curElo[standardizeTeamName(row["Road Team"], False)]["Elo"])
        except:
            awayResElo.append(np.nan)
    lastWeek["Home Resulting Elo"] = homeResElo
    lastWeek["Road Resulting Elo"] = awayResElo
    lastWeek.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek - 1) + '.csv')
    thisWeek = pd.read_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek) + '.csv', encoding = "ISO-8859-1")
    for index, row in thisWeek.iterrows():
        try:
            homeIncElo.append(curElo[standardizeTeamName(row["Home Team"], False)]["Elo"])
        except:
            homeIncElo.append(np.nan)
        try:
            awayIncElo.append(curElo[standardizeTeamName(row["Road Team"], False)]["Elo"])
        except:
            awayIncElo.append(np.nan)
    thisWeek["Home Incoming Elo"] = homeIncElo
    thisWeek["Road Incoming Elo"] = awayIncElo
    thisWeek.to_csv('./new_csv_Data/2021/BettingLinesWeek' + str(curWeek) + '.csv')
