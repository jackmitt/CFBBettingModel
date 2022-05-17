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
    o_μ = []
    o_σ = []
    d_μ = []
    d_σ = []
    for i in range(n_teams):
        oᵢ_μ, oᵢ_σ = norm.fit(trace['offense'][:,i])
        o_μ.append(oᵢ_μ)
        o_σ.append(oᵢ_σ)
        dᵢ_μ, dᵢ_σ = norm.fit(trace['defense'][:,i])
        d_μ.append(dᵢ_μ)
        d_σ.append(dᵢ_σ)
    posteriors['offense'] = [o_μ, o_σ]
    posteriors['defense'] = [d_μ, d_σ]

    return posteriors

def fatten_priors(prev_posteriors, factor, f_thresh):
    priors = prev_posteriors.copy()
    priors['home'][1] = np.minimum(priors['home'][1] * factor, f_thresh)
    priors['intercept'][1] = np.minimum(priors['intercept'][1] * factor, f_thresh)
    priors['offense'][1] = np.minimum(np.array(priors['offense'][1]) * factor, f_thresh)
    priors['defense'][1] = np.minimum(np.array(priors['defense'][1]) * factor, f_thresh)

    return priors

def model_iteration(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, Δσ, samples=2000, tune=1000, cores=1):
    with pm.Model():
        # Global model parameters
        h = pm.Normal('home', mu=priors['home'][0], sigma=priors['home'][1])
        i = pm.Normal('intercept', mu=priors['intercept'][0], sigma=priors['intercept'][1])

        # Team-specific poisson model parameters
        o_star_init = pm.Normal('o_star_init', mu=priors['offense'][0], sigma=priors['offense'][1], shape=n_teams)
        Δ_o = pm.Normal('Δ_o', mu=0.0, sigma=Δσ, shape=n_teams)
        o = pm.Deterministic('offense', o_star_init + Δ_o) #formerly o_star
        #o = pm.Deterministic('offense', o_star - tt.mean(o_star))

        d_star_init = pm.Normal('d_star_init', mu=priors['defense'][0], sigma=priors['defense'][1], shape=n_teams)
        Δ_d = pm.Normal('Δ_d', mu=0.0, sigma=Δσ, shape=n_teams)
        d = pm.Deterministic('defense', d_star_init + Δ_d) #formerly d_star
        #d = pm.Deterministic('defense', d_star - tt.mean(d_star))

        #μₕ = tt.exp(i + h + o[idₕ] - d[idₐ])
        #μₐ = tt.exp(i + o[idₐ] - d[idₕ])

        μₕ = i + h + o[idₕ] - d[idₐ]
        μₐ = i + o[idₐ] - d[idₕ]

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

def model_update(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, f, f_thresh, Δσ):
    priors = fatten_priors(priors, f, f_thresh)
    posteriors = model_iteration(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, Δσ)

    return posteriors

def single_game_prediction(row, posteriors, teams_to_int, decimals = 5):
    precision = f".{decimals}f"
    game_pred = {"H_proj":[],"A_proj":[]}
    idₕ = teams_to_int[row["Home"]]
    idₐ = teams_to_int[row["Away"]]
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
    # Normal(μ₁,σ₁²) + Normal(μ₂,σ₂²) = Normal(μ₁ + μ₂, σ₁² + σ₂²)
    #log_μₕ_μ = i_μ + h_μ + oₕ_μ - dₐ_μ
    #game_pred["H_proj"].append(np.exp(log_μₕ_μ))
    game_pred["H_proj"].append(i_μ + h_μ + oₕ_μ - dₐ_μ)
    #log_λₕ_σ = np.sqrt(i_σ ** 2 + h_σ ** 2 + oₕ_σ ** 2 + dₐ_σ ** 2)
    #log_μₐ_μ = i_μ + oₐ_μ - dₕ_μ
    #game_pred["A_proj"].append(np.exp(log_μₐ_μ))
    game_pred["A_proj"].append(i_μ + oₐ_μ - dₕ_μ)
    #log_λₐ_σ = np.sqrt(i_σ ** 2 + oₐ_σ ** 2 + dₕ_σ ** 2)
    return game_pred
