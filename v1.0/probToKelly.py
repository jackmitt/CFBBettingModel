import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from evalPredictions import testClassification
from sklearn.preprocessing import StandardScaler

predictions = []
z = []
y = []
x = []
a = pd.read_csv('./csv_Data/LogisticPythonPredictionsLRWeek5+Leave-One-OutNoStepwiseScaledC0.25.csv', encoding = "ISO-8859-1")
for index, row in a.iterrows():
    if (float(row["PFITS"]) < 0.5):
        x.append(1 - float(row["PFITS"]))
        y.append(1 - int(row["binSpread"]))
    else:
        x.append(float(row["PFITS"]))
        y.append(int(row["binSpread"]))
model = LogisticRegression(max_iter = 100000, penalty = 'none')
x1 = np.array(x)
y1 = np.array(y)
model.fit(X = x1.reshape(-1,1), y = y1)
for p in model.predict_proba(x1.reshape(-1,1)):
    if (model.classes_[1] == 1):
        predictions.append(p[1])
        if (p[1] > 0.5122):
            z.append(p[1])
    else:
        predictions.append(p[0])
a["PFITS"] = predictions
a["binSpread"] = y
testClassification(a, 300, 'Kelly', Year = False, Week = False, odds = -105, betType = "Spread")
print (np.average(z))
a.to_csv('./csv_Data/LogisticPythonPredictionsLRWeek5+Leave-One-OutNoStepwiseScaledC0.25PTK.csv')
