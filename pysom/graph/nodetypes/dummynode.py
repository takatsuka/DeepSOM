from __future__ import annotations
from node import Node

"""
    Type 5
"""


class DummyNode(Node):
    

    def init(self, uid, data=None):
        super(DummyNode, self).__init__(uid, data=data)
    
    
    """
    HELPER METHODS HERE
    """
    def __str__(self) -> str:
        str_rep = "DummyNode {}".format(self.uid)
        return str_rep
    
    """
    CUSTOM METHODS HERE
    """
    # def get_output(self, slot: int) -> Node:
    #     return self
    
    def check_slot(self, slot: int) -> bool:
        if (slot == 0):
            raise RuntimeError("Slot 0 is reserved for SOMNode")
            return False
        elif (slot < 0):
            raise RuntimeError("Slots must be positive")
            return False
        else:
            return True
        
        
if __name__ == "__main__":
    pass
    