from pysom.nodes.som import SOM, dist_manhattan, dist_euclidean, dist_cosine, exponential_decay, reduce_params
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal
from numpy import zeros, ones, sqrt, array, linalg
import pytest


def test_dist_manhattan():
    data = [[0, 0]]
    weights = [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]
    dist = dist_manhattan(weights, data)
    assert_array_equal(dist, [[2, 2], [2, 2]])


def test_dist_euclidean():
    data = [[0, 0]]
    weights = [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]
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
        assert e_info == "input is 'list', expecting 'numpy.ndarray'"


def test_dist_cosine_error_weights():
    data = array([[0, 0]])
    weights = [[[1, 1], [1, 1]],
               [[1, 1], [1, 1]]]
    with pytest.raises(ValueError) as e_info:
        dist_cosine(data, weights)
        assert e_info == "input is 'list', expecting 'numpy.ndarray'"


def test_exponential_decay():
    assert exponential_decay(0.7, 6, 9) == 0.7 / (1 + 6 / (9 / 2))
    assert exponential_decay(7.4, 9, 4) == 7.4 / (1 + 9 / (4 / 2))
    assert exponential_decay(7.4, 6, 9) == 7.4 / (1 + 6 / (9 / 2))
    assert exponential_decay(sqrt(2), 1, 1) == sqrt(2) / (1 + 1 / (1 / 2))


def test_exponential_decay_error():
    with pytest.raises(ValueError) as e_info:
        exponential_decay(30, 20, 0)
        assert e_info == "max_iter must be positive"


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
def weights(som):
    w_len = len(som.weights)
    # hard coding weights
    som.weights = zeros((w_len, w_len, w_len))
    for i in range(0, w_len):
        som.weights[1, i] = i + 1
    yield som.weights
        

def test_hard_code(weights):
    assert_array_equal(weights[1], array([[1., 1., 1.],
                                          [2., 2., 2.],
                                          [3., 3., 3.]]))

    
def test_check_dims():
    pass
