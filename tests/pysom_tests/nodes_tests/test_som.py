from pysom.nodes.som import SOM, dist_manhattan, dist_euclidean, dist_cosine, exponential_decay, reduce_params, nhood_gaussian, nhood_mexican, meshgrid, arange
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal
from numpy import zeros, ones, sqrt, array, linalg, ravel
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
        som.weights[1, i] = i + 1
    yield som
        

def test_hard_code(som_resource):
    assert_array_equal(som_resource.weights[1], array([[1, 1, 1],
                                                       [2, 2, 2],
                                                       [3, 3, 3]]))


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


def test_verify_pos(som_resource):
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
