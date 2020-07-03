import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

years = []
start = 2003
while (start != 2020):
    years.append(start)
    start += 1
dict = {}
match = False

for year in years:
    stats = pd.read_csv('./csv_Data/advStatsFwdLooking/' + str(year) + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
    adjStats = pd.read_csv('./csv_Data/adjAdvStatsFwdLooking/' + str(year) + '.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])

    for col in stats.columns:
        dict[col] = []
    for col in adjStats.columns:
        if (col != "Week" or col != "Team"):
            dict[col] = []

    for index, row in adjStats.iterrows():
        match = False
        for i, r in stats.iterrows():
            if (row["Team"] == r["Team"] and int(row["Week"]) == int(r["Week"])):
                match = True
                for col in stats.columns:
                    if (col != "Week" and col != "Team"):
                        dict[col].append(r[col])
                break
        if (match):
            for col in adjStats.columns:
                dict[col].append(row[col])

    final = pd.DataFrame.from_dict(dict)
    final.to_csv("./csv_Data/combinedFwdLookingStats/" + str(year) + ".csv")
    print (year, len(final.index))
    for key in dict:
        dict[key] = []
