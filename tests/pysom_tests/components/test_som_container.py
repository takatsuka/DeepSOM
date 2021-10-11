import pytest
import numpy as np
import pysom.utils.decay_funcs as functions
import pysom.components.som as Som
import pysom.components.som_container as SomContainer
import pysom.utils.transition_funcs as transitions


def test_always_true():
    a = "some"
    b = "some"
    assert a == b

def test_initialise():

    width = 7
    height = 8
    indim = 10
    default_som = Som.Som(width, height, indim)

    cont1 = SomContainer.SomContainer(default_som, transitions.concat_binary)

    assert cont1.get_in_len() == indim
    assert cont1.get_out_len() == width * height
    assert len(cont1.in_set) == indim
    assert cont1.in_set[0] == 0
    assert cont1.in_set[indim - 1] == indim - 1

    cont2 = SomContainer.SomContainer(default_som, transitions.coordinates)

    assert cont2.get_in_len() == indim
    assert cont2.get_out_len() == 2
    assert len(cont2.in_set) == indim
    assert cont2.in_set[0] == 0
    assert cont2.in_set[indim - 1] == indim - 1

    cont3 = SomContainer.SomContainer(default_som, transitions.coordinates_distance)

    assert cont3.get_in_len() == indim
    assert cont3.get_out_len() == 3
    assert len(cont3.in_set) == indim
    assert cont3.in_set[0] == 0
    assert cont3.in_set[indim - 1] == indim - 1

def test_make_input():

    width = 13
    height = 22
    indim = 15
    default_som = Som.Som(width, height, indim)

    inset = tuple([i * 2 for i in range(15)])

    cont = SomContainer.SomContainer(default_som, transitions.coordinates, inset)

    invec = -np.arange(30)

    assert invec[0] == 0
    assert invec[29] == -29
    assert len(invec) == 30

    madein = cont.make_input(invec)
    assert len(madein) == 15

    for i in range(0, 15):
        assert madein[i] == -2 * i

def test_operate():
    width = 23
    height = 54
    indim = 100

    som = Som.Som(width, height, indim)
    som.regen_mat(scale=4, offset=-0.25)

    som.set_lr(lr_max=0.7, lr_min=0.001, lr_step=0.0001, lr_func=functions.linear_step)
    som.set_rad(rad_max=height / 2, rad_min=0, rad_step=0.5, rad_func=functions.exp_decay)

    cont = SomContainer.SomContainer(som, transitions.coordinates_distance)

    for i in range(100):
        data = (np.random.random((indim,)) - 0.25) * 4
        cont_output = cont.activate_som(data)
        som_output = som.get_idx_closest(data)
        cont_train = cont.train_som(data, i)

        assert cont_output[0] == som_output[0]
        assert cont_output[0] == cont_train[0]
        assert cont_output[1] == som_output[1]
        assert cont_output[1] == cont_train[1]
