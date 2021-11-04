import numpy as np
from pysom.graph import Graph
from pysom.nodes.dist import Dist
from pysom.nodes.concat import Concat
from pysom.nodes.som import SOM
from pysom.nodes.bmu import BMU
from pysom.node import Node
from pysom.nodes.som import nhood_gaussian, nhood_bubble, nhood_mexican
from pysom.nodes.calibrate import Calibrate
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


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
    file_path = "datasets/sphere/sphere_256.txt"
    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]

    dat = np.array(data)

    g = Graph()

    sel = [(1, [0, 2]), (1, [1])]
    dist1 = g.create(Dist, {"selections": sel})

    g.connect(g.start, dist1, 1)

    som1 = g.create(node_type=SOM, props={'size': 100, 'dim': 2, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000, 'hexagonal': False})
    som2 = g.create(node_type=SOM, props={'size': 100, 'dim': 1, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000, 'hexagonal': False})

    g.connect(dist1, som1, 1)
    g.connect(dist1, som2, 2)

    bmu1 = g.create(node_type=BMU, props={'output': '2D'})
    bmu2 = g.create(node_type=BMU, props={'output': '2D'})

    g.connect(som1, bmu1, 0)
    g.connect(som2, bmu2, 0)

    con1 = g.create(Concat, props={'axis': 1})

    g.connect(bmu1, con1, 1)
    g.connect(bmu2, con1, 1)

    som3 = g.create(node_type=SOM, props={'size': 100, 'dim': 3, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000, 'hexagonal': False})

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


def classify_iris():
    iris = load_iris()

    data = np.apply_along_axis(lambda x: x / np.linalg.norm(x), 1, iris.data)  # normalizing data

    X_train, X_test, y_train, y_test = train_test_split(data, iris.target)

    g = Graph()
    som = g.create(node_type=SOM, props={'size': 7, 'dim': 4, 'sigma': 3, 'lr': 0.5, 'n_iters': 500, 'nhood': nhood_gaussian, 'rand_state': True})
    g.connect(g.start, som, 1)
    cal = g.create(node_type=Calibrate, props={'labels': y_train, 'test': X_test})

    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)
    g.set_input(X_train)

    print(classification_report(y_test, g.get_output()))
    print(g.get_output())


def plot_features(size, out):
    for bmu, labels in out.items():
        labels = list(labels)
        print(labels)

        for i in range(len(labels)):
            plt.text(bmu[0] + 0.1, bmu[1] + (i + 1) / len(labels) - 0.35, labels[i], fontsize=10)

    plt.xticks(np.arange(size + 1))
    plt.yticks(np.arange(size + 1))
    plt.grid()
    plt.show()


def train_animal():

    animal = ['Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle', 'Fox', 'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse', 'Zebra', 'Cow']
    features = [
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],    # Dove
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],    # Chicken
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],    # Duck
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],    # Goose
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Owl
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Hawk
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Eagle
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Fox
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],    # Dog
        [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Wolf
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Cat
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],    # Tiger
        [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Lion
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Horse
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Zebra
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]     # Cow
    ]
   
    feats = pd.DataFrame(features)
    feats.columns = ['Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim']
    size = 5
    g = Graph()

    som = g.create(SOM, props={'size': size, 'dim': 13, "nhood": nhood_mexican, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000})
    g.connect(g.start, som, 1)
    
    cal = g.create(Calibrate, props={"labels": animal})

    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)

    data = scale(feats.values)
    g.set_input(data)

    out = g.get_output()
    plot_features(size, out)


def train_deep_animal():
    """           *->som(size)->bmu(size)->*
                 /                          \\
                /--->som(legs)->bmu(legs)----\\
    animal -> dist                          concat -> som -> calibrate(labels)
                \\-->som(char)->bmu(char)----/
                 \\                         /
                  *->som(move)->bmu(move)->*
    """
    animal = ['Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle', 'Fox', 'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse', 'Zebra', 'Cow']
    features = [
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],    # Dove
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],    # Chicken
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],    # Duck
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],    # Goose
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Owl
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Hawk
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Eagle
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Fox
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],    # Dog
        [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Wolf
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Cat
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],    # Tiger
        [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Lion
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Horse
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Zebra
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]     # Cow
    ]

    feats = pd.DataFrame(features)
    feats.columns = ['Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim']
    g = Graph()

    sel = [(1, [0, 1, 2]), (1, [3, 4]), (1, [5, 6, 7, 8]), (1, [9, 10, 11, 12])]

    dist = g.create(Dist, props={"selections": sel})
    g.connect(g.start, dist, 1)

    som_size = g.create(SOM, props={"size": 16, "dim": 3, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_legs = g.create(SOM, props={"size": 16, "dim": 2, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_char = g.create(SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_move = g.create(SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})

    g.connect(dist, som_size, 1)
    g.connect(dist, som_legs, 2)
    g.connect(dist, som_char, 3)
    g.connect(dist, som_move, 4)

    bmu_size = g.create(BMU, props={"output": "2D"})
    bmu_legs = g.create(BMU, props={"output": "2D"})
    bmu_char = g.create(BMU, props={"output": "2D"})
    bmu_move = g.create(BMU, props={"output": "2D"})

    g.connect(som_size, bmu_size, 0)
    g.connect(som_legs, bmu_legs, 0)
    g.connect(som_char, bmu_char, 0)
    g.connect(som_move, bmu_move, 0)

    concat = g.create(Concat, props={"axis": 1})

    g.connect(bmu_size, concat, 1)
    g.connect(bmu_legs, concat, 1)
    g.connect(bmu_char, concat, 1)
    g.connect(bmu_move, concat, 1)

    size = 6

    som = g.create(SOM, props={'size': size, 'dim': 13, "nhood": nhood_mexican, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000})
   
    g.connect(concat, som, 1)

    cal = g.create(Calibrate, props={"labels": animal})

    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)

    data = scale(feats.values)
    g.set_input(data)

    out = g.get_output()

    print(out)
    plot_features(size, out)
    

def train_deep_animal_hunt():
    """           *--->som(size)->bmu(size)--->*
                 /                              \\
                /----->som(legs)->bmu(legs)------\\
    animal -> dist                          concat -> som -> calibrate(labels)
                \\---->som(char)->bmu(char)------/
                 \\                             /
                  \\-->som(hunt)->bmu(hunt)----/
                   \\                         /
                    *->som(move)->bmu(move)->*
                     (move doubles up on hunt)
    """
    animal = ['Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle',
              'Fox', 'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse', 'Zebra', 'Cow']
    features = [
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],    # Dove
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],    # Chicken
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],    # Duck
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],    # Goose
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Owl
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Hawk
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Eagle
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Fox
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],    # Dog
        [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Wolf
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Cat
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],    # Tiger
        [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Lion
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Horse
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Zebra
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]     # Cow
    ]

    feats = pd.DataFrame(features)
    feats.columns = ['Small', 'Medium', 'Big', '2-legs', '4-legs',
                     'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim']
    g = Graph()

    sel = [(1, [0, 1, 2]), (1, [3, 4]), (1, [5, 6, 7, 8]), (1, [9]), (1, [9, 10, 11, 12])]

    dist = g.create(Dist, props={"selections": sel})
    g.connect(g.start, dist, 1)

    som_size = g.create(
        SOM, props={"size": 16, "dim": 3, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_legs = g.create(
        SOM, props={"size": 16, "dim": 2, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_char = g.create(
        SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_hunt = g.create(
        SOM, props={"size": 16, "dim": 1, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som_move = g.create(
        SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})

    g.connect(dist, som_size, 1)
    g.connect(dist, som_legs, 2)
    g.connect(dist, som_char, 3)
    g.connect(dist, som_hunt, 4)
    g.connect(dist, som_move, 5)

    bmu_size = g.create(BMU, props={"output": "2D"})
    bmu_legs = g.create(BMU, props={"output": "2D"})
    bmu_char = g.create(BMU, props={"output": "2D"})
    bmu_hunt = g.create(BMU, props={"output": "2D"})
    bmu_move = g.create(BMU, props={"output": "2D"})

    g.connect(som_size, bmu_size, 0)
    g.connect(som_legs, bmu_legs, 0)
    g.connect(som_char, bmu_char, 0)
    g.connect(som_hunt, bmu_hunt, 0)
    g.connect(som_move, bmu_move, 0)

    concat = g.create(Concat, props={"axis": 1})

    g.connect(bmu_size, concat, 1)
    g.connect(bmu_legs, concat, 1)
    g.connect(bmu_char, concat, 1)
    g.connect(bmu_hunt, concat, 1)
    g.connect(bmu_move, concat, 1)

    size = 6

    som = g.create(SOM, props={'size': size, 'dim': 14,
                   "nhood": nhood_mexican, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000})

    g.connect(concat, som, 1)

    cal = g.create(Calibrate, props={"labels": animal})

    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)

    data = scale(feats.values)
    g.set_input(data)

    out = g.get_output()

    print(out)
    plot_features(size, out)


def train_deep_animal2():
    """
                  *---> (small, 2leg, feather,fly,swim)--->*
                 /                                          \\
                /                                            \\
    animal -> dist --------> (med, 4leg, hair, run)-------> concat -> som -> calibrate(labels)
                \\                                             /
                 \\                                           /
                  *---> (large, 4leg, hooves, mane, hunt)--->*
    """
    animal = ['Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle', 'Fox', 'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse', 'Zebra', 'Cow']
    features = [
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],    # Dove
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],    # Chicken
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],    # Duck
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],    # Goose
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Owl
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Hawk
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Eagle
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Fox
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],    # Dog
        [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Wolf
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Cat
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],    # Tiger
        [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Lion
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Horse
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Zebra
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]     # Cow
    ]

    feats = pd.DataFrame(features)
    feats.columns = ['Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim']
    g = Graph()

    sel = [(1, [0, 3, 8, 11, 12]), (1, [1, 4, 5, 10]), (1, [2, 4, 6, 7, 9])]

    dist = g.create(Dist, props={"selections": sel})
    g.connect(g.start, dist, 1)

    som1 = g.create(
        SOM, props={"size": 16, "dim": 5, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som2 = g.create(
        SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som3 = g.create(
        SOM, props={"size": 16, "dim": 5, "sigma": 15, "lr": 0.8, "n_iters": 10000})
  
    g.connect(dist, som1, 1)
    g.connect(dist, som2, 2)
    g.connect(dist, som3, 3)

    bmu1 = g.create(BMU, props={"output": "2D"})
    bmu2 = g.create(BMU, props={"output": "2D"})
    bmu3 = g.create(BMU, props={"output": "2D"})
  
    g.connect(som1, bmu1, 0)
    g.connect(som2, bmu2, 0)
    g.connect(som3, bmu3, 0)

    concat = g.create(Concat, props={"axis": 1})

    g.connect(bmu1, concat, 1)
    g.connect(bmu2, concat, 1)
    g.connect(bmu3, concat, 1)

    size = 6

    som = g.create(SOM, props={'size': size, 'dim': 14,
                   "nhood": nhood_mexican, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000})

    g.connect(concat, som, 1)

    cal = g.create(Calibrate, props={"labels": animal})

    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)

    data = scale(feats.values)
    g.set_input(data)

    out = g.get_output()

    print(out)
    plot_features(size, out)


def train_deep_animal_layer():
    """                                         :---------------(2leg,4leg,run)
                  *----> (small, 2leg)*-------------->*         .. pass along ..
                 /       feather,fly   \\       :     :                     |
                |           swim         *--> concat --> (fly, swim)------------------*
                /                       /             :           2leg, 4leg, run     |
    animal -> dist ----> (med, 4leg)------------->(concat)---> (small, med, large)--> *-> calibrate
                \\        hair, run     \\            : (feather, hair, hooves, mane) |
                ||                       *--> concat --> (hunt)-----------------------*
                 \\                     /             :
                  *---> (large, 4leg)->*------------->*
                    hooves, mane, hunt
    """
    animal = ['Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle', 'Fox', 'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse', 'Zebra', 'Cow']
    features = [
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],    # Dove
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],    # Chicken
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],    # Duck
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],    # Goose
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Owl
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Hawk
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],    # Eagle
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Fox
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],    # Dog
        [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Wolf
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],    # Cat
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],    # Tiger
        [0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],    # Lion
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Horse
        [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],    # Zebra
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]     # Cow
    ]

    feats = pd.DataFrame(features)
    feats.columns = ['Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim']
    g = Graph()

    sel = [(1, [0, 3, 8, 11, 12]), (1, [1, 4, 5, 10]), (1, [2, 4, 6, 7, 9])]

    dist = g.create(Dist, props={"selections": sel})
    g.connect(g.start, dist, 1)

    som11 = g.create(SOM, props={"size": 16, "dim": 5, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som12 = g.create(SOM, props={"size": 16, "dim": 4, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    som13 = g.create(SOM, props={"size": 16, "dim": 5, "sigma": 15, "lr": 0.8, "n_iters": 10000})

    g.connect(dist, som11, 1)
    g.connect(dist, som12, 2)
    g.connect(dist, som13, 3)

    bmu11 = g.create(BMU, props={"output": "2D"})
    bmu12 = g.create(BMU, props={"output": "2D"})
    bmu13 = g.create(BMU, props={"output": "2D"})

    g.connect(som11, bmu11, 0)
    g.connect(som12, bmu12, 0)
    g.connect(som13, bmu13, 0)

    con11 = g.create(Concat, props={"axis": 1})
    con12 = g.create(Concat, props={"axis": 1})

    g.connect(bmu11, con11, 1)
    g.connect(bmu12, con11, 1)
    g.connect(bmu12, con12, 1)
    g.connect(bmu13, con12, 1)

    dist_flyswim_24run = g.create(Dist, props={"selections": [(1, [3, 4]), (1, [1, 6, 8])]})
    
    g.connect(con11, dist_flyswim_24run, 1)
    som_flyswim = g.create(SOM, props={"size": 16, "dim": 2, "sigma": 15, "lr": 0.8, "n_iters": 10000})

    g.connect(dist_flyswim_24run, som_flyswim, 1)
    bmu_flyswim = g.create(BMU, props={"output": "2D"})
    g.connect(som_flyswim, bmu_flyswim, 0)
    
    node_24run = g.create(Node)
    g.connect(dist_flyswim_24run, node_24run, 2)    # skips layer

    dist_hunt = g.create(Dist, props={"selections": [(1, [4])]})
    g.connect(con12, dist_hunt, 1)
    som_hunt = g.create(SOM, props={"size": 16, "dim": 1, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    g.connect(dist_hunt, som_hunt, 1)
    bmu_hunt = g.create(BMU, props={"output": "2D"})
    g.connect(som_hunt, bmu_hunt, 0)

    con2 = g.create(Concat, props={"axis": 1})

    g.connect(bmu11, con2, 1)
    g.connect(bmu12, con2, 1)
    g.connect(bmu13, con2, 1)

    dist_sml_feats = g.create(Dist, props={"selections": [(1, [0, 5, 9, 2, 7, 8, 9])]})
    g.connect(con2, dist_sml_feats, 1)
    som_sml_feats = g.create(SOM, props={"size": 16, "dim": 7, "sigma": 15, "lr": 0.8, "n_iters": 10000})
    g.connect(dist_sml_feats, som_sml_feats, 1)
    bmu_sml_feats = g.create(BMU, props={"output": "2D"})
    g.connect(som_sml_feats, bmu_sml_feats, 0)

    con3 = g.create(Concat, props={"axis": 1})

    g.connect(bmu_flyswim, con3, 1)
    g.connect(bmu_hunt, con3, 1)
    g.connect(bmu_sml_feats, con3, 1)
    g.connect(node_24run, con3, 1)

    size = 6
    som = g.create(SOM, props={'size': size, 'dim': 13, "nhood": nhood_mexican, 'sigma': 13, 'lr': 0.8, 'n_iters': 10000})
    g.connect(con3, som, 1)
    cal = g.create(Calibrate, props={"labels": animal})

    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)
    data = scale(feats.values)
    g.set_input(data)
    out = g.get_output()
    print(out)
    plot_features(size, out)


train_deep_animal_layer()
# train_deep_animal2()
# train_deep_animal_hunt()
# train_deep_animal()
# train_animal()
# classify_iris()
# dist_som_concat()
