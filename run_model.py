import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from model import *
from lattice import Lattice


import numpy as np
import time
import random
import pandas as pd
import multiprocessing as mp

from copy import deepcopy

from argparser import argparse

# argument parser to change parameters from the command line (or a bash script)
argparse(sys.argv[1:])

result_path = params.result_path
filename = params.file_name

if os.path.exists(result_path + filename + '.csv'):
	filename = filename + '_' + str(random.random())
	print('+++ Result file already exists! Changing name to avoid override... +++')

def create_instance(**kwargs):
	agents = [Parakeet(**kwargs) for i in range(params.n_agents)]
	environment = deepcopy(Lattice(params.width, params.height))
	if 'pos' not in kwargs:
		xy = None
	else:
		xy = kwargs['pos']

	instances = []
	for i in range(params.n_runs):
		instances.append(DeterministModel(agents, environment, init_pos=xy))

	return instances

if not os.path.isdir(result_path):
	print('Path result does not exist. Creating directory: %s' % result_path)
	os.mkdir(result_path)

if params.n_runs > 1:
	os.mkdir(result_path + filename)
	models = create_instance()

	if params.run_parallel:

		def run_parallel(model):
			random.seed(random.randrange(99999) * random.random() + time.time())
			model.run(params.n_steps)
			return deepcopy(model)
		
		pool = mp.Pool(mp.cpu_count())
		models = pool.map(run_parallel, models)
		pool.join()
		pool.terminate()

	else:

		for model in models:
			model.run(params.n_steps)

	results = [m.result for m in models]
	avg = np.average(results, axis = 0)
	sd = np.std(results, axis = 0)
	sem = sd / np.sqrt(len(results))

	df = pd.DataFrame({'t': list(range(len(avg))),
	'n': avg[:, 1], 'sd_n': sd[:, 1], 'sem_n': sem[:, 1],
	'r': avg[:, 2], 'sd_r': sd[:, 2], 'sem_r': sem[:, 2]})

else:
	model = create_instance()[0]
	model.run()
	model.save_data(result_path, filename)