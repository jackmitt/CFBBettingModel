import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from evalPredictions import testClassification
from sklearn.preprocessing import StandardScaler

we = [1]
for w in we:
    predictions = []
    vars = []
    a = pd.read_csv('./csv_Data/bigboyBinClassificationWeek5+.csv', encoding = "ISO-8859-1")
    #b = pd.read_csv('./csv_Data/bigboyBinClassificationTestWeek5+.csv', encoding = "ISO-8859-1")
    Y = a["binSpread"]
    #Leave-One-Out
    #X = a[["FavHF_aboveAvg", "Elo_diff_aboveAvg", "Sophomore_diff_aboveAvg", "Junior_diff_aboveAvg", "Sr_diff_aboveAvg", "PwrS_diff_aboveAvg", "StDownSr_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_passingPlays.successRate_diff_aboveAvg", "RedZone ppa_diff_aboveAvg", "Pts_diff_aboveAvg", "Junior_diff_Indicator", "Coach_diff_Indicator", "Sr_diff_Indicator", "Exp_diff_Indicator", "StDownExp_diff_Indicator", "PassDownExp_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "adj_standardDowns.explosiveness_diff_Indicator", "adj_passingDowns.explosiveness_diff_Indicator"]]
    for col in a.columns:
        if ("aboveAvg" in col):
            vars.append(col)
    scaler = StandardScaler()
    X = pd.DataFrame(a, columns = vars)
    X[vars] = scaler.fit_transform(X[vars])
    for index, row in a.iterrows():
        print (index)
        xTest = X.iloc[index].to_numpy()
        yTest = Y.iloc[index]
        xTrain = X.copy()
        yTrain = Y.copy()
        xTrain = xTrain.drop(index)
        yTrain = yTrain.drop(index)
        model = LogisticRegression(max_iter = 100000, C = 0.1)
        model.fit(X = xTrain, y = yTrain)
        predictions.append(model.predict_proba(xTest.reshape(1,-1))[0][1])
    a["PFITS"] = predictions
    a.to_csv('./csv_Data/LogisticPythonPredictionsLRWeek5+Leave-One-OutNoStepwiseScaledC0.1.csv')




    #my custom Cross Validated model
    #Y = a["binSpread"]
    #xCols = ['Sr_diff_aboveAvg', 'TOP_diff_Indicator', 'PassDownPpa_diff_aboveAvg', 'adj_successRate_diff_Indicator', 'PassPpa_diff_Indicator', 'adj_standardDowns.explosiveness_diff_aboveAvg', 'adj_passingDowns.ppa_diff_Indicator', 'adj_rushingPlays.successRate_diff_aboveAvg', 'adj_passingDowns.successRate_diff_Indicator', 'adj_ppa_diff_Indicator', 'adj_secondLevelYards_diff_aboveAvg', 'adj_openFieldYards_diff_Indicator', 'adj_passingDowns.explosiveness_diff_Indicator', 'adj_rushingPlays.explosiveness_diff_Indicator', 'Completion_diff_aboveAvg', 'StDownPpa_diff_Indicator', 'adj_standardDowns.explosiveness_diff_Indicator', 'Sophomore_diff_Indicator', 'adj_powerSuccess_diff_aboveAvg', 'RushExp_diff_Indicator', 'adj_standardDowns.ppa_diff_aboveAvg', 'Penalty_diff_aboveAvg', 'FavHF_aboveAvg', 'FavHF', 'Week', 'Ppa_diff_aboveAvg', 'adj_explosiveness_diff_Indicator', 'Senior_diff_aboveAvg', 'PassDownExp_diff_aboveAvg', 'Exp_diff_aboveAvg', 'StDownSr_diff_Indicator', 'Pts_diff_Indicator', 'Freshman_diff_aboveAvg', 'OpenField_diff_aboveAvg', 'Stuff_diff_aboveAvg', 'adj_passingPlays.successRate_diff_Indicator', 'Sophomore_diff_aboveAvg', 'RushPpa_diff_aboveAvg', 'Junior_diff_aboveAvg', 'StDownExp_diff_Indicator', 'adj_standardDowns.ppa_diff_Indicator', 'Sr_diff_Indicator', 'FavHF_Indicator', 'TOP_diff_aboveAvg', 'Exp_diff_Indicator', 'PwrS_diff_Indicator', 'adj_passingPlays.explosiveness_diff_aboveAvg', 'adj_successRate_diff_aboveAvg', 'RushExp_diff_aboveAvg', 'PassDownSr_diff_Indicator', 'PassSr_diff_aboveAvg', 'RushPpa_diff_Indicator', 'FG_diff_aboveAvg', 'Junior_diff_Indicator', 'adj_passingPlays.successRate_diff_aboveAvg', 'StDownPpa_diff_aboveAvg', 'Elo_diff_Indicator', 'adj_secondLevelYards_diff_Indicator', 'PassPpa_diff_aboveAvg', 'adj_explosiveness_diff_aboveAvg', 'adj_rushingPlays.successRate_diff_Indicator', 'FG_diff_Indicator', 'SecLevel_diff_aboveAvg', 'PassExp_diff_Indicator', 'adj_stuffRate_diff_aboveAvg', 'Elo_diff_aboveAvg', 'Penalty_diff_Indicator', 'Completion_diff_Indicator', 'StDownSr_diff_aboveAvg', 'PassDownExp_diff_Indicator', 'adj_rushingPlays.ppa_diff_aboveAvg', 'Coach_diff_Indicator', 'PassDownPpa_diff_Indicator', 'TO_diff_aboveAvg', 'PwrS_diff_aboveAvg', 'RushSr_diff_aboveAvg', 'adj_rushingPlays.ppa_diff_Indicator', 'Ppa_diff_Indicator', 'RedZone ppa_diff_Indicator', 'RedZone ppa_diff_aboveAvg', 'Stuff_diff_Indicator', 'PassSr_diff_Indicator', 'adj_passingDowns.ppa_diff_aboveAvg', 'StDownExp_diff_aboveAvg', 'Year', 'adj_standardDowns.successRate_diff_aboveAvg', 'Senior_diff_Indicator', 'adj_passingPlays.explosiveness_diff_Indicator', 'adj_passingPlays.ppa_diff_aboveAvg', 'TO_diff_Indicator', 'adj_openFieldYards_diff_aboveAvg', 'adj_passingDowns.explosiveness_diff_aboveAvg', 'Pts_diff_aboveAvg', 'OpenField_diff_Indicator', 'PassExp_diff_aboveAvg', 'SecLevel_diff_Indicator']
    #X = pd.DataFrame(a, columns=xCols)
    #temp = X.copy()
    #model = LogisticRegression(max_iter = 100000)
    #X_train, X_test, y_train, y_test = train_test_split(temp, Y, test_size=0.33, random_state=42)
    #b = pd.DataFrame()
    #model.fit(X = X_train, y = y_train)
    #for p in model.predict_proba(X_test):
    #    if (model.classes_[1] == 1):
    #        predictions.append(p[1])
    #    else:
    #        predictions.append(p[0])
    #b = pd.DataFrame()
    #b["binSpread"] = y_test
    #b["PFITS"] = predictions
    #print (testClassification(b, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread", print = False))







    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w5+) w/ new regression step in binClassificationTransform.py

    #Xtrain = a[["FavHF_aboveAvg", "Freshman_diff_aboveAvg", "Sophomore_diff_aboveAvg", "Junior_diff_aboveAvg", "PwrS_diff_aboveAvg", "adj_successRate_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "Penalty_diff_aboveAvg", "Pts_diff_aboveAvg", "Sophomore_diff_Indicator", "Junior_diff_Indicator", "Coach_diff_Indicator", "Exp_diff_Indicator", "PassDownExp_diff_Indicator", "adj_successRate_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "Completion_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w1) w/ new regression step in binClassificationTransform.py - GARBAGE

    #Xtrain = a[["FavHF_aboveAvg", "Freshman_diff_aboveAvg", "Sophomore_diff_aboveAvg", "Junior_diff_aboveAvg", "Senior_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.20 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w234) w/ new regression step in binClassificationTransform.py - GARBAGE

    #Xtrain = a[["FavHF_aboveAvg", "Stuff_diff_aboveAvg", "SecLevel_diff_aboveAvg", "StDownPpa_diff_aboveAvg", "PassDownSr_diff_aboveAvg", "RushPpa_diff_aboveAvg", "adj_standardDowns.ppa_diff_aboveAvg", "adj_passingDowns.successRate_diff_aboveAvg", "Pts_diff_aboveAvg", "FavHF_Indicator", "Junior_diff_Indicator", "Exp_diff_Indicator", "SecLevel_diff_Indicator", "StDownPpa_diff_Indicator", "StDownSr_diff_Indicator", "PassDownPpa_diff_Indicator", "adj_ppa_diff_Indicator", "adj_secondLevelYards_diff_Indicator", "adj_passingDowns.ppa_diff_Indicator", "adj_passingDowns.explosiveness_diff_Indicator", "Penalty_diff_Indicator", "Completion_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w2+) w/ new regression step in binClassificationTransform.py - GARBAGE

    #Xtrain = a[["FavHF_aboveAvg", "Elo_diff_aboveAvg", "FG_diff_aboveAvg", "StDownSr_diff_aboveAvg", "adj_passingDowns.ppa_diff_aboveAvg", "adj_passingDowns.successRate_diff_aboveAvg", "adj_passingDowns.explosiveness_diff_aboveAvg", "Pts_diff_aboveAvg", "FavHF_Indicator", "Senior_diff_Indicator", "Coach_diff_Indicator", "Ppa_diff_Indicator", "PassDownPpa_diff_Indicator", "PassDownSr_diff_Indicator", "RushExp_diff_Indicator", "adj_ppa_diff_Indicator", "adj_passingDowns.explosiveness_diff_Indicator", "adj_passingPlays.successRate_diff_Indicator", "adj_passingPlays.explosiveness_diff_Indicator", "RedZone ppa_diff_Indicator", "TO_diff_Indicator", "Completion_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w4+) w/ new regression step in binClassificationTransform.py

    #Xtrain = a[["FavHF_aboveAvg", "Elo_diff_aboveAvg", "Sophomore_diff_aboveAvg", "FG_diff_aboveAvg", "PwrS_diff_aboveAvg", "StDownExp_diff_aboveAvg", "PassSr_diff_aboveAvg", "adj_successRate_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_passingDowns.successRate_diff_aboveAvg", "adj_passingDowns.explosiveness_diff_aboveAvg", "adj_rushingPlays.successRate_diff_aboveAvg", "adj_passingPlays.successRate_diff_aboveAvg", "adj_passingPlays.explosiveness_diff_aboveAvg", "Pts_diff_aboveAvg", "Completion_diff_aboveAvg", "Sophomore_diff_Indicator", "Exp_diff_Indicator", "OpenField_diff_Indicator", "adj_ppa_diff_Indicator", "adj_successRate_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "adj_standardDowns.explosiveness_diff_Indicator", "adj_passingDowns.explosiveness_diff_Indicator", "TO_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w3+) w/ new regression step in binClassificationTransform.py

    #Xtrain = a[["Senior_diff_aboveAvg", "PwrS_diff_aboveAvg", "adj_successRate_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_passingDowns.ppa_diff_aboveAvg", "adj_passingDowns.successRate_diff_aboveAvg", "adj_passingDowns.explosiveness_diff_aboveAvg", "adj_passingPlays.successRate_diff_aboveAvg", "TO_diff_aboveAvg", "Coach_diff_Indicator", "FG_diff_Indicator", "StDownPpa_diff_Indicator", "PassDownSr_diff_Indicator", "adj_passingDowns.explosiveness_diff_Indicator", "adj_passingPlays.explosiveness_diff_Indicator", "RedZone ppa_diff_Indicator", "TO_diff_Indicator"]]

    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w5+) w/ new regression step in binClassificationTransform.py Set 0

    #Xtrain = a[["FavHF_aboveAvg", "Elo_diff_aboveAvg", "Freshman_diff_aboveAvg", "Sophomore_diff_aboveAvg", "PwrS_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_passingDowns.ppa_diff_aboveAvg", "adj_passingDowns.successRate_diff_aboveAvg", "adj_passingDowns.explosiveness_diff_aboveAvg", "RedZone ppa_diff_aboveAvg", "Pts_diff_aboveAvg", "Junior_diff_Indicator", "Exp_diff_Indicator", "StDownExp_diff_Indicator", "PassDownPpa_diff_Indicator", "PassDownExp_diff_Indicator", "PassExp_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "adj_standardDowns.explosiveness_diff_Indicator", "Pts_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w5+) w/ new regression step in binClassificationTransform.py Set 1

    #Xtrain = a[["FavHF_aboveAvg", "Elo_diff_aboveAvg", "Junior_diff_aboveAvg", "Sr_diff_aboveAvg", "adj_stuffRate_diff_aboveAvg", "adj_standardDowns.successRate_diff_aboveAvg", "adj_passingDowns.ppa_diff_aboveAvg", "Penalty_diff_aboveAvg", "RedZone ppa_diff_aboveAvg", "Pts_diff_aboveAvg", "Junior_diff_Indicator", "Sr_diff_Indicator", "Exp_diff_Indicator", "StDownExp_diff_Indicator", "PassDownExp_diff_Indicator", "adj_explosiveness_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "adj_standardDowns.explosiveness_diff_Indicator", "adj_passingDowns.explosiveness_diff_Indicator", "adj_rushingPlays.successRate_diff_Indicator", "Penalty_diff_Indicator", "TO_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w5+) w/ new regression step in binClassificationTransform.py Set 2

    #Xtrain = a[["FavHF_aboveAvg", "Elo_diff_aboveAvg", "Junior_diff_aboveAvg", "Senior_diff_aboveAvg", "Sr_diff_aboveAvg", "OpenField_diff_aboveAvg", "StDownPpa_diff_aboveAvg", "StDownSr_diff_aboveAvg", "adj_ppa_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_passingDowns.explosiveness_diff_aboveAvg", "adj_passingPlays.successRate", "RedZone ppa_diff_aboveAvg", "Pts_diff_aboveAvg", "Junior_diff_Indicator", "Sr_diff_Indicator", "Exp_diff_Indicator", "PassDownExp_diff_Indicator", "adj_secondLevelYards_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w5+) w/ new regression step in binClassificationTransform.py Set 3

    #Xtrain = a[["FavHF_aboveAvg", "Sophomore_diff_aboveAvg", "Senior_diff_aboveAvg", "PwrS_diff_aboveAvg", "PassSr_diff_aboveAvg", "adj_successRate_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_standardDowns.successRate_diff_aboveAvg", "adj_standardDowns.explosiveness_diff_aboveAvg", "adj_passingDowns.ppa_diff_aboveAvg", "adj_passingDowns.explosiveness_diff_aboveAvg", "adj_rushingPlays.successRate_diff_aboveAvg", "adj_passingPlays.successRate_diff_aboveAvg", "RedZone ppa_diff_aboveAvg", "Pts_diff_aboveAvg", "Junior_diff_Indicator", "Coach_diff_Indicator", "Sr_diff_Indicator", "Exp_diff_Indicator", "StDownExp_diff_Indicator", "PassDownExp_diff_Indicator", "adj_standardDowns.explosiveness_diff_Indicator", "adj_passingPlays.ppa_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w5+) w/ new regression step in binClassificationTransform.py Set 4

    #Xtrain = a[["FavHF_aboveAvg", "Sophomore_diff_aboveAvg", "Junior_diff_aboveAvg", "Sr_diff_aboveAvg", "PwrS_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_passingDowns.successRate_diff_aboveAvg", "Penalty_diff_aboveAvg", "RedZone ppa_diff_aboveAvg", "Pts_diff_aboveAvg", "Sophomore_diff_Indicator", "Junior_diff_Indicator", "Coach_diff_Indicator", "Sr_diff_Indicator", "Exp_diff_Indicator", "OpenField_diff_Indicator", "PassDownExp_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "Completion_diff_Indicator"]]


    #Stepwise w/ Indicators alpha = 0.25 from Minitab TRAIN TEST SPLIT BEFORE STEPWISE (w5+) w/ new regression step in binClassificationTransform.py Set 5

    #Xtrain = a[["FavHF_aboveAvg", "Elo_diff_aboveAvg", "Freshman_diff_aboveAvg", "Sophomore_diff_aboveAvg", "Senior_diff_aboveAvg", "PwrS_diff_aboveAvg", "PassDownSr_diff_aboveAvg", "adj_explosiveness_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_standardDowns.explosiveness_diff_aboveAvg", "adj_passingDowns.explosiveness_diff_aboveAvg", "Pts_diff_aboveAvg", "Junior_diff_Indicator", "Coach_diff_Indicator", "Exp_diff_Indicator", "StDownExp_diff_Indicator", "PassDownExp_diff_Indicator", "PassExp_diff_Indicator", "adj_successRate_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "adj_standardDowns.explosiveness_diff_Indicator", "adj_rushingPlays.successRate_diff_Indicator", "adj_rushingPlays.explosiveness_diff_Indicator", "Completion_diff_Indicator"]]


    #Ytest = b["binSpread"]
    #Xtest = b[["FavHF_aboveAvg", "Freshman_diff_aboveAvg", "Sophomore_diff_aboveAvg", "Junior_diff_aboveAvg", "PwrS_diff_aboveAvg", "adj_successRate_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "Penalty_diff_aboveAvg", "Pts_diff_aboveAvg", "Sophomore_diff_Indicator", "Junior_diff_Indicator", "Coach_diff_Indicator", "Exp_diff_Indicator", "PassDownExp_diff_Indicator", "adj_successRate_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "Completion_diff_Indicator"]]
    #model = LogisticRegression(max_iter = 100000)
    #model.fit(X = Xtrain, y = Ytrain)
    #print (model.classes_)
    #predictions = model.predict_proba(Xtest)
    #z = []
    #for pre in predictions:
    #    z.append(pre[1])
    #b["PFITS"] = z
    #b.to_csv("./csv_Data/LogisticPythonPredictionsLRTestSplitWeek5+FROMMYSTEPWISE.csv")
