from __future__ import annotations
from ..node import Node
import numpy as np


class Concat(Node):
    """
    Node that accepts input and concatenates them

    Attributes:
        uid (str): the unique integer ID of the Concat node instance
        incoming (list): the list of all incoming Node objects that have a
            connection to the current BMU Node instance
    """
    def __init__(self, uid, graph, axis):
        super(Concat, self).__init__(uid, graph)
        self.precon = None
        self.axis = axis

    def __str__(self) -> str:
        str_rep = "ConcatNode {}".format(self.uid)
        return str_rep

    def _evaluate(self):
        ins = [self.get_input(index=i) for i in range(len(self.incoming))]
        self.precon = np.concatenate(tuple(ins), axis=self.axis)

        self.output_ready = True

    def get_output(self, slot: int) -> object:
        """
        Getter function to return the concatenation of associated input nodes.

        Args:
            slot (int):

        Returns:
            Node: [description]
        """
        if slot == 0:
            return self

        if not self.output_ready:
            self._evaluate()

        return self.precon

    def check_slot(self, slot: int) -> bool:
        return slot <= 1


if __name__ == "__main__":
    pass
