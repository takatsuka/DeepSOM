from celery import Celery
from backend import DeepSOM
from backend import LVQ
from backend.PyFront.util import *
from backend.PyFront.visualisations import *
from backend.PyFront.plot3D import *
import numpy as np
import os, io, random, copy
from sklearn.metrics import jaccard_score
from sklearn.svm import SVC
from sklearn.neighbors import NearestCentroid
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, \
                            precision_score, f1_score  

def get_worker(app):
    if os.environ.get('REDIS_URL') is not None:
        redis_url = os.environ['REDIS_URL']
    else:
        # Hard coding locally
        redis_url = "redis://:p07f41a6e741bee30729756c50da995dea7d6ce525982fe9be1f691fb8d863a31@ec2-54-242-89-29.compute-1.amazonaws.com:8019"
        #redis_url = "redis://127.0.0.1:6379"

    app.config['CELERY_BROKER_URL'] = redis_url
    app.config['CELERY_RESULT_BACKEND'] = redis_url
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['CELERY_TASK_SERIALIZER'] = 'pickle'
    app.config['CELERY_RESULT_SERIALIZER'] = 'pickle'
    app.config['CELERY_ACCEPT_CONTENT'] = ['json','pickle']

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

def combine(vecs):  # Vecs is the output of get_output()
    # Currently uses topological coordinates
    return np.concatenate(vecs)  # Combine using brute force

def get_output(som, data_vec):  # SOM output (can be topological or feature space vector)
    return som.find_bmu(data_vec).position

def get_data(data, indices):
    final_data = []
    for i in indices:
        final_data.append(data[i])  
    return final_data

def train_model(task, data, dim, graph, shape, iters, lvq_data, classifiers):
    print("Classifiers:", classifiers)
    task.update_state(state='WORKING', meta={'current': "0% finished"})
    odata = copy.deepcopy(data)
    if lvq_data is not None:
        labels, dt = zip(*data)
        kf = StratifiedKFold(n_splits = int(1/lvq_data[1]), shuffle = True)
        train_i, test_i = list(kf.split(dt, labels))[0]

        data = np.array(dt)[train_i]
        test_data = np.array(odata)[test_i]
        labels = np.array(labels)[train_i]
    
    layers = {}
    deep_som = DeepSOM(iters)
    # Creating som nodes
    # print(graph)
    for node in graph:
        if node == "input-node":
            continue
        if shape == "Rectangle":
            som = deep_som.add_MapRect(iters, -1, 
                    graph[node]["parameters"]["Side Length"], 
                    graph[node]["parameters"]["Neighbourhood Radius"],
                    graph[node]["parameters"]["Decay Constant"],
                    graph[node]["parameters"]["Learning Rate"])
        elif shape == "Hex":
            print("Creating Hex SOM")
            print(graph[node]["parameters"]["Neighbourhood Radius"], graph[node]["parameters"]["Decay Constant"], graph[node]["parameters"]["Learning Rate"])
            som = deep_som.add_MapHex(iters, -1, 
                    graph[node]["parameters"]["Side Length"], 
                    graph[node]["parameters"]["Neighbourhood Radius"],
                    graph[node]["parameters"]["Decay Constant"],
                    graph[node]["parameters"]["Learning Rate"])
        layers[node] = som
    
    # Creating SOM node links using graph object
    getOutputFunc = get_output  # get_output function for final SOM layer 
        # Only applicable for non-trivial Deep SOMs
    for node in graph:
        neighbours = graph[node]["neighbours"]
        if node == "input-node":
            for n in neighbours:
                som = layers[n]
                in_dim = graph[n]["parameters"]["Input Dimensions"]
                if in_dim is None:
                    in_dim = list(range(dim))
                else:
                    in_dim = list(map(lambda x: x-1, in_dim))
                deep_som.set_get_data(som, (lambda tmp_idx: lambda x: get_data(x,tmp_idx))(in_dim))
        else:
            curr_som = layers[node]
            for n in neighbours:
                som = layers[n]
                deep_som.set_get_output(som, get_output)
                deep_som.set_combine(som, combine)
                deep_som.add_link(curr_som, som)

    def update_state(som, iter_t):
        task.update_state(state='WORKING', meta={'current': str(round(100*iter_t/(len(layers)), 4))+"% finished"}) 
    
    deep_som.batch_train_block(data, update_state)

    if lvq_data is not None:
        # Creating LVQ
        task.update_state(state='WORKING', meta={'current': 'Creating LVQ layer...'})
        final_layer = deep_som.get_SOM(deep_som.get_root())
        # node_data = [] 
        # for i in range(len(data)):
        #     node = final_layer.find_bmu(data[i])
        #     node_data.append([labels[i], np.array(node.position)])
        # print("DIM: ===========\n:", dim)
        alpha = 0.5
        # print("=====\nNode Data:", node_data[0])
        inp_dim = len(deep_som.get_SOM(deep_som.get_root()).get_nodes()[0].position)
        print("LVQ Data:", lvq_data)
        lvq_layer = LVQ(iters, inp_dim, lvq_data[0], alpha, 0)  # t_lim, inp_dim, total_class, alpha, l
        # lvq_layer.train(node_data)  # Train the LVQ using SOM output

        cN = ['LVQ', 'SVM', 'RF', 'DT', 'NB', '6NN']  # Classifier names
        fullCN = ['Learning Vector Quantization', 'Support Vector Machine',
                  'Random Forest', 'Decision Tree', 'Naive Bayes',
                  '6 Nearest Neighbors']  # Full classifier names (for display)
        cO = [lvq_layer, SVC(), RandomForestClassifier(), tree.DecisionTreeClassifier(),
              GaussianNB(), KNeighborsClassifier(n_neighbors = 6)]
                    # Classifier objects
        classifierNames = {n: o for n, o in zip(cN, cO)}
            # Dictionary of (name: classifier object)
        namesClassifier = {o: n for n, o in zip(cN, cO)}
            # Dictionary of (classifier object: name)

        clfObjs = []
        for classifier in classifiers:
            clfObjs.append(classifierNames[classifier])

        test_node = []
        test_label, test_data = zip(*test_data)
        for i in range(len(test_data)):
            if getOutputFunc is None:
                node = final_layer.find_bmu(test_data[i])
                test_node.append([test_label[i], np.array(node.position)])
            else:
                test_node.append([test_label[i], deep_som.test(test_data[i], getOutputFunc)])

        ##
        # NOTE: data must be from read_to_vec_with_class!
        # print(f"Pre-CV, {int(1/lvq_data[1])}")
        data_class = list(zip(labels, data))
        if getOutputFunc is None:
            metrics = somCVMetric(deep_som, lvq_layer, odata, sigfigs = 4, 
                        k = int(1/lvq_data[1]), deepSOM = True,
                        funcs = [lvqAccuracy, lvqPrecision, lvqRecall, lvqF1Score])
        else:
            print("Non-Trivial DeepSOM Mode")
            metrics = somCVMetric(deep_som, lvq_layer, odata, sigfigs = 4, 
                        k = int(1/lvq_data[1]), deepSOM = True,
                        funcs = [lvqAccuracy, lvqPrecision, lvqRecall, lvqF1Score],
                        deepSOMGetOutput = getOutputFunc)

        if getOutputFunc is None:
            skmetrics = sklearnCVMetric(deep_som, clfObjs, odata, sigfigs = 4, 
                        k = int(1/lvq_data[1]), deepSOM = True,
                        skfuncs = [accuracy_score, recall_score, precision_score, f1_score])
        else:
            print("Non-Trivial DeepSOM Mode")
            skmetrics = sklearnCVMetric(deep_som, clfObjs, odata, sigfigs = 4, 
                        k = int(1/lvq_data[1]), deepSOM = True,
                        skfuncs = [accuracy_score, recall_score, precision_score, f1_score],
                        deepSOMGetOutput = getOutputFunc)

        lvq_metrics = [f"CV Accuracy: {metrics[lvqAccuracy]}",
                       f"CV Precision: {metrics[lvqPrecision]}",
                       f"CV Recall: {metrics[lvqRecall]}",
                       f"CV F1-Score: {metrics[lvqF1Score]}",
                       "1-Fold Confusion Matrix:"]
        print("LVQ Metrics:", lvq_metrics)
        # lvq_metrics = [f"Accuracy: {round(lvqAccuracy(lvq_layer, test_node), 4)}",
        #                f"Precision: {round(lvqPrecision(lvq_layer, test_node), 4)}",
        #                f"Recall: {round(lvqRecall(lvq_layer, test_node), 4)}",
        #                f"F1-Score: {round(lvqF1Score(lvq_layer, test_node), 4)}",
        #                "Confusion Matrix:"
        #             ]
        confusion_matrix = list(map(lambda x: str(x), lvqConfusionMatrix(lvq_layer, test_node)))
        lvq_metrics.extend(confusion_matrix)
        
        metricDict = {accuracy_score: "Accuracy: ", f1_score: "F1 Score: ",
                      recall_score: "Recall: ", precision_score: "Precision: "}
        lvq_metrics.append("--------------------------")
        lvq_metrics.append("Comparison Classifiers (Cross Validation Metrics):")
        for clfObj in skmetrics:
            if clfObj == lvq_layer:
                continue
            tempStr = f"{namesClassifier[clfObj]}: "
                # String of metrics to display, per classifier
            for metric in skmetrics[clfObj]:
                tempStr += f"{metricDict[metric]} {skmetrics[clfObj][metric]}; "
            lvq_metrics.append(tempStr)
            lvq_metrics.append("\n")
        
        # lvq_metrics.extend(str(skmetrics))
    else:
        lvq_metrics = None

    task.update_state(state='WORKING', meta={'current': 'Visualising UMatrix...'})
    # Visualising SOM UMatrix created and returning
    visualisations = []
    results = visualise_deep_som(deep_som, len(layers), hex_grid=(shape == "Hex"), layers_dict=layers)
    plotIdx = 0
    visualisations.append(results)
    plotIdx += 1
    root_som = deep_som.get_root()
    som_dim = len(deep_som.get_SOM(root_som).get_nodes()[0].position)
    plotTypes = {}
    
    # NOTE: 3D Plots do not work for DeepSOM, as the dataset is not in the same feature space as the final SOM
    if som_dim == 3: #  and dim == 3:
        task.update_state(state='WORKING', meta={'current': 'Visualising 3D SOM Plot...'})
        visualisations.append(genHTMLPlot(deep_som, data, len(layers)-1, True))
        plotTypes["genHTMLPlot"] = plotIdx
        plotIdx += 1
        task.update_state(state='WORKING', meta={'current': 'Visualising 3D Error Plot...'})
        visualisations.append(errorColorPlot(deep_som, data, len(layers)-1, True))
        plotTypes["errorColorPlot"] = plotIdx
        plotIdx += 1
    if dim == 4 and som_dim == 4:
        task.update_state(state='WORKING', meta={'current': 'Visualising 4D SOM Plot...'})
        visualisations.append(gen4DPlot(deep_som, data, len(layers)-1, True))
        plotTypes["gen4DPlot"] = plotIdx
        plotIdx += 1
    task.update_state(state='WORKING', meta={'current': 'Visualising PCA SOM Plot...'})
    mp = deep_som.get_SOM(deep_som.get_root())
    if deep_som.get_node_num() == 1:
        if lvq_data is not None:
            visualisations.append(genPCAPlot(mp, list(zip(labels, data)), classes = True, fig_only = True))
        else:
            visualisations.append(genPCAPlot(mp, data, classes = False, fig_only = True))
        plotTypes["genPCAPlot"] = plotIdx
        plotIdx += 1
    task.update_state(state='WORKING', meta={'current': 'Visualising 4D PCA DeepSOM Plot...'})
    if deep_som.get_node_num() > 1:
        if lvq_data is not None:
            visualisations.append(plotDeepSOM4D(deep_som, list(zip(labels, data)), classes = True, fig_only = True))
        else:
            visualisations.append(plotDeepSOM4D(deep_som, data, classes = False, fig_only = True))
        plotTypes["plotDeepSOM4D"] = plotIdx
        plotIdx += 1
        if lvq_data is not None:
            task.update_state(state='WORKING', meta={'current': 'Visualising 3D PCA DeepSOM Plot...'})
            visualisations.append(plotDeepSOM3D(deep_som, list(zip(labels, data)), classes = True, fig_only = True))
            plotTypes["plotDeepSOM3D"] = plotIdx
            plotIdx += 1
    print(lvq_metrics)
    visualisations.append(plotTypes)
    task.update_state(state='SUCCESS', meta=(visualisations,lvq_metrics))

    return visualisations, lvq_metrics
