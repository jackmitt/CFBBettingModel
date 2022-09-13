import pandas as pd
import numpy as np

def absoluteDiffs():
    dict = {"<2.5":[],"<5":[],"<10":[],">10":[]}
    pred = pd.read_csv("./csv_data/bayes_predictions1.csv", encoding = "ISO-8859-1")
    for index, row in pred.iterrows():
        if (row["season"] < 2017):
            continue
        if (row["Open Spread"] != row["Open Spread"]):
            continue
        try:
            float(row["Open Spread"])
        except:
            continue
        if (abs(row["A_proj"] - row["H_proj"] - float(row["Open Spread"])) < 5):
            if (row["A_proj"] - row["H_proj"] < float(row["Open Spread"])):
                if (row["away_team_reg_score"] - row["home_team_reg_score"] < float(row["Open Spread"])):
                    dict["<2.5"].append(1)
                else:
                    dict["<2.5"].append(0)
            else:
                if (row["away_team_reg_score"] - row["home_team_reg_score"] > float(row["Open Spread"])):
                    dict["<2.5"].append(1)
                else:
                    dict["<2.5"].append(0)
        elif (abs(row["A_proj"] - row["H_proj"] - float(row["Open Spread"])) < 7):
            if (row["A_proj"] - row["H_proj"] < float(row["Open Spread"])):
                if (row["away_team_reg_score"] - row["home_team_reg_score"] < float(row["Open Spread"])):
                    dict["<5"].append(1)
                else:
                    dict["<5"].append(0)
            else:
                if (row["away_team_reg_score"] - row["home_team_reg_score"] > float(row["Open Spread"])):
                    dict["<5"].append(1)
                else:
                    dict["<5"].append(0)
        elif (abs(row["A_proj"] - row["H_proj"] - float(row["Open Spread"])) < 10):
            if (row["A_proj"] - row["H_proj"] < float(row["Open Spread"])):
                if (row["away_team_reg_score"] - row["home_team_reg_score"] < float(row["Open Spread"])):
                    dict["<10"].append(1)
                else:
                    dict["<10"].append(0)
            else:
                if (row["away_team_reg_score"] - row["home_team_reg_score"] > float(row["Open Spread"])):
                    dict["<10"].append(1)
                else:
                    dict["<10"].append(0)
        else:
            #print (row)
            if (row["A_proj"] - row["H_proj"] < float(row["Open Spread"])):
                if (row["away_team_reg_score"] - row["home_team_reg_score"] < float(row["Open Spread"])):
                    dict[">10"].append(1)
                else:
                    dict[">10"].append(0)
            else:
                if (row["away_team_reg_score"] - row["home_team_reg_score"] > float(row["Open Spread"])):
                    dict[">10"].append(1)
                else:
                    dict[">10"].append(0)
    for key in dict:
        print (key, np.average(dict[key]), len(dict[key]))

def clv():
    pred = pd.read_csv("./csv_data/bayes_predictions.csv", encoding = "ISO-8859-1")
    clv = []
    wr = []
    for index, row in pred.iterrows():
        if (row["season"] < 2017):
            continue
        if (row["Open Spread"] == row["Open Spread"] and row["spread"] == row["spread"] and row["H_proj"] == row["H_proj"]):
            try:
                if (row["A_proj"] - row["H_proj"] + 10 < float(row["Open Spread"])):
                    clv.append(float(row["Open Spread"]) - row["spread"])
                    if (row["away_team_reg_score"] - row["home_team_reg_score"] < float(row["Open Spread"])):
                        wr.append(1)
                    elif (row["away_team_reg_score"] - row["home_team_reg_score"] > float(row["Open Spread"])):
                        wr.append(0)
                elif (row["A_proj"] - row["H_proj"] - 10 > float(row["Open Spread"])):
                    clv.append(row["spread"] - float(row["Open Spread"]))
                    if (row["away_team_reg_score"] - row["home_team_reg_score"] > float(row["Open Spread"])):
                        wr.append(1)
                    elif (row["away_team_reg_score"] - row["home_team_reg_score"] < float(row["Open Spread"])):
                        wr.append(0)
            except:
                pass

    print (np.average(clv), len(clv))
    print (np.average(wr), len(wr))
absoluteDiffs()
