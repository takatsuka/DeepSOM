import pytest
import numpy as np

import pysom.utils.transition_funcs as tf
import pysom.utils.decay_funcs as df
from pysom.components.som import Som
from pysom.components.som_container import SomContainer
from pysom.deep_som import DeepSom


def test_always_true():
    a = "some"
    b = "some"
    assert a == b

def test_defaults():
    indim = 30
    dsom = DeepSom(indim)

    assert dsom.get_layer_count() == 1
    assert dsom.get_som_count() == 0

def test_malformed():
    indim = 30
    dsom = DeepSom(indim)

    lay1 = dsom.get_layer(0)

    lay1.add_som_container(
        SomContainer(
            Som(6, 6, 15),
            tf.concat_binary,
            in_set=tuple([i for i in range(15)])))
    lay1.add_som_container(
        SomContainer(
            Som(8, 8, 15),
            tf.concat_binary,
            in_set=tuple([i + 20 for i in range(15)])))

    dsom.add_layer()
    lay2 = dsom.get_layer(1)

    lay2.add_som_container(
        SomContainer(
            Som(10, 10, 50),
            tf.coordinates_distance,
            in_set=tuple([2 * i for i in range(50)])))
    lay2.add_som_container(
        SomContainer(
            Som(10, 10, 50),
            tf.coordinates_distance,
            in_set=tuple([2 * i + 1 for i in range(50)])))

    assert dsom.get_layer_count() == 2
    assert dsom.get_som_count() == 4

    errors = dsom.check_structure(output="")
    assert errors != ""

    with pytest.raises(AttributeError):
        dsom.check_structure(output="crash")

    with pytest.raises(AttributeError):
        dsom.check_structure()

def test_run_dsom():
    indim = 25
    dsom = DeepSom(indim)

    lay1 = dsom.get_layer(0)
    for i in range(5):
        lay1.add_som_container(
            SomContainer(
                Som(10, 10, 5),
                tf.coordinates_distance,
                in_set=tuple([j + 5 * i for j in range(5)])))

    dsom.add_layer()
    lay2 = dsom.get_layer(1)

    # 5 SOMs using the coordinates_distance transition function will have
    # 15 dimensional output.
    # We want one of the layer 2 SOMs to accept all the coordinate entries
    # and one to accept all the distance entries.
    in_set1 = []
    in_set2 = []
    for i in range(15):
        if i % 3 == 2:
            in_set2.append(i)
        else:
            in_set1.append(i)

    som1l2 = Som(5, 5, 10)
    som1l2.regen_mat(scale=10, offset=0)
    som1l2.set_lr(lr_max=2, lr_min=0.1, lr_step=0.1,
                    lr_func=df.linear_step)
    som1l2.set_rad(rad_max=6, rad_min=0, rad_step=0.5,
                    rad_func=df.exp_decay)

    lay2.add_som_container(
        SomContainer(
            som1l2,
            tf.concat_binary,
            in_set=in_set1))

    som2l2 = Som(5, 5, 5)
    som2l2.set_lr(lr_max=1, lr_min=0.1, lr_step=0.001,
                    lr_func=df.exp_decay)
    som2l2.set_rad(rad_max=3, rad_min=0, rad_step=0.2,
                    rad_func=df.linear_step)

    lay2.add_som_container(
        SomContainer(
            som2l2,
            tf.concat_binary,
            in_set=in_set2))

    dsom.add_layer()
    lay3 = dsom.get_layer(2)

    # 2 Soms of output 5x5 each using concat_binary transition function
    # results in 50 dimensional output.
    som1l3 = Som(3, 3, 50)
    lay3.add_som_container(
        SomContainer(
            som1l3,
            tf.coordinates))

    assert dsom.get_layer_count() == 3
    assert dsom.get_som_count() == 8
    errors = dsom.check_structure(output="")
    assert errors == ""

    # The method should not crash since the SOM has been constructed
    # correctly.
    dsom.check_structure(output="crash")
    dsom.check_structure()

    for i in range(0, 10):
        data = np.random.random(25)
        answer = dsom.activate_dsom(data)
        train_answer = dsom.train_dsom(data, i)
        assert len(answer) == 2
        assert len(train_answer) == 2
        assert answer[0] == train_answer[0]
        assert answer[1] == train_answer[1]
