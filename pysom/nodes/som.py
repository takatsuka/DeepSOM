from __future__ import annotations
import numpy as np
from numpy import exp, logical_and, random, outer, linalg, zeros, arange
from numpy import meshgrid, subtract, multiply, unravel_index, einsum
import matplotlib.pyplot as plt
from ..node import Node
from collections import Counter, defaultdict

# @numba.jit(nopython=True)


def exponential_decay(lr: float, curr: int, max_iter: int) -> float:
    """
    Classless utility exponential decay function.

    Args:
        lr (float): the learning rate hyperparameter
        curr (int): an integer value of the current iteration
        max_iter (int): an integer value of the maximum iteration

    Returns:
        float: the exponential decay correction factor
    """
    # exponential decay to reduce lr as iters progress (also used on sigma)
    return lr / (1 + curr / (max_iter / 2))


# @numba.jit(nopython=True)
def reduce_params(lr: float, sig: float, curr: int, max_iter: int) -> tuple:
    """
    Classless helper method applying exponential decay to lr and sig.

    Args:
        lr (float): the learning rate hyperparameter
        sig (float): sigma/radius hyperparameter
        curr (int): an integer value of the current iteration
        max_iter (int): an integer value of the maximum iteration

    Returns:
        tuple: the exponential decayed values of the learning rate and \
            sigma/radius parameters as a 2-tuple
    """
    return exponential_decay(lr, curr, max_iter), \
        exponential_decay(sig, curr, max_iter)


# @numba.jit(nopython=True)
def nhood_gaussian(bmu: tuple, x_mat: np.ndarray, y_mat: np.ndarray,
                   sigma: float) -> np.ndarray:
    """
    Classless learning method via Gaussian function of two input arrays.

    Runs two input arrays through a Gaussian neighourhood function and returns
    the elementwise multiplication of the two resultant arrays.

    Args:
        bmu (tuple): the index of the best matching unit
        x_mat (np.ndarray): the first array to be reweighted and reduced
        y_mat (np.ndarray): the second array to be reweighted and reduced
        sigma (float): the neighbourhood radius

    Returns:
        np.ndarray: the resultant array after the neighbourhood function is \
            applied
    """
    # return gaussian nhood for centroid  (sigma decreases as iters progress)
    # centroid is
    alpha_x = exp((-(x_mat - x_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    # the bmu here
    alpha_y = exp((-(y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    return (alpha_x * alpha_y).transpose()  # Elementwise


# @numba.jit(nopython=True)
def nhood_bubble(bmu: tuple, x_neig: np.ndarray, y_neig: np.ndarray,
                 sigma: float) -> np.ndarray:
    """
    Classless learning method via simple radius search method

    Args:
        bmu (tuple): the index of the best matching unit
        x_neig (np.ndarry): first array to be searched
        y_neig (np.ndarray): second array to be searched
        sigma (float): the neighbourhood radius

    Returns:
        np.ndarray: the resultant array after the neighbourhood function is \
            applied
    """
    alpha_x = logical_and(x_neig > bmu[0] - sigma, x_neig < bmu[0] + sigma)
    alpha_y = logical_and(y_neig > bmu[1] - sigma, y_neig < bmu[1] + sigma)
    return outer(alpha_x, alpha_y)


# @numba.jit(nopython=True)
def nhood_mexican(bmu: tuple, x_mat: np.ndarray, y_mat: np.ndarray,
                  sigma: float) -> np.ndarray:
    """
    Classless learning method using the Mexican hat/Ricker wave method

    Args:
        bmu (tuple): the index of the best matching unit
        x_neig (np.ndarry): first array to be searched
        y_neig (np.ndarray): second array to be searched
        sigma (float): the neighbourhood radius

    Returns:
        np.ndarray: the resultant array after the neighbourhood function is \
            applied
    """
    # return mexican hat nhood for bmu
    m = ((x_mat - x_mat.transpose()[bmu]) ** 2 + (y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2)
    return ((1 - 2 * m) * exp(-m)).transpose()


def dist_cosine(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    Utility distance function using cosine distance

    Args:
        x (np.ndarray): the first array
        w (np.ndarray): the second array

    Returns:
        np.ndarray: array of computed distances based on cosine distance
    """
    num = (x * w).sum(axis=2)
    denum = multiply(linalg.norm(w, axis=2), linalg.norm(x))
    return 1 - num / (denum + 1e-8)


def dist_euclidean(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    Utility distance function using Euclidean distance

    Args:
        x (np.ndarray): the first array
        w (np.ndarray): the second array

    Returns:
        np.ndarray: array of computed distances based on Euclidean distance
    """
    return linalg.norm(subtract(x, w), axis=-1)


def dist_manhattan(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    Utility distance function using Manhattan distance

    Args:
        x (np.ndarray): the first array
        w (np.ndarray): the second array

    Returns:
        np.ndarray: array of computed distances based on Manhattan distance
    """
    return linalg.norm(subtract(x, w), ord=1, axis=-1)


class SOM(Node):
    """
    Node type holding the Self-Organising Map data.

    Geometry and hyperparameters of the SOM class may be defined on a per-SOM
    basis. SOM generally obeys the rules of the parent node type, but must
    be assigned a slot of 0 as in incoming edge as a form of an identity
    check. The training logic of the graph is usually deferred to this class,
    in the sense that it is the only Node type that accepts and is mutated by
    some sort of input data (e.g. training data).

    Args:
        uid (str): the unique integer ID of the BMU node instance
        graph (Graph): the containing Graph instance holding the
                        constructed BMU node
        size (int): the length of any dimension of the n-cube map
        dim (int): the dimensionality of the n-cube map
        sigma (float, optional): the base neighbourhood radius. \
            Defaults to 0.5.
        lr (float, optional): the base learning rate. Defaults to 0.7.
        n_iters (int, optional): the number of iterations to train per epoch. \
            Defaults to 1.
        hexagonal (bool, optional): sets if the resultant map should output \
            as a hexagonal grid or not. Defaults to False.
        dist (callable, optional): the distance function to be used during \
            training for this node. Defaults to dist_euclidean.
        nhood (callable, optional): the neighbourhood search function to be \
            used during training for this node. Defaults to nhood_gaussian.
        rand_state (int, optional): seed to initialise RNG for the initial \
            map weights. Defaults to None.
    """

    def __init__(self, uid: int, graph, size: int, dim: int,
                 sigma: float = 0.5, lr: float = 0.7, n_iters: int = 1,
                 hexagonal: bool = None, dist: callable = dist_euclidean,
                 nhood: callable = nhood_gaussian, rand_state: int = False):
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

    def get_weights(self) -> np.ndarray:
        """
        Helper function to export the weights of the current BMU state

        Returns:
            np.ndarray: the weights matrix of the BMU
        """
        # returns weights with (x * y) rows and data_dim input columns
        return self.weights.reshape(self.size ** 2, self.data_dim)

    def activate(self, x: np.ndarray) -> None:
        """
        Helper function to trigger the distance function for an input vector

        Args:
            x (np.ndarray): the vector that the SOM updates its values on
        """
        # using distance formulas (euclid, cosine or manhattan)
        self.map = self.distance(x, self.weights)

    def bmu(self, x: np.ndarray) -> tuple:
        """
        Getter function to compute and retrieve the BMU for an input vector

        Args:
            x (np.ndarray): the vector that the SOM updates its values on

        Returns:
            tuple: the co-ordinate indices of the BMU found
        """
        # find bmu for data point x, return coords
        self.activate(x)
        return unravel_index(self.map.argmin(), self.map.shape)

    def update(self, x: np.ndarray, bmu: tuple, curr: int,
               max_iter: int) -> None:
        """
        Updates the SOM weights based on an input for the current iteration

        Weights are updated dependent on both the actual training data and
        the defined functions during construction of the SOM node. Reduced
        values are computed based on the iteration, and the learning rate
        and neighbourhood radius attributes are not mutated at all by this
        method.

        Does not return a value.

        Args:
            x (np.ndarray): the vector that the SOM updates its values on
            bmu (tuple): the co-ordinates of the BMU
            curr (int): an integer value of the current iteration
            max_iter (int): an integer value of the maximum iteration
        """
        # Calculate reduced lr and sigma (nhood range) according to the curr num of iters
        lr, sig = reduce_params(self.lr, self.sigma, curr, max_iter)
        if (self.nhood_func == nhood_gaussian or self.nhood_func == nhood_mexican):
            # Lr defines the radius of nhood, as iter increases, lr decreases AND nhood decreases as a factor of lr
            nhood = self.nhood_func(bmu, self.x_mat, self.y_mat, sig) * lr  # TODO: Is this supposed to double up on lr for exponential decay?
        else:
            nhood = self.nhood_func(bmu, self.x_neig, self.y_neig, sig) * lr

        # weights_ij(curr + 1) = weights_ij(curr) + weights_correction_ij(curr)
        # weights_correction_ij(curr) = lr(curr) * nhood(curr) * (x - weights_ij(curr))
        # weights_correction_ij(curr) is determined by lr and nhood func of bmu at curr iter
        # closer a node is to bmu the more its weights are altered
        # nodes within nhood of bmu altered to look more like the input x
        
        self.weights += einsum('ij, ijk->ijk', nhood, x - self.weights)
        """ Example
        X = [0.3 0.6] (input vector)

        initial weight vectors Wj:
        W1 = [0.1, 0.5]
        W2 = [0.2, 0.7]
        W3 = [0.4, 0.3]

        Find BMU j(X):  (eucl dist example)
        d1 = sqrt{(0.3-0.1)^2 + (0.6-0.5)^2} = 0.22
        d2 = sqrt{(0.3-0.2)^2 + (0.6-0.7)^2} = 0.14
        d3 = sqrt{(0.3-0.4)^2 + (0.6-0.3)^2} = 0.32

        Node 3 is winner and W3 is updated according to curr LR (eg 0.2)
        corr_W13 = LR(X1 - W13) = 0.2(0.3 - 0.2) = 0.02
        corr_W23 = LR(X2 - W23) = 0.2(0.6 - 0.7) = -0.02

        Updated Weight W3 at curr+1 iters:
        W3(curr+1) = W3(curr) + corr_W3(curr) = [0.2 0.7] + [0.02 -0.02] = [0.22 0.68]

        W3 of BMU is closer to input X at each iter
        """

    def train(self, data):
        """
        Trains SOM, updating SOM weights based on input data for each iter and bmu for each input data[iter],
        updating weights as a factor of LR and Sigma, reducing nhood radius of each bmu as iter value increases.

        Args:
            data (np.ndarray): The input data to train the SOM on.
        """
        # organizes iters from [0 .. len(data)) for partitions of data
        # e.g. n_iters = 999, len(data) = 256
        # iters = [0 .. 255 0 .. 255 0 .. 255 0 .. 255 0 .. 230]
        iters = arange(self.n_iters) % len(data)

        # enumerating iters s.t. weights[i] results from bmu(data[i]) at curr=i and n_iters=999
        # iter value goes from 0-255, and repeats until n_iters is reached
        # (lr and sigma are calculated within update as a factor of curr and n_iters)
        [self.update(data[iter], self.bmu(data[iter]), curr, self.n_iters)
         for curr, iter in enumerate(iters)]

    def _evaluate(self):
        self.train(self.get_input())
        self.output_ready = True

    def map_labels(self, data, labels):
        """
        Returns a default dictionary mapping the coords[i,j] for each bmu of the input data, to a
        list of labels counted by frequency of mappings (of each label) to the bmu with coords[i,j].
       
        Args:
            data (np.ndarray): The input data the SOM is trained on.
            labels (np.ndarray): Corresponding labels for each row in input data.
        
        Returns:
            label_map (defaultdict): Default dictionary where:
                - Key is coordinate tuple (x,y) for the BMU of each row (vector) in data
                - Value is list [Counter("lab1": count1, "lab2": count2, "lab3": count3)]
        """
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

    som = SOM(1, graph=None, size=100, dim=3, sigma=13, lr=0.7, n_iters=15000,
              nhood=nhood_gaussian, rand_state=True)

    file_path = "../datasets/sphere/sphere_64.txt"
    datastr = [x.strip().split(',') for x in open(file_path).readlines()]
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
