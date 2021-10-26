from graph.graph import Graph
from graph.nodes.dist import *
from graph.nodes.concat import *
from graph.nodes.som import *
from graph.nodes.bmu import *

def example_dist():
    import numpy as np
    dat = [
        [1, 2, 3],
        [4, 5, 6],
        [2, 3, 4]
    ]
    dat = np.array(dat)

    g = Graph()

    sel = [(1, [0, 2]), (1, [1])]
    dist1 = g.create(Dist, {"selections": sel})

    g.connect(g.start, dist1, 1)
    g.connect(dist1, g.end, 1)

    g.set_input(dat)

    print(g.get_output())


def example_dist_con():
    import numpy as np
    dat = [
        [1, 2, 3],
        [4, 5, 6],
        [2, 3, 4]
    ]
    dat = np.array(dat)

    g = Graph()

    sel = [(1, [0, 2]), (1, [1])]
    dist1 = g.create(Dist, {"selections": sel})
    n1 = g.create(Node)
    n2 = g.create(Node)
    con1 = g.create(Concat, {"axis": 1})

    g.connect(g.start, dist1, 1)

    g.connect(dist1, n1, 1)
    g.connect(dist1, n2, 2)

    g.connect(n1, con1, 1)
    g.connect(n2, con1, 1)

    g.connect(con1, g.end, 1)

    g.set_input(dat)

    print(g.get_output())


def simplesom_bmu():
    g = Graph()

    file_path = "../datasets/sphere/sphere_256.txt"
    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]
    
    g.set_input(data=data)

    som = g.create(node_type=SOM, props={'x':100, 'y':100, 'dim':3, 'sigma':6, 'lr':0.8, 'n_iters':1,
                                'nhood':nhood_gaussian, 'topology':'hexagonal'})

    bmu = g.create(node_type=BMU, props={'output':'2D'})

    g.connect(g.start, som, slot=0)
    g.connect(som, bmu, slot=0)
    g.connect(bmu, g.end, slot=1)
    
    out = g.get_output()
    print(out)


simplesom_bmu()
