import random
from scipy.stats import binom
import matplotlib.pyplot as plt

colors = list("rgbcmyk")

def successEvalSim():
    x = random.randint(0,10000)
    if (x/10000 < 0.3):
        return (1)
    elif (x/10000 < 0.6):
        return (2)
    elif (x/10000 < 0.9):
        return (3)
    elif (x/10000 < 0.99):
        return (6)
    else:
        return (11)

dict = {}
for q in range(120):
    print (q)
    dict[q] = 0
    for i in range(39):
        prob1 = binom.pmf(i, 39, 0.05)
        total = 0
        for k in range(10000):
            iridiumCount = 0
            for z in range(i):
                iridiumCount += successEvalSim()
            if (iridiumCount == q):
                total += 1
        prob2 = total / 10000
        dict[q] += prob1 * prob2

print (dict)
plt.scatter(dict.keys(), dict.values(), color = colors.pop())
plt.show()
