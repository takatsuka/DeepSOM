from .imports import *

import os
import numpy as np
import pandas as pd
import plotly.offline as po
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.io import to_html

from sklearn.decomposition import PCA

# Visualisation functions: genHTMLPlot (3D SOM Plot), errorColorPlot, gen4DPlot

def getTrace(x, y, z, c, label, s = 2):
    return go.Scatter3d( x = x, y = y, z = z, mode='markers',
        marker=dict(size=s, line=dict(color='rgb(0, 0, 0)', width=0.5), color=c, opacity=1), name=label)

def plotProcess(X, lab, s = 3, fourDColor = "blue", nodeColor = "green", sPoint = 1.5):
    X = X.values
    t1 = getTrace(X[lab == 0, 0], X[lab == 0, 1], X[lab == 0, 2], s = sPoint, c = fourDColor, label = '1') #match with red=1 initial class
    t2 = getTrace(X[lab == 1, 0], X[lab == 1, 1], X[lab == 1, 2], s = s, c = nodeColor, label = '2') #match with black=3 initial class
    t3 = getTrace(X[lab == 2, 0], X[lab == 2, 1], X[lab == 2, 2], s = s, c = 'black', label = '3') #match with blue=2 initial class
    t4 = getTrace(X[lab == 3, 0], X[lab == 3, 1], X[lab == 3, 2], s = s, c = 'yellow', label = '4') #match with green=0 initial class
    t5 = getTrace(X[lab == 4, 0], X[lab == 4, 1], X[lab == 4, 2], s = s, c = 'cyan', label = '5') #match with black=3 initial class
    t6 = getTrace(X[lab == 5, 0], X[lab == 5, 1], X[lab == 5, 2], s = s, c = 'purple', label = '5')
    t7 = getTrace(X[lab == 6, 0], X[lab == 6, 1], X[lab == 6, 2], s = s, c = 'orange', label = '5')
    t8 = getTrace(X[lab == 7, 0], X[lab == 7, 1], X[lab == 7, 2], s = s, c = 'green', label = '5')
    x, y, z = X[:,0], X[:,1], X[:,2]  # Separate dimensions into variables
    return ([t1, t2, t3, t4, t5, t6, t7, t8], x, y, z)

def showGraph(title, x_colname, x_range, y_colname, y_range, z_colname, z_range, traces, 
              line_x = [], line_y = [], line_z = [], lineWidth = 1):
    layout = go.Layout(title = title,
                       scene = dict(xaxis = dict(title = x_colname, range = x_range),
                                    yaxis = dict(title = y_colname, range = y_range),
                                    zaxis = dict(title = z_colname, range = z_range)))

    trace2 = go.Scatter3d(
        x = line_x, #[0, 5, None, 0, 0, None],
        y = line_y, #[1, 6, None, 0, 10, None],
        z = line_z, #[2, 10, None, -1, 100, None],
        line = dict(width = lineWidth, color = 'black'),
        mode='lines', name='lines' )

    fig = go.Figure(data = traces + [trace2], layout = layout)
    return fig

def genHTMLPlot(mp, data, last_node = None, fig_only=False, showPlot=0):
    if last_node is not None:
        mp = mp.get_SOM(last_node)
    node_loc = []

    ## Generate lines between SOM nodes for plotting
    line_x, line_y, line_z = [], [], []
    for node in mp.get_nodes():
        node_loc.append(node.position)
        x1, y1, z1 = node.position
        for neighbor in node.neighbors:
            if (neighbor.id_v < node.id_v):
                continue
            line_x.append(x1)
            line_y.append(y1)
            line_z.append(z1)

            x2, y2, z2 = neighbor.position
            line_x.append(x2)
            line_y.append(y2)
            line_z.append(z2)

            line_x.append(None)
            line_y.append(None)
            line_z.append(None)

    ## Process data and SOM node location for plotting
    dataset = np.array(data)
    classLab = np.zeros(dataset.shape[0])
    SOMpos = np.array(node_loc)
    inputData = np.concatenate([dataset, SOMpos], axis = 0)
    classLab = np.append(classLab, np.ones(SOMpos.shape[0]), axis=0)
    
    tArray, x, y, z = plotProcess(pd.DataFrame(inputData), classLab.astype(int),
                                  sPoint = 3, s = 2.5)
    fig = showGraph("3D SOM plot", "C1", [min(x),max(x)], "C2", [min(y),max(y)], "C3", [min(z)-1,max(z)], 
                    tArray, line_x, line_y, line_z)
    if fig_only:
        return fig

    plot_html = to_html(fig, include_plotlyjs = False, full_html = False)
    if showPlot == 1:
        po.plot(fig)
    return plot_html  # HTML as a string

def errorColorPlotProcess(X, lab, errors, sPoint = 3):
    X = X.values
    t1 = getTrace(X[lab == 0, 0], X[lab == 0, 1], X[lab == 0, 2], s = 1.5, c = errors, label = '1') #match with red=1 initial class
    t2 = getTrace(X[lab == 1, 0], X[lab == 1, 1], X[lab == 1, 2], s = sPoint, c = 'green', label = '2') #match with black=3 initial class
    t3 = getTrace(X[lab == 2, 0], X[lab == 2, 1], X[lab == 2, 2], s = sPoint, c = 'black', label = '3') #match with blue=2 initial class
    t4 = getTrace(X[lab == 3, 0], X[lab == 3, 1], X[lab == 3, 2], s = sPoint, c = 'green', label = '4') #match with green=0 initial class
    t5 = getTrace(X[lab == 4, 0], X[lab == 4, 1], X[lab == 4, 2], s = sPoint, c = 'cyan', label = '5') #match with black=3 initial class
    t6 = getTrace(X[lab == 5, 0], X[lab == 5, 1], X[lab == 5, 2], s = sPoint, c = 'purple', label = '5')
    t7 = getTrace(X[lab == 6, 0], X[lab == 6, 1], X[lab == 6, 2], s = sPoint, c = 'orange', label = '5')
    t8 = getTrace(X[lab == 7, 0], X[lab == 7, 1], X[lab == 7, 2], s = sPoint, c = 'yellow', label = '5')
    x, y, z = X[:,0], X[:,1], X[:,2]  # Separate dimensions into variables
    return ([t1, t2, t3, t4, t5, t6, t7, t8], x, y, z)

def errorColorPlot(mp, data, last_node = None, fig_only=False, showPlot=0):  # Accepts a trained som mp and dataset
    if last_node is not None:
        mp = mp.get_SOM(last_node)
    node_loc = []
    errors = []
    for vector in data:
        bmu = mp.find_bmu(vector)
        errors.append(np.linalg.norm(bmu.position - vector))

    ## Generate lines between SOM nodes for plotting
    line_x, line_y, line_z = [], [], []
    for node in mp.get_nodes():
        node_loc.append(node.position)
        x1, y1, z1 = node.position
        for neighbor in node.neighbors:
            if (neighbor.id_v < node.id_v):
                continue
            line_x.append(x1)
            line_y.append(y1)
            line_z.append(z1)

            x2, y2, z2 = neighbor.position
            line_x.append(x2)
            line_y.append(y2)
            line_z.append(z2)

            line_x.append(None)
            line_y.append(None)
            line_z.append(None)

    ## Process data and SOM node location for plotting
    dataset = np.array(data)
    classLab = np.zeros(dataset.shape[0])
    SOMpos = np.array(node_loc)
    inputData = np.concatenate([dataset, SOMpos], axis = 0)
    classLab = np.append(classLab, np.ones(SOMpos.shape[0]), axis=0)
    
    tArray, x, y, z = errorColorPlotProcess(pd.DataFrame(inputData), 
                                        classLab.astype(int), errors, sPoint = 3)
    fig = showGraph("Error Plot", "C1", [min(x),max(x)], "C2", [min(y),max(y)], "C3", [min(z)-1,max(z)], 
                    tArray, line_x, line_y, line_z)
    if fig_only:
        return fig

    plot_html = to_html(fig, include_plotlyjs = False, full_html = False)

    if showPlot == 1:
        po.plot(fig)

    return plot_html  # HTML as a string

def gen4DPlot(mp, data, last_node = None, fig_only=False, showPlot=0, data4D = True):  # Expects a 4D dataset
    if last_node is not None:
        mp = mp.get_SOM(mp.get_root())
    node_loc = []
    node4D = []
    point4D = []
    #print(data)
    if data4D:
        for item in data:
            point4D.append(item[3])
    else:
        point4D = None
    ## Generate lines between SOM nodes for plotting
    line_x, line_y, line_z, line_f = [], [], [], []
    for node in mp.get_nodes():
        node_loc.append(node.position)
        x1, y1, z1, f1 = node.position
        node4D.append(f1)
        for neighbor in node.neighbors:
            if (neighbor.id_v < node.id_v):
                continue
            line_x.append(x1)
            line_y.append(y1)
            line_z.append(z1)
            line_f.append(f1)

            x2, y2, z2, f2 = neighbor.position
            line_x.append(x2)
            line_y.append(y2)
            line_z.append(z2)
            line_f.append(f2)

            line_x.append(None)
            line_y.append(None)
            line_z.append(None)
            line_f.append(None)

    ## Process data and SOM node location for plotting
    dataset = np.array(data)
    classLab = np.zeros(dataset.shape[0])
    SOMpos = np.array(node_loc)
    inputData = np.concatenate([dataset, SOMpos], axis = 0)
    classLab = np.append(classLab, np.ones(SOMpos.shape[0]), axis=0)
    
    # print("_____Dataset____")
    # print(dataset)
    # print("____SOMpos____")
    # print(SOMpos)

    tArray, x, y, z = plotProcess(pd.DataFrame(inputData), classLab.astype(int), 
                                    fourDColor = point4D, nodeColor = node4D,
                                    sPoint = 3, s = 2.5)
    fig = showGraph("4D SOM plot", "C1", [min(x),max(x)], "C2", [min(y),max(y)], "C3", [min(z)-1,max(z)], 
                    tArray, line_x, line_y, line_z, lineWidth = 1)
    if fig_only:
        return fig
    plot_html = to_html(fig, include_plotlyjs = False, full_html = False)

    if (showPlot == 1):
        po.plot(fig)
    return plot_html  # HTML as a string

def genPCAPlot(mp, data, fig_only = False, showPlot = 0, classes = False, nodeClass = []):
    # Input a nD dataset on which the SOM mp was trained
    # Accepts SOM ONLY, not DeepSOM nor DeepSOM layers
    # nodeClass is an optional vector of node classes 

    point4D = []  # Point color
    if classes:  # If data is from read_to_vec_with_class
        point4D = [item[0] for item in data]
        X = np.array([item[1] for item in data])
    else:
        X = np.array(data)
        
    if nodeClass == []:
        nodeClass = "green"

    pca = PCA(n_components = 3)  # Initialise PCA object
    pca.fit(X)  # Perform PCA on X
    pcaData = pca.transform(X)  # Generate transformed dataset

    node_loc = []
    ## Generate lines between SOM nodes for plotting
    line_x, line_y, line_z = [], [], []
    for node in mp.get_nodes():
        pcaPos = pca.transform([node.position])[0]
        node_loc.append(pcaPos)
        x1, y1, z1 = pcaPos
        for neighbor in node.neighbors:
            if (neighbor.id_v < node.id_v):
                continue
            line_x.append(x1)
            line_y.append(y1)
            line_z.append(z1)

            pcaPos2 = pca.transform([neighbor.position])[0]
            x2, y2, z2 = pcaPos2
            line_x.append(x2)
            line_y.append(y2)
            line_z.append(z2)

            line_x.append(None)
            line_y.append(None)
            line_z.append(None)

    ## Process data and SOM node location for plotting
    classLab = np.zeros(pcaData.shape[0])
    SOMpos = np.array(node_loc)
    inputData = np.concatenate([pcaData, SOMpos], axis = 0)
    classLab = np.append(classLab, np.ones(SOMpos.shape[0]), axis=0)
    
    # print("_____Dataset____")
    # print(dataset)
    # print("____SOMpos____")
    # print(SOMpos)

    tArray, x, y, z = plotProcess(pd.DataFrame(inputData), classLab.astype(int), 
                                    fourDColor = point4D, nodeColor = nodeClass,
                                    sPoint = 3, s = 2.5)

    fig = showGraph("3D PCA plot", "C1", [min(x),max(x)], "C2", [min(y),max(y)], "C3", [min(z)-1,max(z)], 
                    tArray, line_x, line_y, line_z, lineWidth = 1)
    if fig_only:
        return fig
    plot_html = to_html(fig, include_plotlyjs = False, full_html = False)

    if (showPlot == 1):
        po.plot(fig)
    return plot_html  # HTML as a string

def plotDeepSOM4D(ds, data, classes = False, fig_only = False, showPlot = 0):
    # Set classes = True if data contains classes
    mp = ds.get_SOM(ds.get_root())
    node_loc = []
    node4D = []
    node_data = []
    for node in mp.get_nodes():
        node_data.append(node.position)
    node_data = np.array(node_data)
    pca = PCA(n_components = 4)  # Initialise PCA object
    pca.fit(node_data)  # Perform PCA on X
    pcaData = pca.transform(node_data)  # Generate transformed dataset

    ## Generate lines between SOM nodes for plotting
    line_x, line_y, line_z, line_f = [], [], [], []
    for idx, node in enumerate(mp.get_nodes()):
        x1, y1, z1, f1 = pcaData[idx]
        node_loc.append([x1, y1, z1])
        node4D.append(f1)
        for neighbor in node.neighbors:
            if (neighbor.id_v < node.id_v):
                continue
            line_x.append(x1)
            line_y.append(y1)
            line_z.append(z1)
            line_f.append(f1)

            neighborPos = pca.transform([neighbor.position])
            x2, y2, z2, f2 = neighborPos[0]
            line_x.append(x2)
            line_y.append(y2)
            line_z.append(z2)
            line_f.append(f2)

            line_x.append(None)
            line_y.append(None)
            line_z.append(None)
            line_f.append(None)

    ## Process data and SOM node location for plotting
    SOMpos = np.array(node_loc)
    transformData = []
    dataset = []
    data4D = []
    if classes:
        for label, vector in data:
            dataVec = ds.test_inputs(vector)[ds.get_root()]
            dataVec = pca.transform([dataVec])[0]
            dataset.append(dataVec[0:3])
            data4D.append(dataVec[3])
    else:
        for vector in data:
            dataVec = ds.test_inputs(vector)[ds.get_root()]
            dataVec = pca.transform([dataVec])[0]
            dataset.append(dataVec[0:3])
            data4D.append(dataVec[3])
    dataset = np.array(dataset)
    classLab = np.zeros(dataset.shape[0])
    SOMpos = np.array(node_loc)
    inputData = np.concatenate([dataset, SOMpos], axis = 0)
    classLab = np.append(classLab, np.ones(SOMpos.shape[0]), axis=0)
    
    tArray, x, y, z = plotProcess(pd.DataFrame(inputData), classLab.astype(int),
                                    fourDColor = data4D, 
                                    nodeColor = node4D, sPoint = 2, s = 3)
    fig = showGraph("4D SOM Plot Using PCA", "C1", [min(x),max(x)], "C2", [min(y),max(y)], "C3", [min(z)-1,max(z)], 
                    tArray, line_x, line_y, line_z, lineWidth = 1)
    if fig_only:
        return fig
    plot_html = to_html(fig, include_plotlyjs = False, full_html = False)

    if (showPlot == 1):
        po.plot(fig)
    return plot_html  # HTML as a string

def plotDeepSOM3D(ds, data, classes = False, fig_only = False, showPlot = 0):
    # Set classes = True if data contains classes
    mp = ds.get_SOM(ds.get_root())
    node_loc = []
    node_data = []
    for node in mp.get_nodes():
        node_data.append(node.position)
    node_data = np.array(node_data)
    pca = PCA(n_components = 3)  # Initialise PCA object
    pca.fit(node_data)  # Perform PCA on X
    pcaData = pca.transform(node_data)  # Generate transformed dataset

    ## Generate lines between SOM nodes for plotting
    line_x, line_y, line_z = [], [], []
    for idx, node in enumerate(mp.get_nodes()):
        x1, y1, z1 = pcaData[idx]
        node_loc.append([x1, y1, z1])
        for neighbor in node.neighbors:
            if (neighbor.id_v < node.id_v):
                continue
            line_x.append(x1)
            line_y.append(y1)
            line_z.append(z1)

            neighborPos = pca.transform([neighbor.position])
            x2, y2, z2 = neighborPos[0]
            line_x.append(x2)
            line_y.append(y2)
            line_z.append(z2)

            line_x.append(None)
            line_y.append(None)
            line_z.append(None)

    ## Process data and SOM node location for plotting
    SOMpos = np.array(node_loc)
    transformData = []
    dataset = []
    data4D = []
    if classes:
        for label, vector in data:
            dataVec = ds.test_inputs(vector)[ds.get_root()]
            dataVec = pca.transform([dataVec])[0]
            dataset.append(dataVec[0:3])
            data4D.append(label)
    else:
        for vector in data:
            dataVec = ds.test_inputs(vector)[ds.get_root()]
            dataVec = pca.transform([dataVec])[0]
            dataset.append(dataVec[0:3])

    dataset = np.array(dataset)
    classLab = np.zeros(dataset.shape[0])
    SOMpos = np.array(node_loc)
    inputData = np.concatenate([dataset, SOMpos], axis = 0)
    classLab = np.append(classLab, np.ones(SOMpos.shape[0]), axis=0)
    
    tArray, x, y, z = plotProcess(pd.DataFrame(inputData), classLab.astype(int),
                                    fourDColor = data4D, sPoint = 2, s = 3)
    fig = showGraph("3D DeepSOM Plot Using PCA", "C1", [min(x),max(x)], "C2", [min(y),max(y)], "C3", [min(z)-1,max(z)], 
                    tArray, line_x, line_y, line_z, lineWidth = 1)
    if fig_only:
        return fig
    plot_html = to_html(fig, include_plotlyjs = False, full_html = False)

    if (showPlot == 1):
        po.plot(fig)
    return plot_html  # HTML as a string