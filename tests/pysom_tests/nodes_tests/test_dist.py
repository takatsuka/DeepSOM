import numpy as np
from numpy.testing import assert_array_equal
from pysom.nodes.dist import Dist
from pysom.graph import Graph
import pytest


@pytest.fixture()
def resource():
    g = Graph()
    sel = [(1, [0, 2]), (1, [1])]
    dist = g.create(Dist, {"selections": sel})
    g.connect(g.start, dist, 1)
    g.connect(dist, g.end, 1)
    yield {'graph': g, 'dist': dist}


def test_dist_str(resource):
    g, dist = resource['graph'], resource['dist']
    assert g.find_node(dist).__str__() == "DistNode 3"
    assert str(g.find_node(dist)) == "DistNode 3"


def test_check_slot(resource):
    g, dist = resource['graph'], resource['dist']
    dist_node = g.find_node(dist)
    assert dist_node.check_slot(0)
    assert not dist_node.check_slot(-1)
    assert dist_node.check_slot(len(dist_node.sel) + 1)  # show log output throw no error


def test_output(resource):
    g, dist = resource['graph'], resource['dist']
    dat = [
        [1, 2, 3],
        [4, 5, 6],
        [2, 3, 4]
    ]
    dat = np.array(dat)
    g.set_input(dat)
    assert_array_equal(g.find_node(dist).get_output(1), np.array([[1, 3], [4, 6], [2, 4]]))
    assert isinstance(g.find_node(dist).get_output(0), Dist)
