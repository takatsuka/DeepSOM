
from pysom.graph import Graph
from pysom.node import Node


class TestGraph:

    @classmethod
    def setup_class(cls):
        global g
        g = Graph()

    @classmethod
    def teardown_class(cls):
        pass

    def test_graph_init(cls):
        assert g.start == 0
        assert g.end == 1
        assert len(g.get_nodes()) == 2

    def test_graph_add_single(cls):
        nid = g.create()
        assert nid > 1

    def test_graph_add_single_default(cls):
        nid = g.create()
        node = g.find_node(nid)
        assert(type(node) is Node)

    def test_graph_add_multiple_default(cls):
        assert len(g.get_nodes()) == 2
        nid1 = g.create()
        nid2 = g.create()
        assert len(g.get_nodes()) == 4
        assert (g.find_node(nid1) is not None)
        assert (g.find_node(nid2) is not None)
