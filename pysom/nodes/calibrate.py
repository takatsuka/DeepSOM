from __future__ import annotations
import numpy as np
from ..node import Node


class Calibrate(Node):
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
        super(Calibrate, self).__init__(uid, graph)
        self.test = test
        self.labels = labels
        self.som = None

    def __str__(self) -> str:
        str_rep = "Calibrate {}".format(self.uid)
        return str_rep

    def get_output(self, slot: int) -> Node:
        """
        TODO Getter function to return the classification of associated nodes.

        The concatenation of the incoming arrays will be returned. If there
        are no incoming arrays, then a RuntimeError is raised. If slot is 0,
        then the Concat node itself is returned.

        Args:
            slot (int): if 0, then the Calibrate node instance is returned. \
                Else the concatenation of the arrays are returned.

        Raises:
            RuntimeError: if get_output() is called prior to adding any \
                incoming array(s)

        Returns:
            object: returns the concatenated arrays along the axis defined \
                in the constructor if slot is not 0. Else, the Concat node \
                is returned.
        """
        if slot == 0:
            return self

        self.som = self.get_input()
        label_map = self.som.map_labels(self.som.get_input(), self.labels)
        
        if self.test:
            return self.calibrate(label_map)
        return label_map

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
        if not (0 <= slot <= 1):
            self.graph._log_ex(f"Slots {slot} is not acceptable for {self}")
            return False
        else:
            return True

    def calibrate(self, label_map: dict) -> list:
        """
        Getter function to return a list of labels for the test data, as calibrated on the input
        data of the SOM that it is trained on.

        Utilises the provided label_map dict which maps each BMU coordinate to a Counter of labels,
        with frequency value for each label calculated as a number of data vectors with given label L,
        mapped to the BMU coordinate for an input data vector. This function returns the most common
        label corresponding to a BMU, if the majority of data vectors mapped to a BMU has that label.
        If vectors are mapped to a BMU without a label, then a default label (most common in data), is
        given for that row in the test data.
        
        Returns a list of labels for each row in the test data, as calibrated by the input data used to
        train the SOM, corresponding to the bmu for each row in the input data.

        Args:
            label_map (defaultdict): Default dictionary where:
                - Key is coordinate tuple (x,y) of BMU,
                - Value is list [Counter("lab1": count1, "lab2": count2, "lab3": count3)]

        Returns:
            list: Calibrated labels for each row in input data, in order.
        """
        default = np.sum(list(label_map.values())).most_common()[0][0]

        # Gets all Counter list objects mapped to each BMU in the label_map, and sums all the results for each label
        # After summing up, we retrieve the most common label e.g, Counter({"a": 40, "b": 20, "c": 50}).most_common()
        # will return Counter({"c": 50, "a": 40, "b": 20}), thus, .most_common()[0][0] returns label "c", the overall
        # most common label - that we use as our default label if the BMU for our input data is not in the label_map.
        
        result = []

        for t in self.test:
            # finds the bmu coordinates for the input vector t in test data
            bmu = self.som.bmu(t)
            if bmu in label_map:
                # if bmu is in label_map, give most common label (mapped to bmu) to this row in data
                result.append(label_map[bmu].most_common()[0][0])
            else:
                # else, map most common label (default) to this row in data
                result.append(default)
        return result


if __name__ == "__main__":
    pass
