import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from evalPredictions import testClassification

a = pd.read_csv('./new_csv_Data/bigboyBinClassificationOctTest.csv', encoding = "ISO-8859-1")
b = pd.DataFrame()
bRows = []
c = pd.DataFrame()
cRows = []
for index, row in a.iterrows():
    if (int(row["Year"]) == 2018 or int(row["Year"]) == 2019):
        cRows.append(index)
    else:
        bRows.append(index)
b = a.iloc[bRows]
c = a.iloc[cRows]
b.to_csv("./new_csv_Data/bigboyBinClassificationOctTestTrain.csv")
c.to_csv("./new_csv_Data/bigboyBinClassificationOctTestTest.csv")
