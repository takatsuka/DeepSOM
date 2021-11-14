from pysom.graph import Graph
from pysom.nodes.dist import Dist
from pysom.nodes.concat import Concat
from pysom.nodes.som import SOM
from pysom.nodes.bmu import BMU
from pysom.node import Node
from pysom.nodes.som import nhood_gaussian, nhood_bubble, nhood_mexican
from pysom.nodes.som import dist_cosine, dist_euclidean, dist_manhattan
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.scale import Scale
from pysom.graph import GraphCompileError

import numpy as np

template_2_node = {
    "inout": None,
    "dist": Dist,
    "bypass": Node,
    "concat": Concat,
    "som": SOM,
    "get_bmu": BMU,
    "calibrate": Calibrate,
    "scale": Scale
}


def dist_props(dict, *_):
    axis = dict['axis']
    return {"selections": [(axis, k['sel']) for k in dict['selections']]}


def concat_props(dict, *_):
    return {"axis": dict['axis']}


def som_props(dict, *_):
    nh = {"gaussian": nhood_gaussian,
          "bubble": nhood_bubble, "mexican": nhood_mexican}
    dist = {"cosine": dist_cosine, "euclidean": dist_euclidean,
            "manhattan": dist_manhattan}
    return {
        "size": dict['dim'],
        "dim": dict['inputDim'],
        "sigma": dict['sigma'],
        "lr": dict['lr'],
        "n_iters": dict['train_iter'],
        "hexagonal": dict['shape'] == 'hex',
        "dist": dist[dict['distance_func']],
        "nhood": nh[dict['nhood_func']],
        "norm": dict['pre'] == "normalize"
    }


def bmu_props(dict, *_):
    output = {'index': '1D', 'weights': 'w', 'coord': "2D"}

    return {
        "output": output[dict['shape']],
    }


def calibrate_props(dict, ds, n, *_):
    key = dict['label_key']
    dat = ds.get_object_data(key)

    if dat is None:
        raise GraphCompileError(
            f"Data object {key} expected by {n['name']} is missing.")

    if not isinstance(dat, np.ndarray):
        raise GraphCompileError(
            f"Data object {key} expected by {n['name']}: bad format. {str(dat.__class__)}")

    return {
        "labels": dat.reshape(len(dat)).tolist()
    }


node_props = {
    "inout": None,
    "dist": dist_props,
    "bypass": lambda x, *_: {},
    "concat": concat_props,
    "som": som_props,
    "get_bmu": bmu_props,
    "calibrate": calibrate_props,
    "scale": lambda x, *_: {}
}


def parse_dict(dict, ds):
    g = Graph(loglevel=1000)
    nodes = dict['nodes']
    links = dict['connections']

    for k, n in nodes.items():
        k = int(k)
        if n['template'] not in template_2_node:
            raise GraphCompileError(
                f"Node with type {n['template']} is not supported.")

        type = template_2_node[n['template']]
        if type is None:
            continue

        pp = node_props[n['template']](n['props'], ds, n)
        g.create_with_id(k, type, pp)

    for l in links:
        res = g.connect(l['from'], l['to'], l['props']['slot'])
        if not res:
            raise GraphCompileError(f"Unable to connect {l}.")

    return g
