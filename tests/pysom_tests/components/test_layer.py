from pysom.components.som import Som
from pysom.components.layer import Layer


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
