import numpy as np

def pdf(x):
    #takes a list of values and calculates probability distribution
    mean = np.mean(x)
    std = np.std(x)
    y = 1/(std * np.sqrt(2 * np.pi)) * np.exp( - (x - mean)**2 / (2 * std**2))
    return y