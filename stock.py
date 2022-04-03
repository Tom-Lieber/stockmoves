import os
from datetime import datetime
import pandas as pd

from constants import DATA_PATH
from constants import DELTA_ORIGIN
from constants import FIRST_DATE
from constants import LAST_DATE
from constants import SEARCH_PATTERN
from constants import SEARCH_RANGE_MAX
from constants import SEARCH_RANGE_MIN

class stock:

    symbol = None
    dataframe = None

    patternIndex = 0
    pattern = list(SEARCH_PATTERN)
    currentTickDate = None

    def __init__(self, symbol):
        self.symbol = symbol
        self.dataframe = self.formatDataframe(self.getSymbolPath(self.symbol))

    def getSymbolPath(self, symbol):
        path = os.path.normpath(DATA_PATH + "\\" + symbol + ".us.txt")
        if (os.path.exists(path)):
            return path
        else:
            raise FileNotFoundError()

    def formatDataframe(self, path):
        inputData = pd.read_csv(path, parse_dates=["<DATE>"], date_parser= lambda x: datetime.strptime(x, "%Y%m%d"))
        inputData = inputData.astype({"<TICKER>": str, "<PER>": str, "<TIME>": int, "<OPEN>": float, "<HIGH>": float, "<LOW>": float, "<CLOSE>": float, "<VOL>": int})
        inputData["<DELTA>"] = self.calculateDeltas(inputData)
        filterData = inputData.loc[inputData["<DATE>"] >= FIRST_DATE]
        filterData = filterData.loc[filterData["<DATE>"] <= LAST_DATE]
        return filterData

    def calculateDeltas(self, df):
        deltas = []
        prev = None
        for index, row in df.iterrows():
            if prev != None:
                deltas.append(((row[DELTA_ORIGIN] / prev) - 1) * 100)
            else:
                deltas.append(0)
            prev = row[DELTA_ORIGIN]
        return deltas

    def getDataRowAtDate(self, date):
        return self.dataframe.loc[self.dataframe["<DATE>"] == date].to_dict('records')[0]

    def getCurrentDataRow(self):
        return self.dataframe.loc[self.dataframe["<DATE>"] == self.currentTickDate].to_dict('records')[0]

    def getFutureDataRow(self, days):
        return self.dataframe.loc[self.dataframe.index[self.dataframe["<DATE>"] == self.currentTickDate].tolist()[0] + days].to_dict()

    def checkPattern(self, dataRow):
        #returns true if the pattern is matched at the current row, false if not
        if self.pattern[self.patternIndex] == '+':
            if dataRow["<DELTA>"] >= SEARCH_RANGE_MIN and dataRow["<DELTA>"] <= SEARCH_RANGE_MAX:
                self.patternIndex += 1
            else:
                self.patternIndex = 0
                return False
        elif self.pattern[self.patternIndex] == '-':
            if dataRow["<DELTA>"] <= -SEARCH_RANGE_MIN and dataRow["<DELTA>"] >= -SEARCH_RANGE_MAX:
                self.patternIndex += 1
            else:
                self.patternIndex = 0
                return False

        if self.patternIndex == len(self.pattern):
            self.patternIndex -= 1 #keeps rolling buffer
            return True
        return False

    def tick(self, date):
        self.currentTickDate = date
        try:
            if self.checkPattern(self.getDataRowAtDate(date)):
                #if a pattern is matched, return true
                return True
        except IndexError:
            return False
        return False