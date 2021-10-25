from __future__ import annotations
import numpy as np
from numpy import exp, logical_and, random, outer, linalg, zeros, arange, array, argmin, meshgrid, subtract, multiply, unravel_index, einsum, dot
import matplotlib.pyplot as plt
from graph.node import Node
from graph.nodes.som import SOM



"""
    Type 1
"""


def exponential_decay(lr, curr, max_iter):
    # exponential decay to reduce lr as iters progress (also used on sigma)
    return lr / (1 + curr / (max_iter / 2))


# @numba.jit(nopython=True)
def reduce_params(lr, sig, curr, max_iter):
    return exponential_decay(lr, curr, max_iter), exponential_decay(sig, curr, max_iter)


# @numba.jit(nopython=True)
def gaussian_func(bmu, x_mat, y_mat, sigma):
    # return gaussian nhood for centroid  (sigma decreases as iters progress)
    # centroid is
    alpha_x = exp((-(x_mat - x_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    # the bmu here
    alpha_y = exp((-(y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    return (alpha_x * alpha_y).transpose()


# @numba.jit(nopython=True)
def bubble_func(bmu, x_neig, y_neig, sigma):
    alpha_x = logical_and(x_neig > bmu[0] - sigma, x_neig < bmu[0] + sigma)
    alpha_y = logical_and(y_neig > bmu[1] - sigma, y_neig < bmu[1] + sigma)
    return outer(alpha_x, alpha_y)


# @numba.jit(nopython=True)
def mexican_func(bmu, x_mat, y_mat, sigma):
    # return mexican hat nhood for bmu
    m = ((x_mat - x_mat.transpose()
         [bmu]) ** 2 + (y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2)
    return ((1 - 2 * m) * exp(-m)).transpose()


class BMU(Node):
    
    def __init__(self, uid, graph, output='2D'):
        super(BMU, self).__init__(uid, graph)
        self.som = None
        ret_bmu = {'1D': self.get_1D,
                   '2D': self.get_2D}
        self.output = ret_bmu[output]
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
        self.som = self.get_input()
        return self.output(self.som.get_input())
    
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
    
    def get_weights(self):
        return self.som.weights

    def activate(self, x):
        # using distance formulas (euclid, cosine or manhattan)
        self.som.map = self.som.distance(x, self.som.weights)

    def bmu(self, x):
        # find bmu for data point x, return coords
        self.som.activate(x)
        return unravel_index(self.som.map.argmin(), self.som.map.shape)

    def dist_from_weights(self, data):
        data = array(data)
        flatten_weights = self.som.weights.reshape(-1, self.som.weights.shape[2])
        data_sq = (data ** 2).sum(axis = 1, keepdims = True)
        flatten_weights_sq = (flatten_weights ** 2).sum(axis=1, keepdims=True)
        dot_term = dot(data, flatten_weights.transpose())
        return (dot_term * data_sq * flatten_weights_sq.transpose() * -2) ** 1/2

    def get_1D(self, data):
        return argmin(self.dist_from_weights(data), axis=1)

    def get_2D(self, data):
        bmu_idx = self.get_1D(data)
        return self.som.weights[unravel_index(bmu_idx, self.som.weights.shape[:2])]

    
if __name__ == "__main__":
    
    file_path = "../datasets/sphere/sphere_256.txt"

    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]
