import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
import CFBScrapy as cfb

years = []
weeks = []
cur = 2004
while (cur <= 2019):
    years.append(cur)
    cur += 1
cur = 1
while (cur <= 20):
    weeks.append(cur)
    cur += 1

for year in years:
    for w in weeks:
        print (year, w,"-----------------------------------------------------------------------------------")
        try:
            cfb.get_game_team_stats(year, week = w).to_csv("./csv_Data/teamGameStats/" + str(year) + "_" + str(w) + ".csv")
        except:
            pass
