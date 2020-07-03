import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

we = [4]
for w in we:
    bigboy = pd.read_csv('./csv_Data/bigboyAltWeek' + str(w) + '-.csv', encoding = "ISO-8859-1")
    drop1 = []
    for index, row in bigboy.iterrows():
        print (index)
        if (int(row["Year"]) <= 2013 or int(row["Week"]) == 1):
            drop1.append(index)
    bigboy = bigboy.drop(drop1)
    bigboy.to_csv("./csv_Data/bigboyAltGoodDataWeek" + str(w) + '-.csv')
