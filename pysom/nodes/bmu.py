from __future__ import annotations
import numpy as np
from numpy import array, argmin, unravel_index, dot
from ..node import Node


class BMU(Node):
    """
    Node that finds the Best Matching Unit for an associated SOM node.

    User may choose to receive the BMU information in terms of a 1-dimensional
    vector or in terms of the weights.

    Args:
        uid (int): the unique integer ID of the BMU node instance
        graph (Graph): the containing Graph instance holding the
                        constructed BMU node
        output (str, optional): defines whether to output the coordinate \
            vector of the BMU to 1D or weights themselves. Defaults to 'w'.

    Raises:
        RuntimeError: when the output is not defined as '1D' or 'w'

    Attributes:
        uid (str): the unique integer ID of the BMU node instance
        incoming (list): the list of all incoming Node objects that have a
            connection to the current BMU node instance
    """

    def __init__(self, uid: int, graph, output: str = 'w'):
        if output != '1D' and output != 'w':
            raise RuntimeError("Output should be either '1D' or 'w' only")

        super(BMU, self).__init__(uid, graph)
        self.som = None
        ret_bmu = {'1D': self.get_1D,
                   'w': self.get_weight}
        self.get_bmu = ret_bmu[output]

    def __str__(self) -> str:
        str_rep = "BMUNode {}".format(self.uid)
        return str_rep

    def get_output(self, slot: int) -> object:
        """
        Getter function to return the BMU from an associated SOM node.

        Pulls the SOM data directly into the BMU Node and prepares it for
        evaluation of the actual Best Matching Unit. BMU expects only 1 input
        node, and will thus always request data from slot 0 of the input
        edges. Then it evaluates and returns the BMU as a numpy array.

        Args:
            slot (int): the slot id of the incoming SOM node. If defined as \
                        0, then the BMU object itself is returned. 

        Returns:
            object: returns the BMU vector/array with BMU data determined by \
                the output parameter in the constructor
        """
        if slot == 0:
            return self

        self.som = self.get_input()

        # 1D vector (indices) or 2D vector (weights) of bmu for each row
        return self.get_bmu(self.som.get_input())

    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.

        The BMU class may only accept slot value of either 0 or 1.
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

    # def bmu(self, x):   # can delete?
    #     # find bmu for data point x, and return coords.
    #     self.som.activate(x)
    #     return unravel_index(self.som.map.argmin(), self.som.map.shape)

    def dist_from_weights(self, data: np.ndarray) -> np.ndarray:
        """
        Outputs a grid of distances of an example to SOM weights.

        Args:
            data (np.ndarray): the weights array to be received from an
                               associated output SOM node

        Returns:
            np.ndarray: the grid of distances between the example data \
                        and the SOM
        """
        # helper method to return a grid of distances dist[i,j], i.e.,
        # distances between data point x[i] and weight at j.
        data = array(data)
        flatten_weights = self.som.weights.reshape(-1, self.som.weights.shape[2])
        data_sq = (data ** 2).sum(axis=1, keepdims=True)
        flatten_weights_sq = (flatten_weights ** 2).sum(axis=1, keepdims=True)
        dot_term = dot(data, flatten_weights.transpose())
        res = dot_term * data_sq * flatten_weights_sq.transpose() * -2
        return res ** 1 / 2

    def get_1D(self, data: np.ndarray) -> np.ndarray:
        """
        Helper function to return the BMU as a 1-dimensional vector.

        Args:
            data (np.ndarray): the array of distances to be checked

        Returns:
            np.ndarray: the vector of BMU indices
        """
        # return 1D vector of bmu indices.
        return argmin(self.dist_from_weights(data), axis=1)

    def get_weight(self, data: np.ndarray) -> np.ndarray:
        """
        Helper function to return the BMU weight value itself.

        Args:
            data (np.ndarray): the array of distances to be checked

        Returns:
            np.ndarray: the array of BMU weights
        """
        bmu_idx = self.get_1D(data)
        # return 2D vector of bmu weights.
        return self.som.weights[unravel_index(bmu_idx, self.som.weights.shape[:2])]
