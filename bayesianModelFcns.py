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

    #JUST REALIZED THIS WAS FUCKED UP IN THE SOLO PPA VERSION, NEED TO FIX BETA AND RUN IT AGAIN
    b_μ, b_σ = norm.fit(trace['beta_ppa'])
    posteriors['beta_ppa'] = [b_μ, b_σ]

    b_μ, b_σ = norm.fit(trace['beta_sr'])
    posteriors['beta_sr'] = [b_μ, b_σ]

    b_μ, b_σ = norm.fit(trace['beta_exp'])
    posteriors['beta_exp'] = [b_μ, b_σ]

    return posteriors

def fatten_priors(prev_posteriors, factor, f_thresh):
    priors = prev_posteriors.copy()
    priors['home'][1] = np.minimum(priors['home'][1] * factor, f_thresh)
    priors['intercept'][1] = np.minimum(priors['intercept'][1] * factor, f_thresh)
    priors['beta_ppa'][1] = np.minimum(priors['beta_ppa'][1] * factor, f_thresh)
    priors['beta_sr'][1] = np.minimum(priors['beta_sr'][1] * factor, f_thresh)
    priors['beta_exp'][1] = np.minimum(priors['beta_exp'][1] * factor, f_thresh)

    return priors


def model_iteration(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, stat_posteriors, samples=2000, tune=1000, cores=1):
    with pm.Model():

        # Global model parameters
        h = pm.Normal('home', mu=priors['home'][0], sigma=priors['home'][1])
        i = pm.Normal('intercept', mu=priors['intercept'][0], sigma=priors['intercept'][1])

        #coefficient for ppa
        b_ppa = pm.Normal('beta_ppa', mu=priors['beta_ppa'][0], sigma=priors['beta_ppa'][1])
        b_sr = pm.Normal('beta_sr', mu=priors['beta_sr'][0], sigma=priors['beta_sr'][1])
        b_exp = pm.Normal('beta_exp', mu=priors['beta_exp'][0], sigma=priors['beta_exp'][1])


        #formatting ppa
        o_ppa = pm.Normal('o_ppa', mu=stat_posteriors["o_ppa"][0], sigma=0.01, shape = n_teams)
        d_ppa = pm.Normal('d_ppa', mu=stat_posteriors["d_ppa"][0], sigma=0.01, shape = n_teams)

        o_sr = pm.Normal('o_sr', mu=stat_posteriors["o_sr"][0], sigma=0.01, shape = n_teams)
        d_sr = pm.Normal('d_sr', mu=stat_posteriors["d_sr"][0], sigma=0.01, shape = n_teams)

        o_exp = pm.Normal('o_exp', mu=stat_posteriors["o_exp"][0], sigma=0.01, shape = n_teams)
        d_exp = pm.Normal('d_exp', mu=stat_posteriors["d_exp"][0], sigma=0.01, shape = n_teams)

        μₕ = i + h + b_ppa*(o_ppa[idₕ] - d_ppa[idₐ]) + b_sr*(o_sr[idₕ] - d_sr[idₐ]) + b_exp*(o_exp[idₕ] - d_exp[idₐ])
        μₐ = i + b_ppa*(o_ppa[idₐ] - d_ppa[idₕ]) + b_sr*(o_sr[idₐ] - d_sr[idₕ]) + b_exp*(o_exp[idₐ] - d_exp[idₕ])

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
    h_μ = posteriors["home"][0]
    b_ppa_μ = posteriors["beta_ppa"][0]
    b_sr_μ = posteriors["beta_sr"][0]
    b_exp_μ = posteriors["beta_exp"][0]
    oₕ_ppa_μ = stat_posteriors["o_ppa"][0][idₕ]
    dₕ_ppa_μ = stat_posteriors["d_ppa"][0][idₕ]
    oₐ_ppa_μ = stat_posteriors["o_ppa"][0][idₐ]
    dₐ_ppa_μ = stat_posteriors["d_ppa"][0][idₐ]
    oₕ_sr_μ = stat_posteriors["o_sr"][0][idₕ]
    dₕ_sr_μ = stat_posteriors["d_sr"][0][idₕ]
    oₐ_sr_μ = stat_posteriors["o_sr"][0][idₐ]
    dₐ_sr_μ = stat_posteriors["d_sr"][0][idₐ]
    oₕ_exp_μ = stat_posteriors["o_exp"][0][idₕ]
    dₕ_exp_μ = stat_posteriors["d_exp"][0][idₕ]
    oₐ_exp_μ = stat_posteriors["o_exp"][0][idₐ]
    dₐ_exp_μ = stat_posteriors["d_exp"][0][idₐ]
    game_pred["H_proj"].append(i_μ + h_μ + b_ppa_μ*(oₕ_ppa_μ - dₐ_ppa_μ) + b_sr_μ*(oₕ_sr_μ - dₐ_sr_μ) + b_exp_μ*(oₕ_exp_μ - dₐ_exp_μ))
    #log_λₕ_σ = np.sqrt(i_σ ** 2 + h_σ ** 2 + oₕ_σ ** 2 + dₐ_σ ** 2)
    #log_μₐ_μ = i_μ + oₐ_μ - dₕ_μ
    #game_pred["A_proj"].append(np.exp(log_μₐ_μ))
    game_pred["A_proj"].append(i_μ + b_ppa_μ*(oₐ_ppa_μ - dₕ_ppa_μ) + b_sr_μ*(oₐ_sr_μ - dₕ_sr_μ) + b_exp_μ*(oₐ_exp_μ - dₕ_exp_μ))
    #log_λₐ_σ = np.sqrt(i_σ ** 2 + oₐ_σ ** 2 + dₕ_σ ** 2)
    return game_pred
