from __future__ import annotations
from typing import DefaultDict
import numpy as np
from numpy import exp, float64, logical_and, random, outer, linalg, zeros, arange, cov
from numpy import meshgrid, subtract, multiply, unravel_index, einsum, linspace
from numpy import array, mean
from numpy.linalg import eig
from numpy.core.fromnumeric import argsort
from ..node import Node
# from numba import jit
from collections import Counter, defaultdict


# @jit(nopython=True)
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
    if max_iter <= 0:
        raise ValueError("max_iter must be positive")

    # exponential decay to reduce lr as iters progress (also used on sigma)
    return lr / (1 + curr / (max_iter / 2))


# @jit(nopython=True)
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


# helper method to check if bmu coords given are in grid
def verify_pos(bmu: tuple, x_mat: np.ndarray, y_mat: np.ndarray) -> bool:
    x_tran, y_tran = x_mat.transpose(), y_mat.transpose()
    if bmu[0] >= len(x_mat) or bmu[0] >= len(x_tran):
        raise ValueError("At least the x coordinate of BMU is out of bounds!")
    if bmu[1] >= len(y_mat) or bmu[1] >= len(y_tran):
        raise ValueError("The y coordinate of BMU is out of bounds!")
    return True


# @jit(nopython=True)
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
    verify_pos(bmu, x_mat, y_mat)   # check bmu in grid
    # return gaussian nhood for bmu  (sigma decreases as iters progress)
    alpha_x = exp((-(x_mat - x_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    alpha_y = exp((-(y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2))
    return (alpha_x * alpha_y).transpose()  # Elementwise


# @jit(nopython=True)
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
    # won't throw an error if bmu outside range, will just return true/false if in radius

    # In a grid of size 3, if bmu = (1,1)   If sigma = 2,
    # then bubble returns if sigma = 1.     then bubble returns:
    # 0 0 0                                 1 1 1
    # 0 1 0                                 1 1 1
    # 0 0 0                                 1 1 1
    alpha_x = logical_and(x_neig > bmu[0] - sigma, x_neig < bmu[0] + sigma)
    alpha_y = logical_and(y_neig > bmu[1] - sigma, y_neig < bmu[1] + sigma)

    return outer(alpha_x, alpha_y)


# @jit(nopython=True)
def nhood_mexican(bmu: tuple, x_mat: np.ndarray, y_mat: np.ndarray,
                  sigma: float) -> np.ndarray:
    """
    Classless learning method using the Mexican hat/Ricker wave method

    Args:
        bmu (tuple): the index of the best matching unit
        x_mat (np.ndarry): first array to be searched
        y_mat (np.ndarray): second array to be searched
        sigma (float): the neighbourhood radius

    Returns:
        np.ndarray: the resultant array after the neighbourhood function is \
            applied
    """
    verify_pos(bmu, x_mat, y_mat)  # check bmu in grid
    # return mexican hat nhood for bmu
    m = ((x_mat - x_mat.transpose()
         [bmu]) ** 2 + (y_mat - y_mat.transpose()[bmu]) ** 2) / (2 * sigma ** 2)
    return ((1 - 2 * m) * exp(-m)).transpose()


def dist_cosine(data: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Utility distance function using cosine distance

    Args:
        data (np.ndarray): the first array
        weights (np.ndarray): the second array

    Returns:
        np.ndarray: array of computed distances based on cosine distance
    """
    if not (isinstance(data, np.ndarray) and isinstance(weights, np.ndarray)):
        typ = weights if isinstance(data, np.ndarray) else data
        msg = f"input is {str(type(typ))[7:][:-1]}, expecting 'numpy.ndarray'"
        raise ValueError(msg)

    num = (data * weights).sum(axis=-1)
    denum = multiply(linalg.norm(weights, axis=-1), linalg.norm(data))
    return 1 - num / (denum + 1 * 10 ** -8)


def dist_euclidean(data: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Utility distance function using Euclidean distance

    Args:
        data (np.ndarray): the first array
        weights (np.ndarray): the second array

    Returns:
        np.ndarray: array of computed distances based on Euclidean distance
    """
    return linalg.norm(subtract(data, weights), axis=-1)


def dist_manhattan(data: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Utility distance function using Manhattan distance

    Args:
        data (np.ndarray): the first array
        weights (np.ndarray): the second array

    Returns:
        np.ndarray: array of computed distances based on Manhattan distance
    """
    return linalg.norm(subtract(data, weights), ord=1, axis=-1)


def pca(data):
    M = mean(data.transpose(), axis=1)  # calc mean each col
    C = data - M  # subtract col means (centers cols)
    V = cov(C.transpose())  # covar matrix
    val, vec = eig(V)  # eigendecomp covar matrix
    # P = vec.transpose().dot(C.transpose())
    ord_val = argsort(-val)  # first two capture 85%

    return vec, ord_val


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
        check_points (int, optional): the number of checkpoints recorded in the \
            training log. A checkpoint will store a snapshot of weights captured \
            after each interval of training, defined as the number of iterations \
            to train per checkpoint. Defaults to 1.
        hexagonal (bool, optional): sets if the resultant map should output \
            as a hexagonal grid or not. Defaults to False.
        dist (callable, optional): the distance function to be used during \
            training for this node. Defaults to dist_euclidean.
        nhood (callable, optional): the neighbourhood search function to be \
            used during training for this node. Defaults to nhood_gaussian.
        rand_state (int, optional): seed to initialise RNG for the initial \
            map weights. Defaults to None.
    """

    def __init__(self, uid: int, graph, size: int, dim: int, sigma: float = 0.5,
                 lr: float = 0.7, n_iters: int = 1, check_points: int = 1, hexagonal: bool = None,
                 dist: callable = dist_euclidean, nhood: callable = nhood_gaussian,
                 pca: bool = False, norm: bool = False,
                 rand_state: int = None):
        super(SOM, self).__init__(uid, graph)

        # set size of grid and dims (size, size, dims)
        self.size, self.data_dim = size, dim
        # set LR, sigma, and max num of iters
        self.lr, self.sigma, self.n_iters = lr, sigma, n_iters
        # set distance metric, and nhood function
        self.distance, self.nhood_func = dist, nhood
        # initialize nhood map with size of grid
        self.map = zeros((size, size))
        self.x_neig = self.y_neig = arange(size).astype(
            float)  # set x and y to be 0..size
        # arrange x y as horizontal and vert axis
        self.x_mat, self.y_mat = meshgrid(self.x_neig, self.y_neig)
        self.pca, self.norm = pca, norm
        self._rand_weights(rand_state)
        self.graph = graph
        if not check_points:
            msg = f"Expecting checkpoint value of at least default 1, instead got {check_points}."
            raise ValueError(msg)
        elif check_points > n_iters:
            msg = f"Checkpoints must not exceed number of training iterations.\nCheckpoints must at most be {n_iters} for number of training iterations requested."
            raise ValueError(msg)
        self.cp, self.train_log = 0, {i: np.array(
            []) for i in np.arange(check_points)}
        self.label_map = defaultdict(list)
        if hexagonal:
            # offset every second row if hexagonal grid used
            self.x_mat[::-2] -= 0.5

    def __str__(self) -> str:
        str_rep = "SOMNode {}".format(self.uid)
        return str_rep

    def _check_dims(self, data: np.ndarray) -> bool:
        if self.data_dim != len(data[0]):
            msg = f"Expecting {self.data_dim} dimensions, input has {len(data[0])}"
            raise ValueError(msg)
        for i in range(0, len(data)):
            if self.data_dim != len(data[i]):
                msg = f"Expecting {self.data_dim} dimensions, input has {len(data[i])} in row {i}"
                raise ValueError(msg)
        return True

    def get_weights(self) -> np.ndarray:
        """
        Helper function to export the weights of the current BMU state

        Returns:
            np.ndarray: the weights matrix of the BMU
        """
        # returns weights with (x * y) rows and data_dim input columns
        return self.weights.reshape(self.size ** 2, self.data_dim)

    def _rand_weights(self, rand_state):
        # randomize weights grid
        self.weights = random.RandomState(rand_state).randn(
            self.size, self.size, self.data_dim) * 2
        # normalize weight values
        self.weights /= linalg.norm(self.weights, axis=2, keepdims=True)

    def _pca(self, data):
        # normalize data first...? or leave to user to choose
        vec, ord_val = pca(data)
        grid_length = linspace(-1, 1, self.size, dtype=float64)
        for i, pc0 in enumerate(grid_length):
            for j, pc1 in enumerate(grid_length):
                # first principle component
                self.weights[i, j] = (pc0 * vec[ord_val[0]])
                # add second as linear combination
                self.weights[i, j] += (pc1 * vec[ord_val[1]])

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
               max_iter: int, dump_weight: bool = None) -> None:
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
            nhood = lr * self.nhood_func(bmu, self.x_mat, self.y_mat, sig)
        else:
            nhood = lr * self.nhood_func(bmu, self.x_neig, self.y_neig, sig)

        # weights_ij(curr + 1) = weights_ij(curr) + weights_correction_ij(curr)
        # weights_correction_ij(curr) = lr(curr) * nhood(curr) * (x - weights_ij(curr))
        # weights_correction_ij(curr) is determined by lr and nhood func of bmu at curr iter
        # closer a node is to bmu the more its weights are altered
        # nodes within nhood of bmu altered to look more like the input x
        """
       [[x11 y11 z11]      [[wx11 wy11 wz11]                       [[nx1(x11-wx11) nx1(y11-wy11) nx1(z11-wz11)]
        [x12 y12 z12]   -   [wx12 wy12 wz12]                        [ny1(x12-wx12) ny1(y12-wy12) ny1(z12-wz12)]
        [x13 y13 y13]       [wx13 wy13 wz13]                        [nz1(x13-wx13) nz1(x13-wz13) nz1(x13-wz13)]]

        [x21 y21 z21]       [wx21 wy21 wz21]     [[nx1 ny1 nz1]    [[nx2(x21-wx21) nx2(y21-wy21) nx2(z21-wz21)]
        [x22 y22 z22]   -   [wx22 wy22 wz22]   *  [nx2 ny2 nz2]  =  [ny2(x21-wx21) ny2(y22-wy22) ny2(z22-wz22)]
        [x23 y23 z23]       [wx23 wy23 wz23]      [nx3 ny3 nz3]]    [nz2(x23-wx23) nz2(y23-wy23) nz2(z23-wz23)]]

        [x31 y31 z31]       [wx31 wy31 wz31]                       [[nx3(x31-wx31) nx3(y31-wy31) nx3(z31-wz31)]
        [x32 y32 z32]   -   [wx32 wy32 wz32]                        [ny3(x32-wx32) ny3(y32-wy32) ny3(z32-wz32)]
        [x33 y33 z33]]      [wx33 wy33 wz33]]                       [nz3(x33-wx33) nz3(y33-wy33) nz3(z33-wz33)]]
        
        (3 x 3 x 3)          (3 x 3 x 3)            (3 x 3)                 (3 x 3 x 3)
        """

        self.weights += einsum('ij, ijk->ijk', nhood, x - self.weights)
        if dump_weight:
            self.train_log[self.cp], self.cp = self.get_weights(), self.cp + 1

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
        self._check_dims(data)
        # organizes iters from [0 .. len(data)) for partitions of data
        # e.g. n_iters = 999, len(data) = 256
        # iters = [0 .. 255 0 .. 255 0 .. 255 0 .. 255 0 .. 230]
        iters = arange(self.n_iters) % len(data)

        # enumerating iters s.t. weights[i] results from bmu(data[i]) at curr=i and n_iters=999
        # iter value goes from 0-255, and repeats until n_iters is reached
        # (lr and sigma are calculated within update as a factor of curr and n_iters)

        for curr, iter in enumerate(iters):
            dump_weight = True if not curr % len(self.train_log) else False
            self.update(data[iter], self.bmu(data[iter]),
                        curr, self.n_iters, dump_weight)

    def _evaluate(self):
        if self.graph.global_params['training']:
            data = self.get_input()
            if self.norm:
                data = array(self.get_input(), dtype=np.float64)
                data /= linalg.norm(data, axis=-1, keepdims=True)
            if self.pca:
                self._pca(data)
            self.train(data)
        self.output_ready = True

    def map_labels(self, data: np.ndarray, labels: list):
        """
        Returns a default dictionary mapping the coords[i,j] for each bmu of the input data, to a
        list of labels counted by frequency of mappings (of each label) to the bmu with coords[i,j].

        Args:
            data (np.ndarray): The input data the SOM is trained on.
            labels (list): Corresponding labels for each row in input data.

        Returns:
            label_map (defaultdict): Default dictionary where:
                - Key is coordinate tuple (x,y) for the BMU of each row (vector) in data
                - Value is list [Counter("lab1": count1, "lab2": count2, "lab3": count3)]
        """
        self._check_dims(data)
        label_map = DefaultDict(list)
        # project labels to data
        [label_map[self.bmu(x)].append(l) for x, l in zip(data, labels)]
        for pos in label_map:
            label_map[pos] = Counter(label_map[pos])  # count labels
        return label_map

    def get_output(self, slot: int) -> object:
        """
        Getter function to return the trained weights of the SOM.

        Will trigger the training of the SOM if not done so already for the
        current iteration. May define a slot of 0 for the identity (returns
        itself), otherwise it will return the trained weights if slot is 1.
        All other values of slot are invalid and the method will effectively
        fail in this scenario.

        Args:
            slot (int): if 0, then the SOM node instance is returned. \
                        If 1, weights of the SOM node after training is \
                        returned. Else, slot is invalid and None is returned.

        Returns:
            object: returns the SOM node if slot is 0. Returns the weights \
                    of the SOM as an np.ndarray is slot is 1. Returns None \
                    otherwise.
        """
        if not self.output_ready:
            self._evaluate()

        if slot == 0:
            return self

        if slot == 1:
            return self.get_weights()

        return None

    def check_slot(self, slot: int) -> bool:
        """
        A verification method to confirm if a proposed slot ID can be used.

        The SOM class may only accept slot value of either 0 or 1.
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
