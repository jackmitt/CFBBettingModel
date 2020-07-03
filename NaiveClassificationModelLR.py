import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

predictions = []
a = pd.read_csv('./csv_Data/bigboyBinClassification.csv', encoding = "ISO-8859-1")
Y = a["binSpread"]
xCols = []
#Stepwise with alpha = 0.25 from Minitab
#X = a[["FavHF","FavHF_aboveAvg","Sophomore_diff_aboveAvg","Coach_diff_aboveAvg","Sr_diff_aboveAvg","PwrS_diff_aboveAvg","adj_powerSuccess_diff_aboveAvg","adj_passingDowns.explosiveness_diff_aboveAvg","adj_rushingPlays.successRate_diff_aboveAvg","RedZone ppa_diff_aboveAvg","Pts_diff_aboveAvg"]]
for col in a.columns:
    if (col == "FavHF" or '_aboveAvg' in col):
        xCols.append(col)
X = pd.DataFrame(a, columns=xCols)
model = LogisticRegression(max_iter = 100000)
model.fit(X = X, y = Y)
for p in model.predict_proba(X):
    predictions.append(p[1])
a["PFITS"] = predictions
a.to_csv("./csv_Data/LogisticPythonPredictionsLR.csv")
