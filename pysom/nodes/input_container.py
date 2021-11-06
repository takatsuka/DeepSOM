from __future__ import annotations
from ..node import Node


class InputContainer(Node):
    """
    Node wrapper class that provides storage of input data.

    Args:
        uid (int): the unique integer ID of the InputContainer node instance
        graph (Graph): the containing Graph instance holding the
                        constructed InputContainer node

    Attributes:
        uid (str): the unique integer ID of the Concat node instance
        incoming (list): the list of all incoming Node objects that have a
            connection to the current InputContainer node instance
    """

    def __init__(self, uid: int, graph):
        super(InputContainer, self).__init__(uid, graph)
        self.data = None

    def get_output(self, slot: int) -> object:
        """
        Getter function to return the input data held by this node.

        Args:
            slot (int): remains unused for this class.

        Returns:
            object: returns the input data as a passthrough
        """
        return self.data
