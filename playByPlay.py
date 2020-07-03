import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName
import CFBScrapy as cfb

years = []
weeks = []
cur = 2003
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
        cfb.get_play_by_play_data(year, week = w).to_csv("./csv_Data/playByPlay/" + str(year) + "_" + str(w) + ".csv")
