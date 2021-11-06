from pysom.graph import Graph
from pysom.nodes.dist import Dist
from pysom.nodes.concat import Concat
from pysom.nodes.som import SOM
from pysom.nodes.bmu import BMU
from pysom.node import Node
from pysom.nodes.som import nhood_gaussian, nhood_bubble, nhood_mexican
from pysom.nodes.som import dist_cosine, dist_euclidean, dist_manhattan
from pysom.nodes.calibrate import Calibrate
from pysom.graph import GraphCompileError

template_2_node = {
    "inout": None,
    "dist": Dist,
    "bypass": Node,
    "concat": Concat,
    "som": SOM,
    "get_bmu": BMU
}


def dist_props(dict):
    axis = dict['axis']
    return {"selections": [(axis, k['sel']) for k in dict['selections']]}


def concat_props(dict):
    return {"axis": dict['axis']}


def som_props(dict):
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
    }


def bmu_props(dict):
    output = {'index': '1D', 'weights': 'w'}

    return {
        "output": output[dict['shape']],
    }


node_props = {
    "inout": None,
    "dist": dist_props,
    "bypass": lambda x: {},
    "concat": concat_props,
    "som": som_props,
    "get_bmu": bmu_props
}


def parse_dict(dict):
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

        pp = node_props[n['template']](n['props'])
        g.create_with_id(k, type, pp)

    for l in links:
        res = g.connect(l['from'], l['to'], l['props']['slot'])
        if not res:
            raise GraphCompileError(f"Unable to connect {l}.")

    return g


if __name__ == "__main__":
    import numpy as np
    import sys
    import json

    txt = open(sys.argv[1]).read()
    json = json.loads(txt)
    graph = parse_dict(json)

    dat = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    dat = np.array(dat)

    graph.set_input(dat)

    print(graph.get_output())