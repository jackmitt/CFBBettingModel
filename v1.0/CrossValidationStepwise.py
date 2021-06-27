import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from evalPredictions import testClassification
from sklearn.utils import shuffle
import random

predictions = []
seeds = [4,16,33,67,95,74,44,59,1,83]
a = pd.read_csv('./csv_Data/bigboyBinClassificationWeek5+.csv', encoding = "ISO-8859-1")
Y = a["binSpread"]
xCols = []
for col in a.columns:
    if (col == "FavHF" or '_aboveAvg' in col or '_Indicator' in col):
        xCols.append(col)
X = pd.DataFrame(a, columns=["Elo_diff_aboveAvg"])
best = 0
bestCols = []
temp = X.copy()
model = LogisticRegression(max_iter = 100000)
cvSum = 0
allSums = []
#Cross Validation
for k in range(30):
    X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
    seed = random.randint(1,1000)
    X_train = shuffle(X_train, random_state = seed)
    y_train = shuffle(y_train, random_state = seed)
    for i in range(3):
        print ("Shuffle " + str(k+1) + "/30 -- " + "Cross Validation " + str(i+1) + "/3")
        valRows = []
        trainRows = []
        for j in range(len(X_train.index)):
            if (j < (i+1)*len(X_train.index)/3 and j >= i*len(X_train.index)/3):
                valRows.append(j)
            else:
                trainRows.append(j)
        tempTrainX = X_train.iloc[trainRows]
        tempTrainY = y_train.iloc[trainRows]
        tempValX = X_train.iloc[valRows]
        tempValY = y_train.iloc[valRows]
        b = pd.DataFrame()
        b["binSpread"] = tempValY
        model.fit(X = tempTrainX, y = tempTrainY)
        for p in model.predict_proba(tempValX):
            if (model.classes_[1] == 1):
                predictions.append(p[1])
            else:
                predictions.append(p[0])
        b["PFITS"] = predictions
        predictions = []
        cvSum += testClassification(b, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread", print = False)
    allSums.append(cvSum)
    cvSum = 0
print ("Initial cvSum =", np.average(allSums))
best = np.average(allSums)
bestCols = []
removedCols = []
noImprovement = True
colCount = 1
removedCount = 0
bestImproved = 0
for col in xCols:
    if ("Elo" not in col):
        removedCols.append(col)
        removedCount += 1
bestCols.append("Elo_diff_aboveAvg")
random.shuffle(removedCols)
X = temp.copy()
print ("Starting Addition of Features")
while (bestImproved < removedCount):
    print (bestImproved, removedCount, "Total Features included:", colCount)
    temp = X.copy()
    temp[removedCols[bestImproved]] = a[removedCols[bestImproved]]
    model = LogisticRegression(max_iter = 100000)
    cvSum = 0
    allSums = []
    #Cross Validation
    for k in range(30):
        X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
        seed = random.randint(1,1000)
        X_train = shuffle(X_train, random_state = seed)
        y_train = shuffle(y_train, random_state = seed)
        for i in range(3):
            print ("Shuffle " + str(k+1) + "/30 -- " + "Cross Validation " + str(i+1) + "/3")
            valRows = []
            trainRows = []
            for j in range(len(X_train.index)):
                if (j < (i+1)*len(X_train.index)/3 and j >= i*len(X_train.index)/3):
                    valRows.append(j)
                else:
                    trainRows.append(j)
            tempTrainX = X_train.iloc[trainRows]
            tempTrainY = y_train.iloc[trainRows]
            tempValX = X_train.iloc[valRows]
            tempValY = y_train.iloc[valRows]
            b = pd.DataFrame()
            b["binSpread"] = tempValY
            model.fit(X = tempTrainX, y = tempTrainY)
            for p in model.predict_proba(tempValX):
                if (model.classes_[1] == 1):
                    predictions.append(p[1])
                else:
                    predictions.append(p[0])
            b["PFITS"] = predictions
            predictions = []
            cvSum += testClassification(b, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread", print = False)
        allSums.append(cvSum)
        cvSum = 0
    print ("Current cvSum =", np.average(allSums))
    if (np.average(allSums) > best):
        best = cvSum
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
    if (bestImproved == removedCount):
        bestImproved = 0
        print ("Starting Removal of Features")
        while (bestImproved < colCount):
            print (bestImproved, colCount)
            temp = X.copy()
            temp = temp.drop(columns = [bestCols[bestImproved]])
            model = LogisticRegression(max_iter = 100000)
            cvSum = 0
            allSums = []
            #Cross Validation
            for k in range(30):
                X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
                seed = random.randint(1,1000)
                X_train = shuffle(X_train, random_state = seed)
                y_train = shuffle(y_train, random_state = seed)
                for i in range(3):
                    print ("Shuffle " + str(k+1) + "/30 -- " + "Cross Validation " + str(i+1) + "/3")
                    valRows = []
                    trainRows = []
                    for j in range(len(X_train.index)):
                        if (j < (i+1)*len(X_train.index)/3 and j >= i*len(X_train.index)/3):
                            valRows.append(j)
                        else:
                            trainRows.append(j)
                    tempTrainX = X_train.iloc[trainRows]
                    tempTrainY = y_train.iloc[trainRows]
                    tempValX = X_train.iloc[valRows]
                    tempValY = y_train.iloc[valRows]
                    b = pd.DataFrame()
                    b["binSpread"] = tempValY
                    model.fit(X = tempTrainX, y = tempTrainY)
                    for p in model.predict_proba(tempValX):
                        if (model.classes_[1] == 1):
                            predictions.append(p[1])
                        else:
                            predictions.append(p[0])
                    b["PFITS"] = predictions
                    predictions = []
                    cvSum += testClassification(b, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread", print = False)
                allSums.append(cvSum)
                cvSum = 0
            print ("Current cvSum =", np.average(allSums))
            if (np.average(allSums) > best):
                best = np.average(allSums)
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
        if (not noImprovement):
            bestImproved = 0
            noImprovement = True
        else:
            bestImproved = 1000
print ('-----------------------------------------')
print ("After Cross Validation Stepwise Feature Selection, the Best Features Were Decided to be:")
print (bestCols)
print ("Removed Columns:", removedCols)
print ("Applying Best Model to Test Set:")
X = pd.DataFrame(a, columns=xCols)
temp = X.copy()
model = LogisticRegression(max_iter = 100000)
X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
finalX_train = pd.DataFrame(X_train, columns = bestCols)
finalX_test = pd.DataFrame(X_test, columns = bestCols)
b = pd.DataFrame()
b["binSpread"] = y_test
model.fit(X = finalX_train, y = y_train)
for p in model.predict_proba(finalX_test):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
    else:
        predictions.append(p[0])
b = pd.DataFrame()
b["binSpread"] = y_test
b["PFITS"] = predictions
print ("TEST RESULT:")
print (testClassification(b, 300, 'Kelly', Year = True, Week = True, odds = -105, betType = "Spread", print = False))
