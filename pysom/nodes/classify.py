from __future__ import annotations
import numpy as np
from ..node import Node


class Classify(Node):
    """
    TODO Node that provides a label to associated SOM index (usually BMU).

    Args:
        uid ([type]): [description]
        graph ([type]): [description]
        labels ([type], optional): [description]. Defaults to None.
        test ([type], optional): the input test data that requires \
            labelling. Defaults to None.
    """

    def __init__(self, uid: int, graph, labels=None, test=None):
        super(Classify, self).__init__(uid, graph)
        self.test = test
        self.labels = labels
        self.som = None

    def __str__(self) -> str:
        str_rep = "ClassifyNode {}".format(self.uid)
        return str_rep

    def get_output(self, slot: int) -> Node:
        """
        TODO Getter function to return the classification of associated nodes.

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
        if not self.check_slot(slot):
            raise RuntimeError("Can only get output from slot 0")

        self.som = self.get_input()
        label_map = self.som.map_labels(self.som.get_input(), self.labels)

        return self.classify(label_map)

    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.

        No limitation is imposed on the Classify class with regards to valid
        slot values other than that it must be a positive integer. Returns
        True if it is valid, else a RuntimeError is raised.

        Args:
            slot (int): a proposed integer slot ID to be checked

        Raises:
            RuntimeError: if the slot is zero or negative

        Returns:
            bool: True if the slot is a positive integer
        """
        if (slot == 0):
            raise RuntimeError("Slot 0 is reserved for SOMNode")
        elif (slot < 0):
            raise RuntimeError("Slots must be positive")
        else:
            return True

    def classify(self, label_map: dict) -> list:
        """
        TODO Getter function to return a list of labels for the test data.

        Utilises the provided label_map dict and incoming SOM to extract the


        Args:
            label_map (dict): map

        Returns:
            list: [description]
        """

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
