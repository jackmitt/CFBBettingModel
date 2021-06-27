import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

bigboy = pd.read_csv('./new_csv_Data/bigboy.csv', encoding = "ISO-8859-1")



newDict = {}
for col in bigboy.columns:
    if (col == "Year" or col == "Week" or col == "Favorite" or col == "Spread" or col == "O/U" or col == "Home Score" or col == "Road Score" or col == "Spread Winner" or col == "O/U Outcome" or col == "TrueHF" or col == "alt_spread" or col == "Actual Spread" or col == "Actual Total"):
        newDict[col] = []
    elif (col != "Opponent" and col != "Homefield" and col != "Neutral Field" and col[0] != "X"):
        newDict["H" + col] = []
        newDict["R" + col] = []
for index, row in bigboy.iterrows():
    print (index)
    try:
        if (index+1 == len(bigboy.index)):
            break
        if (row["Opponent"] == bigboy.at[index+1,"Team"]):
            #TEMP week thing
            if (int(row["Week"]) >= 5):
                for col in bigboy.columns:
                    if (col == "Year" or col == "Week" or col == "Favorite" or col == "Spread" or col == "O/U" or col == "Home Score" or col == "Road Score" or col == "Spread Winner" or col == "O/U Outcome" or col == "TrueHF" or col == "alt_spread" or col == "Actual Spread" or col == "Actual Total"):
                        newDict[col].append(row[col])
                    elif (col != "Opponent" and col != "Homefield" and col != "Neutral Field" and col[0] != "X"):
                        newDict["H" + col].append(row[col])
                        newDict["R" + col].append(bigboy.at[index+1,col])
    except:
        pass


dfFinal = pd.DataFrame.from_dict(newDict)
print (dfFinal)
dfFinal.to_csv("./new_csv_Data/bigboyAlt.csv")
