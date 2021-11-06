import numpy as np
from numpy.testing import assert_array_equal
from pysom.nodes.dist import Dist
from pysom.nodes.concat import Concat
from pysom.node import Node
from pysom.graph import Graph
import pytest


@pytest.fixture()
def resource():
    g = Graph()
    sel = [(1, [0, 2]), (1, [1])]
    dist = g.create(Dist, {"selections": sel})
    n1 = g.create(Node)
    n2 = g.create(Node)
    concat = g.create(Concat, {"axis": 1})
    g.connect(g.start, dist, 1)
    g.connect(dist, n1, 1)
    g.connect(dist, n2, 2)
    g.connect(n1, concat, 1)
    g.connect(n2, concat, 1)
    g.connect(concat, g.end, 1)
    yield {'graph': g, 'dist': dist, 'concat': concat}


def test_output(resource):
    g, concat = resource['graph'], resource['concat']
    dat = [
        [1, 2, 3],
        [4, 5, 6],
        [2, 3, 4]
    ]
    expected = [
        [1, 3, 2],
        [4, 6, 5],
        [2, 4, 3],
    ]
    dat = np.array(dat)
    g.set_input(dat)
    assert_array_equal(g.find_node(concat).get_output(slot=1), expected)
    assert isinstance(g.find_node(concat).get_output(slot=0), Concat)


def test_concat_str(resource):
    g, concat = resource['graph'], resource['concat']
    assert g.find_node(concat).__str__() == "ConcatNode 6"
    assert str(g.find_node(concat)) == "ConcatNode 6"


def test_get_output_err():
    g = Graph()
    concat_err = g.create(Concat, props={'axis': 1})
    with pytest.raises(RuntimeError) as e_info:
        g.find_node(concat_err).get_output(slot=1)
    assert str(e_info.value) == "Must add at least one array before concat"


def test_check_slot(resource):
    g, concat = resource['graph'], resource['concat']
    assert g.find_node(concat).check_slot(slot=0)
    assert g.find_node(concat).check_slot(slot=1)
    assert not g.find_node(concat).check_slot(slot=2)
