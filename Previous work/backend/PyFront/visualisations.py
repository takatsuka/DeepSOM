import numpy as np
import io
import matplotlib.pyplot as plt
from matplotlib.collections import RegularPolyCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
from .imports import *
from .util import UMatrix

def visualise_deep_som(deep_som, num_soms, hex_grid=True, layers_dict=None):
    if layers_dict is None:
        SOMs = [deep_som.get_SOM(i) for i in range(num_soms)]
        visualisations = []
        for i in range(num_soms):
            visualisations.append(io.BytesIO())
            if hex_grid:
                hex_visualise_som(som_map = SOMs[i], img_name = visualisations[i])
            else:
                visualise_som_layer(som_map = SOMs[i], img_name = visualisations[i])
            visualisations[i].seek(0)
    else:
        visualisations = {}
        for layer_name, som_idx in layers_dict.items():
            new_plot = io.BytesIO()
            som = deep_som.get_SOM(som_idx)
            if hex_grid:
                hex_visualise_som(som_map = som, img_name = new_plot)
            else:
                visualise_som_layer(som_map = som, img_name = new_plot)
            new_plot.seek(0)
            visualisations[layer_name] = new_plot

    return visualisations

def visualise_som_layer(som_map, img_name = "som_layer.png"):
    # Visualise UMatrix for square SOM
    distances = UMatrix(som_map)
    plt.clf()
    plt.imshow(distances, cmap = "RdBu_r")
    plt.colorbar()
    plt.savefig(img_name)

def hex_visualise_som(som_map, w = 1080, hex_r = 1, img_name = 'hex_som_layer.png'):
    plt.clf()
    all_nodes = som_map.get_nodes()
    d_matrix = np.array([item for row in UMatrix(som_map) for item in row])

    side_len = max(som_map.lengths[0], som_map.lengths[1])
    dpi = 72

    n_centers = []
    counter = 0
    for i in range(som_map.lengths[1]):
        for j in range(som_map.lengths[0]):
            n_centers.append(all_nodes[counter].topo)
            counter += 1
    n_centers = np.array(n_centers)

    xpoints = n_centers[:, 0]
    ypoints = n_centers[:, 1]

    x_range = max(xpoints) - min(xpoints)
    y_range = max(ypoints) - min(ypoints)

    xinch = (w) / dpi
    yinch = (y_range * w / x_range)  / dpi

    fig = plt.figure(figsize=(xinch, yinch), dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')

    ax.scatter(xpoints, ypoints, s=1, marker='s')
    ax.axis([min(xpoints) - 2, max(xpoints) + 2,
            min(ypoints) - 2, max(ypoints) + 2])
    ax.axis('off')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="10%", pad=0.05)
    cax.axis('off')
    fig.canvas.draw()

    staples = ax.transData.transform(np.array([[0, 0], [1, 1]]))
    x_scale = staples[1][0] - staples[0][0]
    # y_scale = staples[1][1] - staples[0][1]

    # r = 1 * min(x_scale, y_scale)
    r = hex_r * x_scale
    area_inner_circle = (math.pi * (math.ceil(r) ** 2))
    collection_bg = RegularPolyCollection(
        numsides=6,
        rotation=0,
        sizes=(area_inner_circle,),
        array=d_matrix,
        cmap="RdBu_r",
        offsets=n_centers,
        transOffset=ax.transData,
    )

    ax.add_collection(collection_bg, autolim=True)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)
    plt.colorbar(collection_bg, cax=cax)
    plt.savefig(img_name, bbox_inches='tight')
    return ax
