from cfbFcns import standardizeTeamName
import pandas as pd

print (standardizeTeamName("San JosÃ© State", True))
str = "San JosÃ© State"
print (str.lower())
stats = pd.read_csv('./csv_Data/advStatsFwdLooking/2016.csv', encoding = "ISO-8859-1").drop(columns = ["Unnamed: 0"])
print (stats.iat[70,1].lower())
