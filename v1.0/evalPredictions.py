import pandas as pd
import numpy as np
import math

#bigboy = pd.read_csv('./csv_Data/bigboy_OLSpredict.csv', encoding = "ISO-8859-1")
#OU = []
#Spread = []
#Combined = []
#OUBuffer = 10
#SpreadBuffer = 0

def testFit(bigboy, OUBuffer, SpreadBuffer, unitSize):
    OU = []
    Spread = []
    Combined = []
    NetWin = 0
    for index, row in bigboy.iterrows():
        if (index == len(bigboy.index) - 2):
            break
        try:
            if (row["Opponent"] == bigboy.at[index+1,"Team"]):
                total = float(row["PFITS"]) + float(bigboy.at[index+1,"PFITS"])
                try:
                    if (total + OUBuffer < float(row["O/U"])):
                        if (row["O/U Outcome"] == "Under"):
                            OU.append(1)
                            Combined.append(1)
                            NetWin += unitSize
                        elif (row["O/U Outcome"] == "Over"):
                            OU.append(0)
                            Combined.append(0)
                            NetWin -= unitSize*1.05
                    elif (total - OUBuffer > float(row["O/U"])):
                        if (row["O/U Outcome"] == "Over"):
                            OU.append(1)
                            Combined.append(1)
                            NetWin += unitSize
                        elif (row["O/U Outcome"] == "Under"):
                            OU.append(0)
                            Combined.append(0)
                            NetWin -= unitSize*1.05
                except:
                    pass
                if (row["Team"] == row["Favorite"]):
                    try:
                        if (float(row["PFITS"]) - float(bigboy.at[index+1,"PFITS"]) - SpreadBuffer > float(row["Spread"])):
                            if (row["Spread Winner"] == row["Team"]):
                                Spread.append(1)
                                Combined.append(1)
                                NetWin += unitSize
                            else:
                                Spread.append(0)
                                Combined.append(0)
                                NetWin -= unitSize*1.05
                        elif (float(row["PFITS"]) - float(bigboy.at[index+1,"PFITS"]) + SpreadBuffer < float(row["Spread"])):
                            if (row["Spread Winner"] == bigboy.at[index+1,"Team"]):
                                Spread.append(1)
                                Combined.append(1)
                                NetWin += unitSize
                            else:
                                Spread.append(0)
                                Combined.append(0)
                                NetWin -= unitSize*1.05
                    except:
                        pass
                elif (bigboy.at[index+1,"Team"] == row["Favorite"]):
                    try:
                        if (float(bigboy.at[index+1,"PFITS"]) - float(row["PFITS"]) - SpreadBuffer > float(bigboy.at[index+1,"Spread"])):
                            if (row["Spread Winner"] == bigboy.at[index+1,"Team"]):
                                Spread.append(1)
                                Combined.append(1)
                                NetWin += unitSize
                            else:
                                Spread.append(0)
                                Combined.append(0)
                                NetWin -= unitSize*1.05
                        elif (float(bigboy.at[index+1,"PFITS"]) - float(row["PFITS"]) + SpreadBuffer < float(bigboy.at[index+1,"Spread"])):
                            if (row["Spread Winner"] == row["Team"]):
                                Spread.append(1)
                                Combined.append(1)
                                NetWin += unitSize
                            else:
                                Spread.append(0)
                                Combined.append(0)
                                NetWin -= unitSize*1.05
                    except:
                        pass
        except KeyError:
            pass
    print ("O/U Percent - Num Bets|", np.average(OU), len(OU))
    print ("Spread Percent - Num Bets|", np.average(Spread), len(Spread))
    print ("Combined Percents - Num Bets|", np.average(Combined), len(Combined))
    print ("Net Winnings:", NetWin)

def testFitAlt(bigboy, OUBuffer, SpreadBuffer, unitSize):
    OU = []
    Spread = []
    Combined = []
    NetWin = 0
    for index, row in bigboy.iterrows():
        try:
            if (float(row["PFITS Spread"]) + SpreadBuffer < float(row["alt_spread"])):
                if (float(row["Actual Spread"]) < float(row["alt_spread"])):
                    Spread.append(1)
                    Combined.append(1)
                    NetWin += unitSize
                elif (float(row["Actual Spread"]) > float(row["alt_spread"])):
                    Spread.append(0)
                    Combined.append(0)
                    NetWin -= unitSize*1.05
            elif (float(row["PFITS Spread"]) - SpreadBuffer > float(row["alt_spread"])):
                if (float(row["Actual Spread"]) > float(row["alt_spread"])):
                    Spread.append(1)
                    Combined.append(1)
                    NetWin += unitSize
                elif (float(row["Actual Spread"]) < float(row["alt_spread"])):
                    Spread.append(0)
                    Combined.append(0)
                    NetWin -= unitSize*1.05
        except:
            pass
        try:
            if (float(row["PFITS Total"]) + OUBuffer < float(row["O/U"])):
                if (int(row["Actual Total"]) < float(row["O/U"])):
                    OU.append(1)
                    Combined.append(1)
                    NetWin += unitSize
                elif (int(row["Actual Total"]) > float(row["O/U"])):
                    OU.append(0)
                    Combined.append(0)
                    NetWin -= unitSize*1.05
            elif (float(row["PFITS Total"]) - OUBuffer > float(row["O/U"])):
                if (int(row["Actual Total"]) > float(row["O/U"])):
                    OU.append(1)
                    Combined.append(1)
                    NetWin += unitSize
                elif (int(row["Actual Total"]) < float(row["O/U"])):
                    OU.append(0)
                    Combined.append(0)
                    NetWin -= unitSize*1.05
        except:
            pass
    print ("O/U Percent - Num Bets|", np.average(OU), len(OU))
    print ("Spread Percent - Num Bets|", np.average(Spread), len(Spread))
    print ("Combined Percents - Num Bets|", np.average(Combined), len(Combined))
    print ("Net Winnings:", NetWin)
    return (NetWin)

def testClassification(bigboy, unitSize, betMethod, Week = False, Year = False, betType = "Spread", odds = -105, manualCO = -1, printOption = True):
    dict = {"All":[],"Week":{},"Year":{},"Cutoff-52.5":[],"52.5-55":[],"55-60":[],"60-70":[],"70+":[]}
    netWin = 0
    bankroll = unitSize * 100
    winScale = 100/abs(odds)
    if (manualCO == -1):
        cutOff = abs(odds)/(abs(odds) + 100)
    else:
        cutOff = manualCO
    for index, row in bigboy.iterrows():
        if (float(row["PFITS"]) > cutOff):
            if (Week and int(row["Week"]) not in dict["Week"]):
                dict["Week"][int(row["Week"])] = []
            if (Year and int(row["Year"]) not in dict["Year"]):
                dict["Year"][int(row["Year"])] = []
            if (betType == "Spread"):
                if (int(row["binSpread"])):
                    dict["All"].append(1)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(1)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(1)
                    if (float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(1)
                    elif (float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(1)
                    elif (float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(1)
                    elif (float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(1)
                    else:
                        dict["70+"].append(1)
                    if (betMethod == "Kelly"):
                        netWin += unitSize * (float(row["PFITS"]) - ((1-float(row["PFITS"]))/winScale)) * winScale * 100
                    elif (betMethod == "Standard"):
                        netWin += unitSize * winScale
                else:
                    dict["All"].append(0)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(0)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(0)
                    if (float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(0)
                    elif (float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(0)
                    elif (float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(0)
                    elif (float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(0)
                    else:
                        dict["70+"].append(0)
                    if (betMethod == "Kelly"):
                        netWin -= unitSize * (float(row["PFITS"]) - ((1-float(row["PFITS"]))/winScale)) * 100
                    elif (betMethod == "Standard"):
                        netWin -= unitSize
            elif (betType == "O/U"):
                if (int(row["binTotal"])):
                    dict["All"].append(1)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(1)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(1)
                    if (float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(1)
                    elif (float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(1)
                    elif (float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(1)
                    elif (float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(1)
                    else:
                        dict["70+"].append(1)
                    if (betMethod == "Kelly"):
                        netWin += unitSize * (float(row["PFITS"]) - ((1-float(row["PFITS"]))/winScale)) * winScale * 100
                    elif (betMethod == "Standard"):
                        netWin += unitSize * winScale
                else:
                    dict["All"].append(0)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(0)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(0)
                    if (float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(0)
                    elif (float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(0)
                    elif (float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(0)
                    elif (float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(0)
                    else:
                        dict["70+"].append(0)
                    if (betMethod == "Kelly"):
                        netWin -= unitSize * (float(row["PFITS"]) - ((1-float(row["PFITS"]))/winScale)) * 100
                    elif (betMethod == "Standard"):
                        netWin -= unitSize
        elif (float(row["PFITS"]) < 1 - cutOff):
            if (Week and int(row["Week"]) not in dict["Week"]):
                dict["Week"][int(row["Week"])] = []
            if (Year and int(row["Year"]) not in dict["Year"]):
                dict["Year"][int(row["Year"])] = []
            if (betType == "Spread"):
                if (not int(row["binSpread"])):
                    dict["All"].append(1)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(1)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(1)
                    if (1 - float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(1)
                    elif (1 - float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(1)
                    elif (1 - float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(1)
                    elif (1 - float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(1)
                    else:
                        dict["70+"].append(1)
                    if (betMethod == "Kelly"):
                        netWin += unitSize * ((1-float(row["PFITS"])) - (float(row["PFITS"])/winScale)) * winScale * 100
                    elif (betMethod == "Standard"):
                        netWin += unitSize * winScale
                else:
                    dict["All"].append(0)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(0)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(0)
                    if (1 - float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(0)
                    elif (1 - float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(0)
                    elif (1 - float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(0)
                    elif (1 - float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(0)
                    else:
                        dict["70+"].append(0)
                    if (betMethod == "Kelly"):
                        netWin -= unitSize * ((1-float(row["PFITS"])) - (float(row["PFITS"])/winScale)) * 100
                    elif (betMethod == "Standard"):
                        netWin -= unitSize
            elif (betType == "O/U"):
                if (not int(row["binTotal"])):
                    dict["All"].append(1)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(1)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(1)
                    if (1 - float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(1)
                    elif (1 - float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(1)
                    elif (1 - float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(1)
                    elif (1 - float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(1)
                    else:
                        dict["70+"].append(1)
                    if (betMethod == "Kelly"):
                        netWin += unitSize * ((1-float(row["PFITS"])) - (float(row["PFITS"])/winScale)) * winScale * 100
                    elif (betMethod == "Standard"):
                        netWin += unitSize * winScale
                else:
                    dict["All"].append(0)
                    if (Week):
                        dict["Week"][int(row["Week"])].append(0)
                    if (Year):
                        dict["Year"][int(row["Year"])].append(0)
                    if (1 - float(row["PFITS"]) < 0.525):
                        dict["Cutoff-52.5"].append(0)
                    elif (1 - float(row["PFITS"]) < 0.55):
                        dict["52.5-55"].append(0)
                    elif (1 - float(row["PFITS"]) < 0.6):
                        dict["55-60"].append(0)
                    elif (1 - float(row["PFITS"]) < 0.7):
                        dict["60-70"].append(0)
                    else:
                        dict["70+"].append(0)
                    if (betMethod == "Kelly"):
                        netWin -= unitSize * ((1-float(row["PFITS"])) - (float(row["PFITS"])/winScale)) * 100
                    elif (betMethod == "Standard"):
                        netWin -= unitSize
    if (printOption):
        print ("Total WR of", np.average(dict["All"]), "off of", len(dict["All"]), "bets (" + str(len(bigboy.index)) + " total games)")
        print ("Total WR of", np.average(dict["Cutoff-52.5"]), "for probabilities Cutoff-.525 (", len(dict["Cutoff-52.5"]), " bets)")
        print ("Total WR of", np.average(dict["52.5-55"]), "for probabilities .525-.55 (", len(dict["52.5-55"]), " bets)")
        print ("Total WR of", np.average(dict["55-60"]), "for probabilities .55-.60 (", len(dict["55-60"]), " bets)")
        print ("Total WR of", np.average(dict["60-70"]), "for probabilities .60-.70 (", len(dict["60-70"]), " bets)")
        print ("Total WR of", np.average(dict["70+"]), "for probabilities .70+ (", len(dict["70+"]), " bets)")
        print ("-----------------------------------------")
        for key in dict["Week"]:
            print (key, np.average(dict["Week"][key]), "(" + str(len(dict["Week"][key])) + " total bets)")
        print ("-----------------------------------------")
        for key in dict["Year"]:
            print (key, np.average(dict["Year"][key]), "(" + str(len(dict["Year"][key])) + " total bets)")
        print ("-----------------------------------------")
        print (netWin)
    return (netWin)
