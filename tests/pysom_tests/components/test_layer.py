from pysom.components.som import Som
from pysom.components.layer import Layer
from pysom.components.som_container import SomContainer
from pysom.utils.transition_funcs import concat_binary
import pytest


# helper function
def setup_layer():
    layer = Layer(1)
    som = Som(3, 3, 2)
    sc = SomContainer(som, concat_binary)
    layer.add_som_container(sc)

    return layer


def test_layer_init_inlen():
    layer = Layer(9)
    assert hasattr(layer, "inlen")
    assert layer.get_in_len() == 9


def test_layer_init_inlen_na():
    layer = Layer(0)
    assert not hasattr(layer, "inlen")


def test_set_get_inlen():
    layer = Layer(9)
    assert layer.get_in_len() == 9
    layer.set_in_len(7)
    assert layer.get_in_len() == 7


def test_set_get_inlen_na():
    layer = Layer(0)
    assert not hasattr(layer, "inlen")
    layer.set_in_len(7)
    assert hasattr(layer, "inlen")
    assert layer.get_in_len() == 7


def test_get_outlen_init():
    layer = Layer(1)
    assert layer.get_out_len() == 0
    layer = Layer(0)
    assert layer.get_out_len() == 0


def test_add_container():
    layer = Layer(1)
    assert layer.get_out_len() == 0

    som = Som(3, 3, 2)
    sc = SomContainer(som, concat_binary)

    layer.add_som_container(sc)

    assert layer.get_layer_size() == 1
    assert len(layer.soms) == 1
    assert layer.get_out_len() == sc.get_out_len()
    assert layer.get_out_len() == 9


def test_insert_container():
    layer = setup_layer()

    som = Som(4, 4, 3)
    sc = SomContainer(som, concat_binary)
    layer.insert_som_container(0, sc)

    assert layer.get_layer_size() == 2
