import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from evalPredictions import testClassification

a = pd.read_csv('./csv_Data/bigboyBinClassificationWeek5+.csv', encoding = "ISO-8859-1")
for i in range(6):
    print (i)
    b = pd.DataFrame()
    bRows = []
    c = pd.DataFrame()
    cRows = []
    for index, row in a.iterrows():
        if (int(row["Year"]) == 2014+i):
            cRows.append(index)
        else:
            bRows.append(index)
    b = a.iloc[bRows]
    c = a.iloc[cRows]
    b.to_csv("./csv_Data/bigboyBinClassificationTrainWeek5+" + str(i) + ".csv")
    c.to_csv("./csv_Data/bigboyBinClassificationTestWeek5+" + str(i) + ".csv")
