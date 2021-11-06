
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
        assert g.start == 1
        assert g.end == 2
        assert len(g.get_nodes()) == 2

    def test_graph_add_single(cls):
        props = dict()
        nid = g.create(Node, props)
        assert nid > 1
