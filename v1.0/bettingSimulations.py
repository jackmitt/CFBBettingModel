import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from evalPredictions import testClassification
from SimultaneousKelly import gradient_ascent

a = pd.read_csv('./csv_Data/LogisticPythonPredictionsLRWeek5+Leave-One-OutNoStepwiseScaledC0.25PTK.csv', encoding = "ISO-8859-1")
pa = list(a["PFITS"].to_numpy())
binSpread = list(a["binSpread"].to_numpy())
pb = []
for i in range(len(pa)):
    pb.append(0.5122)
initWagers = []
for i in range(len(pa)):
    if (pa[i] > 0.5):
        initWagers.append(pa[i] - ((1-pa[i])/((1/pb[i]) - 1)))
    else:
        initWagers.append(1-pa[i] - ((pa[i])/((1/pb[i]) - 1)))
bankroll = 30000
minBR = 99999999999
maxBR = -9999999999999999
for i in range(60):
    paSlice = pa[i*50:(i+1)*50]
    pbSlice = pb[i*50:(i+1)*50]
    wagerSlice = initWagers[i*50:(i+1)*50]
    binSpreadSlice = binSpread[i*50:(i+1)*50]
    removal = []
    for j in range(len(wagerSlice)):
        if (wagerSlice[j] <= 0):
            removal.append(j)
    for j in reversed(range(len(pbSlice))):
        if (j in removal):
            pbSlice.pop(j)
            wagerSlice.pop(j)
            binSpreadSlice.pop(j)
            paSlice.pop(j)
    optimalWagers = gradient_ascent(paSlice, pbSlice, wagerSlice, max_iter = 200)
    for j in range(len(optimalWagers)):
        if (binSpreadSlice[j] == 1):
            if (paSlice[j] > 0.5):
                bankroll += bankroll * optimalWagers[j] * ((1/pbSlice[j]) - 1)
            else:
                bankroll -= bankroll * optimalWagers[j]
        else:
            if (paSlice[j] < 0.5):
                bankroll += bankroll * optimalWagers[j] * ((1/pbSlice[j]) - 1)
            else:
                bankroll -= bankroll * optimalWagers[j]
        if (bankroll < minBR):
            minBR = bankroll
        if (bankroll > maxBR):
            maxBR = bankroll
print ("Final Bankroll:", bankroll)
print ("Max Bankroll:", maxBR)
print ("Min Bankroll:", minBR)
print ("ROI:", (bankroll - 30000)/30000)
