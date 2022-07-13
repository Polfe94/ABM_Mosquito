
""" UNUSED !! """

"""
import numpy as np
import random
from agent import *
import params
import pandas as pd

class GillespieAlgorithm():

	def __init__(self, agents, environment):

		self.agents = agents
		self.environment = environment

		z = zip(list(range(len(self.agents))),
		[i.age for i in self.agents])
		
		self.population = pd.DataFrame(list(z), columns = ['ID', 'Age'])

		# debugging
		self.sample = []
		
		self.r = [r.r_i for r in self.agents]
		self.r_norm = np.array(self.r) / sum(self.r)
		self.R_t = sum(self.r)

		self.rng_t = random.random() # random number to sample the time
		self.rng_action = random.random() # random number to determine if action occurs

		self.time = abs(np.log(self.rng_t)/self.R_t)
	
	def step(self):

		sample = np.random.choice(a = list(range(self.agents)), p = self.r_norm)

		if self.rng_action < float(self.r_norm[sample]):
			self.sample.append(sample) # for debugging and tracking agents' actions

			# do action & report deaths and births
			newborns = self.agents[sample].action(self.environment)

			if newborns > 0:
				for i in range(newborns):
					self.agents.append(Parakeet(len(self.agents)))
					self.agents[-1].pos = self.agents[sample].pos
					self.agents[-1].r_i = params.gamma
					self.r.append(params.gamma)

			# actualize rates
			self.r[sample] = self.agents[sample].r_i
			self.r_norm = np.array(self.r) / sum(self.r)
			self.R_t = sum(self.r)

		# get rng for next iteration
		self.rng_t = random.random()
		self.rng_action = random.random()

		# get time for next iteration
		self.time += abs(np.log(self.rng_t)/self.R_t)

"""
