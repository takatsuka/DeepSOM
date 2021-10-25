from graph import som
from graph.graph import Graph
from graph.nodes.dist import *

def example_dist():
    import numpy as np
    dat = [
        [1,2,3],
        [4,5,6],
        [2,3,4]
    ]
    dat = np.array(dat)


    g = Graph()

    sel = [(1, [0, 2]), (1, [1])]
    dist1 = g.create(Dist, {"selections": sel})

    g.connect(g.start, dist1, 0)
    g.connect(dist1, g.end, 1)

    g.set_input(dat)

    print(g.get_output())


example_dist()