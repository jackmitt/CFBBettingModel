import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
import CFBScrapy as cfb
import os.path
from os import path

years = []
fked = []
weeks = []
cur = 2004
while (cur <= 2019):
    years.append(cur)
    cur += 1
cur = 1
while (cur <= 20):
    weeks.append(cur)
    cur += 1

dict = {}
pts = 0
comp = 0
att = 0
top = 0

for year in years:
    dict[str(year)] = {}
    for w in weeks:
        try:
            a = pd.read_csv('./csv_Data/teamGameStats/' + str(year) + '_' + str(w) + '.csv', encoding = "ISO-8859-1")
        except FileNotFoundError:
            continue
        print (year, w)
        if (path.exists('./csv_Data/teamGameStats/' + str(year) + '_' + str(w) + '.csv')):
            for index, row in a.iterrows():
                #print (row, index)
                if (standardizeTeamName(row["school"],False) not in dict[str(year)]):
                    dict[str(year)][standardizeTeamName(row["school"],False)] = {}
                if ("Week " + str(w) not in dict[str(year)][standardizeTeamName(row["school"],False)]):
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)] = {"Points For":0,"Points Against":0,"Completions":0,"Attempts":0,"Opponent Completions":0,"Opponent Attempts":0,"TOP":0,"Opponent TOP":0}
                if (index != 0 and a.iat[index-1,5] != row["school"] and a.iat[index-1,1] == row["id"]):
                    hold = a.iat[index-1,5]
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["Points Against"] = pts
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["Opponent Completions"] = comp
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["Opponent Attempts"] = att
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["Opponent TOP"] = top
                if (index != 0 and a.iat[index-1,5] != row["school"] and a.iat[index-1,1] != row["id"]):
                    dict[str(year)][standardizeTeamName(hold,False)]["Week " + str(w)]["Points Against"] = pts
                    dict[str(year)][standardizeTeamName(hold,False)]["Week " + str(w)]["Opponent Completions"] = comp
                    dict[str(year)][standardizeTeamName(hold,False)]["Week " + str(w)]["Opponent Attempts"] = att
                    dict[str(year)][standardizeTeamName(hold,False)]["Week " + str(w)]["Opponent TOP"] = top
                dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["Points For"] = int(row["points"])
                pts = int(row["points"])
                if (row["category"] == "completionAttempts"):
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["Completions"] = int(row["stat"].split("-")[0])
                    comp = int(row["stat"].split("-")[0])
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["Attempts"] = int(row["stat"].split("-")[1])
                    att = int(row["stat"].split("-")[1])
                if (row["category"] == "possessionTime"):
                    dict[str(year)][standardizeTeamName(row["school"],False)]["Week " + str(w)]["TOP"] = int(row["stat"].split(":")[0])*60 + int(row["stat"].split(":")[1])
                    top = int(row["stat"].split(":")[0])*60 + int(row["stat"].split(":")[1])
bigboy = pd.read_csv('./csv_Data/bigboy.csv', encoding = "ISO-8859-1")
pf = []
pa = []
com = []
at = []
pct = []
ocom = []
oat = []
opct = []
poss = []
oposs = []

print ("----------------------------------------NEXT----------------------------------------------")

for index, row in bigboy.iterrows():
    print (index)
    if (int(row["Year"]) == 2003):
        pf.append(np.nan)
        pa.append(np.nan)
        com.append(np.nan)
        at.append(np.nan)
        pct.append(np.nan)
        ocom.append(np.nan)
        oat.append(np.nan)
        opct.append(np.nan)
        poss.append(np.nan)
        oposs.append(np.nan)
        continue
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Points For"])
        cur += 1
    if (len(temp) == 0):
        pf.append(np.nan)
    else:
        pf.append(np.average(temp))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Points Against"])
        cur += 1
    if (len(temp) == 0):
        pa.append(np.nan)
    else:
        pa.append(np.average(temp))
    cur = 1
    temp = []
    temp2 = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Completions"])
                temp2.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Attempts"])
        cur += 1
    if (len(temp) == 0):
        com.append(np.nan)
        at.append(np.nan)
        pct.append(np.nan)
    else:
        com.append(np.average(temp))
        at.append(np.average(temp2))
        pct.append(np.sum(temp)/np.sum(temp2))
    cur = 1
    temp = []
    temp2 = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Opponent Completions"])
                temp2.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Opponent Attempts"])
        cur += 1
    if (len(temp) == 0):
        ocom.append(np.nan)
        oat.append(np.nan)
        opct.append(np.nan)
    else:
        ocom.append(np.average(temp))
        oat.append(np.average(temp2))
        opct.append(np.sum(temp)/np.sum(temp2))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["TOP"])
        cur += 1
    if (len(temp) == 0):
        poss.append(np.nan)
    else:
        poss.append(np.average(temp))
    cur = 1
    temp = []
    while (cur < int(row["Week"])):
        if (row["Team"] in dict[str(row["Year"])]):
            if ("Week " + str(cur) in dict[str(row["Year"])][row["Team"]]):
                temp.append(dict[str(row["Year"])][row["Team"]]["Week " + str(cur)]["Opponent TOP"])
        cur += 1
    if (len(temp) == 0):
        oposs.append(np.nan)
    else:
        oposs.append(np.average(temp))

print(len(pf))
print(len(pa))
print(len(com))
print(len(at))
print(len(pct))
print(len(ocom))
print(len(oat))
print(len(opct))
print(len(poss))
print(len(oposs))

bigboy["Avg Points For"] = pf
bigboy["Avg Points Against"] = pa
bigboy["Avg Pass Completions"] = com
bigboy["Avg Pass Attempts"] = at
bigboy["Completion Pct"] = pct
bigboy["Avg Opponent Pass Completions"] = ocom
bigboy["Avg Opponent Pass Attempts"] = oat
bigboy["Opponent Completion Pct"] = opct
bigboy["Avg TOP"] = poss
bigboy["Avg Opponent TOP"] = oposs

bigboy.to_csv("./csv_Data/bigboy.csv")
