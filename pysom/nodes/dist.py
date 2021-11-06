from __future__ import annotations

# from numpy import true_divide
from ..node import Node

"""
    Dist Node
"""


class Dist(Node):

    def __init__(self, uid, graph, selections=[]):
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

    def get_output(self, slot: int) -> Node:
        if slot == 0:
            return self
        if not self.output_ready:
            self._evaluate()

        return self.pre_chopped[slot - 1]

    def check_slot(self, slot: int) -> bool:
        if slot < 0:
            self.graph._log_ex(f"Slots {slot} is not acceptable for {self}")
            return False
        
        if slot > len(self.sel):
            self.graph._log_ex(f"Slots {slot} was assigned from {self} while only {len(self.sel)} outputs are available")

        return True
