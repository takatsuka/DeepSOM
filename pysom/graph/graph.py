
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
        return node
    
    def create_end(self) -> Node:
        node = DummyNode(1, data=0)
        self.end = node
        return node
            
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
        

if __name__ == "__main__":
    g = Graph()
    
    start = g.create_start()
    end = g.create_end()
    
    # Level 1
    n2 = g.create_and_add_node(node_type=DummyNode, data=100)
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
    
    print("Result of n2:", g.find_node(n2).evaluate())
    print("Result of n4:", g.find_node(n4).evaluate())
    print("Result of n5:", g.find_node(n5).evaluate())
    print("Result of n6:", g.find_node(n6).evaluate())
    
    # n1 = g.create_and_add_node(node_type=DummyNode))
    # n2 = g.create_and_add_node(node_type=DummyNode))
    # x = g.create_node(node_type=SOMNode)
    # g.add_node(x)
    
    # print(n1)
    # print(g.get_nodes())
    
    
    # x1 = SOMNode(1)
    # x2 = SOMNode(5)
    # g.add_node(x1)
    # g.add_node(x2)
    
    # print(x1, x2)

    # try:        
    #     print(g.add_connection(x1.get_id, x2.get_id, 0)) # This should be True    
    #     print(g.add_connection(x1.get_id, x2.get_id, 2)) # This should raise RuntimeError  
    # except RuntimeError:
    #     print("I made a mistake :(")