import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from cfbFcns import getTotalBin

dict = {}
a = pd.read_csv('./csv_Data/bigboyAltGoodData.csv', encoding = "ISO-8859-1")
for index, row in a.iterrows():
    if (getTotalBin(row["O/U"]) not in dict):
        dict[getTotalBin(row["O/U"])] = 0
    dict[getTotalBin(row["O/U"])] += 1
for i in sorted(dict.keys()):
    print (i, dict[i])
