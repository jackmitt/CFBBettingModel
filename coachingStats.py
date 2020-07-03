import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

def getCoachRating(team, year):
    df = pd.read_csv('./csv_Data/Coaching/1960-2019.csv', encoding = "ISO-8859-1")
    winPctDiff = []
    teams = []
    g = 0
    fName = "Error"
    lName = "Error"
    for index, row in df.iterrows():
        if (int(row["year"]) > year):
            break
        if (standardizeTeamName(row["school"],False) == team and year == int(row["year"])):
            if (int(row["games"]) > g):
                fName = row["first_name"]
                lName = row["last_name"]
                g = int(row["games"])
    for index, row in df.iterrows():
        if (int(row["year"]) == year):
            break
        if (fName == row["first_name"] and lName == row["last_name"]):
            if (standardizeTeamName(row["school"],False) not in teams):
                teams.append(standardizeTeamName(row["school"],False))
    for a in teams:
        winPctHist = []
        winPct = []
        for index, row in df.iterrows():
            if (int(row["year"]) == year):
                break
            if (standardizeTeamName(row["school"],False) == a and (fName != row["first_name"] or lName != row["last_name"])):
                winPctHist.append(int(row["wins"])/(int(row["losses"])+int(row["wins"])))
            elif (standardizeTeamName(row["school"],False) == a and (fName == row["first_name"] and lName == row["last_name"])):
                winPct.append(int(row["wins"])/(int(row["losses"])+int(row["wins"])))
        if (len(winPctHist) < 5):
            continue
        for bbb in winPct:
            winPctDiff.append(bbb - np.average(winPctHist))
    if (len(winPctDiff) > 0):
        return (np.average(winPctDiff))
    else:
        return 0

dict = {}
cur = 2003
while (cur <= 2019):
    dict[str(cur)] = {}
    cur += 1
coach = []
bigboy = pd.read_csv('./csv_Data/bigboy.csv', encoding = "ISO-8859-1")
for index, row in bigboy.iterrows():
    print (index)
    if (row["Team"] in dict[str(row["Year"])]):
        coach.append(dict[str(row["Year"])][row["Team"]])
    else:
        curRate = getCoachRating(row["Team"], int(row["Year"]))
        coach.append(curRate)
        dict[str(row["Year"])][row["Team"]] = curRate
bigboy["Coach WPAR"] = coach
bigboy.to_csv("./csv_Data/bigboy.csv")
