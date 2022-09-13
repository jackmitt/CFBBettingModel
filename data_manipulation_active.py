from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import json
import pandas as pd
import numpy as np
from helpers import Database
from os import listdir
import pymc3 as pm
import theano.tensor as tt
import theano
import datetime
from itertools import combinations
from scipy.stats import norm
import bayesianModelFcns as bmf
import pickle


def bayesian():
    factor = 1.05                 # Expand the posteriors by this amount before using as priors -- old: 1.05
    f_thresh = 10         # A cap on team variable standard deviation to prevent blowup -- old: 0.075
    Δσ = 0.005               # The standard deviaton of the random walk variables -- old: 0.001

    train = pd.read_csv("./csv_data/results.csv", encoding = "ISO-8859-1")
    finalDict = {}
    train = train.rename(columns={"homeScore": "home_team_reg_score"})
    train = train.rename(columns={"awayScore": "away_team_reg_score"})
    allTeams = []
    for index, row in train.iterrows():
        if (row["homeTeam"] not in allTeams):
            allTeams.append(row["homeTeam"])
        if (row["awayTeam"] not in allTeams):
            allTeams.append(row["awayTeam"])
    teams = np.sort(allTeams)
    teams = pd.DataFrame(teams, columns=["team"])
    teams["i"] = teams.index

    train = train.rename(columns={"homeTeam": "Home"})
    train = train.rename(columns={"awayTeam": "Away"})

    teams_to_int = {}
    for index, row in teams.iterrows():
        teams_to_int[row["team"]] = row["i"]
    #
    all_teams_pair_combinations = combinations(teams['team'], 2)
    team_pairs_dict = {}
    team_pairs_heads_dict = {}
    pair_index = 0
    for pair in all_teams_pair_combinations:
        team_pairs_dict[(pair[0], pair[1])] = pair_index
        team_pairs_dict[(pair[1], pair[0])] = pair_index
        team_pairs_heads_dict[(pair[0], pair[1])] = pair[0]
        team_pairs_heads_dict[(pair[1], pair[0])] = pair[0]
        pair_index += 1
    #
    train = train.merge(teams, left_on='Home', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_home'}).drop('team', axis=1)
    train = train.merge(teams, left_on='Away', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_away'}).drop('team', axis=1)
    train['i_pair'] = train.apply(lambda row: team_pairs_dict[(row['Home'], row['Away'])], axis=1)


    for col in train.columns:
        finalDict[col] = []
    for col in ["H_proj","A_proj"]:
        finalDict[col] = []
    #
    #
    num_teams = len(teams.index)
    priors = {"home":[0,f_thresh],"intercept":[0,f_thresh],"offense":[[],[]],"defense":[[],[]]}
    for i in range(num_teams):
        priors["offense"][0].append(0)
        priors["offense"][1].append(f_thresh)
        priors["defense"][0].append(0)
        priors["defense"][1].append(f_thresh)
    #
    oneIterComplete = False
    startIndex = 0
    for index, row in train.iterrows():
        for col in train.columns:
            finalDict[col].append(row[col])
        if (index != 0 and (row["week"] != train.at[index+1,"week"] or index == len(train.index) - 1)):
            new_obs = train.iloc[startIndex:index+1]
    #
            home_team = theano.shared(new_obs.i_home.values)
            away_team = theano.shared(new_obs.i_away.values)
            team_pair = theano.shared(new_obs.i_pair.values)
    #
            observed_home_pts = new_obs.home_team_reg_score.values
            observed_away_pts = new_obs.away_team_reg_score.values
    #
            posteriors = bmf.model_update(home_team, observed_home_pts, away_team, observed_away_pts, priors, num_teams, factor, f_thresh, Δσ)
    #
            priors = posteriors
    #
            startIndex = index+1
            oneIterComplete = True
        if (oneIterComplete):
            curPred = bmf.single_game_prediction(row, posteriors, teams_to_int, decimals = 5)
            for key in curPred:
                finalDict[key].append(curPred[key][0])
        else:
            for col in ["H_proj","A_proj"]:
                finalDict[col].append(np.nan)
        tempDF = pd.DataFrame.from_dict(finalDict)
        tempDF.to_csv("./csv_data/bayes_predictions.csv", index = False)
        with open("./csv_data/last_prior.pkl", "wb") as f:
            pickle.dump(priors, f)
