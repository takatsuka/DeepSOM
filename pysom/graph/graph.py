from node import Node
from nodetypes.som import SOM


class Graph:
    uid = 2

    def __init__(self):
        self.start = 0
        self.end = 1

        self.nodes = {
            0: Node(self.start, data=0),
            1: Node(self.end, data=0)
        }


    def _create_node(self, node_type=None, props=None) -> Node:
        if node_type is None:
            node = Node(Graph.uid, data=data)
        else:
            node = node_type(Graph.uid, **props)

        Graph.uid += 1

        return node

    def create(self, node_type=None, props=None) -> int:
        node = self._create_node(node_type=node_type, data=data)
        return self._add_node(node)

    def get_nodes(self) -> list:
        return list(self.nodes.values())

    def _add_node(self, node: Node) -> int:
        self.nodes[node.get_id()] = node
        return node.get_id()

    def find_node(self, uid: int) -> Node:
        for node in self.nodes.values():
            if node.get_id() == uid:
                return node
        return None

    def connect(self, node1: int, node2: int, slot: int) -> bool:
        input_node = self.find_node(node1)
        output_node = self.find_node(node2)

        if (input_node is not None) and (output_node is not None):
            return output_node.add_incoming_connection(input_node, slot)
        else:
            return False

    def set_input(self, data): 
        self.find_node(self.start).data = data

    """
    SORTING METHODS
    """


def example_graph():
    """
    Example Graph:
    ~~~~~~~~~~~~~~
                     *->n4->*
                    /        \\                 Reserved Nodes       UID   Type
       start-->*-->n2-->n5--->n6--*-->end      ~~~~~~~~~~~~~~       ~~~   ~~~~~
                \\                /             * START (DummyNode)   0    input
                 *-->n3--->n7-->*              * END   (DummyNode)   1    output

    """
    pass


if __name__ == "__main__":
    g = Graph()

    # Level 1
    n2 = g.create(node_type=Node, data=1)
    n3 = g.create(node_type=Node, data=1)
    g.connect(g.start, n2, 1)
    g.connect(g.start, n3, 1)

    # Bubble
    n4 = g.create(node_type=Node, data=1)
    n5 = g.create(node_type=Node, data=1)
    g.connect(n2, n4, 1)
    g.connect(n2, n5, 1)

    # Top row
    n6 = g.create(node_type=Node, data=1)
    g.connect(n4, n6, 1)
    g.connect(n5, n6, 1)

    # Bottom row
    n7 = g.create(node_type=Node, data=1)
    g.connect(n3, n7, 1)

    # Finishing Connections
    g.connect(n6, g.end, 1)
    g.connect(n7, g.end, 1)

    # Printing Example Graph
    print(example_graph.__doc__)

    print("TOP BRANCH (up to n6)")
    print("========================")
    print("Result of n2:", g.find_node(n2).evaluate(), end="\n\n")
    print("Result of n4:", g.find_node(n4).evaluate(), end="\n\n")
    print("Result of n5:", g.find_node(n5).evaluate(), end="\n\n")
    print("Result of n6:", g.find_node(n6).evaluate(), end="\n\n")

    print("BOTTOM BRANCH (up to n7)")
    print("========================")
    print("Result of n3:", g.find_node(n3).evaluate(), end="\n\n")
    print("Result of n7:", g.find_node(n7).evaluate(), end="\n\n")

    print("OVERALL (result of END)")
    print("========================")
    print("Result of END:", g.find_node(g.end).evaluate(), end="\n\n")
