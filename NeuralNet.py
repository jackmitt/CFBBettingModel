import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from evalPredictions import testFit
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score

bigboy = pd.read_csv('./csv_Data/bigboy.csv', encoding = "ISO-8859-1")
train = pd.read_csv('./csv_Data/train.csv', encoding = "ISO-8859-1")
test = pd.read_csv('./csv_Data/test.csv', encoding = "ISO-8859-1")
bigboy = bigboy.dropna()
train = train.dropna()
test = test.dropna()

Xcols = []
cur = 3
while (cur <= 78):
    Xcols.append(cur)
    cur += 1
cur = 81
while (cur <= 158):
    Xcols.append(cur)
    cur += 1
Xcols.append(167)

fuckedCols = []
fuckedCols.append(3)
fuckedCols.append(15)
cur = 17
while (cur <= 93):
    fuckedCols.append(cur)
    cur += 1
cur = 95
while (cur <= 170):
    fuckedCols.append(cur)
    cur += 1

#Code for no train/test split below

#X = bigboy.iloc[:,Xcols]
#y = bigboy.iloc[:,168]
#scaler = StandardScaler()
#scaler.fit(X)
#X_scaled = scaler.transform(X)
#mlp = MLPRegressor(hidden_layer_sizes=(11, ), max_iter = 10000000, verbose = True, solver = 'adam')
#mlp.fit(X_scaled, y)
#predictions = mlp.predict(X_scaled)
#print ("-----------------------------------------------------------------------------------")
#print ("R-Sq: ", r2_score(y, predictions))
#bigboy["PFITS"] = predictions
#print (bigboy)
#bigboy.to_csv("./csv_Data/bigboy_MLPpredict.csv")
#testFit(bigboy,0,0,100)


X_train = train.iloc[:,fuckedCols]
X_test = test.iloc[:,fuckedCols]
y_train = train.iloc[:,1]
y_test = test.iloc[:,1]
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
mlp = MLPRegressor(hidden_layer_sizes=(11, ), max_iter = 10000000, verbose = True, solver = 'adam', alpha = 1)
mlp.fit(X_train, y_train)
predictions = mlp.predict(X_test)
print ("-----------------------------------------------------------------------------------")
print ("R-Sq: ", r2_score(y_test, predictions))
test["PFITS"] = predictions
test.to_csv("./csv_Data/test_predictions.csv")
testFit(test,5,5,100)
