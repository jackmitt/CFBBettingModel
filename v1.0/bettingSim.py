import pandas as pd
import numpy as np
#####################################This is flawed but im not fixing it at the moment
a = pd.read_csv('./new_csv_Data/betsForOptimization.csv', encoding = "ISO-8859-1")

bankroll = 20000
betResults = []
spreadAmt = []
ouAmt = []
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
            if (i % 2 == 0):
                if (kellySizes[i] > 0):
                    spreadAmt.append(kellySizes[i]*(1/totalKellySizes) * preBR)
                else:
                    spreadAmt.append(np.nan)
            else:
                if (kellySizes[i] > 0):
                    ouAmt.append(kellySizes[i]*(1/totalKellySizes) * preBR)
                else:
                    ouAmt.append(np.nan)
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
                        bankroll += (kellySizes[i]*(1/totalKellySizes)) * preBR * 0.95
                        betSize.append((kellySizes[i]*(1/totalKellySizes)))
                    else:
                        bankroll += (kellySizes[i]) * preBR * 0.95
                        betSize.append((kellySizes[i]))
        print (bankroll, np.sum(betSize), totalKellySizes)
        betResults = []
        kellySizes = []
        preBR = bankroll
    betResults.append(int(row["binSpread"]))
    kellySizes.append((float(row["PFITSSpread"]) - (1 - float(row["PFITSSpread"]))/(0.95)))
    betResults.append(int(row["binTotal"]))
    kellySizes.append((float(row["PFITSTotal"]) - (1 - float(row["PFITSTotal"]))/0.95))

spreadAmt.append(np.nan)
ouAmt.append(np.nan)
a["Spread Amt"] = spreadAmt
a["O/U Amt"] = ouAmt
a.to_csv('./new_csv_Data/betsForOptimization.csv', index = False)
