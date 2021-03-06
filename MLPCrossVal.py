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
allScores = []
a = pd.read_csv('./csv_Data/bigboyBinClassificationWeek5+.csv', encoding = "ISO-8859-1")
Y = a["binSpread"]
xCols = []
for col in a.columns:
    if ("aboveAvg" in col):
        xCols.append(col)
scaler = StandardScaler()
X = pd.DataFrame(a, columns = xCols)
X[xCols] = scaler.fit_transform(X[xCols])
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
rkf = RepeatedKFold(n_splits=10, n_repeats=1, random_state = 432)
best = -9999999999
bestC = -1
counter = 1
C_options = [3, 2.5, 2, 1.75, 1.5, 1.25, 1, 0.9, 0.825, 0.75, 0.625, 0.5, 0.375, 0.25, 0.175, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001]
for c in C_options:
    for train_index, test_index in rkf.split(X_train):
        print (str(counter) + "/10 for", c)
        x_cvTrain, x_cvTest = X_train.iloc[train_index], X_train.iloc[test_index]
        y_cvTrain, y_cvTest = y_train.iloc[train_index], y_train.iloc[test_index]
        model = MLPClassifier(alpha = c, max_iter = 100000)
        b = pd.DataFrame()
        b["binSpread"] = y_cvTest
        model.fit(X = x_cvTrain, y = y_cvTrain)
        for p in model.predict_proba(x_cvTest):
            if (model.classes_[1] == 1):
                predictions.append(p[1])
            else:
                predictions.append(p[0])
        b["PFITS"] = predictions
        predictions = []
        allSums.append(testClassification(b, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread", printOption = False))
        allScores.append(model.score(x_cvTest, y_cvTest))
        counter += 1
    print (c, np.average(allScores), np.average(allSums))
    if (np.average(allScores) > best):
        bestC = c
        best = np.average(allScores)
    allScores = []
    allSums = []
    counter = 0
print ("The best C was", bestC)
model = MLPClassifier(max_iter = 100000, alpha = bestC)
b = pd.DataFrame()
b["binSpread"] = y_test
model.fit(X = X_train, y = y_train)
for p in model.predict_proba(X_test):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
    else:
        predictions.append(p[0])
b["PFITS"] = predictions
allSums.append(testClassification(b, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread"))
print (model.score(X_test, y_test))
