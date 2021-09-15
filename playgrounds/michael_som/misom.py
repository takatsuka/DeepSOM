from numpy import *
import pickle
from numba import jit

@jit(nopython=True)
def exponential_decay(lr, curr, max_iter):
    # exponential decay to reduce lr as iters progress (also used on sigma)
    return lr / (1 + curr / (max_iter / 2))

@jit(nopython=True)
def reduce_params(lr, sig, curr, max_iter):
    return exponential_decay(lr, curr, max_iter), exponential_decay(sig, curr, max_iter)

@jit(nopython=True)
def gaussian_func(bmu, x_mat, y_mat, sigma):
    #return gaussian nhood for centroid  (sigma decreases as iters progress)
    alpha_x = exp((-(x_mat - x_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2) )   # centroid is
    alpha_y = exp((-(y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2) )   # the bmu here
    return (alpha_x * alpha_y).transpose()

class Som(object):
    # Initialise som, randomly generate weights and activate map
    def __init__(self, x, y, dim, sigma, lr):
        self.lr = lr
        self.sigma = sigma

        self.rg = random.RandomState(1)
        self.weights = self.rg.rand(x, y, dim) * 2 - 1
        self.weights /= linalg.norm(self.weights, axis=-1, keepdims=True)

        self.map = zeros((x, y))
        self.x_mat, self.y_mat = meshgrid(arange(x), arange(y))

    def get_weights(self):
        return self.weights

    def activate(self, x):
        # using eucl distance metric
        self.map = linalg.norm(subtract(x, self.weights), axis=-1)

    def bmu(self, x):
        # find bmu for data point x, return coords
        self.activate(x)
        return unravel_index(self.map.argmin(), self.map.shape)

    def update(self, x, bmu, curr, max_iter):
        # update neuron weights, decrease sigma and lr and nhood of bmu
        lr, sig  = reduce_params(self.lr, self.sigma, curr, max_iter)
        nhood = gaussian_func(bmu, self.x_mat, self.y_mat, sig) * lr     # einsum not supported by numba
        self.weights += einsum('ij, ijk->ijk', nhood, x - self.weights)     # but 2x fast as numpy inbuilts
                                                                         # rewrite transpose as einsum contraction?
    def train(self, data, n_iters):
        # train som, update each iter
        iters = arange(n_iters) % len(data)
        [self.update(data[iter], self.bmu(data[iter]), curr, n_iters) for curr, iter in enumerate(iters)]