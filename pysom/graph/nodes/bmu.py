from __future__ import annotations
import numpy as np
from numpy import exp, logical_and, random, outer, linalg, zeros, arange, array, argmin, meshgrid, subtract, multiply, unravel_index, einsum, dot
import matplotlib.pyplot as plt
from graph.node import Node
from graph.nodes.som import SOM


"""
    Type 1
"""


class BMU(Node):

    def __init__(self, uid, graph, output='2D'):
        super(BMU, self).__init__(uid, graph)
        self.som = None
        ret_bmu = {'1D': self.get_1D,
                   '2D': self.get_2D}
        self.get_bmu = ret_bmu[output]
    """
    HELPER METHODS HERE
    """

    def __str__(self) -> str:
        str_rep = "BMUNode {}".format(self.uid)
        return str_rep

    """
    CUSTOM METHODS HERE
    """

    def get_output(self, slot: int) -> Node:
        if not self.check_slot(slot):
            return

        self.som = self.get_input()

        # 1D vector (indices) or 2D vector (weights) of bmu for each row in data
        return self.get_bmu(self.som.get_input())

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
    BMU METHODS HERE
    """

    def bmu(self, x):   # can delete?
        # find bmu for data point x, and return coords.
        self.som.activate(x)
        return unravel_index(self.som.map.argmin(), self.som.map.shape)

    def dist_from_weights(self, data):
        # helper method to return a grid of distances dist[i,j], i.e.,
        # distances between data point x[i] and weight at j.
        data = array(data)
        flatten_weights = self.som.weights.reshape(
            -1, self.som.weights.shape[2])
        data_sq = (data ** 2).sum(axis=1, keepdims=True)
        flatten_weights_sq = (flatten_weights ** 2).sum(axis=1, keepdims=True)
        dot_term = dot(data, flatten_weights.transpose())
        return (dot_term * data_sq * flatten_weights_sq.transpose() * -2) ** 1 / 2

    def get_1D(self, data):
        # return 1D vector of bmu indices.
        return argmin(self.dist_from_weights(data), axis=1)

    def get_2D(self, data):
        bmu_idx = self.get_1D(data)
        # return 2D vector of bmu weights.
        return self.som.weights[unravel_index(bmu_idx, self.som.weights.shape[:2])]


if __name__ == "__main__":
    pass