from pysom.nodes.som import SOM, dist_manhattan, dist_euclidean, dist_cosine, exponential_decay, reduce_params, nhood_gaussian, nhood_mexican, nhood_bubble, meshgrid, arange
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal
from numpy import zeros, sqrt, array, linalg
from pysom.graph import Graph
import numpy as np
import pytest


def test_dist_manhattan():
    data = [[0, 0]]
    weights = [[[1, 1], [1, 1]],
               [[1, 1], [1, 1]]]
    dist = dist_manhattan(weights, data)
    assert_array_equal(dist, [[2, 2], [2, 2]])


def test_dist_euclidean():
    data = [[0, 0]]
    weights = [[[1, 1], [1, 1]],
               [[1, 1], [1, 1]]]
    dist = dist_euclidean(data, weights)
    assert_array_almost_equal(dist, [[sqrt(2), sqrt(2)],
                                     [sqrt(2), sqrt(2)]])


def test_dist_cosine():
    # requires input to be numpy array due to type error (non-int * list)
    data = array([[0, 0]])
    weights = array([[[1, 1], [1, 1]],
                     [[1, 1], [1, 1]]])
    dist = dist_cosine(data, weights)
    assert_array_almost_equal(dist, [[1, 1], [1, 1]])


def test_dist_cosine_error_data():
    # requires input to be numpy array due to type error (non-int * list)
    data = [[0, 0]]
    weights = array([[[1, 1], [1, 1]],
                     [[1, 1], [1, 1]]])
    with pytest.raises(ValueError) as e_info:
        dist_cosine(data, weights)
    assert str(e_info.value) == "input is 'list', expecting 'numpy.ndarray'"


def test_dist_cosine_error_weights():
    data = array([[0, 0]])
    weights = [[[1, 1], [1, 1]],
               [[1, 1], [1, 1]]]
    with pytest.raises(ValueError) as e_info:
        dist_cosine(data, weights)
    assert str(e_info.value) == "input is 'list', expecting 'numpy.ndarray'"


def test_exponential_decay():
    assert exponential_decay(0.7, 6, 9) == 0.7 / (1 + 6 / (9 / 2))
    assert exponential_decay(7.4, 9, 4) == 7.4 / (1 + 9 / (4 / 2))
    assert exponential_decay(7.4, 6, 9) == 7.4 / (1 + 6 / (9 / 2))
    assert exponential_decay(sqrt(2), 1, 1) == sqrt(2) / (1 + 1 / (1 / 2))


def test_exponential_decay_error():
    with pytest.raises(ValueError) as e_info:
        exponential_decay(30, 20, 0)
    assert str(e_info.value) == "max_iter must be positive"


def test_reduce_params():
    lr, sig = 0.7, 7.4
    assert exponential_decay(0.7, 6, 9), exponential_decay(7.4, 6, 9) == reduce_params(lr, sig, 6, 9)
    assert exponential_decay(lr, 6, 9), exponential_decay(sig, 6, 9) == reduce_params(lr, sig, 6, 9)
    assert 0.7 / (1 + 6 / (9 / 2)), 7.4 / (1 + 6 / (9 / 2)) == reduce_params(lr, sig, 6, 9)


@pytest.fixture()
def som():
    yield SOM(None, None, size=3, dim=3)


def test_resource(som):
    w_len = len(som.weights)
    for i in range(0, w_len):
        for j in range(0, w_len):
            assert_almost_equal(1., linalg.norm(som.weights[i, j]))
    

@pytest.fixture()
def som_resource(som):
    w_len = len(som.weights)
    # hard coding weights
    som.weights = zeros((w_len, w_len, w_len))
    for i in range(0, w_len):
        som.weights[i] = i + 1
    yield som
        

def test_hard_code(som_resource):
    for i in range(0, len(som_resource.weights)):
        assert_array_equal(som_resource.weights[i], array([[i + 1] * 3] * 3))

    
def test_check_dims(som):
    assert som._check_dims([[1, 1, 1],
                            [2, 2, 2],
                            [3, 3, 3]])
    assert som._check_dims([[1, 1, 1],
                            [2, 2, 2]])
    assert som._check_dims([[1, 1, 1]])

    assert som.train([[1, 1, 1],
                      [2, 2, 2],
                      [3, 3, 3]]) is None  # implies data is well formed for training


def test_check_dims_error(som):
    with pytest.raises(ValueError) as e_info:
        som._check_dims([[1, 1],
                         [2, 2],
                         [3, 3]])
    assert str(e_info.value) == "Expecting 3 dimensions, input has 2"
    with pytest.raises(ValueError) as e_info:
        som._check_dims([[1, 1, 1],
                         [2, 2],
                         [3, 3, 3]])
    assert str(e_info.value) == "Expecting 3 dimensions, input has 2 in row 1"


def test_nhood_gaussian(som_resource):
    distr = nhood_gaussian((0, 0), som_resource.x_mat, som_resource.y_mat, som_resource.sigma)
    assert distr.max() == 1  # always will be max value unless indices exceed l * w of bmu grid
    assert distr.argmax() == 0  # max value will be in left corner of the grid when (0, 0)
    distr = nhood_gaussian((1, 1), som_resource.x_mat, som_resource.y_mat, som_resource.sigma)
    assert distr.max() == 1
    assert distr.argmax() == 4  # max value will be in center of 3 x 3 grid i.e. @ (1, 1) -> i = 4
    distr = nhood_gaussian((2, 2), som_resource.x_mat, som_resource.y_mat, som_resource.sigma)
    assert distr.max() == 1
    assert distr.argmax() == 8  # max value will be in bottom right of 3 x 3 grid i.e. @ (2, 2) -> i = 8


def test_nhood_mexican(som_resource):
    # similar behaviour to gaussian except peak and steep is much more prominent
    distr = nhood_mexican((0, 0), som_resource.x_mat, som_resource.y_mat, som_resource.sigma)
    # always will be max value unless indices exceed l * w of bmu grid
    assert distr.max() == 1
    assert distr.argmax() == 0  # max value will be in left corner of the grid when (0, 0)
    distr = nhood_mexican((1, 1), som_resource.x_mat, som_resource.y_mat, som_resource.sigma)
    assert distr.max() == 1
    # max value will be in center of 3 x 3 grid i.e. @ (1, 1) -> i = 4
    assert distr.argmax() == 4
    distr = nhood_mexican((2, 2), som_resource.x_mat, som_resource.y_mat, som_resource.sigma)
    assert distr.max() == 1
    # max value will be in bottom right of 3 x 3 grid i.e. @ (2, 2) -> i = 8
    assert distr.argmax() == 8


def test_nhood_bubble(som_resource):
    # in grid of size (3,3) and a bmu @ (1,1), if sigma=0, all coords will be 0
    distr = nhood_bubble((1, 1), som_resource.x_neig, som_resource.y_neig, sigma=0)
    assert not distr.any() == 1
    assert sum(sum(distr)) == 0
    # in grid of size (3,3) and a bmu @ (1,1), if sigma=1, (1,1) should only be 1
    distr = nhood_bubble((1, 1), som_resource.x_neig, som_resource.y_neig, sigma=1)
    assert distr.any() == 1
    assert sum(sum(distr)) == 1
    # in grid of size (3,3) and a bmu @ (1,1), if sigma=2, all coords will be 1
    distr = nhood_bubble((1, 1), som_resource.x_neig, som_resource.y_neig, sigma=2)
    assert distr.all() == 1
    assert sum(sum(distr)) == 9


def test_verify_pos(som_resource):
    # only used in mexican hat and gaussian nhood funcs
    mesh_x, mesh_y = meshgrid(arange(6), arange(7))

    with pytest.raises(ValueError) as e_info:
        nhood_gaussian((6, 5), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "At least the x coordinate of BMU is out of bounds!"
    with pytest.raises(ValueError) as e_info:
        nhood_mexican((6, 5), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "At least the x coordinate of BMU is out of bounds!"
    with pytest.raises(ValueError) as e_info:
        nhood_gaussian((5, 6), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "The y coordinate of BMU is out of bounds!"
    with pytest.raises(ValueError) as e_info:
        nhood_mexican((5, 6), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "The y coordinate of BMU is out of bounds!"

    mesh_x, mesh_y = meshgrid(arange(7), arange(6))

    with pytest.raises(ValueError) as e_info:
        nhood_gaussian((6, 5), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "At least the x coordinate of BMU is out of bounds!"
    with pytest.raises(ValueError) as e_info:
        nhood_mexican((6, 5), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "At least the x coordinate of BMU is out of bounds!"
    with pytest.raises(ValueError) as e_info:
        nhood_gaussian((5, 6), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "The y coordinate of BMU is out of bounds!"
    with pytest.raises(ValueError) as e_info:
        nhood_mexican((5, 6), mesh_x, mesh_y, som_resource.sigma)
    assert str(e_info.value) == "The y coordinate of BMU is out of bounds!"


def test_bmu(som_resource):  # TODO: More tests pending (just uses defaults atm - behaviour should be similar)
    d1, d2, d3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]], [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    bm1, bm2, bm3 = som_resource.bmu(d1), som_resource.bmu(d2), som_resource.bmu(d3)
    assert (bm1, bm2, bm3) == ((0, 0), (1, 0), (2, 0))
    d4, d5 = [[1, 1, 2], [1, 1, 1], [1, 1, 1]], [[1, 2, 3], [1, 2, 2], [1, 1, 1]]
    bm4, bm5 = som_resource.bmu(d4), som_resource.bmu(d5)
    assert (bm4, bm5) == ((0, 1), (0, 2))


def test_activate(som_resource):
    d1, d2, d3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]], [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    som_resource.activate(d1)
    assert_array_equal(som_resource.map[0], array([0, 0, 0]))
    assert_array_equal(som_resource.map[1] * 2, som_resource.map[2])
    som_resource.activate(d2)
    assert_array_equal(som_resource.map[1], array([0, 0, 0]))
    assert_array_equal(som_resource.map[0], som_resource.map[2])
    som_resource.activate(d3)
    assert_array_equal(som_resource.map[2], array([0, 0, 0]))
    assert_array_equal(som_resource.map[1] * 2, som_resource.map[0])


def test_get_weights(som_resource):
    w1, w2, w3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2]], [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    assert som_resource.get_weights().shape == (9, 3)   # flattened from (3, 3, 3)
    assert_array_equal(som_resource.get_weights()[0:3], w1)
    assert_array_equal(som_resource.get_weights()[3:6], w2)
    assert_array_equal(som_resource.get_weights()[6:9], w3)


@pytest.fixture()
def fix_som(som_resource):
    for i in range(0, 3):
        som_resource.weights[i] -= 1
    yield som_resource


@pytest.fixture()
def resource():
    data = [[0, 1, 0], [1, 0, 1], [1, 0, 0], [0, 1, 1]]
    labels = ['dog', 'human', 'monkey', 'unicorn']
    yield {'data': data, 'labels': labels}


def test_map_labels(fix_som, resource):
    mp = fix_som.map_labels(resource['data'], resource['labels'])
    assert list(mp[(0, 0)]) == ['dog', 'monkey']
    assert list(mp[(1, 0)]) == ['human', 'unicorn']


@pytest.fixture()
def hex_som():
    som = SOM(None, None, 3, 2, hexagonal=True)
    yield som


def test_offset(hex_som, fix_som):
    assert_array_equal(hex_som.x_mat[0], hex_som.x_mat[1] - 0.5)
    assert_array_equal(hex_som.x_mat[1], fix_som.x_mat[1])
    assert_array_equal(hex_som.x_mat[2], hex_som.x_mat[1] - 0.5)
    assert_array_equal(hex_som.x_mat[0], hex_som.x_mat[0])


def test_som_str():
    som = SOM(uid=3, graph=None, size=3, dim=3)
    assert som.__str__() == "SOMNode 3"
    assert str(som) == "SOMNode 3"


def test_update():
    som_gaus = SOM(None, None, size=1, dim=1, lr=1, sigma=1)
    som_gaus.update([1], (0, 0), 1, 2)
    som_mexi = SOM(None, None, nhood=nhood_mexican, size=1, dim=1, lr=1, sigma=1)
    som_mexi.update([1], (0, 0), 1, 2)
    som_bubb = SOM(None, None, nhood=nhood_bubble, size=1, dim=1, lr=1, sigma=1)
    som_bubb.update([1], (0, 0), 1, 2)


@pytest.fixture()
def sphere():
    file_path = "datasets/sphere/sphere_64.txt"
    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]
    yield array(data)


def test_run(sphere):
    som = SOM(None, None, 20, 3, 13, 0.7, 1000, nhood=nhood_bubble, dist=dist_cosine, rand_state=True)
    som.train(sphere)
    assert som.get_weights().shape == (400, 3)


# GRAPH RELATED: TODO: Most likely all functions will be covered in one hit

@pytest.fixture()
def g_resource():
    g = Graph()
    som = g.create(SOM, props={'size': 3, 'dim': 1})
    g.connect(g.start, som, 1)
    g.connect(som, g.end, 1)
    data = [[0]]
    g.set_input(data)
    yield {'graph': g, 'som': som}


def test_get_output_slot(g_resource):
    g = g_resource['graph']
    som = g_resource['som']
    assert isinstance(g.find_node(som).get_output(0), SOM)
    assert isinstance(g.find_node(som).get_output(1), np.ndarray)
    assert g.find_node(som).get_output(2) is None


def test_slot(g_resource):
    g = g_resource['graph']
    som = g_resource['som']
    assert g.find_node(som).check_slot(slot=1)
    assert g.find_node(som).check_slot(slot=0)
    assert not g.find_node(som).check_slot(slot=2)
