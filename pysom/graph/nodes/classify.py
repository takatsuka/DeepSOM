from __future__ import annotations
import numpy as np
from graph.node import Node


"""
    Type Classifier
"""


class Classify(Node):

    def __init__(self, uid, graph, labels=None, test=None):
        super(Classify, self).__init__(uid, graph)
        self.test = test
        self.labels = labels
        self.som = None
    """
    HELPER METHODS HERE
    """

    def __str__(self) -> str:
        str_rep = "ClassifyNode {}".format(self.uid)
        return str_rep

    """
    CUSTOM METHODS HERE
    """

    def get_output(self, slot: int) -> Node:
        if not self.check_slot(slot):
            return

        self.som = self.get_input()
        label_map = self.som.map_labels(self.som.get_input(), self.labels)

        return self.classify(label_map)

    def check_slot(self, slot: int) -> bool:
        if (slot == 0):
            raise RuntimeError("Slot 0 is reserved for SOMNode")
            return False
        elif (slot < 0):
            raise RuntimeError("Slots must be positive")
            return False
        else:
            return True

    """
    Classify METHODS HERE
    """
    def classify(self, label_map):

        default = np.sum(list(label_map.values())).most_common()[0][0]
        result = []

        for t in self.test:
            win_pos = self.som.bmu(t)
            if win_pos in label_map:
                result.append(label_map[win_pos].most_common()[0][0])
            else:
                result.append(default)
        return result


if __name__ == "__main__":
    pass
