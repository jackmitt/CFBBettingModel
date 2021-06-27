import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

df5 = pd.read_csv('./csv_Data/TrainingDataByWeek/5.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
df6 = pd.read_csv('./csv_Data/TrainingDataByWeek/6.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
df7 = pd.read_csv('./csv_Data/TrainingDataByWeek/7.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
df8 = pd.read_csv('./csv_Data/TrainingDataByWeek/8.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
df9 = pd.read_csv('./csv_Data/TrainingDataByWeek/9.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
df10 = pd.read_csv('./csv_Data/TrainingDataByWeek/10.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
df999 = pd.read_csv('./csv_Data/TrainingDataByWeek/999.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])

frames = [df5,df6,df7,df8,df9,df10,df999]
dropRows = []
result = pd.concat(frames)
print (result)
for index, row in result.iterrows():
    if (np.isnan(row["Home Incoming Elo"]) or np.isnan(row["Road Incoming Elo"])):
        dropRows.append(index)
print (dropRows)
result = result.drop(dropRows)
print (result)
result.to_csv("./csv_Data/completeTrainSet.csv")
