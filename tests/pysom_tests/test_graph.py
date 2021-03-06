import pytest
from pysom.graph import LOGLEVEL_ALLEXCEPTION, Graph, GraphCompileError
from pysom.node import Node
from pysom.nodes.bmu import BMU
from pysom.nodes.calibrate import Calibrate
from pysom.nodes.concat import Concat
from pysom.nodes.dist import Dist
from pysom.nodes.input_container import InputContainer
from pysom.nodes.som import SOM

"""
Setup and Teardown
"""


def setup_function():
    global g
    g = Graph()


def teardown_function():
    pass


"""
Misc tests
"""


def test_exception_handler():
    with pytest.raises(GraphCompileError):
        g2 = Graph(loglevel=LOGLEVEL_ALLEXCEPTION)
        g2.create_with_id(1)


"""
Construction tests
"""


def test_graph_init():
    assert g.start == 1
    assert g.end == 2
    assert len(g.get_nodes()) == 2


def test_graph_add_single():
    nid = g.create()
    assert nid > 2


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


def test_graph_add_subtype_BMU():
    nid = g.create(node_type=BMU)
    assert (type(g.find_node(nid)) is BMU)


def test_graph_add_subtype_calibrate():
    nid = g.create(node_type=Calibrate)
    assert (type(g.find_node(nid)) is Calibrate)


def test_graph_add_subtype_concatenate():
    props = dict()
    props["axis"] = 0
    nid = g.create(node_type=Concat, props=props)
    assert (type(g.find_node(nid)) is Concat)


def test_graph_add_subtype_distance():
    nid = g.create(node_type=Dist)
    assert (type(g.find_node(nid)) is Dist)


def test_graph_add_subtype_input_container():
    nid = g.create(node_type=InputContainer)
    assert (type(g.find_node(nid)) is InputContainer)


def test_graph_add_subtype_som():
    props = dict()
    props["size"] = 1
    props["dim"] = 1
    nid = g.create(node_type=SOM, props=props)
    assert (type(g.find_node(nid)) is SOM)


def test_graph_custom_id_basic():
    nid = g.create_with_id(10)
    assert (nid == 10)
    assert (g.find_node(10) is not None)


def test_graph_custom_id_override_inbuilts():
    nid1 = g.create_with_id(1)  # Start
    nid2 = g.create_with_id(2)  # End

    assert (len(g.get_nodes()) == 2)
    assert (nid1 == -1)
    assert (nid2 == -1)

    assert (g.find_node(nid1) is None)
    assert (g.find_node(nid2) is None)


def test_graph_custom_id_duplicate():
    nid1 = g.create_with_id(3)  # Start
    nid2 = g.create_with_id(3)  # End

    assert (nid1 != -1)
    assert (nid2 == -1)

    assert (g.find_node(nid1) is not None)
    assert (g.find_node(nid2) is None)

    assert (len(g.get_nodes()) == 3)


"""
Getter and Setter Tests
"""


def test_find_node_good():
    nid = g.create(node_type=Node)
    node = g.find_node(nid)
    assert (node is not None)


def test_find_node_bad():
    node = g.find_node(-1)
    assert (node is None)


def test_get_nodes_basic():
    nid = g.create(node_type=Node)
    nodes = g.get_nodes()
    assert (len(nodes) == 3)

    node = g.find_node(nid)
    assert (nid in nodes.keys())
    assert (nodes[nid] is node)


def test_get_nodes_multiple():
    nid1 = g.create()
    nid2 = g.create()
    nodes = g.get_nodes()

    assert (len(nodes) == 4)

    node1 = g.find_node(nid1)
    node2 = g.find_node(nid2)

    assert (nid1 in nodes.keys())
    assert (nid2 in nodes.keys())
    assert (nodes[nid1] is node1)
    assert (nodes[nid2] is node2)


def test_extract_output_untrained():
    g.create_with_id(100)
    g.set_input(g.find_node(100))
    g.connect(g.start, g.end, 1)

    end_out = g.get_output(1)

    assert (end_out is not None)  # return type is not strict


def test_extract_output_bad_slot():
    end_out = g.get_output(1)
    assert (end_out is None)


def test_extract_output_identity():
    end_out = g.get_output(0)

    assert (end_out is g.find_node(g.end))


def test_set_param():
    try:
        g.set_param("the truth", True)
    except Exception:
        pytest.fail("Should have passed")


def test_set_param_empty():
    try:
        g.set_param("", None)
    except Exception:
        pytest.fail("Should have passed")


def test_set_param_nonstring():
    with pytest.raises(Exception):
        g.set_param(1, "one")


"""
Connection Tests
"""


def test_graph_connect_default_good():
    assert (g.connect(g.start, g.end, 1) is True)


def test_graph_connect_default_self():
    assert (g.connect(g.start, g.start, 1) is False)
    assert (g.connect(g.end, g.end, 1) is False)


def test_graph_connect_new_self():
    nid = g.create()
    assert (g.connect(nid, nid, 1) is False)


def test_graph_connect_invalid():
    assert (g.connect(g.start, -1, 1) is False)
    assert (g.connect(-1, g.end, 1) is False)
    assert (g.connect(-1, -1, 1) is False)


def test_graph_backwards():
    assert (g.connect(g.end, g.start, 1) is True)


# This should be mocked honestly...
def test_bad_connection_default_node():
    nid = g.create()

    assert (g.connect(nid, g.end, 2) is False)  # Node requires 0 or 1


def test_graph_add_connect_single_path():
    nid = g.create()
    start = g.find_node(g.start)
    mid = g.find_node(nid)
    end = g.find_node(g.end)

    assert (len(start.get_incoming()) == 0)
    assert (len(mid.get_incoming()) == 0)
    assert (len(end.get_incoming()) == 0)

    assert (g.connect(g.start, nid, 1) is True)
    assert (g.connect(nid, g.end, 1) is True)

    assert (len(start.get_incoming()) == 0)
    assert (len(mid.get_incoming()) == 1)
    assert (len(end.get_incoming()) == 1)

    assert (len(g.get_nodes()) == 3)


def test_graph_add_connect_skip_new():
    nid = g.create()
    start = g.find_node(g.start)
    mid = g.find_node(nid)
    end = g.find_node(g.end)

    assert (mid is not None)

    assert (len(start.get_incoming()) == 0)
    assert (len(mid.get_incoming()) == 0)
    assert (len(end.get_incoming()) == 0)

    assert (g.connect(g.start, g.end, 1) is True)

    assert (len(start.get_incoming()) == 0)
    assert (len(mid.get_incoming()) == 0)
    assert (len(end.get_incoming()) == 1)

    assert (len(g.get_nodes()) == 3)


def test_graph_add_multiple_long_path():
    nid1 = g.create()
    nid2 = g.create()
    nid3 = g.create()
    nid4 = g.create()

    node1 = g.find_node(nid1)
    node2 = g.find_node(nid2)
    node3 = g.find_node(nid3)
    node4 = g.find_node(nid4)

    assert (node1 is not None)
    assert (node2 is not None)
    assert (node3 is not None)
    assert (node4 is not None)

    assert (len(g.get_nodes()) == 6)

    assert (g.connect(g.start, nid1, 1) is True)
    assert (g.connect(nid1, nid2, 1) is True)
    assert (g.connect(nid2, nid3, 1) is True)
    assert (g.connect(nid3, nid4, 1) is True)
    assert (g.connect(nid4, g.end, 1) is True)

    start = g.find_node(g.start)
    end = g.find_node(g.end)

    assert (len(start.get_incoming()) == 0)
    assert (len(node1.get_incoming()) == 1)
    assert (len(node2.get_incoming()) == 1)
    assert (len(node3.get_incoming()) == 1)
    assert (len(node4.get_incoming()) == 1)
    assert (len(end.get_incoming()) == 1)


def test_graph_branched_paths():
    nid1 = g.create()
    nid2 = g.create()
    nid3 = g.create()
    nid4 = g.create()

    node1 = g.find_node(nid1)
    node2 = g.find_node(nid2)
    node3 = g.find_node(nid3)
    node4 = g.find_node(nid4)

    assert (node1 is not None)
    assert (node2 is not None)
    assert (node3 is not None)
    assert (node4 is not None)

    assert (len(g.get_nodes()) == 6)

    assert (g.connect(g.start, nid1, 1) is True)
    assert (g.connect(g.start, nid2, 1) is True)
    assert (g.connect(nid1, nid3, 1) is True)
    assert (g.connect(nid2, nid4, 1) is True)
    assert (g.connect(nid3, g.end, 1) is True)
    assert (g.connect(nid4, g.end, 1) is True)

    start = g.find_node(g.start)
    end = g.find_node(g.end)

    assert (len(start.get_incoming()) == 0)
    assert (len(node1.get_incoming()) == 1)
    assert (len(node2.get_incoming()) == 1)
    assert (len(node3.get_incoming()) == 1)
    assert (len(node4.get_incoming()) == 1)
    assert (len(end.get_incoming()) == 2)
