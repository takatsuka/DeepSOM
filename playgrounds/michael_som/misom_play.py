import numpy as np
from misom import Som
import pickle
import random
import matplotlib.pyplot as plt
import sys

def save_model(som, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(som, outp, pickle.HIGHEST_PROTOCOL)

def load_model(filename):
    with open(filename, 'rb') as inp:
        return pickle.load(inp)
"""
   SOM implementation for dim reduction:
   Size of grid should contain at least 5*(N**0.5) neurons where N is number of data points in dataset.
   e.g, if you have 400 data points -> SOM should contain 5*20 = 100 neurons (10 x 10 map)
   
   My SOM: x is width of competitive layer, y is height of competitive layer, dim is length of single data 
   row, sigma is a param of neighbour func that decreases each iter, sigma = sigma/(1+iter/(num_iters/2))
   by the decay func that also decreases learning rate lr = lr / (1+iter/(max_iters/2))
   
   Assumptions: eucl distance metric, gaussian neighbour func, rectangular topology (can add others later)
   """

#Generating random data points, 20 x 20 grid, 400 data points between (0,1)

#data = []
#for row in range(20):
    #data.append([])
    #[data[row].append(random.uniform(0,1)) for column in range(20)]


#Now trying Haoyan's sphere_256.txt

datastr = [l.strip().split(',') for l in open(sys.argv[1]).readlines()]
data = [[float(c) for c in e] for e in datastr]


#Generate and train SOM, be mindful of params to fit to data (more research needed)

som = Som(100, 100, 3, 10, 0.5)
som.train(data, 16384)


#Print all SOM weights

som_weights = som.get_weights()
print("All SOM weights")
print(som_weights)
print(5*"\n")


# Copy pasta haoyan graphing code

flatten_weights = [elem for l in som_weights for elem in l] # flattening weights list for graph

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

axes = list(zip(*flatten_weights))     # Seems to work when i fiddle with sigma
axes_o = list(zip(*data))
ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))

ax.scatter(*axes, marker='o', s=1)
ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.savefig(f"misom_donut.png")


#Pickle save / load

# Save
save_model(som, 'misom.p')
# Load
loaded_som = load_model('misom.p')

print("Printing All SOM weights after reloading from pickle")
print(loaded_som.get_weights())