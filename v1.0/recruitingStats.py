import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

bigboy = pd.read_csv('./new_csv_Data/bigboy.csv', encoding = "ISO-8859-1")

Fresh = []
Soph = []
Jun = []
Sen = []
added = False


for index, row in bigboy.iterrows():
    print (index)
    df = pd.read_csv('./csv_Data/Recruiting/' + str(row["Year"]) + '.csv', encoding = "ISO-8859-1")
    added = False
    for indexx, roww in df.iterrows():
        if (row["Team"] == standardizeTeamName(roww["team"],False)):
            Fresh.append(float(roww["points"]))
            added = True
            break
    if (not added):
        Fresh.append(0)
    df = pd.read_csv('./csv_Data/Recruiting/' + str(int(row["Year"])-1) + '.csv', encoding = "ISO-8859-1")
    added = False
    for indexx, roww in df.iterrows():
        if (row["Team"] == standardizeTeamName(roww["team"],False)):
            Soph.append(float(roww["points"]))
            added = True
            break
    if (not added):
        Soph.append(0)
    df = pd.read_csv('./csv_Data/Recruiting/' + str(int(row["Year"])-2) + '.csv', encoding = "ISO-8859-1")
    added = False
    for indexx, roww in df.iterrows():
        if (row["Team"] == standardizeTeamName(roww["team"],False)):
            Jun.append(float(roww["points"]))
            added = True
            break
    if (not added):
        Jun.append(0)
    df = pd.read_csv('./csv_Data/Recruiting/' + str(int(row["Year"])-3) + '.csv', encoding = "ISO-8859-1")
    added = False
    for indexx, roww in df.iterrows():
        if (row["Team"] == standardizeTeamName(roww["team"],False)):
            Sen.append(float(roww["points"]))
            added = True
            break
    if (not added):
        Sen.append(0)
bigboy["Freshman Class"] = Fresh
bigboy["Sophomore Class"] = Soph
bigboy["Junior Class"] = Jun
bigboy["Senior Class"] = Sen

bigboy.to_csv("./new_csv_Data/bigboy.csv")
