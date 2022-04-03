import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import numpy as np
import normals
from scipy.stats import norm

from simulator import simulator
from graphing import graphing
from constants import SYMBOL_FILE

#TODO:
#   Create exit conditions rather than always selling next-day
#   Both time-based and pattern based conditions
#   Log S&P 500 or comparable index fund to determine full market change across time period
# 
#       Common Casino Risk Ratios:
#           Roulette: 1.054
#           Blackjack: 1.005
# 

#INPUT: Ticker, Search Pattern, Percent Change Range
#OUTPUT: Bar chart of next-day outcomes

symbols = []
with open(SYMBOL_FILE, 'r') as symbolFile:
    for line in symbolFile:
        symbols.append(line.strip())

sim = simulator(symbols)
sim.start()
graph = graphing(simulator.matches)
graph.printGraph()




    
