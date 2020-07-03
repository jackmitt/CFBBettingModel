import math
import time
import random
import pandas as pd
import numpy as np
import itertools
import numpy as np
import scipy.optimize
from datetime import datetime
from collections import defaultdict
from scipy.optimize import NonlinearConstraint

#calculates expected log growth rate through Monte Carlo simulation
#pass in array of calculated probabilities, array of implicit probabilities from the book, and array of wagers (in proportions of bankroll)
def expected_log_growth(pa, pb, wager, wager2):
    payout = []
    gradients = []
    for prob in pb:
        payout.append((1/prob) - 1)
    numEvents = len(pa)
    logGrowthCalculations = []
    for m in range(10000):
        simLogGrowth = 0
        simLogGrowth
        for i in range(numEvents):
            rng = random.randint(1,1000)
            if (pa[i] * 1000 >= rng):
                simLogGrowth += np.log(1 + wager[i]*payout[i])
            else:
                simLogGrowth += np.log(1 - wager[i])
        logGrowthCalculations.append(simLogGrowth)
    return (np.average(logGrowthCalculations))

def log_growth_gradient(pa, pb, wager1, wager2):
    return (expected_log_growth(pa, pb, wager1))
a = pd.read_csv('./csv_Data/whitrowT2.csv', encoding = "ISO-8859-1")
#print("Simplex expected log growth:", expected_log_growth(a["p"].to_numpy(), a["pSquiggle"].to_numpy(), a["simplexPct"].to_numpy()))
#print("Constrained expected log growth:", expected_log_growth(a["p"].to_numpy(), a["pSquiggle"].to_numpy(), a["constrainedPct"].to_numpy()))
