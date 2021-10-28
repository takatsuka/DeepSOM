from graph.graph import Graph
from graph.nodes.dist import Dist
from graph.nodes.concat import Concat
from graph.nodes.som import SOM
from graph.nodes.bmu import BMU
from graph.node import Node


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

    file_path = "datasets/sphere/sphere_64.txt"
    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]

    g.set_input(data=data)

    som = g.create(node_type=SOM, props={'size': 100, 'dim': 3, 'sigma': 6, 'lr': 0.8, 'n_iters': 1,
                                         'hexagonal': False})

    bmu = g.create(node_type=BMU, props={'output': '1D'})

    g.connect(g.start, som, slot=1)
    g.connect(som, bmu, slot=0)
    g.connect(bmu, g.end, slot=1)

    out = g.get_output()
    print(out)


def simplesom_plot():
    import numpy as np
    import matplotlib.pyplot as plt
    g = Graph()

    file_path = "datasets/sphere/sphere_256.txt"
    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]

    g.set_input(data=data)

    som = g.create(node_type=SOM, props={'size': 20, 'dim': 3, 'sigma': 6, 'lr': 0.8, 'n_iters': 10000,
                                         'hexagonal': False})

    g.connect(g.start, som, slot=1)
    g.connect(som, g.end, slot=1)

    out = g.get_output()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    axes = list(zip(*out))
    axes_o = list(zip(*data))
    ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))

    ax.scatter(*axes, marker='o', s=1)
    ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def dist_som_concat():
    """
                som1 -> bmu2
                /           \\
    input -> dist1          con1 -> som3
                \\          /
                som2 -> bmu2
    """
    import numpy as np
    import matplotlib.pyplot as plt

    file_path = "../datasets/sphere/sphere_64.txt"
    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]

    dat = np.array(data)

    g = Graph()

    sel = [(1, [0, 2]), (1, [1])]
    dist1 = g.create(Dist, {"selections": sel})

    g.connect(g.start, dist1, 1)

    som1 = g.create(node_type=SOM, props={'size': 20, 'dim': 2, 'sigma': 6, 'lr': 0.8, 'n_iters': 10000, 'hexagonal': False})
    som2 = g.create(node_type=SOM, props={'size': 20, 'dim': 1, 'sigma': 6, 'lr': 0.8, 'n_iters': 10000, 'hexagonal': False})

    g.connect(dist1, som1, 1)
    g.connect(dist1, som2, 2)

    bmu1 = g.create(node_type=BMU, props={'output': '2D'})
    bmu2 = g.create(node_type=BMU, props={'output': '2D'})

    g.connect(som1, bmu1, 0)
    g.connect(som2, bmu2, 0)

    con1 = g.create(Concat, props={'axis': 1})

    g.connect(bmu1, con1, 1)
    g.connect(bmu2, con1, 1)

    som3 = g.create(node_type=SOM, props={'size': 20, 'dim': 3, 'sigma': 6, 'lr': 0.8, 'n_iters': 10000, 'hexagonal': False})

    g.connect(con1, som3, 1)
    g.connect(som3, g.end, 1)

    g.set_input(dat)
    out = g.get_output()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    axes = list(zip(*out))
    axes_o = list(zip(*data))
    ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))

    ax.scatter(*axes, marker='o', s=1)
    ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


dist_som_concat()
