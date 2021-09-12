from typing import *
import numpy as np
import matplotlib.pyplot as plt
from entropy_estimators import continuous
from .imports import *
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, \
                            precision_score, f1_score   
from sklearn.model_selection import KFold, StratifiedKFold
import copy

def supported_file(filename):
    """
    Checks if a file is of a supported file type.
    """
    VALID_EXT = ["txt"]
    return any([("." in filename and filename.rsplit(".")[1].lower() == ext) 
                for ext in VALID_EXT])

def read_to_vec(filename):
    if isinstance(filename, str):
        f = open(filename, 'r')
    else:
        f = filename

    file_dim = f.readline().split()
    if len(file_dim) != 2:
        f.close()
        raise IOError(f"Invalid data file structure, file_dim was {len(file_dim)}")
    
    vec_length = int(file_dim[0])
    n_lines = int(file_dim[1])
    vectors = []

    for _ in range(n_lines):
        line = f.readline()
        if line == "":
            f.close()
            raise IOError("Invalid data file structure")
        vectors.append(np.asarray(list(map(float, line.split()[:vec_length]))))
    
    # scalar = MinMaxScaler()
    # scalar.fit(vectors)
    # vectors = scalar.transform(vectors)

    if isinstance(filename, str):
        f.close()
    return vectors, vec_length

def read_to_vec_with_class(filename):
    if isinstance(filename, str):
        f = open(filename, 'r')
    else:
        f = filename

    file_dim = f.readline().split()
    if len(file_dim) != 2:
        f.close()
        raise IOError("Invalid data file structure, file_dim was {}".format(len(file_dim)))
    
    vec_length = int(file_dim[0])  # Number of dimensions
    n_lines = int(file_dim[1])  # Number of data vectors 
    vectors = []

    for _ in range(n_lines):
        line = f.readline()
        if line == "":
            f.close()
            raise IOError("Invalid data file structure")
        split_line = line.split()
        vectors.append((split_line[vec_length], 
                        np.asarray(list(map(float, split_line[:vec_length])))))
    unique_types = list(set(map(lambda x: x[0], vectors)))
    mapper = {}
    for i in range(len(unique_types)):
        mapper[unique_types[i]] = i 
    for i in range(len(vectors)):
        vectors[i] = (mapper[vectors[i][0]], vectors[i][1])
    
    # labels, data = zip(*vectors)
    # scalar = MinMaxScaler()
    # scalar.fit(data)
    # vectors = scalar.transform(data)
    # vectors = list(zip(labels, data))

    if isinstance(filename, str):
        f.close()
    return vectors, vec_length, len(unique_types)

def UMatrix(som_map):
    neuron_distances: List[List[float]] = []
    all_nodes = som_map.get_nodes()
    for i in range(som_map.lengths[1]):
        temp_row: List[float] = []
        for j in range(som_map.lengths[0]):
            n = all_nodes[i*som_map.lengths[0]+j]
            neighbors: List[Node] = n.neighbors
            temp_row.append(
                sum(map(lambda x: np.linalg.norm(n.position-x),
                        map(lambda x: x.position, neighbors)))/len(neighbors))
        neuron_distances.append(temp_row)
    return neuron_distances

def generate_data_file(num_points:int, c1 = (-10, 0, 0), c2 = (10, 10, 10), 
                       c3 = (0, 0, -15), sd = 1, filename = "3_clusters.txt"):
    # Creates 3 distinct clusters in 3D space and writes to given filename
    # num_points: number of points per cluster
    # c1, c2, c3: centres of each cluster
    # sd: SD with which the centres are perturbed by Gaussian noise

    centers = [c1, c2, c3]

    with open(filename, 'w') as file:
        file.write("3 {}\n".format(num_points))
        for _ in range(num_points):
            c = centers[np.random.randint(0,3)]
            dx,dy,dz = np.random.normal(loc=0,scale=sd,size=3)
            file.write("{} {} {}\n".format(c[0]+dx, c[1]+dy, c[2]+dz))


""" Compute continuous error entroping assuming Normal distribution
    From: https://github.com/paulbrodersen/entropy_estimators
    A more advanced custom entropy can be computed using k-nearest neighbor
        distances, as per Kozachenko and Leonenko (1987) and the extension
        developed by Kraskov et al (2004), and Frenzel and Pombe (2007) """
def error_entropy(som_map, data):
        # Accepts Map2D object and data in read_to_vec form
    errors = []
    for vector in data:
        bmu = som_map.find_bmu(vector)
        errors.append(np.linalg.norm(bmu.position - vector))
    analytic = continuous.get_h_mvn(errors) 
    # kozachenko = continuous.get_h(errors, k=5)
        # get_h should be re-written to determine neighbors based on 
            # SOM neighbors, not Euclidean distance of errors (I think)
    return analytic

def performPCA(data, n_comps = 3):
    rows = len(data)  # Number of rows
    columns = len(data[0])  # Number of columns
    np_data = np.zeros(shape = (rows, columns), dtype = float)
        # Data in numpy format (rows and columns, not list of rows)

    for row, item in enumerate(data):
        for col, val in enumerate(item):
            np_data[row][col] = val

    pca = PCA(n_components = n_comps, whiten = False, random_state = 1000)
    pcaData = pca.fit_transform(np_data)
    pcaVar = pca.get_covariance()  # Covariance between original dimensions

    return (pca, pcaData, pcaVar)

def cooccurenceMetric(mp, data, th = 0.1):
    # th is the threshold for maximum percentage difference between node errors
    # Apolgies for the str(node) usage
        # C++ objects via pybind seem to resist being hashed properly
    strMap = {str(node):node for node in mp.get_nodes()}
    dataBMUs = {str(node):[] for node in mp.get_nodes()}
        # Dictionary of str(node): index of data vectors with this node as BMU
    #print(dataBMUs)
    for idx, vector in enumerate(data):  # Find BMU data vectors for all nodes
        bmu = mp.find_bmu(vector)
        dataBMUs[str(bmu)].append(idx)
    
    nodeErrors = {}  # Dict of str(node): mean error
    for node in dataBMUs:  # Find mean error for each node
        errors = []
        for idx in dataBMUs[node]:
            vector = data[idx]
            errors.append((strMap[node]).position - vector)
        if len(errors) == 0:
            nodeErrors[node] = 0
        else:
            nodeErrors[node] = np.mean(errors)

    nErrors = 0  # Total number of node links surpassing error threshold
    totalConnections = 0  # Total number of node-node links
    for node in mp.get_nodes():  # Find number of significant error differences
        for neighbor in node.neighbors:
            totalConnections += len(node.neighbors)

            err1 = nodeErrors[str(node)]
            err2 = nodeErrors[str(neighbor)]
            if (err2 > err1 + err1 * th) or (err2 < err1 - err1 * th):
                nErrors += 1

    return nErrors/ totalConnections  
    # Returns percentage or node links exceeding error threshold

def lvqPreds(lvq, vectors):  # Computes LVQ predictions for a dataset
    ground_truth = []
    preds = []
    for label, vector in vectors:
        ground_truth.append(label)

        pred = lvq.test(vector)
        preds.append(pred)
        #print(pred, label, end="; ")
    return ground_truth, preds

## All lvq metric functions accept an LVQ() object and a vectors list from read_to_vec_with_class

def lvqAccuracy(lvq, vectors):  # Accuracy
    ground_truth, preds = lvqPreds(lvq, vectors)
    return accuracy_score(ground_truth, preds)

# The 'weighted' method is used for multi-class Precision, Recall and F1-Score
    # Method: Calculate metrics for each label and find their average, 
    #   weighted by number of true instances per label (support).
    #   Can result in F-score not between precision and recall

def lvqRecall(lvq, vectors):  # Recall
    ground_truth, preds = lvqPreds(lvq, vectors)
    return recall_score(ground_truth, preds, average = 'weighted')

def lvqPrecision(lvq, vectors):  # Precision
    ground_truth, preds = lvqPreds(lvq, vectors)
    return precision_score(ground_truth, preds, average = 'weighted')

def lvqF1Score(lvq, vectors):  # F1-Score
    ground_truth, preds = lvqPreds(lvq, vectors)
    return f1_score(ground_truth, preds, average = 'weighted')

def lvqConfusionMatrix(lvq, vectors):  # Confusion matrix (in 2D)
    ground_truth, preds = lvqPreds(lvq, vectors)
    return confusion_matrix(ground_truth, preds)

def lvqCMRavel(lvq, vectors):  # Ravel-ed confusion matrix
    ground_truth, preds = lvqPreds(lvq, vectors)
    return confusion_matrix(ground_truth, preds).ravel()
        # For two-class case returns a tuple consisting of:
        #   (true negatives, false positives, false negatives, true positives)

def lvqGenericMetric(lvq, vectors, func = accuracy_score, **kwargs):
    # Computes any generic sklearn.metrics function for given LVQ and data
    # See: https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics
    # Metric must accept only y_true and y_pred 
        # y_pred must be predicting labels, not probability
    # Defaults to accuracy_score
    
    ground_truth, preds = lvqPreds(lvq, vectors)

    if 'average' in kwargs:
        average = kwargs['average']
        return func(ground_truth, preds, average = average)
    else:
        return func(ground_truth, preds)

def cvMetric(lvq, vectors, k = 5, sigfigs = 4, funcs = [lvqAccuracy]):
    # Perform cross-validation to calculate a performance metric
    # Input a trained or untrained LVQ and the *entire* dataset
    # k: Number of folds; funcs: metrics to be computed
    # funcs is an array of evaluation functions from this file

    data = []
    labels = []
    for label, vector in vectors:  # Extract vectors and labels from input
        data.append(vector)
        labels.append(label)
    data = np.array(data)
    labels = np.array(labels)

    kf = KFold(n_splits = k, shuffle = True)
    metrics = {func: [] for func in funcs}
        # List of values per fold for each metric
    avgMetrics = {func: 0 for func in funcs}
        # Average metric value across all folds
    for train_index, test_index in kf.split(data):  # Perform CV
        train_data, test_data = data[train_index], data[test_index]
        train_labels, test_labels = labels[train_index], labels[test_index]

        tempLVQ = lvq #copy.deepcopy(lvq)
            # The LVQ object is affected by running CV
        tempLVQ.train(list(zip(train_labels, train_data)))

        for func in metrics:  # Compute all metrics for current fold
            testVectors = zip(test_labels, test_data)
            metrics[func].append(func(tempLVQ, testVectors))

    for func in metrics:  # Compute metric averages
        avgMetrics[func] = round(np.mean(metrics[func]), 4)

    return avgMetrics
        
def genLVQPred(som, lvq, data_class, input_vec, deepSOM = False, deepSOMGetOutput = None):
    labels = []
    data = []
    for label, vector in data_class:
        labels.append(label)
        data.append(vector)
    data = np.array(data)
    labels = np.array(labels)

    som.batch_train_block(data)
    node_vectors = []  # Input to LVQ generated from SOM
    node_class = []
    node_data = []
    for label, vector in zip(labels, data):
        if not deepSOM:
            vector = som.find_bmu(vector).position  # BMU from trained SOM
        else:
            vector = som.test(vector, deepSOMGetOutput)
        node_vectors.append(vector)
        node_class.append(label)

    # a = MinMaxScaler()
    # a.fit(node_vectors)
    # node_vectors = a.transform(node_vectors)
    node_data = list(zip(node_class, node_vectors))

    lvq.train(node_data)
    return lvq.test(input_vec)

def somCVMetric(som, lvq, data_class, sigfigs = 4, k = 5, 
                funcs = [lvqAccuracy], deepSOM = False, deepSOMGetOutput = None):
    # NOTE: data_class is from read_to_vec_with_class, not SOM data
    # som is of type DeepSOM
    # deepSOMGetOutput is the get_output py function for the final layer
    labels = []
    data = []
    for label, vector in data_class:
        labels.append(label)
        data.append(vector)
    data = np.array(data)
    labels = np.array(labels)
    # print("\n\nLabels:", labels)
    kf = StratifiedKFold(n_splits = k, shuffle = True, random_state = 13377)
    metrics = {func: [] for func in funcs}
        # List of values per fold for each metric
    avgMetrics = {func: 0 for func in funcs}
        # Average metric value across all folds

    for train_index, test_index in kf.split(data, labels):  # Perform CV
        train_data, test_data = data[train_index], data[test_index]
            # Raw input data (from file)
        train_labels, test_labels = labels[train_index], labels[test_index]

        train_som = som  # Copy
        train_som.batch_train_block(train_data)  # Train on training set

        train_node_vectors = []  # Input to LVQ generated from SOM
        train_node_class = []
        train_node_data = []
        for label, vector in zip(train_labels, train_data):
            if not deepSOM:
                train_vector = train_som.find_bmu(vector).position  # BMU from trained SOM
            else:
                train_vector = train_som.test(vector, deepSOMGetOutput)
            train_node_vectors.append(train_vector)
            train_node_class.append(label)
            # train_node_data.append([label, train_vector])

        # a = MinMaxScaler()
        # a.fit(train_node_vectors)
        # train_node_vectors = a.transform(train_node_vectors)
        train_node_data = list(zip(train_node_class, train_node_vectors))
            #train_node_data.append([label, train_vector])

        test_som = som  # Copy
        test_som.batch_train_block(test_data)

        test_node_vectors = []
        test_node_class = []
        test_node_data = []  # Input to LVQ generated from SOM
        for label, vector in zip(test_labels, test_data):
            if not deepSOM:
                test_vector = test_som.find_bmu(vector).position
            else:
                test_vector = test_som.test(vector, deepSOMGetOutput)
                # node = deepTestOutput.find_bmu(vector)
            test_node_vectors.append(test_vector)
            test_node_class.append(label)
            #test_node_data.append([label, test_vector])

        # aa = MinMaxScaler()
        # aa.fit(test_node_vectors)
        # test_node_vectors = aa.transform(test_node_vectors)
        test_node_data = list(zip(test_node_class, test_node_vectors))
            
        tempLVQ = lvq #copy.deepcopy(lvq)
            # The LVQ object is affected by running CV

        tempLVQ.train(train_node_data)

        for func in metrics:  # Compute all metrics for current fold
            metrics[func].append(func(tempLVQ, test_node_data))

    for func in metrics:  # Compute metric averages
        avgMetrics[func] = round(np.mean(metrics[func]), sigfigs)
    # print(metrics)

    return avgMetrics

from sklearn.svm import SVC
from sklearn.neighbors import NearestCentroid
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def sklearnCVMetric(som, classifiers, data_class, sigfigs = 4, k = 5, 
                skfuncs = [accuracy_score], deepSOM = False, 
                deepSOMGetOutput = None):
    # NOTE: data_class is from read_to_vec_with_class, not SOM data
    # Also works for Deep SOM
    # deepSOMGetOutput is the get_output py function for the final layer
    # classifiers is a list of sklearn-compatible classifier objects
        # E.g: SVC(), NearestCentroid(), GaussianNB(), RandomForestClassifier()
        #      tree.DecisionTreeClassifier(), 
    # skfuncs is a list of scikit learn metric functions
        # E.g: accuracy_score, precision_score, recall_score, f1_score 
    labels = []
    data = []
    for label, vector in data_class:
        labels.append(label)
        data.append(vector)
    data = np.array(data)
    labels = np.array(labels)

    kf = StratifiedKFold(n_splits = k, shuffle = True, random_state = 13377)
    for train_index, test_index in kf.split(data, labels):  # Perform CV
        train_data, test_data = data[train_index], data[test_index]
            # Raw input data (from file)
        train_labels, test_labels = labels[train_index], labels[test_index]

        train_som = som  # Copy
        train_som.batch_train_block(train_data)  # Train on training set

        train_node_vectors = []  # Input to LVQ generated from SOM
        train_node_class = []
        for label, vector in zip(train_labels, train_data):
            if not deepSOM:
                train_vector = train_som.find_bmu(vector).position  # BMU from trained SOM
            else:
                train_vector = train_som.test(vector, deepSOMGetOutput)
            train_node_vectors.append(train_vector)
            train_node_class.append(label)

        test_som = som  # Copy
        test_som.batch_train_block(test_data)

        test_node_vectors = []  # Input to LVQ generated from SOM
        test_node_class = []
        for label, vector in zip(test_labels, test_data):
            if not deepSOM:
                test_vector = test_som.find_bmu(vector).position
            else:
                test_vector = test_som.test(vector, deepSOMGetOutput)
            test_node_vectors.append(test_vector)
            test_node_class.append(label)
        
        classifierMetrics = {}
        # clf = make_pipeline(MinMaxScaler(), classifier)
        for classifier in classifiers:
            clf = classifier
            clf.fit(np.array(train_node_vectors), np.array(train_node_class))
            
            skmetrics = {func: [] for func in skfuncs}
                # List of values per fold for each metric
            for skfunc in skmetrics:  # Compute all metrics for current fold
                preds = clf.predict(test_node_vectors)
                if skfunc in (precision_score, recall_score, f1_score):
                    skmetrics[skfunc].append(skfunc(test_node_class, preds,
                                             average = 'weighted'))
                else:
                    skmetrics[skfunc].append(skfunc(test_node_class, preds))
            classifierMetrics[classifier] = skmetrics
    
    avgClassifierMetrics = {}
    for classifier in classifierMetrics:
        skmetrics = classifierMetrics[classifier]
        
        avgSKMetrics = {func: 0 for func in skfuncs}
            # Average metric value across all folds
        for skfunc in skmetrics:  # Compute metric averages
            avgSKMetrics[skfunc] = round(np.mean(skmetrics[skfunc]), sigfigs)
        avgClassifierMetrics[classifier] = avgSKMetrics

    return avgClassifierMetrics
