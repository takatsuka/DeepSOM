from __future__ import annotations
from graph.node import Node

"""
    Type 2
"""
class InputContainer(Node):
    
    def __init__(self, uid):
        super(InputContainer, self).__init__(uid)
    
    
    def get_output(self, slot: int) -> Node:
        return self.data
    

        
        
if __name__ == "__main__":
    pass