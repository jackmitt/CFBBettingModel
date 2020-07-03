import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from evalPredictions import testClassification
import random

predictions = []
a = pd.read_csv('./csv_Data/bigboyBinClassificationTotals.csv', encoding = "ISO-8859-1")
Y = a["binTotal"]
xCols = []
for col in a.columns:
    if (col == "FavHF" or '_aboveAvg' in col or '_Indicator' in col):
        xCols.append(col)
X = pd.DataFrame(a, columns=xCols)
best = 0
bestCols = []
temp = X.copy()
model = LogisticRegression(max_iter = 100000)
X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
model.fit(X = X_train, y = y_train)
for p in model.predict_proba(X_test):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
    else:
        predictions.append(p[0])
b = pd.DataFrame()
b["binTotal"] = y_test
b["PFITS"] = predictions
predictions = []
netWin = testClassification(b, 300, 'Standard', betType = "O/U")
best = netWin
bestCols = []
removedCols = []
noImprovement = True
colCount = 0
removedCount = 0
bestImproved = 0
for col in temp.columns:
    bestCols.append(col)
    colCount += 1
random.shuffle(bestCols)
X = temp.copy()
print ("Starting Removal of Features")
while (bestImproved < colCount):
    print (bestImproved, colCount)
    temp = X.copy()
    temp = temp.drop(columns = [bestCols[bestImproved]])
    model = LogisticRegression(max_iter = 100000)
    X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
    model.fit(X = X_train, y = y_train)
    for p in model.predict_proba(X_test):
        if (model.classes_[1] == 1):
            predictions.append(p[1])
        else:
            predictions.append(p[0])
    b = pd.DataFrame()
    b["binTotal"] = y_test
    b["PFITS"] = predictions
    predictions = []
    netWin = testClassification(b, 300, 'Standard', betType = "O/U")
    if (netWin > best):
        best = netWin
        removedCols.append(bestCols[bestImproved])
        removedCount += 1
        bestCols = []
        for col in temp.columns:
            bestCols.append(col)
        random.shuffle(bestCols)
        X = temp.copy()
        bestImproved = 0
        colCount -= 1
        print ("IMPROVEMENT SAVED")
    else:
        bestImproved += 1
        print ("no improvement")
    if (bestImproved == colCount):
        bestImproved = 0
        print ("Starting Addition of Features")
        while (bestImproved < removedCount):
            print (bestImproved, removedCount)
            temp = X.copy()
            temp[removedCols[bestImproved]] = a[removedCols[bestImproved]]
            model = LogisticRegression(max_iter = 100000)
            X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
            model.fit(X = X_train, y = y_train)
            for p in model.predict_proba(X_test):
                if (model.classes_[1] == 1):
                    predictions.append(p[1])
                else:
                    predictions.append(p[0])
            b = pd.DataFrame()
            b["binTotal"] = y_test
            b["PFITS"] = predictions
            predictions = []
            netWin = testClassification(b, 300, 'Standard', betType = "O/U")
            if (netWin > best):
                best = netWin
                removedCols.remove(removedCols[bestImproved])
                removedCount -= 1
                bestCols.append(removedCols[bestImproved])
                random.shuffle(removedCols)
                X = temp.copy()
                bestImproved = 0
                noImprovement = False
                colCount += 1
                print ("IMPROVEMENT SAVED")
            else:
                bestImproved += 1
                print ("no improvement")
        if (not noImprovement):
            bestImproved = 0
            noImprovement = True
        else:
            bestImproved = 1000
print ('-----------------------------------------')
print (bestCols)
print ("Removed:", removedCols)
print (best)
