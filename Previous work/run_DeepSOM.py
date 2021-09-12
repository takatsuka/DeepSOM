from backend import *
import numpy as np
from matplotlib import pyplot as plt

from sklearn.svm import SVC
from sklearn.neighbors import NearestCentroid
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, \
                            precision_score, f1_score   

def combine(vecs):  # Vecs is the output of get_output()
    # Currently uses topological coordinates
    return np.concatenate(vecs)  # Combine using brute force

def get_data(data, indices):
    final_data = []
    for i in indices:
        final_data.append(data[i])  
    return final_data

def get_output(som, data_vec):  # SOM output (can be topological or feature space vector)
    return som.find_bmu(data_vec).position

iter_n = 200
dataset = "iris.txt"
data, _ = read_to_vec("data/" + dataset)
vectors, n_dim, n_class = read_to_vec_with_class("data/" + dataset)

ds = DeepSOM(iter_n)  # Deep SOM object

sideX = [15, 15, 15, 30]  # SOM side lengths
sideY = sideX

## Example Deep SOM Structure:
    # a  -\
    # b  --->  c
    # d  -/

    # Where a receives features (1, 2); b receives (2, 3); c receives (1, 3)

## a, b, d are data input SOMs (Root nodes)
a = ds.add_MapHex(iter_n, -1, [sideX[0], sideY[0]])  # One SOM
    # Parameters: number of iterations, feature input dimensions, SOM side lengths
ds.set_get_data(a, lambda x: get_data(x, (0, 1)))
    # Definite input data into a som

d = ds.add_MapHex(iter_n, -1, [sideX[1], sideY[1]])
ds.set_get_data(d, lambda x: get_data(x, (1, 2)))

b = ds.add_MapRect(iter_n, 2, [sideX[2], sideY[2]])
ds.set_get_data(b, lambda x: get_data(x, (0, 2)))

# Larger SOM combining the three two-feature SOMs a, b, d
c = ds.add_MapHex(iter_n, -1, [sideX[3], sideY[3]])

# Set the SOM combination and SOM output parameters for the SOM:
ds.set_get_output(c, get_output)
    # Currently SOMs output feature space vectors (for the BMU of each training example)
ds.set_combine(c, combine)
    # Currently a concatenation

ds.add_link(a, c)  # Link a -> c
ds.add_link(b, c)  # Link b -> c
ds.add_link(d, c)  # Link c -> d

ds.batch_train_block(data)
#print(data)
output_som = ds.get_SOM(ds.get_root())
dim = len(output_som.get_nodes()[0].position)
lvq = LVQ(100, dim, n_class, 0.5, 0)  # t_lim, inp_dim, total_class, alpha, l

metrics = somCVMetric(ds, lvq, vectors, sigfigs = 4, k = 4, deepSOM = True,
                      deepSOMGetOutput = get_output,
                      funcs = [lvqAccuracy])               
print("LVQ:", metrics)

svmMetrics = sklearnCVMetric(ds, SVC(), vectors, deepSOM = True, k = 4,
                             deepSOMGetOutput = get_output, 
                             skfuncs = [accuracy_score])
print("SVM:", svmMetrics)

svmMetrics = sklearnCVMetric(ds, NearestCentroid(), vectors, deepSOM = True, k = 4,
                             deepSOMGetOutput = get_output, 
                             skfuncs = [accuracy_score])
print("KNN:", svmMetrics)

svmMetrics = sklearnCVMetric(ds, GaussianNB(), vectors, deepSOM = True, k = 4,
                             deepSOMGetOutput = get_output, 
                             skfuncs = [accuracy_score])
print("Gaussian Naive Bayes:", svmMetrics)

svmMetrics = sklearnCVMetric(ds, tree.DecisionTreeClassifier(), vectors, deepSOM = True, k = 4,
                             deepSOMGetOutput = get_output, 
                             skfuncs = [accuracy_score])
print("Decision Tree:", svmMetrics)

svmMetrics = sklearnCVMetric(ds, RandomForestClassifier(), vectors, deepSOM = True, k = 4,
                             deepSOMGetOutput = get_output, 
                             skfuncs = [accuracy_score])
print("Random Forest:", svmMetrics)

#plotDeepSOM4D(ds, vectors, showPlot = 1, classes = True)
plotDeepSOM3D(ds, vectors, showPlot = 1, classes = True)

## Plotting code:
# ds_vis = visualise_deep_som(ds, 3, hex_grid=True)
# for i in range(len(ds_vis)):
#     filename = "deep_som_vis" + "_" + str(i) + ".png"
#     with open(filename, 'wb') as f:
#         f.write(ds_vis[i].getvalue())

SOMs = [ds.get_SOM(i) for i in range(4)]
UMatrices = [UMatrix(item) for item in SOMs]
fig, axs = plt.subplots(nrows = 1, ncols = 4, figsize = (12, 5))
for idx, item in enumerate(UMatrices):
    axs[idx].imshow(item, cmap = "RdBu_r")
    # plt.colorbar()
plt.savefig("UMatrixDeepSOM.png")
plt.clf()

# som2 = ds.get_SOM(ds.get_root())
# xs, ys = [], []
# for node in som2.get_nodes():
#     xs.append(node.position[0])
#     ys.append(node.position[1])
# plt.scatter(xs, ys, c = "red", s = 1)

# dataXs, dataYs = [], []
# for item in data:
#     dataXs.append(item[0])
#     dataYs.append(item[1])
# plt.scatter(dataXs, dataYs, c = "purple", s = 0.5)

# plt.savefig("DeepSOMScatter.png")

#genHTMLPlot(ds.get_SOM(ds.get_root()), data, showPlot = 1)

# a = ds.get_SOM(0)
# visualise(a)


