from stock import stock
from trader import trader
import os

from constants import DELTA_ORIGIN
from constants import SIMULATION_MONEY

class simulator:

    stocks = []
    trader = None
    stockLeader = None
    matches = []

    def __init__(self, symbols):
        #initialize stocks
        index = 1
        for symbol in symbols:
            newStock = stock(symbol)
            if newStock.dataframe.empty:
                print("Skipped stock " + symbol + " " + str(index) + " of " + str(len(symbols)) + ". Reason: empty dataframe")
                index += 1
                continue
            self.stocks.append(newStock)
            print("Initialized stock " + symbol + " " + str(index) + " of " + str(len(symbols)))
            index += 1
        self.stockLeader = self.stocks[0].dataframe
        print("Finished initializing stocks.")

        #initialize trader
        self.trader = trader()

    def start(self):
        print("Starting simulation...")
        dayCount = 1
        totalDayCount = len(self.stockLeader)
        for index, row in self.stockLeader.iterrows(): #stockLeader dataframe drives ticks
            for stock in self.stocks:
                if stock.tick(row["<DATE>"]): #pattern completed on this row
                    try:
                        if DELTA_ORIGIN == "<CLOSE>":
                            buyDataRow = stock.getCurrentDataRow()
                            sellDataRow = stock.getFutureDataRow(1)
                        elif DELTA_ORIGIN == "<OPEN>":
                            buyDataRow = stock.getFutureDataRow(1)
                            sellDataRow = stock.getFutureDataRow(2)
                        self.matches.append(((sellDataRow[DELTA_ORIGIN] / buyDataRow[DELTA_ORIGIN]) - 1) * 100)
                        self.trader.trade(buyDataRow, sellDataRow)
                    except KeyError:
                        pass
            print("Simulated day " + str(dayCount) + " of " + str(totalDayCount))
            dayCount += 1
        self.printStats()

    def printStats(self):
        print("TRADER STATS:")
        print("Ending Money: " + str(round(self.trader.money, 2)))
        print("Percent Return: " + str(round(((self.trader.money / SIMULATION_MONEY) - 1) * 100, 2)))
        print("Buy Limited: " + str(self.trader.buyLimited))
        print("Losses Stopped: " + str(self.trader.lossesStopped))
        print("Win Rate: " + str(self.trader.getWinRate()) + "%")
        print("Total Trades: " + str(self.trader.totalTrades))
        print("Trades per Day: " + str(round(self.trader.totalTrades / len(self.stockLeader), 3)))
        print("----------")

        print("STOCK STATS:")
        sum = 0
        for stock in self.stocks:
            sum += ((stock.dataframe[DELTA_ORIGIN].iloc[-1] / stock.dataframe[DELTA_ORIGIN].iloc[0]) - 1) * 100
        mean = sum / len(self.stocks)
        print("Average stock return over period: " + str(round(mean, 2)) + "%")
        print("Amount of Stocks: " + str(len(self.stocks)))
        print("----------")
        