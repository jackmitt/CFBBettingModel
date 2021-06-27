import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

predictions = []
a = pd.read_csv('./csv_Data/bigboyBinClassification.csv', encoding = "ISO-8859-1")
Y = a["binSpread"]
X = a[["FavHF","FavHF_aboveAvg","Sophomore_diff_aboveAvg","Coach_diff_aboveAvg","Sr_diff_aboveAvg","PwrS_diff_aboveAvg","adj_powerSuccess_diff_aboveAvg","adj_passingDowns.explosiveness_diff_aboveAvg","adj_rushingPlays.successRate_diff_aboveAvg","RedZone ppa_diff_aboveAvg","Pts_diff_aboveAvg"]]
rows = []
for i in range(len(a.index)):
    rows.append(i)
for index, row in a.iterrows():
    print (index)
    xTest = X.iloc[index].to_numpy()
    yTest = Y.iloc[index]
    xTrain = X.copy()
    yTrain = Y.copy()
    xTrain = xTrain.drop(index)
    yTrain = yTrain.drop(index)
    model = MLPClassifier(max_iter = 100000, alpha = 0.000000001)
    model.fit(X = xTrain, y = yTrain)
    predictions.append(model.predict_proba(xTest.reshape(1,-1))[0][1])
a["PFITS"] = predictions
a.to_csv("./csv_Data/LogisticPythonPredictionsNN.csv")
