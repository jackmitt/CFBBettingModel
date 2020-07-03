import CFBScrapy as cfb
from cfbFcns import standardizeTeamName
import pandas

thisYear = 2015
t = cfb.get_team_talent(year=thisYear)
t = t.drop(columns=["year"])
pwrRate = []
for i in range(len(t.index)):
    pwrRate.append(float(t.at[i,"talent"])/float(t.at[0,"talent"]))
t["pwrRating"] = pwrRate
dropRows = []
for i in range(len(t.index)):
    if (len(standardizeTeamName(t.at[i,"school"]).split("Error")) > 1):
        dropRows.append(i)
    else:
        t.at[i,"school"] = standardizeTeamName(t.at[i,"school"])
t = t.drop(dropRows)
dropRows = []
a = pandas.read_csv("./csv_Data/AdvancedStatsSeason/2014.csv", encoding = "ISO-8859-1")
for i in range(len(a.index)):
    if (len(standardizeTeamName(a.at[i,"team"]).split("Error")) > 1):
        dropRows.append(i)
    else:
        a.at[i,"team"] = standardizeTeamName(a.at[i,"team"])
a = a.drop(dropRows)
print (t)
print (a)
for i in range(len(t.index)):
    for j in range(len(a.index)):
        if (t.at[i,"school"] == )
#print (t.at[0,"talent"])
