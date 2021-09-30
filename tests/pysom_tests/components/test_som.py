from pysom.components.som import Som
from pysom.utils import decay_funcs as functions
import numpy as np
import math


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


def test_find_bmu():
    data = np.array([[1, 5], [3, 6], [-2, 10]])
    som = Som(3, len(data), 2)
    vector = np.array([1, 2])

    bmu_idx = som.get_idx_closest(vector)
    bmu = som.get_weight(bmu_idx[0], bmu_idx[1])

    d = math.dist(vector, bmu)
    for i in range(len(som.mat)):
        for j in range(len(som.mat[i])):

            assert d <= math.dist(vector, som.mat[i, j])
