import os

path = os.path.dirname(os.path.dirname(__file__)) + os.sep
result_path = path + 'results' + os.sep
file_name = 'test' 


""" MODEL PARAMETERS """
n_vectors = 50
n_hosts = 50
sim_duration_days = 7
time_unit = 'hours'

""" VECTOR RATES """
v_move = 0.25 # host-seeking
v_bite = 0.5 # biting rate (per capita)
v_feed = 1 # blood-feeding
v_gonotrophic = 1/72 # gonotrophic cycle once every 72 hours == handling time

""" HOST RATES """
h_move = 0.1

# two options: center, random
start_node = 'random' # 'center' 

# Lattice size (should have odd coordinates if individuals start at the center)
width    = 50# 101  
height   = 50# 101

# Number of different runs to average results
n_runs = 100
run_parallel = True



