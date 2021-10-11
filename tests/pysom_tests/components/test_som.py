from pysom.components.som import Som
from pysom.utils import decay_funcs as functions
import numpy as np
import sys
import os


PATH_TO_DSOM = "../dsom_code"
if os.path.dirname(__file__) != "":
    PATH_TO_DSOM = os.path.dirname(__file__) + "/" + PATH_TO_DSOM
sys.path.append(PATH_TO_DSOM)

PATH_TO_DATA = "resources"
if os.path.dirname(__file__) != "":
    PATH_TO_DATA = os.path.dirname(__file__) + "/" + PATH_TO_DATA


# helper function
def dist(vector_1, vector_2):
    dims = len(vector_1)
    return np.nansum([(vector_1[i] - vector_2[i]) ** 2 for i in range(dims)])


def test_initialise():
    width = 10
    height = 20
    indim = 6
    som = Som(width, height, indim)

    assert som.mat.shape == (width, height, indim)
    assert som.mat_coord.shape == (width, height, 2)


def test_customise():
    width = 59
    height = 24
    indim = 70

    som = Som(width, height, indim)
    som.set_lr(lr_max=1, lr_min=0.005, lr_step=0.001, lr_func=functions.exp_decay)
    som.set_rad(rad_max=(width + height) / 2, rad_min=0.5, rad_step=1, rad_func=functions.linear_step)
    som.regen_mat(scale=20, offset=-0.5)

    for i in range(len(som.mat)):
        for j in range(len(som.mat[i])):
            assert som.mat[i, j].all() > -10
            assert som.mat[i, j].all() < 10

    som.set_in_norm_p(2)
    som.set_out_norm_p(1)

    for i in range(100):
        data = np.random.random((indim,))
        som.learn(data, i)
        bmu_idx = som.get_idx_closest(data)
        bmu = som.get_weight(bmu_idx[0], bmu_idx[1])

    bmu_idx = som.get_idx_closest(np.random.random(indim))
    assert len(bmu_idx) == 2
    bmu = som.get_weight(bmu_idx[0], bmu_idx[1])
    assert (som.indim,) == bmu.shape


def test_customise_2():  # doesn't seem to like this one at get_weight()
    width = 23
    height = 54
    indim = 100

    som = Som(width, height, indim)
    som.regen_mat(scale=4, offset=-0.25)

    som.set_lr(lr_max=0.7, lr_min=0.001, lr_step=0.0001, lr_func=functions.linear_step)
    som.set_rad(rad_max=height / 2, rad_min=0, rad_step=0.5, rad_func=functions.exp_decay)

    assert (som.mat >= -1).all()
    assert (som.mat <= 3).all()

    for i in range(150):
        data = (np.random.random((indim,)) - 0.25) * 4
        som.learn(data, i)
        bmu_idx = som.get_idx_closest(data)
        bmu = som.get_weight(bmu_idx[0], bmu_idx[1])

    bmu_idx = som.get_idx_closest(np.random.random(indim))
    assert len(bmu_idx) == 2
    bmu = som.get_weight(bmu_idx[0], bmu_idx[1])
    assert (som.indim,) == bmu.shape


def test_find_bmu():
    data = np.array([[1, 5], [3, 6], [-2, 10]])
    som = Som(3, len(data), 2)
    vector = np.array([1, 2])

    bmu_idx = som.get_idx_closest(vector)
    bmu = som.get_weight(bmu_idx[0], bmu_idx[1])

    d = dist(vector, bmu)

    for i in range(len(som.mat)):
        for j in range(len(som.mat[i])):

            assert d <= dist(vector, som.mat[i, j])


def test_find_bmu_2():
    data = np.array([[1, 5, 2], [3, 6, 4], [-2, 10, 8]])
    som = Som(3, len(data), 3)
    vector = np.array([9, 21, 3])

    bmu_idx = som.get_idx_closest(vector)
    bmu = som.get_weight(bmu_idx[0], bmu_idx[1])

    d = dist(vector, bmu)

    for i in range(len(som.mat)):
        for j in range(len(som.mat[i])):

            assert d <= dist(vector, som.mat[i, j])


def test_find_bmu_3():
    data = np.array([[1, 5, 2, 4, 7], [3, 6, 4, 9, 8], [-2, 10, 8, 0, 9]])
    som = Som(3, len(data), 5)
    vector = np.array([0, 1, 0, 21, -5])

    bmu_idx = som.get_idx_closest(vector)
    bmu = som.get_weight(bmu_idx[0], bmu_idx[1])

    d = dist(vector, bmu)

    for i in range(len(som.mat)):
        for j in range(len(som.mat[i])):
            assert d <= dist(vector, som.mat[i, j])


def test_sphere_learn():
    width = 100
    height = 100
    indim = 3

    som = Som(width, height, indim)
    som.regen_mat(scale=2, offset=-0.5)

    data_file = open(PATH_TO_DATA + "/sphere_4096.txt", "r")
    dataset_lines = data_file.readlines()
    data_file.close()

    for i in range(len(dataset_lines)):
        dataset_lines[i] = dataset_lines[i].strip("\n").split(",")
        for j in range(len(dataset_lines[i])):
            dataset_lines[i][j] = float(dataset_lines[i][j])

    data = np.array(dataset_lines)

    for i in range(16384):
        point = data[np.random.randint(0, len(data))]
        som.learn(point, i)
