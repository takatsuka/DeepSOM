from pysom.components.som import Som
from pysom.utils import decay_funcs as functions


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
            assert som.mat[i, j].any() > -10
            assert som.mat[i, j].any() < 10
