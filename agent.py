import random
import math
import numpy as np
from copy import deepcopy
import params
import functools

''' PREVIOUS CONSIDERATIONS '''
# Contact rate and other factors depend on host and vector density. 
# We eliminate that with a constant N for both vector and host.
# Implement biting preference towards some hosts ? (infected, low protective)

'''
VECTOR AGENT 
'''

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
		# possible states: host-seeking, probing, blood-feeding, digesting
		self.state = 'host-seeking'  
		self.infectious = False # carries disease ?
		self.satiation = 0

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

	def feed(self):
		self.satiation += random.random()
		if self.satiation > 1:
			self.satiated = True

		self.state = ''

	''' ACTION CHOICE '''
	def action(self, grid):
		pass


'''
HOST AGENT 
'''
class Human():
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
		# possible states: active, inactive
		self.state = 'active'  
		self.infectious = False # carries disease ?
		self.atraction = 0 # preference 
  
	def action(self, grid):
		pass