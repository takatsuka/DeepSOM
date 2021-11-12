from __future__ import annotations
from ..node import Node
import numpy as np


class Scale(Node):
    """
    Node that standardize data
    This is an example of a very simple functional node.

    """

    def __init__(self, uid: int, graph):
        super(Scale, self).__init__(uid, graph)

    def __str__(self) -> str:
        str_rep = "ScaleNode {}".format(self.uid)
        return str_rep

    def get_output(self, slot: int) -> object:

        if slot == 0:
            return self

        m = self.get_input()
        m = (m - np.mean(m, axis=0)) / np.std(m, axis=0)

        return m

    def check_slot(self, slot: int) -> bool:

        if not (0 <= slot <= 1):
            self.graph._log_ex(f"Slots {slot} is not acceptable for {self}")
            return False
        else:
            return True
