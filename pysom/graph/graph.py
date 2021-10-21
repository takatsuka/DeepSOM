from node import Node
from nodetypes.somnode import SOMNode
from nodetypes.dummynode import DummyNode


class Graph:

    uid = 2

    def __init__(self):
        self.start = None
        self.end = None
        self.nodes = dict()
        
    """
    HELPER METHODS
    """
    def create_start(self) -> Node:
        node = DummyNode(0, data=0)
        self.start = node
        return self.add_node(node)
    
    def create_end(self) -> Node:
        node = DummyNode(1, data=0)
        self.end = node
        return self.add_node(node)
            
    def create_node(self, node_type=None, data=None) -> Node:
        if node_type is None:
            node = Node(Graph.uid, data=data)
        else:
            node = node_type(Graph.uid, data=data)
            
        Graph.uid += 1
        
        return node

    def create_and_add_node(self, node_type=None, data=None) -> int:
        node = self.create_node(node_type=node_type, data=data)
        return self.add_node(node)
        
    def get_nodes(self) -> list:
        return list(self.nodes.values())
        
    def add_node(self, node: Node) -> int:
        self.nodes[node.get_id()] = node
        return node.get_id()
    
    def find_node(self, uid: int) -> Node:
        for node in self.nodes.values():
            if node.get_id() == uid:
                return node
        return None

    def add_connection(self, node1: int, node2: int, slot: int) -> bool:
        input_node = self.find_node(node1)
        output_node = self.find_node(node2)
        
        if (input_node is not None) and (output_node is not None):
            return output_node.add_incoming_connection(input_node, slot)
        else:
            return False
        
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
    
    start = g.create_start()
    end = g.create_end()
    
    # Level 1
    n2 = g.create_and_add_node(node_type=DummyNode, data=1)
    n3 = g.create_and_add_node(node_type=DummyNode, data=1)
    g.add_connection(start, n2, 1)
    g.add_connection(start, n3, 1)
    
    # Bubble
    n4 = g.create_and_add_node(node_type=DummyNode, data=1)
    n5 = g.create_and_add_node(node_type=DummyNode, data=1)
    g.add_connection(n2, n4, 1)
    g.add_connection(n2, n5, 1)

    # Top row
    n6 = g.create_and_add_node(node_type=DummyNode, data=1)
    g.add_connection(n4, n6, 1)
    g.add_connection(n5, n6, 1)
    
    # Bottom row
    n7 = g.create_and_add_node(node_type=DummyNode, data=1)
    g.add_connection(n3, n7, 1)
    
    # Finishing Connections
    g.add_connection(n6, end, 1)
    g.add_connection(n7, end, 1)

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
    print("Result of END:", g.find_node(end).evaluate(), end="\n\n")
