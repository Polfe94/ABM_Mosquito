# import numpy as np
from agent import *
# import params
import pandas as pd
from gillespie import GillespieAlgorithm
#from collections import Counter
# from itertools import compress
# from copy import deepcopy

class Model(GillespieAlgorithm):

	def __init__(self, environment):
     
		super().__init__(environment)
		
		x = []
		y = []
		id = []
		for i in self.agents:
			x.append(i.pos[0])
			y.append(i.pos[1])
			id.append(i.id)
		self.result = pd.DataFrame({'x': x, 'y': y, 'id': id, 't': [0] * len(x)})
  
	def save_data(self, path, filename):
		pass

	def run(self, steps):
     
		for i in range(steps):
			id = self.step()


