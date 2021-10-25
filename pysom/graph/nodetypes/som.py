from __future__ import annotations
from node import Node

"""
    Type 0
"""
class SOM(Node):
    
    def __init__(self, uid):
        print("Hello from SOMnode")
        super(SOM, self).__init__(uid)
    
    
    """
    HELPER METHODS HERE
    """
    def __str__(self) -> str:
        str_rep = "SOMNode {}".format(self.uid)
        return str_rep
    
    """
    CUSTOM METHODS HERE
    """
    def get_output(self, slot: int) -> Node:
        return self
    
    def check_slot(self, slot: int) -> bool:
        if (slot != 0):
            raise RuntimeError("SOMNode can only output to slot 0")
            return False
        else:
            # if (slot in self.slots.keys()):
            #     raise RuntimeError("Cannot duplicate the slot")
            return True
        
        
if __name__ == "__main__":
    pass