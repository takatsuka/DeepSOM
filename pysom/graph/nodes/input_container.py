from __future__ import annotations
from graph.node import Node

"""
    Input Container
    Contains input
"""
class InputContainer(Node):
    
    def __init__(self, uid):
        super(InputContainer, self).__init__(uid)
    
    
    def get_output(self, slot: int) -> Node:
        return self.data