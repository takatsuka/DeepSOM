from __future__ import annotations
from ..node import Node
import numpy as np


class Concat(Node):
    """
    Node that accepts input nodes and provides concatenation as the output.

    Must specify a specific axis to concatenate the input nodes along or be
    None. If axis is not None, then the arrays must of same shape other than
    the dimension nominated. If axis is None, then the array will be
    flattened prior to concatenation.

    Args:
        uid (int): the unique integer ID of the Concat node instance
        graph (Graph): the containing Graph instance holding the
                        constructed Concat node
        axis (int): the axis corresponding to the dimension along which the \
            concatenation should act on.

    Attributes:
        uid (str): the unique integer ID of the Concat node instance
        incoming (list): the list of all incoming Node objects that have a
            connection to the current Concat node instance
    """
    def __init__(self, uid: int, graph, axis: int):
        super(Concat, self).__init__(uid, graph)
        self.precon = None
        self.axis = axis

    def __str__(self) -> str:
        str_rep = "ConcatNode {}".format(self.uid)
        return str_rep

    def _evaluate(self) -> None:
        ins = [self.get_input(index=i) for i in range(len(self.incoming))]
        self.precon = np.concatenate(tuple(ins), axis=self.axis)

        self.output_ready = True

    def get_output(self, slot: int) -> object:
        """
        Getter function to return the concatenation of associated nodes.

        The concatenation of the incoming arrays will be returned. If there
        are no incoming arrays, then a RuntimeError is raised. If slot is 0,
        then the Concat node itself is returned.

        Args:
            slot (int): if 0, then the Concat node instance is returned. \
                Else the concatenation of the arrays are returned.

        Raises:
            RuntimeError: if get_output() is called prior to adding any \
                incoming array(s)

        Returns:
            object: returns the concatenated arrays along the axis defined \
                in the constructor if slot is not 0. Else, the Concat node \
                is returned.
        """
        if len(self.incoming) == 0:
            raise RuntimeError("Must add at least one array before concat")

        if slot == 0:
            return self

        if not self.output_ready:
            self._evaluate()

        return self.precon

    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.

        No limitation is imposed on the Concat class with regards to valid
        slot values other than that it must be a positive integer. Returns
        True if it is valid, else a RunetimError is raised.

        Args:
            slot (int): a proposed integer slot ID to be checked

        Raises:
            RuntimeError: if the slot is zero or negative

        Returns:
            bool: True if the slot is a positive integer
        """

        if not (0 <= slot <= 1):
            self.graph._log_ex(f"Slots {slot} is not acceptable for {self}")
            return False
        else:
            return True
