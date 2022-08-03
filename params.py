import os

path = os.path.dirname(os.path.dirname(__file__)) + os.sep
result_path = path + 'results' + os.sep
file_name = 'test' 


""" MODEL PARAMETERS """
n_vectors = 50
n_hosts = 50
sim_duration_days = 7
time_unit = 'hours'
prob_infection = 1

""" VECTOR RATES """
v_move = 1 # host-seeking
v_bite = 20 # biting rate (per capita)
v_feed = 15 # blood-feeding
v_gonotrophic = 1/24 # gonotrophic cycle once every 24 hours

""" HOST RATES """
h_move = 1/12

# two options: center, random
start_node = 'random' # 'center' 

# Lattice size (should have odd coordinates if individuals start at the center)
width    = 50 # 101  
height   = 50 # 101

# Number of different runs to average results
n_runs = 100
run_parallel = True



