import pandas as pd
import numpy as np
import datetime
import pymc3 as pm
import theano.tensor as tt
import theano
from itertools import combinations
from scipy.stats import norm
from scipy.integrate import quad, dblquad
from math import factorial, exp, sqrt, pi

def get_model_posteriors(trace, n_teams):
    posteriors = {}
    h_μ, h_σ = norm.fit(trace['home'])
    posteriors['home'] = [h_μ, h_σ]
    i_μ, i_σ = norm.fit(trace['intercept'])
    posteriors['intercept'] = [i_μ, i_σ]
    b_μ, b_σ = norm.fit(trace['beta1'])
    posteriors['beta1'] = [i_μ, i_σ]

    return posteriors

def fatten_priors(prev_posteriors, factor, f_thresh):
    priors = prev_posteriors.copy()
    priors['home'][1] = np.minimum(priors['home'][1] * factor, f_thresh)
    priors['intercept'][1] = np.minimum(priors['intercept'][1] * factor, f_thresh)
    priors['beta1'][1] = np.minimum(priors['beta1'][1] * factor, f_thresh)

    return priors


def model_iteration(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, stat_posteriors, samples=2000, tune=1000, cores=1):
    with pm.Model():

        # Global model parameters
        h = pm.Normal('home', mu=priors['home'][0], sigma=priors['home'][1])
        i = pm.Normal('intercept', mu=priors['intercept'][0], sigma=priors['intercept'][1])

        #coefficient for ppa
        b = pm.Normal('beta1', mu=priors['beta1'][0], sigma=priors['beta1'][1])

        #formatting ppa
        o_ppa = pm.Normal('o_ppa', mu=stat_posteriors["offense"][0], sigma=0.01, shape = n_teams)
        d_ppa = pm.Normal('d_ppa', mu=stat_posteriors["defense"][0], sigma=0.01, shape = n_teams)

        μₕ = i + h + b*(o_ppa[idₕ] - d_ppa[idₐ])
        μₐ = i + b*(o_ppa[idₐ] - d_ppa[idₕ])

        # Likelihood of observed data
        sₕ = pm.Normal('sₕ', mu=μₕ, sigma=20, observed=sₕ_obs)
        sₐ = pm.Normal('sₐ', mu=μₐ, sigma=20, observed=sₐ_obs)

        trace = pm.sample(
            samples,
            tune=tune,
            chains=3,
            cores=cores,
            progressbar=True,
            return_inferencedata=False
        )

        posteriors = get_model_posteriors(trace, n_teams)

        return posteriors

def model_update(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, stat_posteriors):
    priors = fatten_priors(priors, 1, 20)
    posteriors = model_iteration(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, stat_posteriors)

    return posteriors

def single_game_prediction(row, posteriors, stat_posteriors, teams_to_int, decimals = 5):
    precision = f".{decimals}f"
    game_pred = {"H_proj":[],"A_proj":[]}
    idₕ = teams_to_int[row["Home"]]
    idₐ = teams_to_int[row["Away"]]
    i_μ = posteriors["intercept"][0]
    i_σ = posteriors["intercept"][1]
    h_μ = posteriors["home"][0]
    h_σ = posteriors["home"][1]
    b_μ = posteriors["beta1"][0]
    b_σ = posteriors["beta1"][1]
    oₕ_μ = stat_posteriors["offense"][0][idₕ]
    dₕ_μ = stat_posteriors["defense"][0][idₕ]
    oₐ_μ = stat_posteriors["offense"][0][idₐ]
    dₐ_μ = stat_posteriors["defense"][0][idₐ]
    game_pred["H_proj"].append(i_μ + h_μ + b_μ*(oₕ_μ - dₐ_μ))
    #log_λₕ_σ = np.sqrt(i_σ ** 2 + h_σ ** 2 + oₕ_σ ** 2 + dₐ_σ ** 2)
    #log_μₐ_μ = i_μ + oₐ_μ - dₕ_μ
    #game_pred["A_proj"].append(np.exp(log_μₐ_μ))
    game_pred["A_proj"].append(i_μ + b_μ*(oₐ_μ - dₕ_μ))
    #log_λₐ_σ = np.sqrt(i_σ ** 2 + oₐ_σ ** 2 + dₕ_σ ** 2)
    return game_pred
