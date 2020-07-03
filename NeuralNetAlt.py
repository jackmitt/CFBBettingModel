import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from evalPredictions import testFit
from evalPredictions import testFitAlt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score

bigboy = pd.read_csv('./csv_Data/bigboyAlt.csv', encoding = "ISO-8859-1")
train = pd.read_csv('./csv_Data/trainAlt.csv', encoding = "ISO-8859-1")
test = pd.read_csv('./csv_Data/testAlt.csv', encoding = "ISO-8859-1")
bigboy = bigboy.dropna()
train = train.dropna()
test = test.dropna()

cols = []
cur = 5
while(cur <= 158):
    cols.append(cur)
    cur += 1
cols.append(166)
cur = 170
while(cur <= 213):
    cols.append(cur)
    cur += 1
# Xcols.append(167)
#
# fuckedCols = []
# fuckedCols.append(4)
# fuckedCols.append(5)
# cur = 7
# while (cur <= 44):
#     fuckedCols.append(cur)
#     cur += 1
# cur = 47
# while (cur <= 84):
#     fuckedCols.append(cur)
#     cur += 1
# fuckedCols.append(88)
# fuckedCols.append(89)
# cur = 91
# while (cur <= 166):
#     fuckedCols.append(cur)
#     cur += 1
# fuckedCols.append(170)

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

# best = -999999
# hl = -999999
# for i in range(20):
#     print (i+1)
#     tot = []
#     for j in range(5):
#         X_train = train.iloc[:,Xcols]
#         X_test = test.iloc[:,Xcols]
#         y_train = train.iloc[:,174]
#         y_test = test.iloc[:,174]
#         scaler = StandardScaler()
#         scaler.fit(X_train)
#         X_train = scaler.transform(X_train)
#         X_test = scaler.transform(X_test)
#         mlp = MLPRegressor(hidden_layer_sizes=(i+1, ), max_iter = 10000000, verbose = False, solver = 'adam', alpha = 0.001)
#         mlp.fit(X_train, y_train)
#         predictions = mlp.predict(X_test)
#         #print ("-----------------------------------------------------------------------------------")
#         #print ("R-Sq OU: ", r2_score(y_test, predictions))
#         test["PFITS Total"] = predictions
#
#         X_train = train.iloc[:,Xcols]
#         X_test = test.iloc[:,Xcols]
#         y_train = train.iloc[:,173]
#         y_test = test.iloc[:,173]
#         scaler = StandardScaler()
#         scaler.fit(X_train)
#         X_train = scaler.transform(X_train)
#         X_test = scaler.transform(X_test)
#         mlp = MLPRegressor(hidden_layer_sizes=(i+1, ), max_iter = 10000000, verbose = False, solver = 'adam', alpha = 0.001)
#         mlp.fit(X_train, y_train)
#         predictions = mlp.predict(X_test)
#         # print ("-----------------------------------------------------------------------------------")
#         # print ("R-Sq Spread: ", r2_score(y_test, predictions))
#         test["PFITS Spread"] = predictions
#
#
#         #test.to_csv("./csv_Data/test_predictionsAlt.csv")
#         tot.append(testFitAlt(test,0,0,100))
#     if (np.average(tot) > best):
#         best = np.average(tot)
#         hl = i+1
# print ("Best:", best)
# print ("Hidden Layers:", hl)


X_train = train.iloc[:,cols]
X_test = test.iloc[:,cols]
y_train = train.iloc[:,169]
y_test = test.iloc[:,169]
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
mlp = MLPRegressor(hidden_layer_sizes=(4, ), max_iter = 10000000, verbose = False, solver = 'adam', alpha = 0.001)
mlp.fit(X_train, y_train)
predictions = mlp.predict(X_test)
print ("-----------------------------------------------------------------------------------")
print ("R-Sq OU: ", r2_score(y_test, predictions))
test["PFITS Total"] = predictions

X_train = train.iloc[:,cols]
X_test = test.iloc[:,cols]
y_train = train.iloc[:,168]
y_test = test.iloc[:,168]
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
mlp = MLPRegressor(hidden_layer_sizes=(4, ), max_iter = 10000000, verbose = False, solver = 'adam', alpha = 0.001)
mlp.fit(X_train, y_train)
predictions = mlp.predict(X_test)
print ("-----------------------------------------------------------------------------------")
print ("R-Sq Spread: ", r2_score(y_test, predictions))
test["PFITS Spread"] = predictions

testFitAlt(test,0,0,100)
testFitAlt(test,3,3,100)
testFitAlt(test,5,5,100)
test.to_csv("./csv_Data/NN_test_predictionsAlt.csv")
