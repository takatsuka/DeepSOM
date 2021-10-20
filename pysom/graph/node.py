from __future__ import annotations

"""

Types:
    0 - SOM Node
    1 - Get BMU
    2 - etc. etc.
"""
class Node:

    def __init__(self, uid, data=None):
        self.uid = uid
        self.type = 0
        self.data = data # used for storing actual SOM class
        self.incoming = list()  # 2-tuple (output_node, slot)
                
        # self.slots = list()           
        # {
        #     0: DefaultConnection(self), # only in SOMNode, unused in DistNode
        #     1: DistConnection(self, indices), # DistConnection stores the actual indices
        #     2: DistConnection(self, indices), # configured by user
        #     3: DistConnection(self, indices) # configured by user
        # }
    def __str__(self) -> str:
        str_rep = "Empty Node {}".format(self.uid)
        return str_rep
        
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Node) -> bool:
        if (isinstance(other, Node)):
            return other.uid == self.uid
        else:
            return False

    def __hash__(self) -> int:
        return self.uid   

    def get_id(self) -> int:
        return self.uid

    def get_incoming(self) -> list:
        return self.incoming

    # TO DO
    def evaluate(self) -> int:
        total = 0
        for node in self.incoming:
            print(node[0])
            total += node[0].get_output(node[1])
        return total + self.data
    
    def get_output(self, slot: int) -> int:  # change this later maybe?
        return self.evaluate()
    
    # Defer to concrete class
    def check_slot(self, slot: int) -> bool:
        return False

    # Default method for all concrete classes
    def add_incoming_connection(self, output_node: Node, slot: int) -> bool:        
        if output_node.check_outgoing_connection(self, slot):
            self.incoming.append( (output_node, slot) )
            return True
        
        return False

    # Default method for all concrete classes
    def check_outgoing_connection(self, input_node: Node, slot: int) -> bool:
        if self.check_slot(slot):
            return True
        else:
            return False

if __name__ == "__main__": 
    x1 = Node()
    x2 = Node()
    print(x1)
    print(x2)
    pass
