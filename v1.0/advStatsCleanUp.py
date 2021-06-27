import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName

#creates forward looking adv stats file for a given year using normal adv stats game file

years = []
cur = 2014
for i in range(6):
    years.append(str(cur))
    cur += 1

def avg(arr):
    if (len(arr) > 0):
        return sum(arr)/len(arr)
    return np.nan

for year in years:
    df = pd.read_csv('./new_csv_data/advStatsGame/' + year + '.csv', encoding = "ISO-8859-1")
    dropRows = []
    for index, row in df.iterrows():
        if (index > 0 and row["gameId"] == df.at[index-1,"gameId"]):
            dropRows.append(index)
    df = df.drop(dropRows)
    dict = {"Week":[],"Team":[],"Offense":{},"Defense":{}}
    subDictOff = {"Ppa":[],"Sr":[],"Exp":[],"PwrS":[],"Stuff":[],"SecLevel":[],"OpenField":[],"StDownPpa":[],"StDownSr":[],"StDownExp":[],"PassDownPpa":[],"PassDownSr":[],"PassDownExp":[],"RushPpa":[],"RushSr":[],"RushExp":[],"PassPpa":[],"PassSr":[],"PassExp":[]}
    subDictDef = {"Ppa":[],"Sr":[],"Exp":[],"PwrS":[],"Stuff":[],"SecLevel":[],"OpenField":[],"StDownPpa":[],"StDownSr":[],"StDownExp":[],"PassDownPpa":[],"PassDownSr":[],"PassDownExp":[],"RushPpa":[],"RushSr":[],"RushExp":[],"PassPpa":[],"PassSr":[],"PassExp":[]}
    for index, row in df.iterrows():
        dict["Week"].append(row["week"])
        dict["Team"].append(standardizeTeamName(row["team"], False))
        dict["Week"].append(row["week"])
        dict["Team"].append(standardizeTeamName(row["opponent"], False))
        #Offense
        subDictOff["Ppa"].append(row["offense.ppa"])
        subDictDef["Ppa"].append(row["defense.ppa"])
        subDictOff["Ppa"].append(row["defense.ppa"])
        subDictDef["Ppa"].append(row["offense.ppa"])

        subDictOff["Sr"].append(row["offense.successRate"])
        subDictDef["Sr"].append(row["defense.successRate"])
        subDictOff["Sr"].append(row["defense.successRate"])
        subDictDef["Sr"].append(row["offense.successRate"])

        subDictOff["Exp"].append(row["offense.explosiveness"])
        subDictDef["Exp"].append(row["defense.explosiveness"])
        subDictOff["Exp"].append(row["defense.explosiveness"])
        subDictDef["Exp"].append(row["offense.explosiveness"])

        subDictOff["PwrS"].append(row["offense.powerSuccess"])
        subDictDef["PwrS"].append(row["defense.powerSuccess"])
        subDictOff["PwrS"].append(row["defense.powerSuccess"])
        subDictDef["PwrS"].append(row["offense.powerSuccess"])

        subDictOff["Stuff"].append(row["offense.stuffRate"])
        subDictDef["Stuff"].append(row["defense.stuffRate"])
        subDictOff["Stuff"].append(row["defense.stuffRate"])
        subDictDef["Stuff"].append(row["offense.stuffRate"])

        subDictOff["SecLevel"].append(row["offense.secondLevelYards"])
        subDictDef["SecLevel"].append(row["defense.secondLevelYards"])
        subDictOff["SecLevel"].append(row["defense.secondLevelYards"])
        subDictDef["SecLevel"].append(row["offense.secondLevelYards"])

        subDictOff["OpenField"].append(row["offense.openFieldYards"])
        subDictDef["OpenField"].append(row["defense.openFieldYards"])
        subDictOff["OpenField"].append(row["defense.openFieldYards"])
        subDictDef["OpenField"].append(row["offense.openFieldYards"])

        subDictOff["StDownPpa"].append(row["offense.standardDowns.ppa"])
        subDictDef["StDownPpa"].append(row["defense.standardDowns.ppa"])
        subDictOff["StDownPpa"].append(row["defense.standardDowns.ppa"])
        subDictDef["StDownPpa"].append(row["offense.standardDowns.ppa"])

        subDictOff["StDownSr"].append(row["offense.standardDowns.successRate"])
        subDictDef["StDownSr"].append(row["defense.standardDowns.successRate"])
        subDictOff["StDownSr"].append(row["defense.standardDowns.successRate"])
        subDictDef["StDownSr"].append(row["offense.standardDowns.successRate"])

        subDictOff["StDownExp"].append(row["offense.standardDowns.explosiveness"])
        subDictDef["StDownExp"].append(row["defense.standardDowns.explosiveness"])
        subDictOff["StDownExp"].append(row["defense.standardDowns.explosiveness"])
        subDictDef["StDownExp"].append(row["offense.standardDowns.explosiveness"])

        subDictOff["PassDownPpa"].append(row["offense.passingDowns.ppa"])
        subDictDef["PassDownPpa"].append(row["defense.passingDowns.ppa"])
        subDictOff["PassDownPpa"].append(row["defense.passingDowns.ppa"])
        subDictDef["PassDownPpa"].append(row["offense.passingDowns.ppa"])

        subDictOff["PassDownSr"].append(row["offense.passingDowns.successRate"])
        subDictDef["PassDownSr"].append(row["defense.passingDowns.successRate"])
        subDictOff["PassDownSr"].append(row["defense.passingDowns.successRate"])
        subDictDef["PassDownSr"].append(row["offense.passingDowns.successRate"])

        subDictOff["PassDownExp"].append(row["offense.passingDowns.explosiveness"])
        subDictDef["PassDownExp"].append(row["defense.passingDowns.explosiveness"])
        subDictOff["PassDownExp"].append(row["defense.passingDowns.explosiveness"])
        subDictDef["PassDownExp"].append(row["offense.passingDowns.explosiveness"])

        subDictOff["RushPpa"].append(row["offense.rushingPlays.ppa"])
        subDictDef["RushPpa"].append(row["defense.rushingPlays.ppa"])
        subDictOff["RushPpa"].append(row["defense.rushingPlays.ppa"])
        subDictDef["RushPpa"].append(row["offense.rushingPlays.ppa"])

        subDictOff["RushSr"].append(row["offense.rushingPlays.successRate"])
        subDictDef["RushSr"].append(row["defense.rushingPlays.successRate"])
        subDictOff["RushSr"].append(row["defense.rushingPlays.successRate"])
        subDictDef["RushSr"].append(row["offense.rushingPlays.successRate"])

        subDictOff["RushExp"].append(row["offense.rushingPlays.explosiveness"])
        subDictDef["RushExp"].append(row["defense.rushingPlays.explosiveness"])
        subDictOff["RushExp"].append(row["defense.rushingPlays.explosiveness"])
        subDictDef["RushExp"].append(row["offense.rushingPlays.explosiveness"])

        subDictOff["PassPpa"].append(row["offense.passingPlays.ppa"])
        subDictDef["PassPpa"].append(row["defense.passingPlays.ppa"])
        subDictOff["PassPpa"].append(row["defense.passingPlays.ppa"])
        subDictDef["PassPpa"].append(row["offense.passingPlays.ppa"])

        subDictOff["PassSr"].append(row["offense.passingPlays.successRate"])
        subDictDef["PassSr"].append(row["defense.passingPlays.successRate"])
        subDictOff["PassSr"].append(row["defense.passingPlays.successRate"])
        subDictDef["PassSr"].append(row["offense.passingPlays.successRate"])

        subDictOff["PassExp"].append(row["offense.passingPlays.explosiveness"])
        subDictDef["PassExp"].append(row["defense.passingPlays.explosiveness"])
        subDictOff["PassExp"].append(row["defense.passingPlays.explosiveness"])
        subDictDef["PassExp"].append(row["offense.passingPlays.explosiveness"])
    dict["Offense"] = subDictOff
    dict["Defense"] = subDictDef
    #Forward looking week - week 1 stats are entered as week 2, week 1 and 2 stats averaged for week 3 and so on so that week matches up with predicting spreads
    final = {"Week":[],"Team":[],"oPpa":[],"oSr":[],"oExp":[],"oPwrS":[],"oStuff":[],"oSecLevel":[],"oOpenField":[],"oStDownPpa":[],"oStDownSr":[],"oStDownExp":[],"oPassDownPpa":[],"oPassDownSr":[],"oPassDownExp":[],"oRushPpa":[],"oRushSr":[],"oRushExp":[],"oPassPpa":[],"oPassSr":[],"oPassExp":[],"dPpa":[],"dSr":[],"dExp":[],"dPwrS":[],"dStuff":[],"dSecLevel":[],"dOpenField":[],"dStDownPpa":[],"dStDownSr":[],"dStDownExp":[],"dPassDownPpa":[],"dPassDownSr":[],"dPassDownExp":[],"dRushPpa":[],"dRushSr":[],"dRushExp":[],"dPassPpa":[],"dPassSr":[],"dPassExp":[]}
    for i in range(len(dict["Team"])):
        week = int(dict["Week"][i])
        team = dict["Team"][i]
        if (week != 99):
            final["Week"].append(week+1)
        else:
            final["Week"].append("Year End")
        final["Team"].append(team)
        dPpa = []
        dSr = []
        dExp = []
        dPwrS = []
        dStuff = []
        dSecLevel = []
        dOpenField = []
        dStDownPpa = []
        dStDownSr = []
        dStDownExp = []
        dPassDownPpa = []
        dPassDownSr = []
        dPassDownExp = []
        dRushPpa = []
        dRushSr = []
        dRushExp = []
        dPassPpa = []
        dPassSr = []
        dPassExp = []
        oPpa = []
        oSr = []
        oExp = []
        oPwrS = []
        oStuff = []
        oSecLevel = []
        oOpenField = []
        oStDownPpa = []
        oStDownSr = []
        oStDownExp = []
        oPassDownPpa = []
        oPassDownSr = []
        oPassDownExp = []
        oRushPpa = []
        oRushSr = []
        oRushExp = []
        oPassPpa = []
        oPassSr = []
        oPassExp = []
        k = 0
        while (k < len(dict["Week"]) and int(dict["Week"][k]) <= week):
            if (team == dict["Team"][k]):
                oPpa.append(float(dict["Offense"]["Ppa"][k]))
                oSr.append(float(dict["Offense"]["Sr"][k]))
                oExp.append(float(dict["Offense"]["Exp"][k]))
                oPwrS.append(float(dict["Offense"]["PwrS"][k]))
                oStuff.append(float(dict["Offense"]["Stuff"][k]))
                oSecLevel.append(float(dict["Offense"]["SecLevel"][k]))
                oOpenField.append(float(dict["Offense"]["OpenField"][k]))
                oStDownPpa.append(float(dict["Offense"]["StDownPpa"][k]))
                oStDownSr.append(float(dict["Offense"]["StDownSr"][k]))
                oStDownExp.append(float(dict["Offense"]["StDownExp"][k]))
                oPassDownPpa.append(float(dict["Offense"]["PassDownPpa"][k]))
                oPassDownSr.append(float(dict["Offense"]["PassDownSr"][k]))
                oPassDownExp.append(float(dict["Offense"]["PassDownExp"][k]))
                oRushPpa.append(float(dict["Offense"]["RushPpa"][k]))
                oRushSr.append(float(dict["Offense"]["RushSr"][k]))
                oRushExp.append(float(dict["Offense"]["RushExp"][k]))
                oPassPpa.append(float(dict["Offense"]["PassPpa"][k]))
                oPassSr.append(float(dict["Offense"]["PassSr"][k]))
                oPassExp.append(float(dict["Offense"]["PassExp"][k]))
                dPpa.append(float(dict["Defense"]["Ppa"][k]))
                dSr.append(float(dict["Defense"]["Sr"][k]))
                dExp.append(float(dict["Defense"]["Exp"][k]))
                dPwrS.append(float(dict["Defense"]["PwrS"][k]))
                dStuff.append(float(dict["Defense"]["Stuff"][k]))
                dSecLevel.append(float(dict["Defense"]["SecLevel"][k]))
                dOpenField.append(float(dict["Defense"]["OpenField"][k]))
                dStDownPpa.append(float(dict["Defense"]["StDownPpa"][k]))
                dStDownSr.append(float(dict["Defense"]["StDownSr"][k]))
                dStDownExp.append(float(dict["Defense"]["StDownExp"][k]))
                dPassDownPpa.append(float(dict["Defense"]["PassDownPpa"][k]))
                dPassDownSr.append(float(dict["Defense"]["PassDownSr"][k]))
                dPassDownExp.append(float(dict["Defense"]["PassDownExp"][k]))
                dRushPpa.append(float(dict["Defense"]["RushPpa"][k]))
                dRushSr.append(float(dict["Defense"]["RushSr"][k]))
                dRushExp.append(float(dict["Defense"]["RushExp"][k]))
                dPassPpa.append(float(dict["Defense"]["PassPpa"][k]))
                dPassSr.append(float(dict["Defense"]["PassSr"][k]))
                dPassExp.append(float(dict["Defense"]["PassExp"][k]))
            k += 1
        copy = oPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPpa"].append(avg(adj))
        copy = oSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oSr"].append(avg(adj))
        copy = oExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oExp"].append(avg(adj))
        copy = oPwrS
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPwrS"].append(avg(adj))
        copy = oStuff
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oStuff"].append(avg(adj))
        copy = oSecLevel
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oSecLevel"].append(avg(adj))
        copy = oOpenField
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oOpenField"].append(avg(adj))
        copy = oStDownPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oStDownPpa"].append(avg(adj))
        copy = oStDownSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oStDownSr"].append(avg(adj))
        copy = oStDownExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oStDownExp"].append(avg(adj))
        copy = oPassDownPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPassDownPpa"].append(avg(adj))
        copy = oPassDownSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPassDownSr"].append(avg(adj))
        copy = oPassDownExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPassDownExp"].append(avg(adj))
        copy = oRushPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oRushPpa"].append(avg(adj))
        copy = oRushSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oRushSr"].append(avg(adj))
        copy = oRushExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oRushExp"].append(avg(adj))
        copy = oPassPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPassPpa"].append(avg(adj))
        copy = oPassSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPassSr"].append(avg(adj))
        copy = oPassExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["oPassExp"].append(avg(adj))
        copy = dPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPpa"].append(avg(adj))
        copy = dSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dSr"].append(avg(adj))
        copy = dExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dExp"].append(avg(adj))
        copy = dPwrS
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPwrS"].append(avg(adj))
        copy = dStuff
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dStuff"].append(avg(adj))
        copy = dSecLevel
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dSecLevel"].append(avg(adj))
        copy = dOpenField
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dOpenField"].append(avg(adj))
        copy = dStDownPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dStDownPpa"].append(avg(adj))
        copy = dStDownSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dStDownSr"].append(avg(adj))
        copy = dStDownExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dStDownExp"].append(avg(adj))
        copy = dPassDownPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPassDownPpa"].append(avg(adj))
        copy = dPassDownSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPassDownSr"].append(avg(adj))
        copy = dPassDownExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPassDownExp"].append(avg(adj))
        copy = dRushPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dRushPpa"].append(avg(adj))
        copy = dRushSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dRushSr"].append(avg(adj))
        copy = dRushExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dRushExp"].append(avg(adj))
        copy = dPassPpa
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPassPpa"].append(avg(adj))
        copy = dPassSr
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPassSr"].append(avg(adj))
        copy = dPassExp
        adj = []
        for z in range(len(copy)):
            if (not np.isnan(copy[z])):
                adj.append(copy[z])
        final["dPassExp"].append(avg(adj))
    dfFinal = pd.DataFrame.from_dict(final)
    #print (dfFinal)
    dfFinal.to_csv("./new_csv_Data/advStatsFwdLooking/" + year + ".csv")
