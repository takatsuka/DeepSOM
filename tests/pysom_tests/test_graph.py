
from pysom.graph import Graph
from pysom.node import Node



def setup_function():
    global g
    g = Graph()

def teardown_function():
    pass

def test_graph_init():
    assert g.start == 0
    assert g.end == 1
    assert len(g.get_nodes()) == 2

def test_graph_add_single():
    nid = g.create()
    assert nid > 1

def test_graph_add_single_default():
    nid = g.create()
    node = g.find_node(nid)
    assert(type(node) is Node)

def test_graph_add_multiple_default():
    assert len(g.get_nodes()) == 2
    nid1 = g.create()
    nid2 = g.create()
    assert len(g.get_nodes()) == 4
    assert (g.find_node(nid1) is not None)
    assert (g.find_node(nid2) is not None)
