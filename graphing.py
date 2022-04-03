import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import normals

from constants import QUANTIZE_AMT
from constants import STOP_LOSS

class graphing:

    tokens = None
    types = None
    matchData = None
    mean = None
    std = None

    def __init__(self, matches):
        self.tokens = matches
        self.types = self.quantizeMatches(self.tokens)
        self.matchData = pd.DataFrame.from_dict(self.getTypeAmounts(self.types))
        self.mean = np.mean(self.types)
        self.std = np.std(self.types)
        self.printStats()

    def quantizeMatches(self, matches):
        typeList = []
        for match in matches:
            tries = 0
            maxTries = (1000 + 100) / QUANTIZE_AMT
            test = -100.0
            upperBound = None
            while tries <= maxTries and upperBound == None:
                if match <= test:
                    upperBound = test
                test += QUANTIZE_AMT
                tries += 1
            if upperBound != None:
                lowerBound = upperBound - QUANTIZE_AMT
                if match - lowerBound < upperBound - match: #rounds up if halfway
                    typeList.append(lowerBound)
                else:
                    typeList.append(upperBound)
            else:
                typeList.append(None)
        return typeList

    def getTypeAmounts(self, typeData):
        amounts = []
        types = []
        for type in typeData:
            if types.count(type) > 0:
                continue
            types.append(type)
            amounts.append(typeData.count(type))
        return {"TYPE": types, "TOKENS": amounts}

    def printStats(self):
        print("PATTERN STATS:")
        print("Mean: " + str(self.mean))
        print("STD: " + str(self.std))
        print("n: " + str(len(self.tokens)))
        print("68% chance of return between " + str(self.mean - self.std) + " and " + str(self.mean + self.std))
        avgGain = np.mean([x for x in self.tokens if x > 0])
        avgLoss = np.mean([x for x in self.tokens if x < 0 and x > -STOP_LOSS])
        print("Average Gain: " + str(round(avgGain, 2)))
        print("Average Loss: " + str(round(avgLoss, 2)))
        #print("Profitability Ratio: " + str( (((self.mean) / STOP_LOSS) + 1) * 0.5 ) )
        ZeroZScore = (0-self.mean) / self.std
        print("Chance of postive return per trade given the data: " + str(round((1 - norm.cdf(ZeroZScore)) * 100, 2)))
        print("Profitability Ratio: " + str( (avgGain / -avgLoss) *  (1 - norm.cdf(ZeroZScore)) ))

    def printGraph(self):
        self.types.sort()
        fig, axs = plt.subplots(2) #setup two plots on a figure
        axs[0].set_xlabel("Percent Change")
        axs[0].bar(self.matchData["TYPE"], self.matchData["TOKENS"])
        axs[1].plot(self.types, normals.pdf(self.types), color= "red")
        axs[1].plot([self.mean, self.mean], [0, max(normals.pdf(self.types))], color = "black")
        plt.show()