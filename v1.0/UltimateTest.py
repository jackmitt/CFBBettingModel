import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import StandardScaler
from evalPredictions import testClassification
from sklearn.utils import shuffle
import random

predictions = []
allSums = []
x = []
y = []
z = []
allScores = []
a = pd.read_csv('./new_csv_Data/bigboyBinClassificationOctTestTrain.csv', encoding = "ISO-8859-1")
y_train = a["binSpread"]
xCols = []
for col in a.columns:
    if ("aboveAvg" in col):
        xCols.append(col)
scaler = StandardScaler()
X_train = pd.DataFrame(a, columns = xCols)
X_train[xCols] = scaler.fit_transform(X_train[xCols])
bSpread = pd.read_csv('./new_csv_Data/bigboyBinClassificationOctTestTest.csv', encoding = "ISO-8859-1")
y_test = bSpread["binSpread"]
X_test = pd.DataFrame(bSpread, columns = xCols)
X_test[xCols] = scaler.transform(X_test[xCols])

model = LogisticRegression(max_iter = 100000, C = 0.25)
model.fit(X = X_train, y = y_train)
for p in model.predict_proba(X_test):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
    else:
        predictions.append(p[0])
bSpread["PFITS"] = predictions
predictions = []
for index, row in bSpread.iterrows():
    if (float(row["PFITS"]) < 0.5):
        x.append(1 - float(row["PFITS"]))
        y.append(1 - int(row["binSpread"]))
    else:
        x.append(float(row["PFITS"]))
        y.append(int(row["binSpread"]))
# model = LogisticRegression(max_iter = 100000, penalty = 'none')
# x1 = np.array(x)
# y1 = np.array(y)
# model.fit(X = x1.reshape(-1,1), y = y1)
# for p in model.predict_proba(x1.reshape(-1,1)):
#     if (model.classes_[1] == 1):
#         predictions.append(p[1])
#         if (p[1] > 0.5122):
#             z.append(p[1])
#     else:
#         predictions.append(p[0])
bSpread["PFITS"] = x
bSpread["binSpread"] = y
print ("SPREAD ------------------------------------------------------------------------")
testClassification(bSpread, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread", printOption = True)
print ("-------------------------------------------------------------------------------")




predictions = []
allSums = []
x = []
y = []
z = []
allScores = []
a = pd.read_csv('./new_csv_Data/bigboyBinClassificationTotalsALTTrain.csv', encoding = "ISO-8859-1")
y_train = a["binTotal"]
xCols = []
for col in a.columns:
    if ("aboveAvg" in col):
        xCols.append(col)
scaler = StandardScaler()
X_train = pd.DataFrame(a, columns = xCols)
X_train[xCols] = scaler.fit_transform(X_train[xCols])
bTotal = pd.read_csv('./new_csv_Data/bigboyBinClassificationTotalsALTTest.csv', encoding = "ISO-8859-1")
y_test = bTotal["binTotal"]
X_test = pd.DataFrame(bTotal, columns = xCols)
X_test[xCols] = scaler.transform(X_test[xCols])

model = LogisticRegression(max_iter = 100000, C = 0.25)
model.fit(X = X_train, y = y_train)
for p in model.predict_proba(X_test):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
    else:
        predictions.append(p[0])
bTotal["PFITS"] = predictions
predictions = []
for index, row in bTotal.iterrows():
    if (float(row["PFITS"]) < 0.5):
        x.append(1 - float(row["PFITS"]))
        y.append(1 - int(row["binTotal"]))
    else:
        x.append(float(row["PFITS"]))
        y.append(int(row["binTotal"]))
# model = LogisticRegression(max_iter = 100000, penalty = 'none')
# x1 = np.array(x)
# y1 = np.array(y)
# model.fit(X = x1.reshape(-1,1), y = y1)
# for p in model.predict_proba(x1.reshape(-1,1)):
#     if (model.classes_[1] == 1):
#         predictions.append(p[1])
#         if (p[1] > 0.5122):
#             z.append(p[1])
#     else:
#         predictions.append(p[0])
bTotal["PFITS"] = x
bTotal["binTotal"] = y
print ("TOTALS --------------------------------------------------------------------------")
testClassification(bTotal, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "O/U", printOption = True)

dict = {"Year":[], "Week":[], "Home":[], "Away":[], "PFITSSpread":[], "PFITSTotal":[], "binSpread":[], "binTotal":[]}
for index, row in bTotal.iterrows():
    print (index)
    for index2, row2, in bSpread.iterrows():
        if (row["Year"] == row2["Year"] and row["Week"] == row2["Week"] and row["HTeam"] == row2["HTeam"] and row["RTeam"] == row2["RTeam"]):
            dict["Year"].append(row["Year"])
            dict["Week"].append(row["Week"])
            dict["Home"].append(row["HTeam"])
            dict["Away"].append(row["RTeam"])
            dict["PFITSSpread"].append(row2["PFITS"])
            dict["PFITSTotal"].append(row["PFITS"])
            dict["binSpread"].append(row2["binSpread"])
            dict["binTotal"].append(row["binTotal"])
            break
#
dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv("./new_csv_Data/betsForOptimization.csv")
