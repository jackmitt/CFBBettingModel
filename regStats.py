import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
import CFBScrapy as cfb
import os.path
from os import path

years = []
fked = []
weeks = []
cur = 2003
while (cur <= 2019):
    years.append(cur)
    cur += 1
cur = 1
while (cur <= 20):
    weeks.append(cur)
    cur += 1
cur = 2005
while (cur <= 2013):
    fked.append(cur)
    cur += 1

dict = {}

for year in years:
    dict[str(year)] = {}
    for w in weeks:
        print (year, w)
        if (path.exists('./csv_Data/playByPlay/' + str(year) + '_' + str(w) + '.csv')):
            for index, row in pd.read_csv('./csv_Data/playByPlay/' + str(year) + '_' + str(w) + '.csv', encoding = "ISO-8859-1").iterrows():
                if (standardizeTeamName(row["home"],False) not in dict[str(year)]):
                    dict[str(year)][standardizeTeamName(row["home"],False)] = {}
                if (standardizeTeamName(row["away"],False) not in dict[str(year)]):
                    dict[str(year)][standardizeTeamName(row["away"],False)] = {}
                if ("Week " + str(w) not in dict[str(year)][standardizeTeamName(row["home"],False)]):
                    dict[str(year)][standardizeTeamName(row["home"],False)]["Week " + str(w)] = {"Offense Penalty Yards":0,"Defense Penalty Yards":0,"FG Made":0,"FG Attempts":0,"oRedZone ppa":[],"dRedZone ppa":[],"Turnovers":0,"Opponent Turnovers":0}
                if ("Week " + str(w) not in dict[str(year)][standardizeTeamName(row["away"],False)]):
                    dict[str(year)][standardizeTeamName(row["away"],False)]["Week " + str(w)] = {"Offense Penalty Yards":0,"Defense Penalty Yards":0,"FG Made":0,"FG Attempts":0,"oRedZone ppa":[],"dRedZone ppa":[],"Turnovers":0,"Opponent Turnovers":0}
                if (row["play_type"] == "Penalty"):
                    if (int(row["yards_gained"]) < 0):
                        dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["Offense Penalty Yards"] -= int(row["yards_gained"])
                    elif (int(row["yards_gained"]) > 0):
                        dict[str(year)][standardizeTeamName(row["defense"],False)]["Week " + str(w)]["Defense Penalty Yards"] += int(row["yards_gained"])
                    elif (year in fked):
                        try:
                            pText = row["play_text"].split()
                            #print (pText)
                            if (len(pText) > 0 and row["play_text"].split()[0] != "0" and row["play_text"].split()[-1] != "DECLINED." and ("OFFSETTING" not in pText and "offsetting," not in pText) and row["play_text"].split()[-1] != "declined."):
                                if (pText[0] != "PENALTY" and (pText[1].lower() == "penalty" or pText[2].lower() == "penalty" or pText[3].lower() == "penalty") and pText[0] != "Clock"):
                                    string = ""
                                    thisOne = False
                                    for word in pText:
                                        if (word == "PENALTY" or word == "penalty"):
                                            thisOne = True
                                            continue
                                        if (thisOne):
                                            try:
                                                yardage = int(word)
                                            except ValueError:
                                                for words in pText:
                                                    if (words.isdigit()):
                                                        yardage = int(words)
                                            break
                                        if (string == ""):
                                            string = word
                                        else:
                                            string += " "
                                            string += word
                                    if (len(standardizeTeamName(string, True).split("Error:")) > 1):
                                        print (standardizeTeamName(string, True))
                                    if (standardizeTeamName(string, False) == standardizeTeamName(row["offense"],False)):
                                        dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["Offense Penalty Yards"] += yardage
                                    elif (standardizeTeamName(string, False) == standardizeTeamName(row["defense"],False)):
                                        dict[str(year)][standardizeTeamName(row["defense"],False)]["Week " + str(w)]["Defense Penalty Yards"] += yardage
                                else:
                                    count = 0
                                    least = 99
                                    while (count < len(pText)):
                                        if (pText[count] == "PENALTY"):
                                            if (len(standardizeTeamName(pText[count+1], True).split("Error:")) > 1):
                                                print (standardizeTeamName(pText[count+1], True))
                                            penTeam = standardizeTeamName(pText[count+1], True)
                                            least = count
                                        if (pText[count].isdigit() and count > least):
                                            yardage2 = int(pText[count])
                                        count += 1
                                    if (standardizeTeamName(penTeam, False) == standardizeTeamName(row["offense"],False)):
                                        dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["Offense Penalty Yards"] += yardage2
                                    elif (standardizeTeamName(penTeam, False) == standardizeTeamName(row["defense"],False)):
                                        dict[str(year)][standardizeTeamName(row["defense"],False)]["Week " + str(w)]["Defense Penalty Yards"] += yardage2
                        except AttributeError:
                            #print ("EXCEPTION")
                            pass
                if (row["play_type"] == "Field Goal Good"):
                    dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["FG Made"] += 1
                if (row["play_type"] == "Field Goal Good" or row["play_type"] == "Field Goal Missed" or row["play_type"] == "Blocked Field Goal" or row["play_type"] == "Missed Field Goal Return" or row["play_type"] == "Missed Field Goal Return Touchdown" or row["play_type"] == "Blocked Field Goal Touchdown"):
                    dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["FG Attempts"] += 1
                if (row["play_type"] == "Uncategorized"):
                    text = str(row["play_text"]).split()
                    if ("field" in text and "no" in text):
                        dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["FG Attempts"] += 1
                    elif ("field" in text):
                        dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["FG Made"] += 1
                        dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["FG Attempts"] += 1
                if (int(row["yards_to_goal"]) <= 20):
                    if (row["ppa"] is not None and not np.isnan(float(row["ppa"]))):
                        dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["oRedZone ppa"].append(float(row["ppa"]))
                        dict[str(year)][standardizeTeamName(row["defense"],False)]["Week " + str(w)]["dRedZone ppa"].append(float(row["ppa"]))
                if (row["play_type"] == "Fumble Recovery (Opponent)" or row["play_type"] == "Fumble Return Touchdown" or row["play_type"] == "Interception" or row["play_type"] == "Pass Interception Return" or row["play_type"] == "Interception Return Touchdown" or row["play_type"] == "Pass Interception"):
                    dict[str(year)][standardizeTeamName(row["offense"],False)]["Week " + str(w)]["Turnovers"] += 1
                    dict[str(year)][standardizeTeamName(row["defense"],False)]["Week " + str(w)]["Opponent Turnovers"] += 1

bigboy = pd.read_csv('./csv_Data/bigboy.csv', encoding = "ISO-8859-1")
opy = []
dpy = []
fgp = []
orz = []
drz = []
to = []
oto = []

print ("----------------------------------------NEXT----------------------------------------------")

for index, row in bigboy.iterrows():
    print (index)
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Offense Penalty Yards"])
        cur += 1
    if (len(temp) == 0):
        opy.append(np.nan)
    else:
        opy.append(np.average(temp))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Defense Penalty Yards"])
        cur += 1
    if (len(temp) == 0):
        dpy.append(np.nan)
    else:
        dpy.append(np.average(temp))
    cur = 1
    temp = []
    temp2 = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["FG Made"])
                temp2.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["FG Attempts"])
        cur += 1
    if (len(temp) == 0):
        fgp.append(np.nan)
    else:
        fgp.append(np.sum(temp)/np.sum(temp2))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                if (len(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["oRedZone ppa"]) != 0):
                    temp.append(np.average(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["oRedZone ppa"]))
        cur += 1
    if (len(temp) == 0):
        orz.append(np.nan)
    else:
        orz.append(np.average(temp))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                if (len(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["dRedZone ppa"]) != 0):
                    temp.append(np.average(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["dRedZone ppa"]))
        cur += 1
    if (len(temp) == 0):
        drz.append(np.nan)
    else:
        drz.append(np.average(temp))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Turnovers"])
        cur += 1
    if (len(temp) == 0):
        to.append(np.nan)
    else:
        to.append(np.average(temp))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Opponent Turnovers"])
        cur += 1
    if (len(temp) == 0):
        oto.append(np.nan)
    else:
        oto.append(np.average(temp))
bigboy["Offense penalty avg"] = opy
bigboy["Defense penalty avg"] = dpy
bigboy["FG pct"] = fgp
bigboy["oRedZone ppa"] = orz
bigboy["dRedZone ppa"] = drz
bigboy["Turnover avg"] = to
bigboy["Opponent turnover avg"] = oto

bigboy.to_csv("./csv_Data/bigboy.csv")
