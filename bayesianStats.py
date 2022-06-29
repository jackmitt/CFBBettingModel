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
    posteriors = {}
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

def stats_fatten_priors(prev_posteriors, factor, f_thresh):
    priors = prev_posteriors.copy()
    priors['offense'][1] = np.minimum(np.array(priors['offense'][1]) * factor, f_thresh)
    priors['defense'][1] = np.minimum(np.array(priors['defense'][1]) * factor, f_thresh)

    return priors


def stats_iteration(idₕ, ppa_h_obs, idₐ, ppa_a_obs, priors, n_teams, samples=2000, tune=1000, cores=1):
    with pm.Model():
        #Team PPA Efficiency
        o = pm.Normal('offense', mu=priors['offense'][0], sigma=np.array(priors['offense'][1]), shape=n_teams)
        d = pm.Normal('defense', mu=priors['defense'][0], sigma=np.array(priors['defense'][1]), shape=n_teams)


        home_ppa = pm.Normal('ppa_home', mu=o[idₕ] - d[idₐ], observed=ppa_h_obs)
        away_ppa = pm.Normal('ppa_away', mu=o[idₐ] - d[idₕ], observed=ppa_a_obs)

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

def stats_update(idₕ, ppa_h_obs, idₐ, ppa_a_obs, priors, n_teams):
    priors = stats_fatten_priors(priors, 1, 0.5)
    posteriors = stats_iteration(idₕ, ppa_h_obs, idₐ, ppa_a_obs, priors, n_teams)

    return posteriors
