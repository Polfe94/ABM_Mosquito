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

class Mosquito():
	
	def __init__(self, pos = None, coords = (0, 0)):
		
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
		self.r_i = []
		# possible states: host-seeking, biting, digesting
		self.state = 'host-seeking'  
		self.infectious = False # carries disease ?


	def move(self, grid):
		pass
	
	def dispersal_moore(self, grid):
		pass

	def dispersal_neumann(self, grid):
		pass
	

	''' RATES '''
	# Contact rate (Cvh): total number of contact events between mosquito-human per time unit in a given area
	# Bloodfeeding rate (Bvh): average number of blood meals a single mosquito attains from hosts per time unit in a given area
	# Biting rate: average number of bites a single mosquito takes from hosts per time unit in a given area
	## Human focused -> # Bite exposure rate (Evh): number of bites (with or without blood-feeding) a single host experiences per time unit in a given area
	"""Notes: Bloodfeeding, biting rate, and bite exposure are per capita. Contact rate is not."""
 
	''' POSSIBLE ACTIONS '''
	# host preference ?? some studies show vector preference towards infected individuals
	# gonotrophic cycle duration ???
	# biting (gets a percentatge of satiation) # bloodfeeding ?? two separate parameters???
	# host-seeking (moves until it finds a human to bite)
	# digesting (digests blood)
	# laying (lays eggs, how many ???)
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
