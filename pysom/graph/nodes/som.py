from __future__ import annotations
import numpy as np
from numpy import exp, logical_and, random, outer, linalg, zeros, arange, meshgrid, subtract, multiply, unravel_index, einsum
import matplotlib.pyplot as plt
from graph.node import Node


"""
    Type 0
"""
# @numba.jit(nopython=True)
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


class SOM(Node):

    def __init__(self, uid, x, y, dim, sigma=0.3, lr=0.7, 
        topology="rectangular", dist="euclidean", nhood=gaussian_func):

        super(SOM, self).__init__(uid)
        self.lr = lr
        self.sigma = sigma
        self.rg = random.RandomState(1)
        self.weights = self.rg.rand(x, y, dim) * 2 - 1
        self.weights /= linalg.norm(self.weights, axis=-1, keepdims=True)
        self.map = zeros((x, y))
        self.x_neig = arange(x).astype(float)
        self.y_neig = arange(y).astype(float)
        self.x_mat, self.y_mat = meshgrid(self.x_neig, self.y_neig)

        if topology == 'hexagonal':
            self.x_mat[::-2] -= 0.5

        metric = {'euclidean': self.euclidean,
                  'cosine': self.cosine, 'manhattan': self.manhattan}

        self.distance = metric[dist]
        self.nhood_func = nhood
    
    """
    HELPER METHODS HERE
    """
    def __str__(self) -> str:
        str_rep = "SOMNode {}".format(self.uid)
        return str_rep
    
    """
    CUSTOM METHODS HERE
    """
    def get_output(self, slot: int) -> Node:
        if not self.check_slot(slot):
            raise RuntimeError("SOMNode can only output to slot 0")
        return self
    
    def check_slot(self, slot: int) -> bool:
        if (slot != 0):
            return False
        return True

    """
    SOM METHODS HERE
    """
    def get_weights(self):
        return self.weights

    def cosine(self, x, w):
        num = (x * w).sum(axis=2)
        denum = multiply(linalg.norm(w, axis=2), linalg.norm(x))
        return 1 - num / (denum + 1e-8)

    def euclidean(self, x, w):
        return linalg.norm(subtract(x, w), axis=-1)

    def manhattan(self, x, w):
        return linalg.norm(subtract(x, w), ord=1, axis=-1)

    def activate(self, x):
        # using distance formulas (euclid, cosine or manhattan)
        self.map = self.distance(x, self.weights)

    def bmu(self, x):
        # find bmu for data point x, return coords
        self.activate(x)
        return unravel_index(self.map.argmin(), self.map.shape)

    def update(self, x, bmu, curr, max_iter):
        # update neuron weights, decrease sigma and lr and nhood of bmu
        lr, sig = reduce_params(self.lr, self.sigma, curr, max_iter)
        if self.nhood_func == gaussian_func or self.nhood_func == mexican_func:
            # einsum not supported by numba
            nhood = self.nhood_func(bmu, self.x_mat, self.y_mat, sig) * lr
        else:
            nhood = self.nhood_func(bmu, self.x_neig, self.y_neig, sig) * lr
        # but 2x fast as numpy inbuilts
        self.weights += einsum('ij, ijk->ijk', nhood, x - self.weights)
        # rewrite transpose as einsum contraction?

    def train(self, data, n_iters):
        # train som, update each iter
        iters = arange(n_iters) % len(data)
        [self.update(data[iter], self.bmu(data[iter]), curr, n_iters)
         for curr, iter in enumerate(iters)]


if __name__ == "__main__":
    
    file_path = "../../datasets/sphere/sphere_256.txt"

    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]

    som = SOM(uid=2, x=100, y=100, dim=3, sigma=6, lr=0.8, nhood=gaussian_func, 
                dist="manhattan", topology="hexagonal")

    som.train(data, 1000)

    sample = data[0]
    print(som.bmu(sample))  # bmu for sample vector

    som_weights = som.get_weights()
    print(som.get_weights()) # dump som weights

    # flattening weights list for graph
    flatten_weights = [elem for l in som_weights for elem in l]

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    axes = list(zip(*flatten_weights))     # Seems to work when i fiddle with sigma
    axes_o = list(zip(*data))
    ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))

    ax.scatter(*axes, marker='o', s=1)
    ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.savefig("sphere.png")





