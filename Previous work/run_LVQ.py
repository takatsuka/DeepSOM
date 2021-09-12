from backend import read_to_vec, visualise_som_layer, error_entropy, \
    genHTMLPlot, errorColorPlot, performPCA, gen4DPlot, \
    cooccurenceMetric, hex_visualise_som, read_to_vec_with_class, \
    lvqAccuracy, lvqRecall, lvqPrecision, lvqF1Score, lvqConfusionMatrix, \
    lvqCMRavel, lvqGenericMetric, cvMetric, somCVMetric
from backend import MapRect, MapHex, Node, LVQ
# from sklearn.metrics import jaccard_score

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sklearn.decomposition import PCA

## Import Data:
dataset = "iris.txt"  # Iris: A classic 4D Dataset with class 
data, _ = read_to_vec("data/" + dataset)
n_lines = len(data)
vectors, n_dim, n_class = read_to_vec_with_class("data/" + dataset)
    # vectors is a list of (class, vector) tuples
    # n_class is the number of unique classes
    # n_dim is number of data dimension (4 for Iris)

## Train the SOM (Or use a pre-trained som)
som_map = MapHex(100, n_dim, [20, 20], 0, 0, 0.8)  # SOM class
    # MapRect Arguments: t_lim, inp_dim, vector of lengths, sigma, lambda, alpha

som_map.batch_train(data)  # Train the SOM first

## Set SOM Map Here: (Last layer of DeepSOM)
mp = som_map
#####

## Train the LVQ, based on mp:
node_data = []  # Input to LVQ generated from SOM
for label, vector in vectors:  # Class label and vector from dataset
        # Computes BMU for each data vector and associated the BMU position
            # with the class of the data vector
        # The idea is to train the LVQ on the last layer on the Deep SOM,
            # generating the same map as the SOM, but with associated class

    node = mp.find_bmu(vector)
    node_data.append([label, np.array(node.position)])  # Format for LVQ train

lvq = LVQ(100, n_dim, n_class, 1, 0)  # t_lim, inp_dim, total_class, alpha, l
lvq.train(node_data)  # Train the LVQ using SOM output

## Output performance metrics:
print("\n")
print(f"Accuracy: {round(lvqAccuracy(lvq, node_data), 4)}")
print(f"Precision: {round(lvqPrecision(lvq, node_data), 4)}")
print(f"Recall: {round(lvqRecall(lvq, node_data), 4)}")
print(f"F1-Score: {round(lvqF1Score(lvq, node_data), 4)}")
# print(f"(Example) Jaccard Similarity Coefficient Score: {round(lvqGenericMetric(lvq, node_data, func = jaccard_score, average = 'micro'), 4)}")

print(f"\nConfusion Matrix: \n{lvqConfusionMatrix(lvq, node_data)}")
# tn, fp, fn, tp = lvqCMRavel(lvq, vectors)
    # Only works for two-class case
# print(f"True Negatives: {tn}; False Positives: {fp}; False Negatives: {fn}; True Positives: {tp}")

cvMetrics = cvMetric(lvq, node_data, k = 6, sigfigs = 4,
                     funcs = [lvqAccuracy, lvqPrecision, lvqRecall, lvqF1Score])
    # CV should be run at the end as it changes the LVQ object (re-training)
    # Returns a dictionary of (function object: accuracy metric)

cvAccuracy = cvMetrics[lvqAccuracy]
cvPrecision = cvMetrics[lvqPrecision]
cvRecall = cvMetrics[lvqRecall]
cvF1Score = cvMetrics[lvqF1Score]

print(f"CV Accuracy: {cvAccuracy}")
print(f"CV Precision: {cvPrecision}")
print(f"CV Recall: {cvRecall}")
print(f"CV F1-Score: {cvF1Score}")


print(somCVMetric(mp, lvq, vectors, k = 6, sigfigs = 4, deepSOM = False,
                  funcs = [lvqAccuracy, lvqPrecision, lvqRecall, lvqF1Score]))
## Plot Iris in color
# gen4DPlot(mp, data, showPlot=1)