from __future__ import annotations

# from numpy import true_divide
from ..node import Node
import numpy as np


class Dist(Node):
    """
    Node that extract specific dimensions of data as a distribution method.

    The Dist node must accept a list of distribution selections where each of
    the selections represent a 2-tuple slice of information that describes
    how any input data is to be distributed. Each tuple is of the form
    (axis, [dimensions]).
    
    For example, a tuple of form (1, [0 2]) suggests the extraction of data
    along the 1st axis (0-indexed, so 1st axis is vertical) and along axis
    entries 0 and 2 out of the entire axis.

    Args:
        uid (int): the unique integer ID of the Dist node instance
        graph (Graph): the containing Graph instance holding the
                        constructed Concat node
        selections (list, optional): a list of tuples defining the distribution
                                     of the input of form (axis, [dimensions]).
                                     Defaults to an empty list.

    Attributes:
        uid (str): the unique integer ID of the Concat node instance
        incoming (list): the list of all incoming Node objects that have a
            connection to the current Concat node instance
    """

    def __init__(self, uid: int, graph, selections: list = []):
        super(Dist, self).__init__(uid, graph)
        self.sel = selections
        self.pre_chopped = []

    def __str__(self) -> str:
        str_rep = "DistNode {}".format(self.uid)
        return str_rep

    def _evaluate(self):
        # if self.output_ready:
        #   return
        dat = self.get_input()
        self.pre_chopped = [dat.take(sel, axis=axis) for axis, sel in self.sel]

        self.output_ready = True

    def get_output(self, slot: int) -> object:
        """
        Getter function to return the distributed data of the input data.

        The user provided slot shall pertain to the order in which the data is
        to be distributed as defined by the selections during the construction
        of the Dist node. If slot is 0, then it will return the Dist node
        itself as an identity function.

        Args:
            slot (int): if 0, then the Dist node is returned. Else, returns
                        the distributed data based at the selection index,
                        based off 1-indexing rule.

        Returns:
            object: returns the Dist node if slot is 0, else returns an
                    np.ndarray of the distributed data at the selection index
        """

        if slot == 0:
            return self
        if not self.output_ready:
            self._evaluate()

        return self.pre_chopped[slot - 1]

    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.

        The Dist class may not accept a negative slot value. Does not return
        itself if slot is 0, unlike other typical Node classes. If slot
        provided exceeds the number of selections, then the slot is invalid.
        Returns True if it is valid, else False is returned.

        Args:
            slot (int): a proposed integer slot ID to be checked. Validity
                        of a positive or zero slot depends on selections
                        provided by user during construction.

        Returns:
            bool: True if the slot is valid, else returns False
        """

        if slot < 0:
            self.graph._log_ex(f"Slots {slot} is not acceptable for {self}")
            return False

        if slot > len(self.sel):
            self.graph._log_ex(f"Slots {slot} was assigned from {self} while only {len(self.sel)} outputs are available")

        return True
