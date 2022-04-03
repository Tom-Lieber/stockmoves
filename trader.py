import pandas as pd
from math import floor

from constants import SIMULATION_MONEY
from constants import STOP_LOSS
from constants import DELTA_ORIGIN
from constants import PER_TRADE_AMT

class trader:
    money = 0
    buyLimited = False #true if can't buy stock due to inadequate funds
    lossesStopped = 0
    wins = 0
    losses = 0
    totalTrades = 0

    def __init__(self):
        self.money = SIMULATION_MONEY

    def trade(self, buyDataRow, sellDataRow):
        #check funds
        if buyDataRow[DELTA_ORIGIN] > self.money:
            self.buyLimited = True
            return
        #buy turn
        sharesAmt = floor(PER_TRADE_AMT / buyDataRow[DELTA_ORIGIN])
        boughtShares = 0
        while sharesAmt > 0 and self.money >= buyDataRow[DELTA_ORIGIN] :
            self.money -= buyDataRow[DELTA_ORIGIN]
            sharesAmt -= 1
            boughtShares += 1
        if boughtShares == 0:
            return
        #stop loss turn
        if DELTA_ORIGIN == "<OPEN>" and buyDataRow["<LOW>"] <= buyDataRow[DELTA_ORIGIN] * (1 - (STOP_LOSS / 100)):
            self.money -= buyDataRow[DELTA_ORIGIN] * 1 - (STOP_LOSS / 100)
            self.lossesStopped += 1
            self.losses += 1
            self.totalTrades += 1
            return
        if DELTA_ORIGIN == "<CLOSE>" and sellDataRow["<LOW>"] <= sellDataRow[DELTA_ORIGIN] * (1 - (STOP_LOSS / 100)):
            self.money -= sellDataRow[DELTA_ORIGIN] * 1 - (STOP_LOSS / 100)
            self.lossesStopped += 1
            self.losses += 1
            self.totalTrades += 1
            return
        #sell turn
        self.money += sellDataRow[DELTA_ORIGIN] * boughtShares
        #logging
        if buyDataRow[DELTA_ORIGIN] < sellDataRow[DELTA_ORIGIN]:
            self.wins += 1
        elif buyDataRow[DELTA_ORIGIN] > sellDataRow[DELTA_ORIGIN]:
            self.losses += 1
        self.totalTrades += 1

    def getWinRate(self):
        return round((self.wins / self.totalTrades) * 100, 2)
