import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression

train = pd.read_csv('./csv_Data/trainAlt.csv', encoding = "ISO-8859-1")
test = pd.read_csv('./csv_Data/testAlt.csv', encoding = "ISO-8859-1")
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

colNames = list(train.columns)
X_train = train.iloc[:,cols]
X_test = test.iloc[:,cols]
y_train = train.iloc[:,168]
y_test = test.iloc[:,168]
ols = LinearRegression()
selector = RFE(ols, 20, step=1, verbose = 1)
selector = selector.fit(X_train, y_train)
ranks = selector.support_
count = 0
for bool in ranks:
    if (bool):
        print (colNames[count])
    count += 1
