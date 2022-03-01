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

dict = {}
dict["Year"] = []
dict["Ppa"] = []


years = [2014, 2015, 2016, 2017, 2018, 2019, 2021]
for year in years:
    print (year)
    # create an instance of the API class
    api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration)) # int | Year/season filter for games (optional)
    api_response = api_instance.get_advanced_team_game_stats(year=year, season_type="regular")

    for x in api_response:
        dict["Year"].append(year)
        dict["Ppa"].append(x.offense["ppa"])


dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv("./new_csv_Data/aaaappatest.csv")
