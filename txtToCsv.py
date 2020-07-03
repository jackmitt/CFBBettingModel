#Formatting of txt files changes after 2009
import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
import datetime

thisYear = "2009"
f = open("./txt_Spreads/" + thisYear + ".txt", "r")

testBool = False
testCount = 0

teams = 0
dict = {"Week":[],"Date":[],"Home Team":[],"Road Team":[],"Neutral Field":[],"Night Game":[],"Postseason Game":[],"Favorite":[],"Spread":[],"O/U":[],"Home Score":[],"Road Score":[],"Spread Winner":[],"O/U Outcome":[]}
lines = f.readlines()

if (int(thisYear) < 2010):
    for i in range(len(lines)):
        if (lines[i] != "\n" and lines[i] != " \n"):
            splitLine = lines[i].split()
            #print (splitLine)
            if (splitLine[0] == "(SUR:"):
                games = int(splitLine[1].split("-")[1]) + int(splitLine[1].split("-")[0])
                j = 1
                while (j<=games):
                    x = j
                    row = lines[x+i].split()
                    #print (row)
                    if (len(row[0].split("(")) > 1):
                        games += 1
                        j += 1
                        continue
                    if (len(row) <= 4):
                        j += 1
                        continue
                    if (row[2] == "Cancelled" or row[3] == "Cancelled"):
                        j += 1
                        continue
                    getOut = False
                    for ele in row:
                        if (ele == "NC" or ele == "nc"):
                            getOut = True
                    if (getOut):
                        j += 1
                        continue
                    k = 1
                    home = True
                    teamString = ""
                    while (row[k] != "W" and row[k] != "L" and row[k] != "N"):
                        for char in row[k]:
                            if (char.islower()):
                                home = False
                        if (teamString == ""):
                            teamString = row[k].split("-ot")[0].split("-OT")[0].split("#")[0].split("-2ot")[0].split("-3ot")[0].split("-4ot")[0].split("-5ot")[0].split("-6ot")[0].split("-7ot")[0]
                        else:
                            teamString = teamString + " " + row[k].split("-ot")[0].split("-OT")[0].split("#")[0].split("-2ot")[0].split("-3ot")[0].split("-4ot")[0].split("-5ot")[0].split("-6ot")[0].split("-7ot")[0]
                        k = k + 1
                        if (k == len(row)):
                            getOut = True
                            break
                    if (getOut):
                        j += 1
                        continue
                    if (len(standardizeTeamName(teamString, True).split("Error: ")) > 1):
                        print (standardizeTeamName(teamString, True))
                    if (len(standardizeTeamName(lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], True).split("Error: ")) > 1):
                        print (standardizeTeamName(lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], True))
                    if (len(row[0].split("*")) == 2):
                        NG = True
                    else:
                        NG = False
                    try:
                        if (len(lines[i+x+1].split()[0].split("(")) > 1):
                            NF = True
                            if (len(lines[i+x+1].split("Bowl")) > 1 or len(lines[i+x+1].split("Championship")) > 1):
                                PG = True
                            else:
                                PG = False
                        else:
                            NF = False
                            PG = False
                    except:
                        NF = False
                        PG = False
                    for n in range(len(dict["Date"])):
                        if (dict["Home Team"][n] == standardizeTeamName(lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False) or dict["Home Team"][n] == standardizeTeamName(teamString, False)):
                            if (dict["Road Team"][n] == standardizeTeamName(lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False) or dict["Road Team"][n] == standardizeTeamName(teamString, False)):
                                if ((PG and dict["Postseason Game"][n] == 1) or (not PG and dict["Postseason Game"][n] == 0)):
                                    getOut = True
                    try:
                        if (row[6] == "nt"):
                            getOut = True
                    except:
                        pass
                    if (getOut):
                        j += 1
                        continue
                    if (PG):
                        dict["Postseason Game"].append(1)
                    else:
                        dict["Postseason Game"].append(0)
                    if (NG):
                        dict["Night Game"].append(1)
                    else:
                        dict["Night Game"].append(0)
                    if (NF):
                        dict["Neutral Field"].append(1)
                    else:
                        dict["Neutral Field"].append(0)
                    if (row[0].split("*")[0].split(".")[0] == "A"):
                        curDate = datetime.date(month = 8, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "S"):
                        curDate = datetime.date(month = 9, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "O"):
                        curDate = datetime.date(month = 10, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "N"):
                        curDate = datetime.date(month = 11, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "D"):
                        curDate = datetime.date(month = 12, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "J"):
                        curDate = datetime.date(month = 1, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear) + 1)
                    dict["Date"].append(curDate.strftime("%m/%d/%Y"))
    # HARDCODE WEEKS FOR EVERY YEAR
                    lowDate = datetime.date(month = 8, day = 21, year = int(thisYear))
                    highDate = datetime.date(month = 9, day = 7, year = int(thisYear))
                    if (curDate <= highDate and curDate > lowDate):
                        dict["Week"].append(1)
                    else:
                        highDate = datetime.date(month = 9, day = 13, year = int(thisYear))
                        weekIter = 2
                        while (not (curDate <= highDate)):
                            weekIter += 1
                            highDate = highDate + datetime.timedelta(days = 7)
                        dict["Week"].append(weekIter)
                    if (row[k] == "W"):
                        dict["Spread Winner"].append(standardizeTeamName(lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False))
                    elif(row[k] == "L"):
                        dict["Spread Winner"].append(standardizeTeamName(teamString, False))
                    else:
                        dict["Spread Winner"].append("Push")
                    k += 1
                    if (home):
                        dict["Home Team"].append(standardizeTeamName(lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False))
                        dict["Road Team"].append(standardizeTeamName(teamString, False))
                    else:
                        dict["Road Team"].append(standardizeTeamName(lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False))
                        dict["Home Team"].append(standardizeTeamName(teamString, False))
                    reference = lines[i-1].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0]
                    if (len(row[k].split("+")) > 1):
                        dict["Favorite"].append(standardizeTeamName(teamString, False))
                        if (len(row[k].split("'")) > 1):
                            dict["Spread"].append(float(row[k].split("+")[1].split("'")[0]) + 0.5)
                        elif (len(row[k].split("’")) > 1):
                            dict["Spread"].append(float(row[k].split("+")[1].split("’")[0]) + 0.5)
                        else:
                            dict["Spread"].append(row[k].split("+")[1])
                    else:
                        dict["Favorite"].append(standardizeTeamName(reference, False))
                        if (len(row[k].split("'")) > 1):
                            dict["Spread"].append(float(row[k].split("-")[1].split("'")[0]) + 0.5)
                        elif (len(row[k].split("’")) > 1):
                            dict["Spread"].append(float(row[k].split("-")[1].split("’")[0]) + 0.5)
                        else:
                            if (row[k] == "P"):
                                dict["Spread"].append("0")
                            else:
                                dict["Spread"].append(row[k].split("-")[1])
                    k += 1
                    if (home):
                        dict["Home Score"].append(row[k].split("-")[0])
                        dict["Road Score"].append(row[k].split("-")[1])
                    else:
                        dict["Home Score"].append(row[k].split("-")[1])
                        dict["Road Score"].append(row[k].split("-")[0])
                    k += 1
                    if (k >= len(row)):
                        dict["O/U Outcome"].append(np.nan)
                        dict["O/U"].append(np.nan)
                    else:
                        if (len(row[k].split("o")) > 1):
                            dict["O/U Outcome"].append("Over")
                            if (len(row[k].split("'")) > 1):
                                dict["O/U"].append(float(row[k].split("'")[0].split("o")[1]) + 0.5)
                            elif (len(row[k].split("’")) > 1):
                                dict["O/U"].append(float(row[k].split("’")[0].split("o")[1]) + 0.5)
                            else:
                                dict["O/U"].append(float(row[k].split("o")[1]))
                        elif (len(row[k].split("u")) > 1):
                            dict["O/U Outcome"].append("Under")
                            if (len(row[k].split("'")) > 1):
                                dict["O/U"].append(float(row[k].split("'")[0].split("u")[1]) + 0.5)
                            elif (len(row[k].split("’")) > 1):
                                dict["O/U"].append(float(row[k].split("’")[0].split("u")[1]) + 0.5)
                            else:
                                dict["O/U"].append(float(row[k].split("u")[1]))
                        elif (len(row[k].split("n")) > 1):
                            dict["O/U Outcome"].append("Push")
                            if (len(row[k].split("'")) > 1):
                                dict["O/U"].append(float(row[k].split("'")[0].split("n")[1]) + 0.5)
                            elif (len(row[k].split("’")) > 1):
                                dict["O/U"].append(float(row[k].split("’")[0].split("n")[1]) + 0.5)
                            else:
                                dict["O/U"].append(float(row[k].split("n")[1]))
                        else:
                            print (row)
                    j += 1

else:
    for i in range(len(lines)):
        if (lines[i] != "\n" and lines[i] != " \n"):
            splitLine = lines[i].split()
            #print (splitLine)
            if (splitLine[0] == "(SUR:"):
                games = int(splitLine[1].split("-")[1]) + int(splitLine[1].split("-")[0])
                j = 1
                while (j<=games):
                    x = 2*j
                    row = lines[x+i].split()
                    #print (row)
                    if (len(row[0].split("(")) > 1):
                        games += 1
                        j += 1
                        continue
                    if (len(row) <= 4):
                        j += 1
                        continue
                    if (row[2] == "Cancelled" or row[3] == "Cancelled"):
                        j += 1
                        continue
                    getOut = False
                    for ele in row:
                        if (ele == "NC" or ele == "nc"):
                            getOut = True
                    if (getOut):
                        j += 1
                        continue
                    k = 1
                    home = True
                    teamString = ""
                    while (row[k] != "W" and row[k] != "L" and row[k] != "N"):
                        for char in row[k]:
                            if (char.islower()):
                                home = False
                        if (teamString == ""):
                            teamString = row[k].split("-ot")[0].split("-OT")[0].split("#")[0].split("-2ot")[0].split("-3ot")[0].split("-4ot")[0].split("-5ot")[0].split("-6ot")[0].split("-7ot")[0]
                        else:
                            teamString = teamString + " " + row[k].split("-ot")[0].split("-OT")[0].split("#")[0].split("-2ot")[0].split("-3ot")[0].split("-4ot")[0].split("-5ot")[0].split("-6ot")[0].split("-7ot")[0]
                        k = k + 1
                    if (len(standardizeTeamName(teamString, True).split("Error: ")) > 1):
                        print (standardizeTeamName(teamString, True))
                    if (len(standardizeTeamName(lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], True).split("Error: ")) > 1):
                        print (standardizeTeamName(lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], True))
                    if (len(row[0].split("*")) == 2):
                        NG = True
                    else:
                        NG = False
                    try:
                        if (len(lines[i+x+2].split()[0].split("(")) > 1):
                            NF = True
                            if (len(lines[i+x+2].split("Bowl")) > 1 or len(lines[i+x+2].split("Championship")) > 1):
                                PG = True
                            else:
                                PG = False
                        else:
                            NF = False
                            PG = False
                    except:
                        NF = False
                        PG = False
                    for n in range(len(dict["Date"])):
                        if (dict["Home Team"][n] == standardizeTeamName(lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False) or dict["Home Team"][n] == standardizeTeamName(teamString, False)):
                            if (dict["Road Team"][n] == standardizeTeamName(lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False) or dict["Road Team"][n] == standardizeTeamName(teamString, False)):
                                if ((PG and dict["Postseason Game"][n] == 1) or (not PG and dict["Postseason Game"][n] == 0)):
                                    getOut = True
                    try:
                        if (row[6] == "nt"):
                            getOut = True
                    except:
                        pass
                    if (getOut):
                        j += 1
                        continue
                    if (PG):
                        dict["Postseason Game"].append(1)
                    else:
                        dict["Postseason Game"].append(0)
                    if (NG):
                        dict["Night Game"].append(1)
                    else:
                        dict["Night Game"].append(0)
                    if (NF):
                        dict["Neutral Field"].append(1)
                    else:
                        dict["Neutral Field"].append(0)
                    if (row[0].split("*")[0].split(".")[0] == "A"):
                        curDate = datetime.date(month = 8, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "S"):
                        curDate = datetime.date(month = 9, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "O"):
                        curDate = datetime.date(month = 10, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "N"):
                        curDate = datetime.date(month = 11, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "D"):
                        curDate = datetime.date(month = 12, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear))
                    elif (row[0].split("*")[0].split(".")[0] == "J"):
                        curDate = datetime.date(month = 1, day = int(row[0].split("*")[0].split(".")[1]), year = int(thisYear) + 1)
                    dict["Date"].append(curDate.strftime("%m/%d/%Y"))
    # HARDCODE WEEKS FOR EVERY YEAR
                    lowDate = datetime.date(month = 8, day = 25, year = int(thisYear))
                    highDate = datetime.date(month = 9, day = 6, year = int(thisYear))
                    if (curDate <= highDate and curDate > lowDate):
                        dict["Week"].append(1)
                    else:
                        highDate = datetime.date(month = 9, day = 12, year = int(thisYear))
                        weekIter = 2
                        while (not (curDate <= highDate)):
                            weekIter += 1
                            highDate = highDate + datetime.timedelta(days = 7)
                        dict["Week"].append(weekIter)
                    if (row[k] == "W"):
                        dict["Spread Winner"].append(standardizeTeamName(lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False))
                    elif(row[k] == "L"):
                        dict["Spread Winner"].append(standardizeTeamName(teamString, False))
                    else:
                        dict["Spread Winner"].append("Push")
                    k += 1
                    if (home):
                        dict["Home Team"].append(standardizeTeamName(lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False))
                        dict["Road Team"].append(standardizeTeamName(teamString, False))
                    else:
                        dict["Road Team"].append(standardizeTeamName(lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0], False))
                        dict["Home Team"].append(standardizeTeamName(teamString, False))
                    reference = lines[i-2].split(" (AT)")[0].split(" (P.A.T.)")[0].split(" (FT)")[0].split("\n")[0]
                    if (len(row[k].split("+")) > 1):
                        dict["Favorite"].append(standardizeTeamName(teamString, False))
                        if (len(row[k].split("'")) > 1):
                            dict["Spread"].append(float(row[k].split("+")[1].split("'")[0]) + 0.5)
                        elif (len(row[k].split("’")) > 1):
                            dict["Spread"].append(float(row[k].split("+")[1].split("’")[0]) + 0.5)
                        else:
                            dict["Spread"].append(row[k].split("+")[1])
                    else:
                        dict["Favorite"].append(standardizeTeamName(reference, False))
                        if (len(row[k].split("'")) > 1):
                            dict["Spread"].append(float(row[k].split("-")[1].split("'")[0]) + 0.5)
                        elif (len(row[k].split("’")) > 1):
                            dict["Spread"].append(float(row[k].split("-")[1].split("’")[0]) + 0.5)
                        else:
                            if (row[k] == "P"):
                                dict["Spread"].append("0")
                            else:
                                dict["Spread"].append(row[k].split("-")[1])
                    k += 1
                    if (home):
                        dict["Home Score"].append(row[k].split("-")[0])
                        dict["Road Score"].append(row[k].split("-")[1])
                    else:
                        dict["Home Score"].append(row[k].split("-")[1])
                        dict["Road Score"].append(row[k].split("-")[0])
                    k += 1
                    if (k >= len(row)):
                        dict["O/U Outcome"].append(np.nan)
                        dict["O/U"].append(np.nan)
                    else:
                        if (len(row[k].split("o")) > 1):
                            dict["O/U Outcome"].append("Over")
                            if (len(row[k].split("'")) > 1):
                                dict["O/U"].append(float(row[k].split("'")[0].split("o")[1]) + 0.5)
                            elif (len(row[k].split("’")) > 1):
                                dict["O/U"].append(float(row[k].split("’")[0].split("o")[1]) + 0.5)
                            else:
                                dict["O/U"].append(float(row[k].split("o")[1]))
                        elif (len(row[k].split("u")) > 1):
                            dict["O/U Outcome"].append("Under")
                            if (len(row[k].split("'")) > 1):
                                dict["O/U"].append(float(row[k].split("'")[0].split("u")[1]) + 0.5)
                            elif (len(row[k].split("’")) > 1):
                                dict["O/U"].append(float(row[k].split("’")[0].split("u")[1]) + 0.5)
                            else:
                                dict["O/U"].append(float(row[k].split("u")[1]))
                        elif (len(row[k].split("n")) > 1):
                            dict["O/U Outcome"].append("Push")
                            if (len(row[k].split("'")) > 1):
                                dict["O/U"].append(float(row[k].split("'")[0].split("n")[1]) + 0.5)
                            elif (len(row[k].split("’")) > 1):
                                dict["O/U"].append(float(row[k].split("’")[0].split("n")[1]) + 0.5)
                            else:
                                dict["O/U"].append(float(row[k].split("n")[1]))
                        else:
                            print (row)
                    j += 1

print (len(dict["Date"]))
print (len(dict["Home Team"]))
print (len(dict["Road Team"]))
print (len(dict["Neutral Field"]))
print (len(dict["Night Game"]))
print (len(dict["Postseason Game"]))
print (len(dict["Favorite"]))
print (len(dict["Spread"]))
print (len(dict["O/U"]))
print (len(dict["Home Score"]))
print (len(dict["Road Score"]))
print (len(dict["Spread Winner"]))
print (len(dict["O/U Outcome"]))
df = pd.DataFrame(dict)
df = df.sort_values(by=["Week"])
df.to_csv("./csv_Data/BettingResults/" + thisYear + ".csv")
