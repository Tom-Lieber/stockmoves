from datetime import datetime
import os

DATA_PATH = os.path.normpath("data/")
SYMBOL_FILE = os.path.normpath("stocklists/technology.txt")
DELTA_ORIGIN = "<CLOSE>" #What price are deltas calculated from?
FIRST_DATE = datetime(2018, 1, 1)
LAST_DATE = datetime(2020, 1, 1)
SEARCH_PATTERN = "+" #parsed as changes per day
SEARCH_RANGE_MIN = 1.0 #Disregard for pattern matching if change is below this amount
SEARCH_RANGE_MAX = 50.0 #Disregard for pattern matching if change is above this amount
QUANTIZE_AMT = 0.5 #How are tokens sorted into types for final chart?
SIMULATION_MONEY = 10000 #simulation starting money amount
PER_TRADE_AMT = 200 #How much money can be spent on a single trade?
STOP_LOSS = 20 #At what percent drop from principal do you sell?
MAX_SHARE_PRICE = 300 #How much is the trader willing to pay per share? UNUSED