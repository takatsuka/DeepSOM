from backend import read_to_vec, genHTMLPlot, UMatrix, visualise_deep_som
from backend import DeepSOM, MapRect, Node, MapHex
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

def combine(vecs):  # Vecs is the output of get_output()
    # Currently uses topological coordinates
    return np.concatenate(vecs)  # Combine using brute force

def get_data(data, id_v):
    return data[id_v:id_v + 2]  
    # For 7balls.txt, use dimensions [1, 2] and [2, 3] to train SOMs A and B, respectively

def get_output(som, data_vec):  # SOM output (can be topological or feature space vector)
    bmus = som.find_bmu_k(data_vec, 1)
    
    # Masa's suggestion:
    # return [bmus[0].topo[0], bmus[0].topo[1], sum((data_vec - bmus[0].position)**2), 
    #         bmus[1].topo[0], bmus[1].topo[1], sum((data_vec - bmus[1].position)**2), 
    #         bmus[2].topo[0], bmus[2].topo[1], sum((data_vec - bmus[2].position)**2)]
    
    # Masa's suggestion, but with BMU position instead of error
    # return [bmus[0].topo[0], bmus[0].topo[1], sum(bmus[0].position**2), 
    #         bmus[1].topo[0], bmus[1].topo[1], sum(bmus[1].position**2), 
    #         bmus[2].topo[0], bmus[2].topo[1], sum(bmus[2].position**2)]

    # BMU position only
    # return [sum(bmus[0].position**2), sum(bmus[1].position**2), sum(bmus[2].position**2)]

    # Topo only
    # return [bmus[0].topo[0], bmus[0].topo[1], 
    #         bmus[1].topo[0], bmus[1].topo[1], 
    #         bmus[2].topo[0], bmus[2].topo[1]]

    # Top 3 BMU Concatenated Positions
    return list(bmus[0].position) #+ list(bmus[1].position) + list(bmus[2].position)

    # output = []
    # for node in bmus:
    #     output.append(node.topo[0])
    #     output.append(node.topo[1])
    #     output.append(np.linalg.norm(data_vec - node.position))
    # return output


iter_n = 100
data, _ = read_to_vec("data/7balls.txt")

ds = DeepSOM(iter_n)  # Deep SOM object

sideX = [15, 15, 15, 30]  # SOM side lengths
sideY = sideX

## Example Deep SOM Structure:
    # a  -\
    # b  --->  c
    # d  -/

    # Where a receives features (1, 2); b receives (2, 3); c receives (1, 3)

## a, b, d are data input SOMs (Root nodes)
a = ds.add_MapHex(iter_n, 2, [sideX[0], sideY[0]])  # One SOM
    # Parameters: number of iterations, feature input dimensions, SOM side lengths
ds.set_get_data(a, lambda x: get_data(x, 0))
    # Definite input data into a

d = ds.add_MapRect(iter_n, 2, [sideX[1], sideY[1]])
ds.set_get_data(d, lambda x: x[[0,2]])

b = ds.add_MapRect(iter_n, 2, [sideX[2], sideY[2]])
ds.set_get_data(b, lambda x: get_data(x, 1))

# Larger SOM combining the three two-feature SOMs a, b, d
c = ds.add_MapRect(iter_n, 6, [sideX[3], sideY[3]])

# Set the SOM combination and SOM output parameters for the SOM:
ds.set_get_output(c, get_output)
    # Currently SOMs output feature space vectors (for the BMU of each training example)
ds.set_combine(c, combine)
    # Currently a concatenation

ds.add_link(a, c)  # Link a -> c
ds.add_link(b, c)  # Link b -> c
ds.add_link(d, c)  # Link c -> d

print("Training")
ds.batch_train(data)

## Plotting code:
print("Visualising")
visualise_deep_som(ds, 4, "Top 1, Concatenated Pos")
# SOMs = [ds.get_SOM(i) for i in range(4)]
# UMatrices = [UMatrix(item) for item in SOMs]

# fig, axs = plt.subplots(nrows = 1, ncols = 4, sharex = False, figsize = (12, 5))
# for idx, item in enumerate(UMatrices):
#     axs[idx].imshow(item, cmap = "RdBu_r")
#     #plt.colorbar()
# plt.show()


# som2 = ds.get_SOM(0)
# xs, ys = [], []
# for node in som2.get_nodes():
#     xs.append(node.position[0])
#     ys.append(node.position[1])
# plt.scatter(xs, ys, s = 0.5)

# dataXs = []
# dataYs = []
# for item in data:
#     dataXs.append(item[0])
#     dataYs.append(item[1])


# #print(dataXs, dataYs)
# plt.scatter(dataXs, dataYs, c = "red", s = 0.5)

# plt.show()
# #a = ds.get_SOM(0)
# #visualise(a)


