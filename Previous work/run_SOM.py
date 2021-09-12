## Run visualisation tests from here

from backend import read_to_vec, visualise_som_layer, error_entropy, \
    genHTMLPlot, errorColorPlot, performPCA, gen4DPlot, \
    cooccurenceMetric, hex_visualise_som, read_to_vec_with_class, \
    LVQ, lvqAccuracy, lvqPrecision, lvqRecall, somCVMetric, lvqF1Score, \
    genPCAPlot
from backend import MapRect, MapHex, Node

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sklearn.decomposition import PCA

# visualise_som_layer(mp)  # Generate 2D clustering (distance) visualisation (test_img.png)

def basicExample():
    #dataset = "grasps.txt"
    dataset = "scurve01.txt"
    data, _ = read_to_vec("data/" + dataset)
    #(int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha)
    n = 30
    mp = MapHex(2, 3, [n, 25], 0, 0, 0.7)  # SOM class
        # MapRect Arguments: t_lim, inp_dim, vector of lengths, sigma, lambda, alpha
    mp.batch_train(data)
    #print(error_entropy(mp, data))
    return mp, data

def classExample():
    vectors, n_dim, n_class = read_to_vec_with_class("data/7balls.txt")
    mp = MapHex(200, n_dim, [20, 20], 0, 0, 0.7)  # SOM class
    mp.batch_train([item[1] for item in vectors])
    return mp, vectors, n_dim, n_class

def metricExample():
    dataset = "iris.txt"
    data, _ = read_to_vec("data/" + dataset)
    vectors, n_dim, n_class = read_to_vec_with_class("data/" + dataset)
    #(int t_lim, int inp_dim, vector<int> lengths, int sigma, double l, double alpha)
    n = 20
    mp = MapHex(200, n_dim, [n, n], 0, 0, 0.7)  # SOM class
    # MapRect Arguments: t_lim, inp_dim, vector of lengths, sigma, lambda, alpha
    mp.batch_train(data)
    #print(error_entropy(mp, data))
    return mp, data, vectors, n_dim, n_class

def pcaExample():
    data, _ = read_to_vec("data/" + "tic-tac-toe.txt")
    pca, data, pcaVar = performPCA(data, n_comps = 3)
    mp = MapHex(100, 3, [10, 10], 0, 0, 0.7)
    mp.batch_train(data)    
    genHTMLPlot(mp, data)
    return mp, data

def fourDColorExample():
    data, _ = read_to_vec("data/" + "grasps.txt")
    pca, data, pcaVar = performPCA(data, n_comps = 4)
    mp = MapHex(100, 4, [10, 10], 0, 0, 0.7)
    mp.batch_train(data)    
    gen4DPlot(mp, data)
    return mp, data

def entropyTraining(data, datasetName):
    max_t = 100
    entropys = []

    mp = MapHex(max_t, 3, [20, 20], 10, 32, 0.3)

    def lm(som, t):
        print(t)
        entropys.append(error_entropy(som, data))
    mp.batch_train_cb(data, lm)

    plt.clf()
    plt.plot(list(range(0, max_t)), entropys, c = "purple")
    plt.title("Error Entropy Over Training, For " + datasetName)
    plt.xlabel("Number of Training Iterations")
    plt.ylabel("Continuous Error Entropy")
    plt.savefig("entropyfig.png")

    return list(range(0, max_t)), entropys, mp

def errorHist(mp, data):
    errors = []
    for vector in data:
        bmu = mp.find_bmu(vector)
        errors.append(np.linalg.norm(bmu.position - vector))
    plt.hist(errors)
    plt.savefig("errorhist.png")


#iters, entropys, mp = entropyTraining()

#errorHist(mp, data)

#errorColorPlot(mp, data)  # SOM colored by error

#mp, data = fourDColorExample()

#mp, data = pcaExample()

#mp, data = basicExample()
#hex_visualise_som(mp)

# mp, data, vectors, n_dim, n_class = metricExample()
# hex_visualise_som(mp)
# genPCAPlot(mp, vectors, showPlot = 1, classes = True)
# lvq = LVQ(100, n_dim, n_class, 1, 0)  # t_lim, inp_dim, total_class, alpha, l
# metrics = somCVMetric(mp, lvq, vectors, sigfigs=4, k=8, deepSOM=False,
#                       funcs=[lvqAccuracy, lvqPrecision, lvqRecall, lvqF1Score])  # , lvqF1Score])
# print(metrics)
#print(cooccurenceMetric(mp, data))

mp, vectors, n_dim, n_class = classExample()
genPCAPlot(mp, vectors, showPlot = 1, classes = True)
