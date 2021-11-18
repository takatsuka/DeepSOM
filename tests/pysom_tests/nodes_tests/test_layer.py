import numpy as np
import pytest
from pysom.graph import Graph
from pysom.nodes.dist import Dist
from pysom.nodes.concat import Concat
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.layer import Layer
from pysom.nodes.som import SOM
from pysom.nodes.bmu import BMU
from pysom.node import Node


def test_simple_2d_layer():
    parallel = True

    dat = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15, 16, 17, 18],
        [19, 20, 21, 22, 23, 24, 25, 26, 27],
        [28, 29, 30, 31, 32, 33, 34, 35, 36]
    ]
    dat = np.array(dat)

    g = Graph()

    lay1_soms = [
        {"size": 100, "dim": 3}, {"size": 100, "dim": 3},
        {"size": 100, "dim": 3}
    ]
    lay1_attrs = {"parallel_mode": parallel,
                  "all_som_props": lay1_soms, "bmu_output": "2D"}
    lay1 = g.create(Layer, lay1_attrs)

    g.connect(g.start, lay1, 1)
    g.connect(lay1, g.end, 1)

    g.set_input(dat)

    result = g.get_output()
    assert result.shape == (4, 6)


def test_simple_1d_layer():
    parallel = False

    dat = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, -1],
        [10, 11, 12, 13, 14, 15, 16, 17, 18, -2],
        [19, 20, 21, 22, 23, 24, 25, 26, 27, -3],
        [28, 29, 30, 31, 32, 33, 34, 35, 36, -4],
        [37, 38, 39, 40, 41, 42, 43, 44, 45, -5],
        [46, 47, 48, 49, 50, 51, 52, 53, 54, -6]
    ]
    dat = np.array(dat)

    g = Graph()

    lay1_soms = [
        {"size": 80, "dim": 2}, {"size": 80, "dim": 2},
        {"size": 80, "dim": 2}, {"size": 80, "dim": 2},
        {"size": 80, "dim": 2}
    ]
    lay1_attrs = {"parallel_mode": parallel,
                  "all_som_props": lay1_soms, "bmu_output": "1D"}
    lay1 = g.create(Layer, lay1_attrs)

    g.connect(g.start, lay1, 1)
    g.connect(lay1, g.end, 1)

    g.set_input(dat)

    result = g.get_output()
    assert result.shape == (6, 5)


def test_larger_2d_layer():
    parallel = False

    # 'Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim'
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
    features = np.array(features)

    g = Graph()

    # The SOMs in the layer are created with the intention to process
    # Size, Legs, Features, Hunting, Movement
    lay1_soms = [
        {"size": 120, "dim": 3}, {"size": 120, "dim": 2},
        {"size": 120, "dim": 4}, {"size": 120, "dim": 1},
        {"size": 120, "dim": 3}
    ]
    lay1_attrs = {
        "parallel_mode": parallel, "all_som_props": lay1_soms,
        "bmu_output": "2D"
    }
    lay1 = g.create(Layer, lay1_attrs)

    g.connect(g.start, lay1, 1)
    g.connect(lay1, g.end, 1)

    g.set_input(features)

    result = g.get_output()
    assert result.shape == (16, 10)


def test_larger_1d_layer():
    parallel = False

    # 'Small', 'Medium', 'Big', '2-legs', '4-legs', 'Hair', 'Hooves', 'Mane', 'Feathers', 'Hunt', 'Run', 'Fly', 'Swim'
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
    features = np.array(features)

    g = Graph()

    # The SOMs in the layer are created with the intention to process
    # Size, Legs, Features, Hunting, Movement
    lay1_soms = [
        {"size": 120, "dim": 3}, {"size": 120, "dim": 2},
        {"size": 120, "dim": 4}, {"size": 120, "dim": 1},
        {"size": 120, "dim": 3}
    ]
    lay1_attrs = {
        "parallel_mode": parallel, "all_som_props": lay1_soms,
        "bmu_output": "1D"
    }
    lay1 = g.create(Layer, lay1_attrs)

    g.connect(g.start, lay1, 1)
    g.connect(lay1, g.end, 1)

    g.set_input(features)

    result = g.get_output()
    assert result.shape == (16, 5)


def test_huge_2d_layer():
    parallel = False

    # 200 data points, 50 features
    data_shape = (200, 100)
    data = np.random.rand(data_shape[0], data_shape[1])

    g = Graph()

    lay1_soms = [
        {"size": 200, "dim": 18}, {"size": 200, "dim": 14},
        {"size": 200, "dim": 18}, {"size": 200, "dim": 12},
        {"size": 200, "dim": 8}, {"size": 200, "dim": 14},
        {"size": 200, "dim": 12}, {"size": 200, "dim": 4}
    ]
    lay1_attrs = {
        "parallel_mode": parallel, "all_som_props": lay1_soms,
        "bmu_output": "2D"
    }
    lay1 = g.create(Layer, lay1_attrs)

    g.connect(g.start, lay1, 1)
    g.connect(lay1, g.end, 1)

    g.set_input(data)

    result = g.get_output()
    # On 2d output is number of data points by number of soms x 2
    assert result.shape == (data_shape[0], 16)


def test_huge_1d_layer():
    parallel = True

    # 200 data points, 50 features
    data_shape = (200, 100)
    data = np.random.rand(data_shape[0], data_shape[1])

    g = Graph()

    lay1_soms = [
        {"size": 200, "dim": 18}, {"size": 200, "dim": 14},
        {"size": 200, "dim": 18}, {"size": 200, "dim": 12},
        {"size": 200, "dim": 8}, {"size": 200, "dim": 14},
        {"size": 200, "dim": 12}, {"size": 200, "dim": 4}
    ]
    lay1_attrs = {
        "parallel_mode": parallel, "all_som_props": lay1_soms,
        "bmu_output": "1D"
    }
    lay1 = g.create(Layer, lay1_attrs)

    g.connect(g.start, lay1, 1)
    g.connect(lay1, g.end, 1)

    g.set_input(data)

    result = g.get_output()
    # On 1D the output is number of examples by number of SOMs
    assert result.shape == (data_shape[0], 8)


def test_layer_node():
    parallel = False

    animal = [
        'Dove', 'Chicken', 'Duck', 'Goose', 'Owl', 'Hawk', 'Eagle',
        'Fox', 'Dog', 'Wolf', 'Cat', 'Tiger', 'Lion', 'Horse',
        'Zebra', 'Cow'
    ]

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
    features = np.array(features)

    g = Graph()

    lay1_soms = [
        {"size": 100, "dim": 3, "n_iters": 1000},  # size
        {"size": 100, "dim": 2, "n_iters": 1000},  # legs
        {"size": 100, "dim": 4, "n_iters": 1000},  # features
        {"size": 100, "dim": 1, "n_iters": 1000},  # hunt
        {"size": 100, "dim": 3, "n_iters": 1000}   # movement
    ]
    lay1_attrs = {
        "parallel_mode": parallel,
        "all_som_props": lay1_soms,
        "bmu_output": "2D"
    }

    lay1 = g.create(Layer, lay1_attrs)
    g.connect(g.start, lay1, 1)

    lay2_soms = [
        {"size": 100, "dim": 4, "n_iters": 1000},  # size + legs ?
        # features + hunt + movement ?
        {"size": 100, "dim": 6, "n_iters": 1000},
    ]
    lay2_attrs = {
        "parallel_mode": False,
        "all_som_props": lay2_soms,
        "bmu_output": "2D"
    }

    lay2 = g.create(Layer, lay2_attrs)
    g.connect(lay1, lay2, 1)

    size = 7
    # creating final just to calibrate on -
    som = g.create(SOM, {'size': size, 'dim': 4})
    # can redesign layer/calibrate to work together
    cal = g.create(Calibrate, {'labels': animal})

    g.connect(lay2, som, 1)
    g.connect(som, cal, 0)
    g.connect(cal, g.end, 1)

    g.set_input(features)
    g.get_output()
