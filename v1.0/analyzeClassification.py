import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from evalPredictions import testClassification

#Spread Part
a = pd.read_csv('./csv_Data/LogisticPythonPredictionsLRWeek5+Leave-One-OutNoStepwiseScaled.csv', encoding = "ISO-8859-1")
testClassification(a, 300, 'Kelly', Year = True, Week = True, odds = -105, betType = "Spread")

a = pd.read_csv('./csv_Data/LogisticPythonPredictionsLRWeek5+Leave-One-OutNoStepwiseScaledC0.25.csv', encoding = "ISO-8859-1")
testClassification(a, 300, 'Kelly', Year = True, Week = True, odds = -105, betType = "Spread")

a = pd.read_csv('./csv_Data/LogisticPythonPredictionsLRWeek5+Leave-One-OutNoStepwiseScaledC0.1.csv', encoding = "ISO-8859-1")
testClassification(a, 300, 'Kelly', Year = True, Week = True, odds = -105, betType = "Spread")

#a = pd.read_csv("./csv_Data/LogisticPythonPredictionsLRTestSplitWeek4+TRAINEDWEEK5+.csv", encoding = "ISO-8859-1")
#testClassification(a, 300, 'Kelly', Year = True, Week = True, odds = -105, betType = "Spread")
#print ("--------------------------------------------------------------")
#print ("--------------------------------------------------------------")

#O/U Part
#a = pd.read_csv('./csv_Data/LogisticPythonPredictionsLRTotal0.25.csv', encoding = "ISO-8859-1")
#testClassification(a, 100, 'Kelly', Year = True, Week = True, odds = -105, betType = "O/U")

#we = [2,3,4,5,6,7]
#for w in we:
#    a = pd.read_csv('./csv_Data/LogisticPythonPredictionsLRTotalWeek' + str(w) + '+0.25.csv', encoding = "ISO-8859-1")
#    testClassification(a, 300, 'Kelly', Year = True, Week = True, odds = -105, betType = "O/U")
#    print ("----------------------------------------------------------")

#print ("SPREAD BETTING BELOW\n\n")

#we = [0,1,2,3,4,5]
#for w in we:
#    a = pd.read_csv("./csv_Data/LogisticPythonPredictionsRFCTestSplitWeek5+" + str(w) + ".csv", encoding = "ISO-8859-1")
#    testClassification(a, 300, 'Kelly', Year = True, Week = True, odds = -105, betType = "Spread")
#    print ("----------------------------------------------------------")
