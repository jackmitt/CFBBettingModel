from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import pandas as pd
import numpy as np
from cfbFcns import standardizeTeamName


# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'XBWTTfw3Jo8o/r/jmDnRA6SsnoHp0MKKPBEE0UGID/hPKqzKLV/+0Ljn06dCbQRS'
configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration))
year = 2018 # int | Year/season filter for games (optional)
week = 1 # int | Week filter (optional)

api_response = api_instance.get_advanced_team_game_stats(year=year, week=week, season_type="regular")
dict = {}
dict["gameId"] = []
dict["week"] = []
dict["team"] = []
dict["opponent"] = []
for a in ["offense", "defense"]:
    dict[a + ".ppa"] = []
    dict[a + ".successRate"] = []
    dict[a + ".explosiveness"] = []
    dict[a + ".powerSuccess"] = []
    dict[a + ".stuffRate"] = []
    dict[a + ".secondLevelYards"] = []
    dict[a + ".openFieldYards"] = []
    dict[a + ".standardDowns.ppa"] = []
    dict[a + ".standardDowns.successRate"] = []
    dict[a + ".standardDowns.explosiveness"] = []
    dict[a + ".passingDowns.ppa"] = []
    dict[a + ".passingDowns.successRate"] = []
    dict[a + ".passingDowns.explosiveness"] = []
    dict[a + ".rushingPlays.ppa"] = []
    dict[a + ".rushingPlays.successRate"] = []
    dict[a + ".rushingPlays.explosiveness"] = []
    dict[a + ".passingPlays.ppa"] = []
    dict[a + ".passingPlays.successRate"] = []
    dict[a + ".passingPlays.explosiveness"] = []

for x in api_response:
    dict["gameId"].append(x.game_id)
    dict["week"].append(x.week)
    dict["team"].append(x.team)
    dict["opponent"].append(x.opponent)
    dict["offense" + ".ppa"].append(x.offense["ppa"])
    dict["offense" + ".successRate"].append(x.offense["successRate"])
    dict["offense" + ".explosiveness"].append(x.offense["explosiveness"])
    dict["offense" + ".powerSuccess"].append(x.offense["powerSuccess"])
    dict["offense" + ".stuffRate"].append(x.offense["stuffRate"])
    dict["offense" + ".secondLevelYards"].append(x.offense["secondLevelYards"])
    dict["offense" + ".openFieldYards"].append(x.offense["openFieldYards"])
    dict["offense" + ".standardDowns.ppa"].append(x.offense["standardDowns"]["ppa"])
    dict["offense" + ".standardDowns.successRate"].append(x.offense["standardDowns"]["successRate"])
    dict["offense" + ".standardDowns.explosiveness"].append(x.offense["standardDowns"]["explosiveness"])
    dict["offense" + ".passingDowns.ppa"].append(x.offense["passingDowns"]["ppa"])
    dict["offense" + ".passingDowns.successRate"].append(x.offense["passingDowns"]["successRate"])
    dict["offense" + ".passingDowns.explosiveness"].append(x.offense["passingDowns"]["explosiveness"])
    dict["offense" + ".rushingPlays.ppa"].append(x.offense["rushingPlays"]["ppa"])
    dict["offense" + ".rushingPlays.successRate"].append(x.offense["rushingPlays"]["successRate"])
    dict["offense" + ".rushingPlays.explosiveness"].append(x.offense["rushingPlays"]["explosiveness"])
    dict["offense" + ".passingPlays.ppa"].append(x.offense["passingPlays"]["ppa"])
    dict["offense" + ".passingPlays.successRate"].append(x.offense["passingPlays"]["successRate"])
    dict["offense" + ".passingPlays.explosiveness"].append(x.offense["passingPlays"]["explosiveness"])
    dict["defense" + ".ppa"].append(x.defense["ppa"])
    dict["defense" + ".successRate"].append(x.defense["successRate"])
    dict["defense" + ".explosiveness"].append(x.defense["explosiveness"])
    dict["defense" + ".powerSuccess"].append(x.defense["powerSuccess"])
    dict["defense" + ".stuffRate"].append(x.defense["stuffRate"])
    dict["defense" + ".secondLevelYards"].append(x.defense["secondLevelYards"])
    dict["defense" + ".openFieldYards"].append(x.defense["openFieldYards"])
    dict["defense" + ".standardDowns.ppa"].append(x.defense["standardDowns"]["ppa"])
    dict["defense" + ".standardDowns.successRate"].append(x.defense["standardDowns"]["successRate"])
    dict["defense" + ".standardDowns.explosiveness"].append(x.defense["standardDowns"]["explosiveness"])
    dict["defense" + ".passingDowns.ppa"].append(x.defense["passingDowns"]["ppa"])
    dict["defense" + ".passingDowns.successRate"].append(x.defense["passingDowns"]["successRate"])
    dict["defense" + ".passingDowns.explosiveness"].append(x.defense["passingDowns"]["explosiveness"])
    dict["defense" + ".rushingPlays.ppa"].append(x.defense["rushingPlays"]["ppa"])
    dict["defense" + ".rushingPlays.successRate"].append(x.defense["rushingPlays"]["successRate"])
    dict["defense" + ".rushingPlays.explosiveness"].append(x.defense["rushingPlays"]["explosiveness"])
    dict["defense" + ".passingPlays.ppa"].append(x.defense["passingPlays"]["ppa"])
    dict["defense" + ".passingPlays.successRate"].append(x.defense["passingPlays"]["successRate"])
    dict["defense" + ".passingPlays.explosiveness"].append(x.defense["passingPlays"]["explosiveness"])

dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv("./new_csv_Data/currentSeason/week" + str(week) + ".csv")
