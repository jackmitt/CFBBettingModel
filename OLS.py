import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from evalPredictions import testFitAlt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

train = pd.read_csv('./csv_Data/trainAlt.csv', encoding = "ISO-8859-1")
test = pd.read_csv('./csv_Data/testAlt.csv', encoding = "ISO-8859-1")
train = train.dropna()
test = test.dropna()

X_train = train[["RoSr","HoPassDownPpa","RdRushPpa","RdRushSr","Hadj_offense.standardDowns.successRate","Hadj_defense.powerSuccess","Radj_defense.stuffRate","Hadj_defense.rushingPlays.successRate","HElo","RElo","TrueHF","RFreshman Class","HJunior Class","HSenior Class","RSenior Class","RFG pct","RoRedZone ppa","HAvg Points For","RAvg Points For","HAvg Points Against","RAvg Points Against","RAvg Opponent Pass Completions"]]
X_test = test[["RoSr","HoPassDownPpa","RdRushPpa","RdRushSr","Hadj_offense.standardDowns.successRate","Hadj_defense.powerSuccess","Radj_defense.stuffRate","Hadj_defense.rushingPlays.successRate","HElo","RElo","TrueHF","RFreshman Class","HJunior Class","HSenior Class","RSenior Class","RFG pct","RoRedZone ppa","HAvg Points For","RAvg Points For","HAvg Points Against","RAvg Points Against","RAvg Opponent Pass Completions"]]
y_train = train.iloc[:,168]
y_test = test.iloc[:,168]
ols = LinearRegression()
ols.fit(X_train, y_train)
predictions = ols.predict(X_test)
print ("-----------------------------------------------------------------------------------")
print ("R-Sq: ", r2_score(y_test, predictions))
test["PFITS Spread"] = predictions
print(test)
testFitAlt(test,5,5,100)
