import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

bigboy = pd.read_csv('./csv_Data/bigboyAlt.csv', encoding = "ISO-8859-1")

bbDict = {}
train = {}
test = {}
for col in bigboy.columns:
    train[col] = []
    test[col] = []
    bbDict[col] = bigboy[col].tolist()

for i in range(len(bbDict["Year"])):
    if (int(bbDict["Year"][i]) < 2018):
        for col in bigboy.columns:
            train[col].append(bbDict[col][i])
    else:
        for col in bigboy.columns:
            test[col].append(bbDict[col][i])

finalTrain = pd.DataFrame.from_dict(train)
finalTest = pd.DataFrame.from_dict(test)
print (finalTrain)
print (finalTest)
print (bigboy)

finalTrain.to_csv("./csv_Data/trainAlt.csv")
finalTest.to_csv("./csv_Data/testAlt.csv")
