from __future__ import annotations
from ..node import Node
import numpy as np


class Scale(Node):
    """
    Node that simply standardises some input data.
    """

    def __init__(self, uid: int, graph):
        super(Scale, self).__init__(uid, graph)

    def __str__(self) -> str:
        str_rep = "ScaleNode {}".format(self.uid)
        return str_rep

    def get_output(self, slot: int) -> object:
        """
        Getter function to return the standarised values of an input nodeß.

        Args:
            slot (int): if 0, then the Scale node instance is returned. \
                Else the standardised values of the input data is returned.

        Returns:
            object: returns the standardised values of the input data \
                if slot is not defined as 0. Else, the Scale node \
                itself is returned.
        """
        if slot == 0:
            return self

        m = self.get_input()
        m = (m - np.mean(m, axis=0)) / np.std(m, axis=0)

        return m

    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.

        The Scale class may only accept slot value of either 0 or 1.
        Returns True if it is valid, else False is returned.

        Args:
            slot (int): a proposed integer slot ID to be checked. May only be
                        0 or 1.

        Returns:
            bool: True if the slot is valid, else returns False
        """

        if not (0 <= slot <= 1):
            self.graph._log_ex(f"Slots {slot} is not acceptable for {self}")
            return False
        else:
            return True
