from __future__ import annotations
import numpy as np
from numpy import exp, cov, argsort, transpose, linspace, logical_and, random, outer, linalg, zeros, arange, meshgrid, subtract, multiply, unravel_index, einsum
import matplotlib.pyplot as plt
from ..node import Node
from collections import Counter, defaultdict

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
def nhood_gaussian(bmu, x_mat, y_mat, sigma):
    # return gaussian nhood for centroid  (sigma decreases as iters progress)
    # centroid is
    alpha_x = exp((-(x_mat - x_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    # the bmu here
    alpha_y = exp((-(y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    return (alpha_x * alpha_y).transpose()


# @numba.jit(nopython=True)
def nhood_bubble(bmu, x_neig, y_neig, sigma):
    alpha_x = logical_and(x_neig > bmu[0] - sigma, x_neig < bmu[0] + sigma)
    alpha_y = logical_and(y_neig > bmu[1] - sigma, y_neig < bmu[1] + sigma)
    return outer(alpha_x, alpha_y)


# @numba.jit(nopython=True)
def nhood_mexican(bmu, x_mat, y_mat, sigma):
    # return mexican hat nhood for bmu
    m = ((x_mat - x_mat.transpose()
         [bmu]) ** 2 + (y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2)
    return ((1 - 2 * m) * exp(-m)).transpose()


def dist_cosine(x, w):
    num = (x * w).sum(axis=2)
    denum = multiply(linalg.norm(w, axis=2), linalg.norm(x))
    return 1 - num / (denum + 1e-8)


def dist_euclidean(x, w):
    return linalg.norm(subtract(x, w), axis=-1)


def dist_manhattan(x, w):
    return linalg.norm(subtract(x, w), ord=1, axis=-1)


class SOM(Node):

    def __init__(self, uid, graph, size, dim, sigma=0.5, lr=0.7, n_iters=1,
                 hexagonal=False, dist=dist_euclidean, nhood=nhood_gaussian, rand_state=False):

        super(SOM, self).__init__(uid, graph)
        self.size = size
        self.data_dim = dim

        self.lr = lr
        self.sigma = sigma
        self.rg = random.RandomState(rand_state)
        self.n_iters = n_iters

        self.weights = self.rg.rand(size, size, dim) * 2 - 1
        self.weights /= linalg.norm(self.weights, axis=-1, keepdims=True)
        self.map = zeros((size, size))
        self.x_neig = arange(size).astype(float)
        self.y_neig = arange(size).astype(float)
        self.x_mat, self.y_mat = meshgrid(self.x_neig, self.y_neig)

        if hexagonal:
            self.x_mat[::-2] -= 0.5

        self.distance = dist
        self.nhood_func = nhood

    def __str__(self) -> str:
        str_rep = "SOMNode {}".format(self.uid)
        return str_rep

    def get_weights(self):
        return self.weights.reshape(self.size ** 2, self.data_dim)

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
        if self.nhood_func == nhood_gaussian or self.nhood_func == nhood_mexican:
            nhood = self.nhood_func(bmu, self.x_mat, self.y_mat, sig) * lr
        else:
            nhood = self.nhood_func(bmu, self.x_neig, self.y_neig, sig) * lr
        self.weights += einsum('ij, ijk->ijk', nhood, x - self.weights)

    def train(self, data):
        # train som, update each iter
     
        iters = arange(self.n_iters) % len(data)
        [self.update(data[iter], self.bmu(data[iter]), curr, self.n_iters)
         for curr, iter in enumerate(iters)]

    def _evaluate(self):
        self.train(self.get_input())
        self.output_ready = True

    def map_labels(self, data, labels):
        label_map = defaultdict(list)
        for neuron, lab in zip(data, labels):
            label_map[self.bmu(neuron)].append(lab)
        for pos in label_map:
            label_map[pos] = Counter(label_map[pos])
        return label_map

    def get_output(self, slot: int) -> Node:
        if not self.output_ready:
            self._evaluate()

        if slot == 0:
            return self

        if slot == 1:
            return self.get_weights()

        return None

    def check_slot(self, slot: int) -> bool:
        return slot <= 1


if __name__ == "__main__":
    
    som = SOM(1, graph=None, size=100, dim=3, sigma=13, lr=0.7, n_iters=15000, nhood=nhood_gaussian, rand_state=True)
    
    file_path = "../datasets/sphere/sphere_64.txt"
    datastr = [l.strip().split(',') for l in open(file_path).readlines()]
    data = [[float(c) for c in e] for e in datastr]

    dat = np.array(data)

    som.train(dat)

    out = som.get_weights()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    axes = list(zip(*out))
    axes_o = list(zip(*data))
    ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))

    ax.scatter(*axes, marker='o', s=1)
    ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
