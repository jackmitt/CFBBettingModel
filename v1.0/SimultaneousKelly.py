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
#if another list of wagers is passed into altWager, then the difference is returned. Else, the log growth rate for that one list is returned
def expected_log_growth(pa, pb, wager, altWager = []):
    payout = []
    gradients = []
    for prob in pb:
        payout.append((1/prob) - 1)
    numEvents = len(pa)
    logGrowthCalculations = []
    logGrowthCalculationsAlt = []
    if (len(altWager) == 0):
        numIter = 10000000
    else:
        numIter = 100
    for m in range(numIter):
        simLogGrowth = 0
        simLogGrowthAlt = 0
        for i in range(numEvents):
            rng = random.randint(1,1000)
            if (pa[i] * 1000 >= rng):
                simLogGrowth += np.log(1 + wager[i]*payout[i])
                if (len(altWager) != 0):
                    simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
            else:
                simLogGrowth += np.log(1 - wager[i])
                if (len(altWager) != 0):
                    simLogGrowthAlt += np.log(1 - altWager[i])
        logGrowthCalculations.append(simLogGrowth)
        logGrowthCalculationsAlt.append(simLogGrowthAlt)
    if (len(altWager) == 0):
        return (np.average(logGrowthCalculations))
    else:
        #print (np.average(logGrowthCalculationsAlt), np.average(logGrowthCalculations))
        return (np.average(logGrowthCalculationsAlt) - np.average(logGrowthCalculations), np.average(logGrowthCalculations))

#returns a list of the gradients for x given the actual probabilities, book probabilities, old wager list
def log_growth_gradients(pa, pb, wager):
    gradients = []
    growthRates = []
    for i in range(len(wager)):
        toAvg = []
        toAvg2 = []
        for j in range(1):
            #epsilon = random.gauss(0, wager[i])
            epsilon = 0.01
            xNew = wager[i] + epsilon
            newWager = wager.copy()
            newWager[i] = xNew
            diff, calc = expected_log_growth(pa, pb, wager, newWager)
            toAvg.append(diff/epsilon)
            toAvg2.append(calc)
        gradients.append(np.average(toAvg))
        growthRates.append(np.average(toAvg2))
    return (gradients, growthRates)

def gradient_ascent(pa, pb, kellyWagers, max_iter = 10000, verbose = True):
    bankrollConstraint = min(np.sum(kellyWagers), 1)
    wager = kellyWagers.copy()
    learningRates = []
    for i in range(len(pa)):
        learningRates.append([5, True])

    iterCount = 1
    while(np.average(learningRates)*2 < 100000 and iterCount < max_iter):
        if (verbose):
            print ("Iteration: " + str(iterCount))
        iterCount += 1
        #rngIndex = random.randint(0, len(wager)-1)
        #eq 18
        t = np.log(wager)
        gradients, logGrowths = log_growth_gradients(pa, pb, wager)
        if (verbose):
            print ("Average learning rate:", np.average(learningRates)*2)
        weightedSumGradients = 0
        for i in range(len(gradients)):
            # if (gradients[i] < 0):
            #     if (not learningRates[i][1]):
            #         learningRates[i][0] = learningRates[i][0]*1.05
            #     else:
            #         learningRates[i][0] = learningRates[i][0]*0.95
            #     learningRates[i][1] = False
            # else:
            #     if (learningRates[i][1]):
            #         learningRates[i][0] = learningRates[i][0]*1.05
            #     else:
            #         learningRates[i][0] = learningRates[i][0]*0.95
            #     learningRates[i][1] = True
            weightedSumGradients += gradients[i]*wager[i]
        #eq 19
        dt = []
        for i in range(len(gradients)):
            dt.append(wager[i]*(gradients[i] - weightedSumGradients))
        #print (t)
        #print (dt)
        #print(learningRates)
        #adjustment to x
        for i in range(len(gradients)):
            t[i] = t[i] + dt[i]*learningRates[i][0]
        #eq 15
        for i in range(len(wager)):
            wager[i] = np.exp(t[i])/(np.sum(np.exp(t)) + (1-bankrollConstraint))
        if (verbose):
            print (wager)
            print ("TOTAL BANKROLL BET: " + str(np.sum(wager)))
    return (wager)


a = pd.read_csv('./csv_Data/whitrowT2.csv', encoding = "ISO-8859-1")
pa = a["p"].to_numpy()
pb = a["pSquiggle"].to_numpy()
wager = a["kellyPct"].to_numpy()

a["OUR ALGO"] = gradient_ascent(pa, pb, wager)
# a.to_csv("./csv_Data/whitrowT1.csv")
#print("Simplex expected log growth:", expected_log_growth(a["p"].to_numpy(), a["pSquiggle"].to_numpy(), a["simplexPct"].to_numpy()))
#print("Constrained expected log growth:", expected_log_growth(a["p"].to_numpy(), a["pSquiggle"].to_numpy(), a["constrainedPct"].to_numpy()))
