import numpy as np
import random
from agent import *
import params
import pandas as pd
from copy import deepcopy

class GillespieAlgorithm:

	def __init__(self, environment):

		self.agents = [Mosquito(id = i) for i in range(params.n_vectors)] + [Human(id = i + params.n_vectors) for i in range(params.n_hosts)]
  
		self.environment = deepcopy(environment)
		self.place_agents()
  
		self.r = pd.DataFrame({'id': list(range(params.n_vectors+params.n_hosts)),
							'r': [params.v_move]*params.n_vectors + [params.h_move]*params.n_hosts,
       						'label': ['v_move']*params.n_vectors + ['h_move']*params.n_hosts})
  
		self.R_t = self.r['r'].sum()
		self.r_norm = list(self.r['r'] / self.R_t)
	
		self.rng_t = random.random() # random number to sample the time
		self.rng_action = random.random() # random number to determine if action occurs

		self.time = abs(np.log(self.rng_t)/self.R_t)
  
	def place_agents(self):
     
		for a in self.agents:
			pos = a.pos
			if self.environment.grid[pos] is None:
				self.environment.grid[pos] = [a]
			else:
				self.environment.grid[pos].append(a)
    
	# def update_rates(self):
		
	# 	self.r = []
	# 	self.labels = []
	# 	self.ids = []
	# 	for i in self.agents:
	# 		self.r.extend(i.r_i)
	# 		self.labels.extend(i.r_labels)
	# 		self.ids.extend([i.id] * len(i.r_labels))
   
	def update_rates(self, id):
     
			self.r = self.r.drop(self.r[self.r['id'] == id].index).reset_index(drop = True)
			for i in range(len(self.agents[id].r_i)):
				self.r = pd.concat([self.r, pd.DataFrame({'id': [id],
                                              'r': [self.agents[id].r_i[i]],
                                              'label': [self.agents[id].r_label[i]]})], ignore_index= True)
		
			self.R_t = self.r['r'].sum()
			self.r_norm = list(self.r['r'] / self.R_t)
   		
	def step(self):

		sample = np.random.choice(a = list(range(len(self.r))), p = self.r_norm)
		id = self.r['id'][sample]
  
		if self.rng_action < float(self.r_norm[sample]):
			# print(id)

			# do action
			self.agents[id].action(self.environment, choice = self.r['label'][sample])

			# actualize rates
			self.update_rates(id)

		# get rng for next iteration
		self.rng_t = random.random()
		self.rng_action = random.random()

		# get time for next iteration
		self.time += abs(np.log(self.rng_t)/self.R_t)
  
		return id

