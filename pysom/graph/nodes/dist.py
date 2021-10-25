from __future__ import annotations

from numpy import true_divide
from graph.node import Node

"""
    Type 2
"""
class Dist(Node):
    
    def __init__(self, uid, graph, selections=[]):
        super(Dist, self).__init__(uid, graph)
        self.sel = selections
        self.pre_chopped = []

    def __str__(self) -> str:
        str_rep = "DistNode {}".format(self.uid)
        return str_rep


    def evaluate(self):
        if self.output_ready: return
        dat = self.get_input()
        self.pre_chopped = [dat.take(sel, axis=axis) for axis, sel in self.sel]
        
        self.output_ready = True


    def get_output(self, slot: int) -> Node:
        if not self.output_ready:
            self.evaluate()
        print(self.pre_chopped)
        if slot == 0: return self
        
        return self.pre_chopped[slot - 1]
    
    def check_slot(self, slot: int) -> bool:
        return slot <= len(self.sel)
        
        
if __name__ == "__main__":
    pass