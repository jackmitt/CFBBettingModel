from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import json
import pandas as pd
import numpy as np

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'XBWTTfw3Jo8o/r/jmDnRA6SsnoHp0MKKPBEE0UGID/hPKqzKLV/+0Ljn06dCbQRS'
configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration))
game_id = 56 # int | Game id filter (optional)
year = 56 # int | Year/season filter for games (optional)
week = 56 # int | Week filter (optional)
season_type = 'regular' # str | Season type filter (regular or postseason) (optional) (default to regular)
team = 'team_example' # str | Team (optional)
home = 'home_example' # str | Home team filter (optional)
away = 'away_example' # str | Away team filter (optional)
conference = 'conference_example' # str | Conference abbreviation filter (optional)


for i in range(2001, 2021):
    dict = {}
    dict[str(i)] = []
    api_response = api_instance.get_advanced_team_game_stats(year=i)
    for a in api_response:
        dict[str(i)].append(a.offense["ppa"])
    print (i, np.average(dict[str(i)]))
