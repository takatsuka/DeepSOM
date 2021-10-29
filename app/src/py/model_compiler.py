from pysom.graph.graph import Graph
from pysom.graph.node import Node
from pysom.graph.nodes.dist import Dist
from pysom.graph.nodes.concat import Concat
from pysom.graph.nodes.som import SOM
from pysom.graph.nodes.bmu import BMU

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

node_props = {
    "inout": None,
    "dist": dist_props,
    "bypass": lambda x : {},
    "concat": concat_props,
}


def parse_dict(dict):
    g = Graph()
    nodes = dict['nodes']
    links = dict['connections']

    for k in nodes:
        n = nodes[k]
        type = template_2_node[n['template']]

        if not type:
            continue

        pp = node_props[n['template']](n['props'])
        g.create(node_type=type, props=pp)
    
    for l in links:
        g.connect(l['from'], l['to'], l['props']['slot'])

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
    