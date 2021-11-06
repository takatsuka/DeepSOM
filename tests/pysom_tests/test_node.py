from _pytest.outcomes import fail
import pytest
from pysom.node import Node
from pysom.graph import Graph

"""
Setup and Teardown
"""


def setup_function():
    global g
    g = Graph()


def teardown_function():
    pass


"""
Getter and setter tests
"""


def test_get_id_basic():
    node = Node(1, g)
    assert (node.get_id() == 1)


# Logic can been removed, now the owner of Node has to handle had id
# def test_get_id_bad():
#     with pytest.raises(Exception):
#         node = Node(-1, g)

def test_get_incoming_empty():
    node = Node(1, g)
    assert (len(node.get_incoming()) == 0)


def test_make_input_ready_empty():
    try:
        node = Node(1, g)
        node.make_input_ready()
    except Exception:
        fail("Making input ready on empty list of incoming should not cause \
            errors")


def test_make_input_ready_nonempty():
    try:
        n1 = g.create()
        n2 = g.create()
        g.connect(n1, n2, 0)

        node = g.find_node(n2)
        node.make_input_ready()
    except Exception:
        fail("Making input ready on a single connection should not cause \
            errors")


def test_get_input_basic():
    node1 = Node(1, g)
    node2 = Node(2, g)

    node2.add_incoming_connection(node1, 0)
    out = node2.get_input(0)
    assert (out is node1)


def test_get_input_bad_empty():
    with pytest.raises(IndexError):
        node = Node(1, g)
        node.get_input(0)


def test_get_output_identity():
    node = Node(1, g)
    assert (node.get_output(0) is node)


def test_get_output_general():
    node1 = Node(1, g)
    node2 = Node(2, g)

    node2.add_incoming_connection(node1, 0)  # passthrough connection
    res = node2.get_output(1)
    assert (res == node1)
