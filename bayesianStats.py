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

def stats_get_model_posteriors(trace, n_teams):
    posteriors = {"o_ppa":[],"d_ppa":[],"o_sr":[],"d_sr":[],"o_exp":[],"d_exp":[]}
    for x in ["ppa","sr","exp"]:
        o_μ = []
        o_σ = []
        d_μ = []
        d_σ = []
        for i in range(n_teams):
            oᵢ_μ, oᵢ_σ = norm.fit(trace['o_' + x][:,i])
            o_μ.append(oᵢ_μ)
            o_σ.append(oᵢ_σ)
            dᵢ_μ, dᵢ_σ = norm.fit(trace['d_' + x][:,i])
            d_μ.append(dᵢ_μ)
            d_σ.append(dᵢ_σ)
        posteriors['o_' + x] = [o_μ, o_σ]
        posteriors['d_' + x] = [d_μ, d_σ]

    return posteriors

def stats_fatten_priors(prev_posteriors, factor, f_thresh):
    priors = prev_posteriors.copy()
    for x in ["ppa","sr","exp"]:
        #REALLY TEMP WAY TO DO THIS
        if (x == "exp"):
            f_thresh = f_thresh * 2
        for y in ["o_","d_"]:
            priors[y + x][1] = np.minimum(np.array(priors[y + x][1]) * factor, f_thresh)

    return priors


def stats_iteration(idₕ, ppa_h_obs, idₐ, ppa_a_obs, sr_h_obs, sr_a_obs, exp_h_obs, exp_a_obs, priors, n_teams, samples=2000, tune=1000, cores=1):
    with pm.Model():
        #PPA
        o_ppa = pm.Normal('o_ppa', mu=priors['o_ppa'][0], sigma=np.array(priors['o_ppa'][1]), shape=n_teams)
        d_ppa = pm.Normal('d_ppa', mu=priors['d_ppa'][0], sigma=np.array(priors['d_ppa'][1]), shape=n_teams)

        #Success Rate
        o_sr = pm.Normal('o_sr', mu=priors['o_sr'][0], sigma=np.array(priors['o_sr'][1]), shape=n_teams)
        d_sr = pm.Normal('d_sr', mu=priors['d_sr'][0], sigma=np.array(priors['d_sr'][1]), shape=n_teams)

        #PPA
        o_exp = pm.Normal('o_exp', mu=priors['o_exp'][0], sigma=np.array(priors['o_exp'][1]), shape=n_teams)
        d_exp = pm.Normal('d_exp', mu=priors['d_exp'][0], sigma=np.array(priors['d_exp'][1]), shape=n_teams)


        home_ppa = pm.Normal('ppa_home', mu=o_ppa[idₕ] - d_ppa[idₐ], observed=ppa_h_obs)
        away_ppa = pm.Normal('ppa_away', mu=o_ppa[idₐ] - d_ppa[idₕ], observed=ppa_a_obs)

        home_sr = pm.Normal('sr_home', mu=o_sr[idₕ] - d_sr[idₐ], observed=sr_h_obs)
        away_sr = pm.Normal('sr_away', mu=o_sr[idₐ] - d_sr[idₕ], observed=sr_a_obs)

        home_exp = pm.Normal('exp_home', mu=o_exp[idₕ] - d_exp[idₐ], observed=exp_h_obs)
        away_exp = pm.Normal('exp_away', mu=o_exp[idₐ] - d_exp[idₕ], observed=exp_a_obs)


        trace = pm.sample(
            samples,
            tune=tune,
            chains=3,
            cores=cores,
            progressbar=True,
            return_inferencedata=False
        )

        posteriors = stats_get_model_posteriors(trace, n_teams)

        return posteriors

def stats_update(idₕ, ppa_h_obs, idₐ, ppa_a_obs, sr_h_obs, sr_a_obs, exp_h_obs, exp_a_obs, priors, n_teams):
    priors = stats_fatten_priors(priors, 1, 0.5)
    posteriors = stats_iteration(idₕ, ppa_h_obs, idₐ, ppa_a_obs, sr_h_obs, sr_a_obs, exp_h_obs, exp_a_obs, priors, n_teams)

    return posteriors
