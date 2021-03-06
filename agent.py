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
		# possible states: host-seeking, handling, contact <---
		self.state = 'host-seeking'  
		self.infectious = False # carries disease ?
		self.satiation = 0

		# Moore neighborhood
		# self.dispersal_moore()

		# Neumann neighborhood
		self.dispersal_neumann()

	def dispersal_moore(self):
		self.available_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

	def dispersal_neumann(self, grid):
		self.available_moves = [(1, 0), (-1, 0), (0, 1), (0, -1),
		(-1, -1), (-1, 1), (1, 1), (1, -1)]

	# move avoiding collision
	def move(self, grid):
		c = np.array(random.choice(self.available_moves))
		pos = np.array(self.pos) + c
		idx = np.where(pos < 0)[0]
		pos[idx] = grid.limits[idx]
		idx = np.where(pos > grid.limits)[0]
		pos[idx] = 0
		self.pos = pos

	# move with bouncing around edges
	# def move(self, grid):

	# 	available = False
	# 	while not available:
	# 		c = np.array(random.choice(self.available_moves))
	# 		pos = np.array(self.pos) + c
	# 		if np.sum(np.logical_or(pos < 0, pos > grid.limits)) == 0:
	# 			available = True

	# 	self.pos = tuple(pos)
	
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

	def choose_host(self, hosts):
		p = np.array([h.atraction for h in hosts]) / len(hosts) # bite preference
		host = np.random.choice(hosts, p = p)

		return host

	def feed(self, host):
		self.satiation += random.random()

		if self.satiation > 1:
			self.state = 'handling'
			self.r_i = params.v_gonotrophic

		if host.infectous:
			if random.random() < params.prob_infection:
				self.infectious = True

	def bite(self, host):

		if self.infectious:
			if random.random() < params.prob_infection:
				host.infectious = True

	def handling(self, grid):
		self.satiation = 0

		if grid.host_presence(self.pos):
			self.state = 'contact'
			self.r_i = params.v_bite + params.v_feed
		
		else:
			self.state = 'host-seeking'
			self.r_i = params.v_move


	''' ACTION CHOICE '''
	def action(self, grid):
		
		if self.state == 'host-seeking':

			if grid.host_presence(self.pos):

					self.state = 'contact'
					self.r_i = params.v_bite + params.v_feed

			else:

				self.move(grid)

		elif self.state == 'handling':

			self.handling(grid)

		elif self.state == 'contact':

			if grid.host_presence(self.pos):

				hosts = grid.available_hosts(self.pos)
				h = self.choose_host(hosts)

				''' DEFINE PROBABILITY OR SEPARATE RATE '''
				self.bite(h)
				self.feed(h)



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