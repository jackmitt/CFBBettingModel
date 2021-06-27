import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

we = [2,3,4,5,6,7]
for w in we:
    predictions = []
    a = pd.read_csv('./csv_Data/bigboyBinClassificationTotalsWeek' + str(w) + '+.csv', encoding = "ISO-8859-1")
    Y = a["binTotal"]
    #Stepwise no indicators with alpha = 0.25 from Minitab
    X = a[["FG_total_aboveAvg","Stuff_total_aboveAvg","OpenField_total_aboveAvg","StDownSr_total_aboveAvg","RushExp_total_aboveAvg","PassExp_total_aboveAvg","adj_openFieldYards_total_aboveAvg","adj_standardDowns.ppa_total_aboveAvg","adj_rushingPlays.explosiveness_total_aboveAvg","Penalty_total_aboveAvg","Pts_total_aboveAvg","FG_total_Indicator","PwrS_total_Indicator","SecLevel_total_Indicator","PassDownSr_total_Indicator","RushSr_total_Indicator","adj_stuffRate_total_Indicator","adj_standardDowns.explosiveness_total_Indicator","adj_passingDowns.ppa_total_Indicator","adj_rushingPlays.ppa_total_Indicator","adj_rushingPlays.successRate_total_Indicator","adj_rushingPlays.explosiveness_total_Indicator","adj_passingPlays.successRate_total_Indicator"]]
    for index, row in a.iterrows():
        print (index)
        xTest = X.iloc[index].to_numpy()
        yTest = Y.iloc[index]
        xTrain = X.copy()
        yTrain = Y.copy()
        xTrain = xTrain.drop(index)
        yTrain = yTrain.drop(index)
        model = LogisticRegression(max_iter = 100000)
        model.fit(X = xTrain, y = yTrain)
        predictions.append(model.predict_proba(xTest.reshape(1,-1))[0][1])
    a["PFITS"] = predictions
    a.to_csv('./csv_Data/LogisticPythonPredictionsLRTotalWeek' + str(w) + '+0.25.csv')
