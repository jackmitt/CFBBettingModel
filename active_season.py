import pickle
import pandas as pd
import numpy as np
import bayesianModelFcns_active as bmf
from os.path import exists
import os
import pymc3 as pm
import theano.tensor as tt
import theano

def single_game_prediction(row, posteriors, teams_to_int, decimals = 5):
    precision = f".{decimals}f"
    game_pred = {"H_proj":[],"A_proj":[]}
    idₕ = teams_to_int[row["homeTeam"]]
    idₐ = teams_to_int[row["awayTeam"]]
    i_μ = posteriors["intercept"][0]
    i_σ = posteriors["intercept"][1]
    h_μ = posteriors["home"][0]
    h_σ = posteriors["home"][1]
    oₕ_μ = posteriors["offense"][0][idₕ]
    oₕ_σ = posteriors["offense"][1][idₕ]
    oₐ_μ = posteriors["offense"][0][idₐ]
    oₐ_σ = posteriors["offense"][1][idₐ]
    dₕ_μ = posteriors["defense"][0][idₕ]
    dₕ_σ = posteriors["defense"][1][idₕ]
    dₐ_μ = posteriors["defense"][0][idₐ]
    dₐ_σ = posteriors["defense"][1][idₐ]
    game_pred["H_proj"].append(i_μ + h_μ + oₕ_μ - dₐ_μ)
    game_pred["A_proj"].append(i_μ + oₐ_μ - dₕ_μ)
    return game_pred

def predict():
    with open("./csv_data/current/prior.pkl","rb") as inputFile:
        priors = pickle.load(inputFile)

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

    train = pd.read_csv("./csv_data/current/lines_week2.csv", encoding = "ISO-8859-1")

    games = {}
    for index, row in train.iterrows():
        try:
            cur_pred = single_game_prediction(row, priors, teams_to_int)
        except:
            continue
        games[(row["homeTeam"], row["awayTeam"])] = {"spread":row["spread"],"H_proj":cur_pred["H_proj"][0],"A_proj":cur_pred["A_proj"][0]}

    dict = {"Home":[],"Away":[],"Spread":[],"H_proj":[],"A_proj":[]}
    for key in games:
        dict["Home"].append(key[0])
        dict["Away"].append(key[1])
        dict["Spread"].append(games[key]["spread"])
        dict["H_proj"].append(games[key]["H_proj"])
        dict["A_proj"].append(games[key]["A_proj"])
        # if (abs(games[key]["A_proj"] - games[key]["H_proj"] - games[key]["spread"]) > 7):
        #     if (games[key]["A_proj"] - games[key]["H_proj"] < games[key]["spread"]):
        #         games[key]["Bet"] = key[0]
        #     else:
        #         games[key]["Bet"] = key[1]

    df = pd.DataFrame.from_dict(dict)
    df.to_csv("./csv_data/current/week1.csv", index = False)

def update():
    factor = 1.05                 # Expand the posteriors by this amount before using as priors -- old: 1.05
    f_thresh = 10         # A cap on team variable standard deviation to prevent blowup -- old: 0.075
    Δσ = 0.005               # The standard deviaton of the random walk variables -- old: 0.001

    if (not exists("./csv_data/current/prior.pkl")):
        with open("./csv_data/last_prior1.pkl","rb") as inputFile:
            priors = pickle.load(inputFile)
    else:
        with open("./csv_data/current/prior.pkl","rb") as inputFile:
            priors = pickle.load(inputFile)

    train = pd.read_csv("./csv_data/results.csv", encoding = "ISO-8859-1")
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

    train = pd.read_csv("./csv_data/current/results.csv", encoding = "ISO-8859-1")
    droprows = []
    for index, row in train.iterrows():
        if (row["home_points"] != row["home_points"] or row["home_team"] not in teams_to_int or row["away_team"] not in teams_to_int):
            droprows.append(index)
    train = train.drop(droprows)
    train = train.reset_index(drop=True)
    train = train.rename(columns={"home_points": "home_team_reg_score"})
    train = train.rename(columns={"away_points": "away_team_reg_score"})

    train = train.rename(columns={"home_team": "Home"})
    train = train.rename(columns={"away_team": "Away"})
    ihome = []
    iaway = []
    for index, row in train.iterrows():
        ihome.append(teams_to_int[row["Home"]])
        iaway.append(teams_to_int[row["Away"]])
    train["i_home"] = ihome
    train["i_away"] = iaway
    num_teams = len(teams_to_int.keys())
    print (train)

    oneIterComplete = False
    startIndex = 0
    for index, row in train.iterrows():
        if (index != 0 and (index == len(train.index) - 1 or row["week"] != train.at[index+1,"week"])):
            new_obs = train.iloc[startIndex:index+1]
    #
            home_team = theano.shared(new_obs.i_home.values)
            away_team = theano.shared(new_obs.i_away.values)
    #
            observed_home_pts = new_obs.home_team_reg_score.values
            observed_away_pts = new_obs.away_team_reg_score.values
    #
            posteriors = bmf.model_update(home_team, observed_home_pts, away_team, observed_away_pts, priors, num_teams, factor, f_thresh, Δσ)
    #
            priors = posteriors
    #
            startIndex = index+1
        with open("./csv_data/current/prior.pkl", "wb") as f:
            pickle.dump(priors, f)

predict()
