import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

bigboy = pd.read_csv('./csv_Data/bigboyAltGoodDataWeek234.csv', encoding = "ISO-8859-1")
bigboy = bigboy.dropna()
years = [2014,2015,2016,2017,2018,2019]
Hadded = False
Radded = False
dict = {}
for year in years:
    print (year)
    a = pd.read_csv('./csv_Data/advStatsSeason/' + str(year - 1) + '.csv', encoding = "ISO-8859-1")
    for index, row in bigboy.iterrows():
        Hadded = False
        Radded = False
        if (int(row["Year"]) > year):
            break
        elif (int(row["Year"]) < year):
            continue
        for i, r in a.iterrows():
            if (row["HTeam"] == standardizeTeamName(r["team"], False)):
                Hadded = True
                for col in a.columns:
                    if (col != "team" and col != "season" and col != "conference"):
                        if ("offense" in col):
                            letter = "o"
                        else:
                            letter = "d"
                        if ("H" + letter + "_lastYear_" + col.split("ense.")[1] not in dict):
                            dict["H" + letter + "_lastYear_" + col.split("ense.")[1]] = []
                        dict["H" + letter + "_lastYear_" + col.split("ense.")[1]].append(r[col])
            elif (row["RTeam"] == standardizeTeamName(r["team"], False)):
                Radded = True
                for col in a.columns:
                    if (col != "team" and col != "season" and col != "conference"):
                        if ("offense" in col):
                            letter = "o"
                        else:
                            letter = "d"
                        if ("R" + letter + "_lastYear_" + col.split("ense.")[1] not in dict):
                            dict["R" + letter + "_lastYear_" + col.split("ense.")[1]] = []
                        dict["R" + letter + "_lastYear_" + col.split("ense.")[1]].append(r[col])
        if (not Hadded):
            for col in a.columns:
                if (col != "team" and col != "season" and col != "conference"):
                    if ("offense" in col):
                        letter = "o"
                    else:
                        letter = "d"
                    if ("H" + letter + "_lastYear_" + col.split("ense.")[1] not in dict):
                        dict["H" + letter + "_lastYear_" + col.split("ense.")[1]] = []
                    dict["H" + letter + "_lastYear_" + col.split("ense.")[1]].append(np.nan)
        if (not Radded):
            for col in a.columns:
                if (col != "team" and col != "season" and col != "conference"):
                    if ("offense" in col):
                        letter = "o"
                    else:
                        letter = "d"
                    if ("R" + letter + "_lastYear_" + col.split("ense.")[1] not in dict):
                        dict["R" + letter + "_lastYear_" + col.split("ense.")[1]] = []
                    dict["R" + letter + "_lastYear_" + col.split("ense.")[1]].append(np.nan)

for key in dict:
    bigboy[key] = dict[key]
bigboy.to_csv("./csv_Data/bigboyAltGoodDataWeek234.csv")
