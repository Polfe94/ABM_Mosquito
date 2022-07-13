import numpy as np
from agent import *
import params
import pandas as pd
#from collections import Counter
from itertools import compress
from copy import deepcopy

class DeterministModel:

	def __init__(self, agents, environment, init_pos = None):

		self.agents = agents
		self.environment = environment
		self.life_table = params.df
		if init_pos is None:
			self.init_pos = self.agents[0].pos

		self.environment.grid[self.init_pos] = len(self.agents)
  
		self.births = []

		# self.df = pd.DataFrame({'x': [self.agents[0].pos[0]],
		# 'y': [self.agents[0].pos[1]],
		# 't': [0],
		# 'n': [len(self.agents)]})

		# visualization gif
		self.frames = [deepcopy(self.environment.grid)]
		self.dispersion = []

	def population_metrics(self):
		pass
	
	def step(self):

		pos = []
		coords = []
		d_idx = []
		births = []
		# moves = []

		for a in self.agents:
			# death, newborns, d, alpha = a.action(self.environment)
			death, newborns = a.action(self.environment)
			d_idx.append(death)
			for i in range(newborns):
				births.append(Parakeet(0, pos = a.pos, coords = a.coords))
    
			self.births.append(newborns) ## keep track of number of births
			
			pos.append(a.pos)
			coords.append(a.coords)
			# moves.append(d)
   
		# self.dispersion.append(moves)
		self.agents = list(compress(self.agents, d_idx))
		coords = list(compress(coords, d_idx))
		# coords = list(compress(coords, [i != (0,0) for i in coords]))
		self.dispersion.append(coords)

		self.agents.extend(deepcopy(births))
		# c = Counter(pos)
		# df = pd.DataFrame([[x[0], x[1], key, c[x]] for x in c],
		# columns= ['x', 'y', 't', 'n'])
		# self.df = pd.concat([self.df, df], axis = 0)
		# upos = list(set(pos)) # unique positions
		# if len(upos) > 1:
		# 	maxd = max(abs(np.linalg.norm(np.array(upos) - self.init_pos, axis = 1)))

		# else:
		# 	maxd = 0.0

		
		if len(coords) > 0:
			maxd = np.max(abs(np.linalg.norm(np.array(coords) - (0, 0), axis = 1)))
			# maxd = np.quantile(abs(np.linalg.norm(np.array(coords) - (0, 0), axis = 1)), 0.5)
		else:
			maxd = 0
   
		return len(self.agents), maxd

	def save_data(self, path, filename):
		# self.df.to_csv(path + filename + '_df.csv')
		self.result.to_csv(path + filename + '_result.csv')
		# self.dispersion.to_csv(path + filename + '_dispersion.csv')

	def run(self, steps):

		# d = {'t': [0], 'n': [len(self.agents)], 'r': [0], 'diff': [0]}
		d = {'t': [0], 'n': [len(self.agents)], 'r': [0]}
		for i in range(steps):
			a, r = self.step()
			d['t'].append(i + 1)
			d['n'].append(a)
			d['r'].append(r)
			# d['diff'].append(abs(d['diff'][-1] - d['r'][-1]))
			self.frames.append(deepcopy(self.environment.grid))

		self.result = pd.DataFrame(d)
		# self.dispersion = pd.DataFrame(self.dispersion)

