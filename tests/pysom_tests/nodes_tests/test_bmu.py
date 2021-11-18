from numpy.testing import assert_array_equal
import numpy as np
from numpy import array
from pysom.nodes.bmu import BMU
from pysom.nodes.som import SOM
from pysom.graph import Graph
import pytest


def test_init_err():
    with pytest.raises(RuntimeError) as e_info:
        BMU(None, None, output='3D')
    assert str(e_info.value) == "Output should be either '1D', '2D' or 'w' only"


def test_init_1D():
    bmu = BMU(None, None, output='1D')
    assert bmu.get_bmu == bmu.get_1D


def test_init_weight():
    bmu = BMU(None, None, output='w')
    assert bmu.get_bmu == bmu.get_weight


def test_bmu_str():
    bmu = BMU(uid=3, graph=None, output='1D')
    assert bmu.__str__() == "BMUNode 3"
    assert str(bmu) == "BMUNode 3"


@pytest.fixture()
def g_bmu1D():
    g = Graph()
    dat = [
        [0, 0],
        [0, 0]
    ]
    dat = array(dat)
    som = g.create(SOM, props={'size': 2, 'dim': 2})
    bmu = g.create(BMU, props={'output': '1D'})
    g.connect(g.start, som, 1)
    g.connect(som, bmu, 0)
    g.connect(bmu, g.end, 1)

    # hard code SOM weights
    s = g.find_node(som)
    s.weights = [
        [[0, 0],
         [0, 0]],
        [[1, 1],
         [1, 1]]
    ]
    g.set_input(dat)
    yield {'graph': g, 'bmu': bmu}


@pytest.fixture()
def g_bmu2D():
    g = Graph()
    dat = [
        [0, 0],
        [0, 0]
    ]
    dat = array(dat)
    som = g.create(SOM, props={'size': 2, 'dim': 2})
    bmu = g.create(BMU, props={'output': '2D'})
    g.connect(g.start, som, 1)
    g.connect(som, bmu, 0)
    g.connect(bmu, g.end, 1)

    # hard code SOM weights
    s = g.find_node(som)
    s.weights = [
        [[0, 0],
         [0, 0]],
        [[1, 1],
         [1, 1]]
    ]
    g.set_input(dat)
    yield {'graph': g, 'bmu': bmu}


@pytest.fixture()
def g_bmu_weight():
    g = Graph()
    dat = [
        [0, 0],
        [0, 0]
    ]
    dat = array(dat)
    som = g.create(SOM, props={'size': 2, 'dim': 2})
    bmu = g.create(BMU, props={'output': 'w'})
    g.connect(g.start, som, 1)
    g.connect(som, bmu, 0)
    g.connect(bmu, g.end, 1)

    # hard code SOM weights
    s = g.find_node(som)
    s.weights = [
        [[0, 0],
         [0, 0]],
        [[1, 1],
         [1, 1]]
    ]
    g.set_input(dat)
    yield {'graph': g, 'bmu': bmu}


def test_get_output_slot0(g_bmu1D):
    g = g_bmu1D['graph']
    bmu = g_bmu1D['bmu']
    assert isinstance(g.find_node(bmu).get_output(0), BMU)


def test_get_output_slot1_1D(g_bmu1D):
    g = g_bmu1D['graph']
    bmu = g_bmu1D['bmu']
    out = g.find_node(bmu).get_output(slot=1)
    assert isinstance(out, np.ndarray)
    assert out.shape == (2, 1)
    assert_array_equal(out, array([[0], [0]]))


def test_get_output_slot1_2D(g_bmu2D):
    g = g_bmu2D['graph']
    bmu = g_bmu2D['bmu']
    out = g.find_node(bmu).get_output(slot=1)
    assert isinstance(out, np.ndarray)
    assert out.shape == (2, 2)
    assert_array_equal(out, array([[0, 0], [0, 0]]))


def test_get_output_slot1_weight(g_bmu_weight):
    g = g_bmu_weight['graph']
    bmu = g_bmu_weight['bmu']
    out = g.find_node(bmu).get_output(slot=1)
    assert isinstance(out, np.ndarray)
    assert out.shape == (2, 2)
    assert_array_equal(out, array([[0, 0],
                                   [0, 0]]))


@pytest.fixture()
def resource():
    g = Graph()
    s = g.create(SOM, props={'size': 3, 'dim': 1})
    bmu = g.create(BMU, props={'output': 'w'})
    g.connect(g.start, s, 1)
    g.connect(s, bmu, 0)
    g.connect(bmu, g.end, 1)
    data = [[0]]

    yield {'graph': g, 'bmu': bmu, 'som': s, 'data': data}


def test_inputs(resource):
    g = resource['graph']
    bmu = resource['bmu']
    s = resource['som']
    data = resource['data']
    expected_som = g.find_node(s)
    assert isinstance(expected_som, SOM)
    assert isinstance(g.find_node(bmu), BMU)
    g.set_input(data)
    found_som = g.find_node(bmu).get_input()
    assert isinstance(found_som, SOM)
    assert found_som == expected_som
    assert_array_equal(found_som.get_input(), data)


def test_check_slot(resource):
    g = resource['graph']
    bmu = resource['bmu']
    assert g.find_node(bmu).check_slot(0)
    assert g.find_node(bmu).check_slot(1)
    assert not g.find_node(bmu).check_slot(2)
