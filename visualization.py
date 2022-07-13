from matplotlib import image
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import numpy as np
import imageio
import os
from itertools import compress
# from IPython import display


""" IDEAS FOR VISUALIZATION """
# plot the grid cells at each step
# plot a dot in the center of each occupied cell
# the color of the dot is the mean age in the spot
# the size of the dot is the number of agents in the spot

def gif(model, path, filename = 'SIM', delete_frames = True, **kwargs):
    
    if path[-1] != os.sep:
        path += os.sep
    
    x, y = model.environment.x, model.environment.y
    zmin = 0
    zmax = np.quantile([np.max(model.frames[i]) for i in range(len(model.frames))], q = 0.9)
    # zmax = max([np.max(model.frames[i]) for i in range(len(model.frames))])
    
    print('Retrieving frames ...')
    for i in range(len(model.frames)):
        z = model.frames[i]
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        c = ax.pcolormesh(x, y, z, cmap = 'viridis', vmin = zmin, vmax = zmax, shading = 'auto')
        plt.savefig('../results/frame_%s.png' % i, dpi = 200)
        plt.close()
        
    print('Creating gif')
    # writer = imageio.get_writer('%sSIM.gif' % path, mode = 'I')
    imgs = []
    for i in range(len(model.frames)):
        fig = imageio.imread('../results/frame_%s.png' % i)
        imgs.append(fig)
        # writer.append_data(fig)
    imageio.mimsave(path + filename + '.gif', imgs, **kwargs)
        
    #writer.close()
    if delete_frames:
        frames = os.listdir('../results/')
        frames = list(compress(frames, ['png' in i for i in frames]))
        for f in frames:
            os.remove('../results/%s' % f)