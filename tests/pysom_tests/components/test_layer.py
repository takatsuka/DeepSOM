from pysom.components.som import Som
from pysom.components.layer import Layer
from pysom.components.som_container import SomContainer
from pysom.utils.transition_funcs import concat_binary, coordinates_distance, coordinates
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
    assert layer.get_som_container(0).get_out_len() == sc.get_out_len()
    assert layer.get_out_len() == 9


def test_insert_container():
    layer = setup_layer()

    som = Som(4, 4, 3)
    sc = SomContainer(som, concat_binary)
    layer.insert_som_container(0, sc)

    assert layer.get_layer_size() == 2
    assert layer.soms[0] == sc
    assert layer.get_out_len() == layer.get_som_container(0).get_out_len() + layer.get_som_container(1).get_out_len()


def test_defaults():
    inlen = 30
    layer = Layer(inlen)

    assert layer.get_layer_size() == 0
    assert layer.get_in_len() == inlen
    assert layer.get_out_len() == 0

    som1 = Som(5, 5, 10)
    cont1 = SomContainer(som1, concat_binary)

    layer.add_som_container(cont1)

    assert layer.get_out_len() == 25

    som2 = Som(13, 13, 10)
    cont2 = SomContainer(
        som2,
        coordinates,
        in_set=tuple([i + 10 for i in range(10)]))

    layer.add_som_container(cont2)

    assert layer.get_out_len() == 27

    som3 = Som(7, 8, 10)
    cont3 = SomContainer(
        som3,
        coordinates_distance,
        in_set=tuple([i + 20 for i in range(10)]))

    layer.add_som_container(cont3)

    assert layer.get_out_len() == 30
    assert layer.get_in_len() == 30
    assert layer.get_layer_size() == 3

def test_som_moves():
    inlen = 100
    layer = Layer(inlen)

    somc1 = SomContainer(
        Som(3, 4, 5),
        concat_binary)
    somc2 = SomContainer(
        Som(4, 3, 5),
        concat_binary,
        in_set=tuple([i + 5 for i in range(5)]))
    somc3 = SomContainer(
        Som(4, 5, 3),
        coordinates_distance,
        in_set=tuple([i + 10 for i in range(3)]))
    somc4 = SomContainer(
        Som(5, 4, 3),
        coordinates,
        in_set=tuple([i + 13 for i in range(3)]))

    layer.add_som_container(somc1)
    layer.add_som_container(somc2)
    layer.add_som_container(somc3)
    layer.add_som_container(somc4)

    assert layer.get_som_container(0) is somc1
    assert layer.get_som_container(1) is somc2
    assert layer.get_som_container(2) is somc3
    assert layer.get_som_container(3) is somc4

    layer.pop_som_container(2)
    layer.insert_som_container(0, somc3)
    layer.pop_som_container(2)
    layer.insert_som_container(5, somc2)

    assert layer.get_som_container(0) is somc3
    assert layer.get_som_container(1) is somc1
    assert layer.get_som_container(2) is somc4
    assert layer.get_som_container(3) is somc2
    