from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import json
import pandas as pd
import numpy as np
from helpers import Database


def preMatchAverages():
    # Configure API key authorization: ApiKeyAuth
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = 'XBWTTfw3Jo8o/r/jmDnRA6SsnoHp0MKKPBEE0UGID/hPKqzKLV/+0Ljn06dCbQRS'
    configuration.api_key_prefix['Authorization'] = 'Bearer'

    # create an instance of the API class
    api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration))
    games_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

    adv_stats_map = {"ppa":"ppa","sr":"successRate","exp":"explosiveness","pwr":"powerSuccess","stuff":"stuffRate","line":"lineYards","second":"secondLevelYards","open":"openFieldYards"}
    mini_adv_stats_map = {"ppa":"ppa","sr":"successRate","exp":"explosiveness"}

    A = Database(["Year","Week","Home","Away","Neutral","Home Score","Away Score","H_o_ppa","H_d_ppa","H_o_sr","H_d_sr","H_o_exp","H_d_exp","H_o_pwr","H_d_pwr","H_o_stuff","H_d_stuff","H_o_line","H_d_line","H_o_second","H_d_second","H_o_open","H_d_open","H_o_std_ppa","H_d_std_ppa","H_o_std_sr","H_d_std_sr","H_o_std_exp","H_d_std_exp","H_o_passdown_ppa","H_d_passdown_ppa","H_o_passdown_sr","H_d_passdown_sr","H_o_passdown_exp","H_d_passdown_exp","H_o_rush_ppa","H_d_rush_ppa","H_o_rush_sr","H_d_rush_sr","H_o_rush_exp","H_d_rush_exp","H_o_passplay_ppa","H_d_passplay_ppa","H_o_passplay_sr","H_d_passplay_sr","H_o_passplay_exp","H_d_passplay_exp","H_pen_yards","H_o_fum_to_rush","H_d_fum_to_rush","H_o_int_to_pass","H_d_int_to_pass","A_o_ppa","A_d_ppa","A_o_sr","A_d_sr","A_o_exp","A_d_exp","A_o_pwr","A_d_pwr","A_o_stuff","A_d_stuff","A_o_line","A_d_line","A_o_second","A_d_second","A_o_open","A_d_open","A_o_std_ppa","A_d_std_ppa","A_o_std_sr","A_d_std_sr","A_o_std_exp","A_d_std_exp","A_o_passdown_ppa","A_d_passdown_ppa","A_o_passdown_sr","A_d_passdown_sr","A_o_passdown_exp","A_d_passdown_exp","A_o_rush_ppa","A_d_rush_ppa","A_o_rush_sr","A_d_rush_sr","A_o_rush_exp","A_d_rush_exp","A_o_passplay_ppa","A_d_passplay_ppa","A_o_passplay_sr","A_d_passplay_sr","A_o_passplay_exp","A_d_passplay_exp","A_pen_yards","A_o_fum_to_rush","A_d_fum_to_rush","A_o_int_to_pass","A_d_int_to_pass"])


    for year in range(2015, 2022):
        seasonDict = {}
        for week in range(1, 17):
            cur_adv_stats = api_instance.get_advanced_team_game_stats(year=year,week=week,season_type='regular',exclude_garbage_time=True)
            cur_std_stats = games_instance.get_team_game_stats(year=year,week=week,season_type='regular')
            homeTeam = True
            for team in cur_adv_stats:
                if (team.team not in seasonDict):
                    seasonDict[team.team] = {"priors":{},"o_ppa":[],"d_ppa":[],"o_sr":[],"d_sr":[],"o_exp":[],"d_exp":[],"o_pwr":[],"d_pwr":[],"o_stuff":[],"d_stuff":[],"o_line":[],"d_line":[],"o_second":[],"d_second":[],"o_open":[],"d_open":[],"o_std_ppa":[],"d_std_ppa":[],"o_std_sr":[],"d_std_sr":[],"o_std_exp":[],"d_std_exp":[],"o_passdown_ppa":[],"d_passdown_ppa":[],"o_passdown_sr":[],"d_passdown_sr":[],"o_passdown_exp":[],"d_passdown_exp":[],"o_rush_ppa":[],"d_rush_ppa":[],"o_rush_sr":[],"d_rush_sr":[],"o_rush_exp":[],"d_rush_exp":[],"o_passplay_ppa":[],"d_passplay_ppa":[],"o_passplay_sr":[],"d_passplay_sr":[],"o_passplay_exp":[],"d_passplay_exp":[],"pen_yards":[],"o_fum":0,"d_fum":0,"o_rushes":0,"d_rushes":0,"o_int":0,"d_int":0,"o_passes":0,"d_passes":0}
                if (team.opponent not in seasonDict):
                    seasonDict[team.opponent] = {"priors":{},"o_ppa":[],"d_ppa":[],"o_sr":[],"d_sr":[],"o_exp":[],"d_exp":[],"o_pwr":[],"d_pwr":[],"o_stuff":[],"d_stuff":[],"o_line":[],"d_line":[],"o_second":[],"d_second":[],"o_open":[],"d_open":[],"o_std_ppa":[],"d_std_ppa":[],"o_std_sr":[],"d_std_sr":[],"o_std_exp":[],"d_std_exp":[],"o_passdown_ppa":[],"d_passdown_ppa":[],"o_passdown_sr":[],"d_passdown_sr":[],"o_passdown_exp":[],"d_passdown_exp":[],"o_rush_ppa":[],"d_rush_ppa":[],"o_rush_sr":[],"d_rush_sr":[],"o_rush_exp":[],"d_rush_exp":[],"o_passplay_ppa":[],"d_passplay_ppa":[],"o_passplay_sr":[],"d_passplay_sr":[],"o_passplay_exp":[],"d_passplay_exp":[],"pen_yards":[],"o_fum":0,"d_fum":0,"o_rushes":0,"d_rushes":0,"o_int":0,"d_int":0,"o_passes":0,"d_passes":0}
                    # pri_year_adv = api_instance.get_advanced_team_season_stats(year=year-1,team=team.team)
                    # pri_year_std = api_instance.get_team_season_stats(year=year-1,team=team.team)
                    # for key in adv_stats_map:
                    #     seasonDict[team.team]["priors"]["o_" + key] = pri_year_adv[0].offense[adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["d_" + key] = pri_year_adv[0].defense[adv_stats_map[key]]
                    # for key in mini_adv_stats_map:
                    #     seasonDict[team.team]["priors"]["o_std_" + key] = pri_year_adv[0].offense["standardDowns"][mini_adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["d_std_" + key] = pri_year_adv[0].defense["standardDowns"][mini_adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["o_passdown_" + key] = pri_year_adv[0].offense["passingDowns"][mini_adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["d_passdown_" + key] = pri_year_adv[0].defense["passingDowns"][mini_adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["o_rush_" + key] = pri_year_adv[0].offense["standardDowns"][mini_adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["d_rush_" + key] = pri_year_adv[0].defense["standardDowns"][mini_adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["o_passplay_" + key] = pri_year_adv[0].offense["rushingPlays"][mini_adv_stats_map[key]]
                    #     seasonDict[team.team]["priors"]["d_passplay_" + key] = pri_year_adv[0].defense["passingPlays"][mini_adv_stats_map[key]]
                    #seasonDict[team.team]["priors"]["pen_yards"] = pri_year_std
                    # for stat in pri_year_std:
                    #     if (stat.stat_name == "")
                # if (homeTeam):
                #     this_game = games_instance.get_games(year=year,id=team.game_id)
                #     A.addCellToRow(year)
                #     A.addCellToRow(week)
                #     A.addCellToRow(this_game.home_team)
                #     A.addCellToRow(this_game.away_team)
                #     A.addCellToRow(this_game.neutral_site)
                #     A.addCellToRow(this_game.home_points)
                #     A.addCellToRow(this_game.away_points)


                for key in adv_stats_map:
                    seasonDict[team.team]["o_" + key].append(team.offense[adv_stats_map[key]])
                    seasonDict[team.team]["d_" + key].append(team.defense[adv_stats_map[key]])
                for key in mini_adv_stats_map:
                    seasonDict[team.team]["o_std_" + key].append(team.offense["standardDowns"][mini_adv_stats_map[key]])
                    seasonDict[team.team]["d_std_" + key].append(team.defense["standardDowns"][mini_adv_stats_map[key]])
                    seasonDict[team.team]["o_passdown_" + key].append(team.offense["passingDowns"][mini_adv_stats_map[key]])
                    seasonDict[team.team]["d_passdown_" + key].append(team.defense["passingDowns"][mini_adv_stats_map[key]])
                    seasonDict[team.team]["o_rush_" + key].append(team.offense["standardDowns"][mini_adv_stats_map[key]])
                    seasonDict[team.team]["d_rush_" + key].append(team.defense["standardDowns"][mini_adv_stats_map[key]])
                    seasonDict[team.team]["o_passplay_" + key].append(team.offense["rushingPlays"][mini_adv_stats_map[key]])
                    seasonDict[team.team]["d_passplay_" + key].append(team.defense["passingPlays"][mini_adv_stats_map[key]])
                for game in cur_std_stats:
                    if (game.id == team.game_id):
                        for cat in game.teams[0]["stats"]:
                            if (cat["category"] == "fumblesRecovered" or cat["category"] == "fumblesLost"):
                                seasonDict[game.teams[0]["school"]]["o_fum"] += int(cat["stat"])
                                seasonDict[game.teams[1]["school"]]["d_fum"] += int(cat["stat"])
                            elif (cat["category"] == "rushingAttempts"):
                                seasonDict[game.teams[0]["school"]]["o_rushes"] += int(cat["stat"])
                                seasonDict[game.teams[1]["school"]]["d_rushes"] += int(cat["stat"])
                            elif (cat["category"] == "interceptions"):
                                seasonDict[game.teams[0]["school"]]["o_int"] += int(cat["stat"])
                                seasonDict[game.teams[1]["school"]]["d_int"] += int(cat["stat"])
                            elif (cat["category"] == "completionAttempts"):
                                seasonDict[game.teams[0]["school"]]["o_passes"] += int(cat["stat"].split("-")[1])
                                seasonDict[game.teams[1]["school"]]["d_passes"] += int(cat["stat"].split("-")[1])
                            elif (cat["category"] == "totalPenaltiesYards"):
                                seasonDict[game.teams[0]["school"]]["pen_yards"].append(int(cat["stat"].split("-")[1]))
                        for cat in game.teams[1]["stats"]:
                           if (cat["category"] == "fumblesRecovered" or cat["category"] == "fumblesLost"):
                               seasonDict[game.teams[1]["school"]]["o_fum"] += int(cat["stat"])
                               seasonDict[game.teams[0]["school"]]["d_fum"] += int(cat["stat"])
                           elif (cat["category"] == "rushingAttempts"):
                               seasonDict[game.teams[1]["school"]]["o_rushes"] += int(cat["stat"])
                               seasonDict[game.teams[0]["school"]]["d_rushes"] += int(cat["stat"])
                           elif (cat["category"] == "interceptions"):
                               seasonDict[game.teams[1]["school"]]["o_int"] += int(cat["stat"])
                               seasonDict[game.teams[0]["school"]]["d_int"] += int(cat["stat"])
                           elif (cat["category"] == "completionAttempts"):
                               seasonDict[game.teams[1]["school"]]["o_passes"] += int(cat["stat"].split("-")[1])
                               seasonDict[game.teams[0]["school"]]["d_passes"] += int(cat["stat"].split("-")[1])
                           elif (cat["category"] == "totalPenaltiesYards"):
                               seasonDict[game.teams[1]["school"]]["pen_yards"].append(int(cat["stat"].split("-")[1]))
            print (seasonDict)
