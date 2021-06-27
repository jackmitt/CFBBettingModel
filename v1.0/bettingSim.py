import pandas as pd
import numpy as np

a = pd.read_csv('./csv_Data/betsForOptimization.csv', encoding = "ISO-8859-1")
bankroll = 30000
betResults = []
for index, row in a.iterrows():
    print (index)
    if (index == 0 or a.at[index - 1, "Week"] != row["Week"] or index == len(a.index) - 1):
        betSize = []
        for b in betResults:
            betSize.append((1/len(betResults)) * preBR)
            if (b == 0):
                bankroll -= (1/len(betResults)) * preBR
            else:
                bankroll += (1/len(betResults)) * preBR * 0.95238
        betResults = []
        preBR = bankroll
        print (bankroll)
    betResults.append(int(row["binSpread"]))
    betResults.append(int(row["binTotal"]))


bankroll = 30000
betResults = []
kellySizes = []
for index, row in a.iterrows():
    print (index)
    if (index == 0 or a.at[index - 1, "Week"] != row["Week"] or index == len(a.index) - 1):
        betSize = []
        totalKellySizes = 0
        for x in kellySizes:
            if (x > 0):
                totalKellySizes += x
        for i in range(len(betResults)):
            if (kellySizes[i] > 0):
                if (betResults[i] == 0):
                    if (totalKellySizes > 1):
                        bankroll -= (kellySizes[i]*(1/totalKellySizes)) * preBR
                        betSize.append((kellySizes[i]*(1/totalKellySizes)))
                    else:
                        bankroll -= (kellySizes[i]) * preBR
                        betSize.append((kellySizes[i]))
                else:
                    if (totalKellySizes > 1):
                        bankroll += (kellySizes[i]*(1/totalKellySizes)) * preBR * 0.95238
                        betSize.append((kellySizes[i]*(1/totalKellySizes)))
                    else:
                        bankroll += (kellySizes[i]) * preBR * 0.95238
                        betSize.append((kellySizes[i]))
        print (bankroll, np.sum(betSize), totalKellySizes)
        betResults = []
        kellySizes = []
        preBR = bankroll
    betResults.append(int(row["binSpread"]))
    kellySizes.append((float(row["PFITSSpread"]) - 0.5122)/0.4878)
    betResults.append(int(row["binTotal"]))
    kellySizes.append((float(row["PFITSTotal"]) - 0.5122)/0.4878)
