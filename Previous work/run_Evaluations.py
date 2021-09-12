from backend import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from sklearn.svm import SVC
from sklearn.neighbors import NearestCentroid
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

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

dataset = "7balls.txt"
dataFeatures = {"iris.txt": [(0, 1), (1, 2), (2, 3)],
                "seeds.txt": [(0, 1), (2, 3, 4), (5, 6)],
                "7balls.txt": [(0, 1), (1, 2), (0, 2)],
                "yeast.txt": [(0, 1), (2, 3, 4), (5, 6, 7)]}
somFeatures = dataFeatures[dataset]


data, _ = read_to_vec("data/" + dataset)
vectors, n_dim, n_class = read_to_vec_with_class("data/" + dataset)

## Classification metrics over iterations
lvqMaxIter = 100
maxIter = 5
lvqTime = []
svmTime = []

classifiers = {SVC(): 'SVM', tree.DecisionTreeClassifier(): 'DT',
               RandomForestClassifier(): 'RF', GaussianNB(): 'NB',
               NearestNeighbors(n_neighbors = 6): 'KNN'}
accuracies = {classifier: [] for classifier in classifiers.values()}
accuracies['IterN'] = []
accuracies['LVQ'] = []

for iterN in range(1, maxIter):
    print("Iteration:", iterN)
    ds = DeepSOM(iterN) 
    sideX = [15, 15, 15, 20]
    a = ds.add_MapHex(iterN, -1, [sideX[0], sideX[0]], 0, 0, 0.2)
    ds.set_get_data(a, lambda x: get_data(x, somFeatures[0]))
    d = ds.add_MapHex(iterN, -1, [sideX[1], sideX[1]], 0, 0, 0.2)
    ds.set_get_data(d, lambda x: get_data(x, somFeatures[1]))
    b = ds.add_MapRect(iterN, 2, [sideX[2], sideX[2]], 0, 0, 0.2)
    ds.set_get_data(b, lambda x: get_data(x, somFeatures[2]))
    c = ds.add_MapHex(iterN, -1, [sideX[3], sideX[3]], 0, 0, 0.2)
    ds.set_get_output(c, get_output)
    ds.set_combine(c, combine)
    ds.add_link(a, c)
    ds.add_link(b, c)
    ds.add_link(d, c)
    ds.batch_train_block(data)
    print("End Iter")
    output_som = ds.get_SOM(ds.get_root())
    dim = len(output_som.get_nodes()[0].position)
    lvq = LVQ(lvqMaxIter, dim, n_class, 0.5, 0)
    #classifiers[lvq] = 'LVQ'
    # metrics = somCVMetric(ds, lvq, vectors, sigfigs = 4, k = 4, deepSOM = True,
    #                   deepSOMGetOutput = get_output, funcs = [lvqAccuracy])
    trainClassifiers = [lvq] + list(classifiers)
    metrics = sklearnCVMetric(ds, trainClassifiers, vectors, deepSOM = True, k = 4,
                              deepSOMGetOutput = get_output, skfuncs = [accuracy_score])
    for classifier in metrics:
        tdata = metrics[classifier]
        if classifier == lvq:
            classifierName = 'LVQ'
        else:
            classifierName = classifiers[classifier]
        accuracies[classifierName].append(tdata[accuracy_score])
    accuracies['IterN'].append(iterN)
    # lvqTime.append([iterN, metrics[classifiers[0]][accuracy_score]])
    # svmTime.append([iterN, metrics[classifiers[1]][accuracy_score]])

print(metrics)
#lvqDF = pd.DataFrame(lvqTime, columns = ['IterN', 'Accuracy'])
#svmDF = pd.DataFrame(svmTime, columns = ['IterN', 'Accuracy'])

#lvqDF.to_csv("feasibility/data/LVQ Accuracy.csv")
#svmDF.to_csv("feasibility/data/SVM Accuracy.csv")
print(accuracies)
df = pd.DataFrame(accuracies)
colors = {'LVQ': 'blue', 'SVM': 'red', 'DT': 'green', 'RF': 'darkgreen', 'NB': 'Purple'}
for item in accuracies:
    if item != 'IterN':
        plt.plot(df['IterN'], df[item], color = colors[item], label = item)
#plt.plot(svmDF['IterN'], svmDF['Accuracy'], color = "red", label = "SVM")
plt.legend()
plt.savefig("feasibility/plots/AccuracyPlot")
plt.clf()
