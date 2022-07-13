# import networkx as nx
import numpy as np

class Lattice:

    def __init__(self, width, height, scale = 150):

        # Create squared lattice
        self.grid = np.zeros((width, height), dtype = int)
        i = np.indices((width, height))
        x = np.concatenate(i[0]).ravel().tolist()
        y = np.concatenate(i[1]).ravel().tolist()
        self.coords = list(zip(x, y))
        self.x, self.y = np.meshgrid(np.linspace(0, height, width), np.linspace(0, height, height))
        
        # number of units (meters) per pixel in the grid
        self.scale = scale 
        



""" OLD CLASS """
"""
        '''
        self.G = nx.grid_2d_graph(width, height)
        self.coords = dict( (n, n) for n in self.G.nodes() )
        '''



        # self.leftX = [width] + list(range(width + 1))
        # self.rightX = list(range(width + 1)) + [0]
        # self.bottomY = [height] + list(range(height + 1))
        # self.topY = list(range(height + 1)) + [0]
        
        # eight neighbors from top-left to mid-left
        self.moore = [(-1, 1), (0, 1), (1, 1), (1, 0),
                      (1, -1), (0, -1), (-1, -1), (-1, 0)]
        
        # four neighbors
        self.neumann = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  
        '''
        VISUALIZATION
        import matplotlib.pyplot as plt
        labels = dict( ((i, j), i * 10 + j) for i, j in self.G.nodes() )
        nx.draw_networkx(self.G, pos=self.coords, labels=labels)

        plt.axis('off')
        plt.show()
        '''
        
    def get_neighbors_moore(self, pos):
        n = []
        for i in self.moore:
            pass
            
    # def get_neighbors(self, pos):
    #     return list(self.G.neighbors(pos))

    def mating_spots(self, coords):
        pass
"""