import os
# import sys
import pandas as pd
# import numpy as np
# from io import StringIO
# import re
# import subprocess
import math
import random

path = os.path.dirname(os.path.dirname(__file__)) + os.sep
result_path = path + 'results' + os.sep
file_name = 'test' 


""" MODEL PARAMETERS """
n_agents = 3 # 10 ??
n_steps  = 10 # 15 # 100 ? 
starting_age = 1 # ???
adulthood = 1 # age of becoming an adult
max_dispersal_age = 3

# two options: center, random
start_node = 'center' # 'random'


# Lattice size (should have odd coordinates)
width    = 101  
height   = 101

if width % 2 == 0:
    width += 1

if height % 2 == 0:
    height += 1


""" DISPERSAL DISTRIBUTIONS """
# Fit without ~59000 outlier
def fit1():
    beta = 0.0005567593
    L1 = 0.0003858284
    L2 = 0.0090770018
    rmax = 28578
    return beta, L1, L2, rmax

# Fit without ~59000 and ~28000 outliers
def fit2():
    beta = 0.0009293295
    L1 = 0.0005018196      
    L2 = 0.0091381715
    rmax = 10508
    return beta, L1, L2, rmax

# OLD fit
def old_fit():
    beta = 0.00071277
    L1 = 0.00050245     
    L2 = 0.00909844
    rmax = 3840
    return beta, L1, L2, rmax

# double exponential (2D)
def kernel(fit):
    M = 0.000005590063 # function maximum
    beta, L1, L2, rmax = fit()

    rmin = 1

    d1 = beta * ((1 + L1 * rmin)/ L1 **2) * math.exp(-L1 * rmin)
    d2 = (1- beta) * ((1 + L2 * rmin) / L2 ** 2) * math.exp(-L2 * rmin)
    d3 = -beta *((1 + L1 * rmax) / L1 ** 2) * math.exp(-L1 * rmax)
    d4 = -(1- beta)* ((1+L2 * rmax) / L2 ** 2) * math.exp(-L2 * rmax)
     
    C = (1 / (2 * math.pi)) * (1 / (d1 + d2 + d3 + d4))
    
    while True:
        r = random.uniform(rmin, rmax)
        y = random.uniform(0, M)
        p = C * (beta * math.exp(-L1 * r) + (1 - beta)* math.exp(-L2 * r))
        if y < p:
            return r

fit = fit2

# try:
#     p = subprocess.Popen('/usr/bin/Rscript --vanilla %sdoubleExp_sampling.R', shell = True, stdout = subprocess.PIPE)
#     p = str(p.stdout.read(), 'utf-8')
#     p = StringIO(p)
#     p = str(pd.read_csv(p))
#     p = re.sub(r'\[.*?\]', '', p)
#     p = p.split('')
#     p.remove('')

# except:
#     print('Something went wrong during kernel importation. Using default sampling distribution')

""" PARAKEET ACTION'S PROBABILITIES """
try:
    df = pd.read_csv(path + 'data' + os.sep + 'life_table.csv')
    
except:
    print('COULD NOT FIND LIFE TABLE. Switching to default values...')
    df = pd.DataFrame({'age': list(range(16)),
                   'px': [1, 0.6] + [0.8] * 13 + [0],
                   'mx': [0, 0, 0.6] + [0.8] * 6 +[0.6, 0.4, 0.2] + [0] * 4,
                   'ma': [0, 1.05, 1.47, 1.58] + [1.47] * 8 + [0] * 4})

try:
    lays = pd.read_csv(path + 'data' + os.sep + 'parakeet_productivity.csv')

except:
    print('COULD NOT FIND EGG LAY TABLE. Switching to default values...')
    lays = pd.DataFrame({'Productivity': [0] * 76 + [1] * 23+
    [2] * 51 + [3] * 65 + [4] * 72 + [5] * 44 + [6] * 34 + [7] * 12 +
    [8] * 3 + [9] + [11], 'POSTA': [1] * 382})

lays_p = {'Values': list(set(lays['Productivity']))}
lays_p['Probabilities'] = [len(lays[lays['Productivity'] == i])/len(lays) for i in lays_p['Values']]

try:
    dispersals = pd.read_csv(path + 'data' + os.sep + 'dispersal.csv')
    dispersal_prob = [len(dispersals[dispersals['d'] == 0]) / len(dispersals)]
    dispersal_prob.append(1 - dispersal_prob[0])

except:
    print('COULD NOT FIND DISPERSAL DISTANCES. Switching to default values...')
    dispersal_prob = [0.3, 0.7]

# Number of different runs to average results
n_runs = 1000
run_parallel = True



