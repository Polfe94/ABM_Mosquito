import random
import math
import numpy as np
from copy import deepcopy
import params
import functools

'''
PARAKEET AGENT 
'''

kernel = functools.partial(params.kernel, fit = params.fit)

class Parakeet():
	
	def __init__(self, age, pos = None, coords = (0, 0), dispersal = 'jump'):

		self.age = age
		
		if pos is None:
			# Position, state and rates initialization
			if params.start_node == 'center':
				x, y = int(params.width / 2), int(params.height / 2)
			else:
				x, y  = random.randrange(params.width), random.randrange(params.height)
		else:
			x, y = pos

		self.pos = (x, y)
		self.coords = coords
		self.probabilities = {'px': params.df['px'][self.age],
					'mx': params.df['mx'][self.age]}
  
		# Dispersal movement
		self.move = self.choose_dispersal_strategy(dispersal)
		self.has_nested = False


	# Pick the appropriate dispersal strategy for parakeets
	def choose_dispersal_strategy(cls, dispersal):

		if dispersal == 'jump':
			return cls.dispersal_jump

		elif dispersal == 'moore':
			return cls.dispersal_moore

		elif dispersal == 'neumann':
			return cls.dispersal_neumann

	def update_probabilities(self):
		k = list(self.probabilities.keys())
		for p in k:
			self.probabilities[p] = params.df[p][self.age]


	''' MOVEMENT FUNCTIONS '''
	# Border effect (repulsion)
	def dispersal_jump(self, grid):
		prev_pos = self.pos

		# dispersion parameters 
		alpha = 2 * math.pi * random.random() # angle
		d = kernel() # distance
		r = d / grid.scale # distance in meters to pixels in grid

		# new position
		x, y = r * math.cos(alpha) + self.pos[0], r * math.sin(alpha) + self.pos[1]
		self.coords = x, y
		xy = np.array([(x, y)])

		# compute Euclidean distances
		closest_cell = np.linalg.norm(np.array(grid.coords) - xy, axis=1)
		minxy = np.where(closest_cell == min(closest_cell))[0]
		self.pos = grid.coords[int(minxy)]

		# update move in the grid
		grid.grid[prev_pos] -= 1
		grid.grid[self.pos] += 1
  
		# return (d, alpha)
	
	def dispersal_moore(self, grid):
		pass

	def dispersal_neumann(self, grid):
		pass
	
 
	''' POSSIBLE ACTIONS '''
	def die(self, grid):
		grid.grid[self.pos] -= 1

	def mate(self, grid):
		# Note that there is a probability of non-mating at all
		n = np.random.choice(params.lays_p['Values'], p = params.lays_p['Probabilities'])
		grid.grid[self.pos] += n
		# number of births should be divided by 2 (number of reproductive units i.e. females)
		return n

	def grow(self):
		self.age += 1

	''' ACTION CHOICE '''
	def action(self, grid):

		# returns boolean (is the agent still alive?) and integer (newborn parakeets)

		if random.random() >= self.probabilities['px']:
			self.die(grid)
			return False, 0
			# return False, 0, 0, 0

		if self.age < params.adulthood:
			newborns = 0
			# d = 0
			# alpha = 0
		
		elif self.age <= params.max_dispersal_age:
			if not self.has_nested:
				dispersal = np.random.choice([False, True], p = params.dispersal_prob)
				if dispersal:
					# d, alpha = self.move(grid)
					self.move(grid)
					self.has_nested = True

			newborns = self.mate(grid)

		else:
			newborns = self.mate(grid)
			# d = 0
			# alpha = 0

		self.grow()
		self.update_probabilities()

		return True, newborns#, d, alpha
