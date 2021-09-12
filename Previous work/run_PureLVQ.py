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
# data, _ = read_to_vec("data/" + dataset)
# n_lines = len(data)
vectors, n_dim, n_class = read_to_vec_with_class("data/" + dataset)
    # vectors is a list of (class, vector) tuples
    # n_class is the number of unique classes
    # n_dim is number of data dimension (4 for Iris)


lvq = LVQ(100, n_dim, n_class, 1, 0)  # t_lim, inp_dim, total_class, alpha, l
lvq.train(vectors)  # Train the LVQ using SOM output

## Output performance metrics:
# print("\n")
# print(f"Accuracy: {round(lvqAccuracy(lvq, vectors), 4)}")
# print(f"Precision: {round(lvqPrecision(lvq, vectors), 4)}")
# print(f"Recall: {round(lvqRecall(lvq, vectors), 4)}")
# print(f"F1-Score: {round(lvqF1Score(lvq, vectors), 4)}")
# print(f"(Example) Jaccard Similarity Coefficient Score: {round(lvqGenericMetric(lvq, node_data, func = jaccard_score, average = 'micro'), 4)}")

print(f"\nConfusion Matrix: \n{lvqConfusionMatrix(lvq, vectors)}")
# tn, fp, fn, tp = lvqCMRavel(lvq, vectors)
    # Only works for two-class case
# print(f"True Negatives: {tn}; False Positives: {fp}; False Negatives: {fn}; True Positives: {tp}")

# cvMetrics = cvMetric(lvq, vectors, k = 5, sigfigs = 4,
#                      funcs = [lvqAccuracy, lvqPrecision, lvqRecall, lvqF1Score])
    # CV should be run at the end as it changes the LVQ object (re-training)
    # Returns a dictionary of (function object: accuracy metric)

# cvAccuracy = cvMetrics[lvqAccuracy]
# cvPrecision = cvMetrics[lvqPrecision]
# cvRecall = cvMetrics[lvqRecall]
# cvF1Score = cvMetrics[lvqF1Score]

# print(f"CV Accuracy: {cvAccuracy}")
# print(f"CV Precision: {cvPrecision}")
# print(f"CV Recall: {cvRecall}")
# print(f"CV F1-Score: {cvF1Score}")

## Plot Iris in color
# gen4DPlot(mp, data, showPlot=1)