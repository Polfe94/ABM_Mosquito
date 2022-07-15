# import networkx as nx
import numpy as np

class Lattice:

    def __init__(self, width, height):

        # Create squared lattice
        self.grid = np.empty((width, height), dtype = object)
        self.grid.fill([])
        
        i = np.indices((width, height))
        x = np.concatenate(i[0]).ravel().tolist()
        y = np.concatenate(i[1]).ravel().tolist()
        self.coords = list(zip(x, y))
        self.x, self.y = np.meshgrid(np.linspace(0, height, width), np.linspace(0, height, height))