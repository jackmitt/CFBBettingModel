import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
from cfbFcns import getBin
from sklearn.linear_model import LinearRegression

we = [1]
Drop = True
#dropping columns that arent relevant
#relCols = ["Spread","Week","Year","TrueHF","HTeam","Favorite","Spread Winner","Elo_diff_aboveAvg","Sophomore_diff_aboveAvg","Junior_diff_aboveAvg","Sr_diff_aboveAvg","PwrS_diff_aboveAvg","StDownSr_diff_aboveAvg","PassDownExp_diff_aboveAvg","adj_powerSuccess_diff_aboveAvg","adj_standardDowns.ppa_diff_aboveAvg","adj_passingDowns.explosiveness_diff_aboveAvg","adj_rushingPlays.successRate_diff_aboveAvg","adj_rushingPlays.successRate_diff_aboveAvg","RedZone ppa_diff_aboveAvg","Points_diff_aboveAvg","Junior_diff_Indicator","Coach_diff_Indicator","Sr_diff_Indicator","Exp_diff_Indicator","Stuff_diff_Indicator","OpenField_diff_Indicator","StDownExp_diff_Indicator","PassDownExp_diff_Indicator","adj_standardDowns.ppa_diff_Indicator","adj_standardDowns.explosiveness_diff_Indicator","adj_rushingPlays.ppa_diff_Indicator"]
for w in we:
    reg = pd.DataFrame()
    #ignore 37 or greater spreads
    a = pd.read_csv('./new_csv_Data/bigboyAlt.csv', encoding = "ISO-8859-1")
    rem = []
    for col in a.columns:
        if ("totalPPA" in col):
            rem.append(col)
    a = a.drop(columns=rem)
    #dropping columns that arent relevant before dropping N.A rows so more games get included
    #for col in a.columns:
        #for b in relCols:
        #    if (b.split("_diff")[0] in col):
            #    Drop = False
        #    if ("adj_" in b):
            #    if (b.split("_diff")[0].split("adj_")[1] in col):
        #            Drop = False
    #    if (Drop):
        #    a = a.drop(columns=col)
    #    Drop = True
    #TEMP ADDITION
    a = a.dropna()
    print (len(a.index))
    if ("binSpread" not in a.columns):
        temp = []
        for index, row in a.iterrows():
            if (row["Spread Winner"] == row["Favorite"]):
                temp.append(1)
            elif (row["Spread Winner"] == "Push"):
                temp.append(np.nan)
            else:
                temp.append(0)
        a["binSpread"] = temp
    if ("FavHF" not in a.columns):
        temp = []
        for index, row in a.iterrows():
            if (row["HTeam"] == row["Favorite"] and int(row["TrueHF"]) == 1):
                temp.append(1)
            elif (int(row["TrueHF"]) == 0):
                temp.append(0.5)
            else:
                temp.append(0)
        a["FavHF"] = temp
    dict = {}
    for index, row in a.iterrows():
        #print (index)
        if (row["HTeam"] == row["Favorite"]):
            homeFav = True
        else:
            homeFav = False
        for col in a.columns:
            if ('H' == col[0] and 'o' == col[1] and "Score" not in col):
                if (homeFav):
                    if ("FE_" + col.split("Ho")[1] not in dict):
                        dict["FE_" + col.split("Ho")[1]] = []
                    dict["FE_" + col.split("Ho")[1]].append((float(row[col]) + float(row["Rd" + col.split("Ho")[1]])) / 2)
                else:
                    if ("DE_" + col.split("Ho")[1] not in dict):
                        dict["DE_" + col.split("Ho")[1]] = []
                    dict["DE_" + col.split("Ho")[1]].append((float(row[col]) + float(row["Rd" + col.split("Ho")[1]])) / 2)
            elif ('R' == col[0] and 'o' == col[1] and "Score" not in col):
                if (homeFav):
                    if ("DE_" + col.split("Ro")[1] not in dict):
                        dict["DE_" + col.split("Ro")[1]] = []
                    dict["DE_" + col.split("Ro")[1]].append((float(row[col]) + float(row["Hd" + col.split("Ro")[1]])) / 2)
                else:
                    if ("FE_" + col.split("Ro")[1] not in dict):
                        dict["FE_" + col.split("Ro")[1]] = []
                    dict["FE_" + col.split("Ro")[1]].append((float(row[col]) + float(row["Hd" + col.split("Ro")[1]])) / 2)
            elif ("Hadj_offense." in col):
                if (homeFav):
                    if ("FE_adj_" + col.split("Hadj_offense.")[1] not in dict):
                        dict["FE_adj_" + col.split("Hadj_offense.")[1]] = []
                    dict["FE_adj_" + col.split("Hadj_offense.")[1]].append((float(row[col]) + float(row["Radj_defense." + col.split("Hadj_offense.")[1]])) / 2)
                else:
                    if ("DE_adj_" + col.split("Hadj_offense.")[1] not in dict):
                        dict["DE_adj_" + col.split("Hadj_offense.")[1]] = []
                    dict["DE_adj_" + col.split("Hadj_offense.")[1]].append((float(row[col]) + float(row["Radj_defense." + col.split("Hadj_offense.")[1]])) / 2)
            elif ("Radj_offense." in col):
                if (homeFav):
                    if ("DE_adj_" + col.split("Radj_offense.")[1] not in dict):
                        dict["DE_adj_" + col.split("Radj_offense.")[1]] = []
                    dict["DE_adj_" + col.split("Radj_offense.")[1]].append((float(row[col]) + float(row["Hadj_defense." + col.split("Radj_offense.")[1]])) / 2)
                else:
                    if ("FE_adj_" + col.split("Radj_offense.")[1] not in dict):
                        dict["FE_adj_" + col.split("Radj_offense.")[1]] = []
                    dict["FE_adj_" + col.split("Radj_offense.")[1]].append((float(row[col]) + float(row["Hadj_defense." + col.split("Radj_offense.")[1]])) / 2)
            elif (" Class" in col and 'H' == col[0]):
                if (homeFav):
                    if (col.split(" Class")[0].split("H")[1] + "_diff" not in dict):
                        dict[col.split(" Class")[0].split("H")[1] + "_diff"] = []
                    dict[col.split(" Class")[0].split("H")[1] + "_diff"].append(int(row[col]) - int(row["R" + col.split(" Class")[0].split("H")[1] + " Class"]))
                else:
                    if (col.split(" Class")[0].split("H")[1] + "_diff" not in dict):
                        dict[col.split(" Class")[0].split("H")[1] + "_diff"] = []
                    dict[col.split(" Class")[0].split("H")[1] + "_diff"].append(int(row["R" + col.split(" Class")[0].split("H")[1] + " Class"]) - int(row[col]))
            elif ("HCoach" in col):
                if ("Coach_diff" not in dict):
                    dict["Coach_diff"] = []
                if (homeFav):
                    dict["Coach_diff"].append(float(row["HCoach WPAR"]) - float(row["RCoach WPAR"]))
                else:
                    dict["Coach_diff"].append(float(row["RCoach WPAR"]) - float(row["HCoach WPAR"]))
            elif (col == "HElo"):
                if (homeFav):
                    if ("Elo_diff" not in dict):
                        dict["Elo_diff"] = []
                    dict["Elo_diff"].append(float(row[col]) - float(row["RElo"]))
                else:
                    if ("Elo_diff" not in dict):
                        dict["Elo_diff"] = []
                    dict["Elo_diff"].append(float(row["RElo"]) - float(row[col]))
            elif ("Offense penalty" in col):
                if ("H" == col[0]):
                    if (homeFav):
                        if ("FE_Penalty" not in dict):
                            dict["FE_Penalty"] = []
                        dict["FE_Penalty"].append((float(row[col]) + float(row["RDefense penalty avg"])) / 2)
                    else:
                        if ("DE_Penalty" not in dict):
                            dict["DE_Penalty"] = []
                        dict["DE_Penalty"].append((float(row[col]) + float(row["RDefense penalty avg"])) / 2)
                else:
                    if (homeFav):
                        if ("DE_Penalty" not in dict):
                            dict["DE_Penalty"] = []
                        dict["DE_Penalty"].append((float(row[col]) + float(row["HDefense penalty avg"])) / 2)
                    else:
                        if ("FE_Penalty" not in dict):
                            dict["FE_Penalty"] = []
                        dict["FE_Penalty"].append((float(row[col]) + float(row["HDefense penalty avg"])) / 2)
            elif (col == "HFG pct"):
                if ("FG_diff" not in dict):
                    dict["FG_diff"] = []
                if (homeFav):
                    dict["FG_diff"].append(float(row["HFG pct"]) - float(row["RFG pct"]))
                else:
                    dict["FG_diff"].append(float(row["RFG pct"]) - float(row["HFG pct"]))
            elif (col == "HoRedZone ppa"):
                if (homeFav):
                    if ("FE_RZ_ppa" not in dict):
                        dict["FE_RZ_ppa"] = []
                    dict["FE_RZ_ppa"].append((float(row["HoRedZone ppa"]) + float(row["RdRedZone ppa"])) / 2)
                else:
                    if ("DE_RZ_ppa" not in dict):
                        dict["DE_RZ_ppa"] = []
                    dict["DE_RZ_ppa"].append((float(row["HoRedZone ppa"]) + float(row["RdRedZone ppa"])) / 2)
            elif (col == "RoRedZone ppa"):
                if (homeFav):
                    if ("DE_RZ_ppa" not in dict):
                        dict["DE_RZ_ppa"] = []
                    dict["DE_RZ_ppa"].append((float(row["RoRedZone ppa"]) + float(row["HdRedZone ppa"])) / 2)
                else:
                    if ("FE_RZ_ppa" not in dict):
                        dict["FE_RZ_ppa"] = []
                    dict["FE_RZ_ppa"].append((float(row["RoRedZone ppa"]) + float(row["HdRedZone ppa"])) / 2)
            elif (col == "HTurnover avg"):
                if (homeFav):
                    if ("FE_TO" not in dict):
                        dict["FE_TO"] = []
                    dict["FE_TO"].append((float(row["HTurnover avg"]) + float(row["ROpponent turnover avg"])) / 2)
                else:
                    if ("DE_TO" not in dict):
                        dict["DE_TO"] = []
                    dict["DE_TO"].append((float(row["HTurnover avg"]) + float(row["ROpponent turnover avg"])) / 2)
            elif (col == "RTurnover avg"):
                if (homeFav):
                    if ("DE_TO" not in dict):
                        dict["DE_TO"] = []
                    dict["DE_TO"].append((float(row["RTurnover avg"]) + float(row["HOpponent turnover avg"])) / 2)
                else:
                    if ("FE_TO" not in dict):
                        dict["FE_TO"] = []
                    dict["FE_TO"].append((float(row["RTurnover avg"]) + float(row["HOpponent turnover avg"])) / 2)
            elif (col == "HAvg Points For"):
                if (homeFav):
                    if ("FE_Pts" not in dict):
                        dict["FE_Pts"] = []
                    dict["FE_Pts"].append((float(row["HAvg Points For"]) + float(row["RAvg Points Against"])) / 2)
                else:
                    if ("DE_Pts" not in dict):
                        dict["DE_Pts"] = []
                    dict["DE_Pts"].append((float(row["HAvg Points For"]) + float(row["RAvg Points Against"])) / 2)
            elif (col == "RAvg Points For"):
                if (homeFav):
                    if ("DE_Pts" not in dict):
                        dict["DE_Pts"] = []
                    dict["DE_Pts"].append((float(row["RAvg Points For"]) + float(row["HAvg Points Against"])) / 2)
                else:
                    if ("FE_Pts" not in dict):
                        dict["FE_Pts"] = []
                    dict["FE_Pts"].append((float(row["RAvg Points For"]) + float(row["HAvg Points Against"])) / 2)
            elif (col == "HCompletion Pct"):
                if (homeFav):
                    if ("FE_Completion" not in dict):
                        dict["FE_Completion"] = []
                    dict["FE_Completion"].append((float(row["HCompletion Pct"]) + float(row["ROpponent Completion Pct"])) / 2)
                else:
                    if ("DE_Completion" not in dict):
                        dict["DE_Completion"] = []
                    dict["DE_Completion"].append((float(row["HCompletion Pct"]) + float(row["ROpponent Completion Pct"])) / 2)
            elif (col == "RCompletion Pct"):
                if (homeFav):
                    if ("DE_Completion" not in dict):
                        dict["DE_Completion"] = []
                    dict["DE_Completion"].append((float(row["RCompletion Pct"]) + float(row["HOpponent Completion Pct"])) / 2)
                else:
                    if ("FE_Completion" not in dict):
                        dict["FE_Completion"] = []
                    dict["FE_Completion"].append((float(row["RCompletion Pct"]) + float(row["HOpponent Completion Pct"])) / 2)
            elif (col == "HAvg TOP"):
                if (homeFav):
                    if ("FE_TOP" not in dict):
                        dict["FE_TOP"] = []
                    dict["FE_TOP"].append((float(row["HAvg TOP"]) + float(row["RAvg Opponent TOP"])) / 2)
                else:
                    if ("DE_TOP" not in dict):
                        dict["DE_TOP"] = []
                    dict["DE_TOP"].append((float(row["HAvg TOP"]) + float(row["RAvg Opponent TOP"])) / 2)
            elif (col == "RAvg TOP"):
                if (homeFav):
                    if ("DE_TOP" not in dict):
                        dict["DE_TOP"] = []
                    dict["DE_TOP"].append((float(row["RAvg TOP"]) + float(row["HAvg Opponent TOP"])) / 2)
                else:
                    if ("FE_TOP" not in dict):
                        dict["FE_TOP"] = []
                    dict["FE_TOP"].append((float(row["RAvg TOP"]) + float(row["HAvg Opponent TOP"])) / 2)
    print ("---------------------------------------------------")
    print (len(a.index))
    for key in dict:
        print (key, len(dict[key]))
        a[key] = dict[key]
    dict = {}
    for index, row in a.iterrows():
        for col in a.columns:
            if ("FE_" in col):
                if (col.split("FE_")[1] + "_diff" not in dict):
                    dict[col.split("FE_")[1] + "_diff"] = []
                dict[col.split("FE_")[1] + "_diff"].append(float(row[col]) - float(row["DE_" + col.split("FE_")[1]]))
    for key in dict:
        a[key] = dict[key]
    a = a.dropna()
    reg["Spread"] = a["Spread"]
    for col in a.columns:
        if ("_diff" in col or col == "FavHF"):
            reg[col] = a[col]
    dict = {}
    temp = pd.DataFrame()
    for index, row in a.iterrows():
        print (index)
        temp = reg.copy()
        temp = temp.drop(index = index)
        for col in a.columns:
            if ("_diff" in col or col == "FavHF"):
                testSpread = a.at[index, "Spread"]
                if (col + "_aboveAvg" not in dict):
                    dict[col + "_aboveAvg"] = []
                #Change depending on model weeks
                if (getBin(row["Spread"], W234 = False) == -1):
                    dict[col + "_aboveAvg"].append(np.nan)
                    continue
                model = LinearRegression(fit_intercept = False)
                model.fit(X = temp["Spread"].to_numpy().reshape(-1,1), y = temp[col].to_numpy().reshape(-1,1))
                dict[col + "_aboveAvg"].append(a.at[index, col] - model.predict(testSpread.reshape(1,-1))[0][0])
        temp = pd.DataFrame()
    for key in dict:
        a[key] = dict[key]
    dict = {}
    count = 0
    for col in a.columns:
        if ("_aboveAvg" in col):
            dict[col.split("_aboveAvg")[0] + "_Indicator"] = []
            mean = a[col].mean()
            stdev = a[col].std()
            for index, row in a.iterrows():
                if (((float(row[col]) - mean)/stdev) <= -1.645):
                    dict[col.split("_aboveAvg")[0] + "_Indicator"].append(-1)
                elif (((float(row[col]) - mean)/stdev) >= 1.645):
                    dict[col.split("_aboveAvg")[0] + "_Indicator"].append(1)
                else:
                    dict[col.split("_aboveAvg")[0] + "_Indicator"].append(0)
            count = 0
            for x in dict[col.split("_aboveAvg")[0] + "_Indicator"]:
                if (x != 0):
                    count += 1
            print (col, count/len(dict[col.split("_aboveAvg")[0] + "_Indicator"]))
    for key in dict:
        a[key] = dict[key]
    a = a.dropna()
    a.to_csv("./new_csv_Data/bigboyBinClassification.csv")
