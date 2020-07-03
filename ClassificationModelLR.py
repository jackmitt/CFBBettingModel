import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

we = [0,1,2,3,4,5]
for w in we:
    print (w)
    predictions = []
    a = pd.read_csv('./csv_Data/bigboyBinClassificationTrainWeek5+' + str(w) + '.csv', encoding = "ISO-8859-1")
    b = pd.read_csv('./csv_Data/bigboyBinClassificationTestWeek5+' + str(w) + '.csv', encoding = "ISO-8859-1")
    Ytrain = a["binSpread"]
    vars = ["FavHF_aboveAvg", "Elo_diff_aboveAvg", "Sophomore_diff_aboveAvg", "Junior_diff_aboveAvg", "Sr_diff_aboveAvg", "PwrS_diff_aboveAvg", "StDownSr_diff_aboveAvg", "adj_powerSuccess_diff_aboveAvg", "adj_passingPlays.successRate_diff_aboveAvg", "RedZone ppa_diff_aboveAvg", "Pts_diff_aboveAvg", "Junior_diff_Indicator", "Coach_diff_Indicator", "Sr_diff_Indicator", "Exp_diff_Indicator", "StDownExp_diff_Indicator", "PassDownExp_diff_Indicator", "adj_standardDowns.ppa_diff_Indicator", "adj_standardDowns.explosiveness_diff_Indicator", "adj_passingDowns.explosiveness_diff_Indicator"]
    Xtrain = a[vars]
    Ytest = b["binSpread"]
    Xtest = b[vars]
    model = LogisticRegression(max_iter = 100000)
    model.fit(X = Xtrain, y = Ytrain)
    print (model.classes_)
    predictions = model.predict_proba(Xtest)
    z = []
    for pre in predictions:
        z.append(pre[1])
    b["PFITS"] = z
    b.to_csv("./csv_Data/LogisticPythonPredictionsLRTestSplitWeek5+" + str(w) + ".csv")
