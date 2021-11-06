from __future__ import annotations
from ..node import Node

"""
    Input Container
    Contains input
"""


class InputContainer(Node):

    def __init__(self, uid, graph):
        super(InputContainer, self).__init__(uid, graph)
        self.data = None

    def get_output(self, slot: int) -> Node:
        return self.data
