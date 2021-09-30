import numpy as np
from pysom.utils import decay_funcs as functions

# Defaults
LR_MAX = 0.7
LR_MIN = 0.1
LR_STEP = (LR_MAX - LR_MIN) / 100
LR_FUNC = functions.exp_decay
RADIUS_MAX = 0.7
RADIUS_MIN = 0.7
RADIUS_STEP = (RADIUS_MAX - RADIUS_MIN) / 100
RADIUS_FUNC = functions.exp_decay
NORM_P = 2


def regen_mat(width, height, indim, scale, offset):
    return (np.random.default_rng().random((width, height, indim), dtype=np.float64) + offset) * scale


def get_idx_closest(example, mat, in_dist_p):
    flat_idx = np.argmin(np.norm(mat - example, ord=in_dist_p, axis=2))
    return (flat_idx // mat.shape[0], flat_idx % mat.shape[1])


def learn(example, epoch, mat, mat_coord, lr, rad, in_dist_p, out_dist_p):

    width, height, _ = mat.shape
    bmu = get_idx_closest(example, mat, in_dist_p)

    dists_mat = np.norm(mat_coord - np.array(bmu), ord=out_dist_p, axis=2)
    influence_mat = np.exp(-(dists_mat / rad) ** 2).reshape(width, height, 1)

    return mat - ((mat - example) * influence_mat * lr)


def set_epoch(epoch, lr_max, lr_min, lr_step, lr_func, rad_max, rad_min, rad_step, rad_func):
    lr = lr_func(epoch, lr_max, lr_min, lr_step)
    rad = rad_func(epoch, rad_max, rad_min, rad_step)
    return lr, rad


def som_activate(example, mat, in_dist_p):
    flat_idx = np.argmin(np.norm(mat - example, ord=in_dist_p, axis=2))
    return (flat_idx // mat.shape[0], flat_idx % mat.shape[1])


def som_learn_batch(batch, mat, mat_coord, lr, rad, in_dist_p, out_dist_p):
    w, h, _ = mat.shape
    batch
    for example in batch:
        bmu = som_activate(example, mat, in_dist_p)

        dists_mat = np.norm(mat_coord - np.array(bmu), ord=out_dist_p, axis=2)
        influence_mat = np.exp(-(dists_mat * (1 / rad)) ** 2).reshape(w, h, 1)
        mat = mat - ((mat - example) * influence_mat * lr)

    return mat


class Som:
    def __init__(self, width, height, indim):
        """Constructor for an individual SOM.

        Args:
            width (int): The width of the output node grid.
            height (int): The height of the output node grid.
            indim (int): The number of dimensions for inputs

        Returns:
            class Som: The new SOM object
        """

        self.set_lr(LR_MAX, LR_MIN, LR_STEP, LR_FUNC)
        self.set_rad(RADIUS_MAX, RADIUS_MIN, RADIUS_STEP, RADIUS_FUNC)

        # Distance functions will be Minkowski distance
        # with exponent p from these variables
        self.in_dist_p = NORM_P
        self.out_dist_p = NORM_P

        self.width = width
        self.height = height
        self.indim = indim

        self.mat = regen_mat(self.width, self.height, self.indim, 1, 0)
        idx_mat = np.unravel_index(np.arange(self.width * self.height).reshape(self.width, self.height), (self.width, self.height))
        self.mat_coord = np.stack(idx_mat, 2)

    def set_lr(self, lr_max=None, lr_min=None, lr_step=None, lr_func=None):
        """Customise learning rate settings. The SOM begins with defaults;
        this function must be used for any specific desired behaviour. If
        any of the parameters is not provided, it will not be modified from
        its current value.

        Note that the exact effect of the other three parameters on the
        model's behaviour depends on which learning rate function is chosen.
        See the 'functions' module for details.

        Args:
            lr_max (float): The largest value the learning rate ever takes
                on. This is the initial value of the learning rate at epoch=0.
            lr_min (float): The smallest value the learning rate ever takes
                on. Should never be < 0. Depending on chosen function,
                lr_min of 0 may result in the SOM reaching a state where
                training has no effect.
            lr_step (float): A value which determines how quickly the
                learning rate falls. Generally, a larger step value means
                quicker descent. See the chosen learning rate function for
                details on exactly how the learning rate is affected.
            lr_func (function): A function from the 'functions' module, which
                takes in the epoch and max, min, and step values, and returns
                the learning rate for that current epoch. Learning rate
                functions should decrease as epoch increases.

        Returns:
            None
        """

        if lr_max != None:
            self.lr_max = lr_max
        if lr_min != None:
            self.lr_min = lr_min
        if lr_step != None:
            self.lr_step = lr_step
        if lr_func != None:
            self.lr_func = lr_func

    def set_rad(self, rad_max=None, rad_min=None, rad_step=None, rad_func=None):
        """Customise settings for finding the size of the neighbourhood
        radius around the BMU. The SOM begins with defaults; this function
        must be used for any specific desired behaviour. If any of the
        parameters is not provided, it will not be modified from its current
        value.

        Note that the exact effect of the other three parameters on the
        model's behaviour depends on which neighbourhood radius function is
        chosen. See the 'functions' module for details.

        Args:
            rad_max (float): The largest value the neighbourhood radius ever
                takes on. This is the initial value of the neighbourhood
                radius at epoch=0.
            rad_min (float): The smallest value the neighbourhood radius ever
                takes on. Should never be < 0.
            rad_step (float): A value which determines how quickly the
                neighbourhood radius falls. Generally, a larger step value
                means quicker descent. See the chosen neighbourhood radius
                function for details on exactly how the neighbourhood radius
                is affected.
            rad_func (function): A function from the 'functions' module, which
                takes in the epoch and max, min, and step values, and returns
                the neighbourhood radius for that current epoch. Neighbourhood
                radius functions should decrease as epoch increases.

        Returns:
            None
        """

        if rad_max != None:
            self.rad_max = rad_max
        if rad_min != None:
            self.rad_min = rad_min
        if rad_step != None:
            self.rad_step = rad_step
        if rad_func != None:
            self.rad_func = rad_func

    def set_in_norm_p(self, p):
        """Distance between input and node weight is calculated using
        Minkowski distance: For exponent p
        d(x, y) = (sum((x - y)**p))**(1/p)
        This method allows the exponent p for distances in input space
        to be chosen. Otherwise, default will be used.

        Args:
            p (int/str/np.inf): The exponent to be used in calculating
                distance in input space. Must be a positive integer,
                a string "inf", or the numpy object np.inf. In the latter
                cases, the distance function will become the maximum/supremum
                norm.

        Returns:
            None
        """

        if isinstance(p, int) and p > 0:
            self.in_dist_p = p
        elif p == np.inf or (isinstance(p, str) and p.lower() == "inf"):
            self.in_dist_p = np.inf

    def set_out_norm_p(self, p):
        """Distance between node positions on the output grid are calculated
        using Minkowski distance: For exponent p
        d(x, y) = (sum((x - y)**p))**(1/p)
        This method allows the exponent p for distances in output space
        to be chosen. Otherwise, default will be used.

        Args:
            p (int/str/np.inf): The exponent to be used in calculating
                distance in output space. Must be a positive integer,
                a string "inf", or the numpy object np.inf. In the latter
                cases, the distance function will become the maximum/supremum
                norm.

        Returns:
            None
        """

        if isinstance(p, int) and p > 0:
            self.out_dist_p = p
        elif p == np.inf or (isinstance(p, str) and p.lower() == "inf"):
            self.out_dist_p = np.inf

    def __str__(self):
        return str(self.mat)

    def regen_mat(self, scale=1, offset=0):
        """Resets the node grid to a matrix of randomly generated values.
        This function, unlike the constructor, permits scaling and offsets,
        and must be used if those features are desired in the node weights.
        Note that if any training has been performed, this method will undo
        that training.

        Args:
            scale (float): Defaults to 1 (no scaling). After the offset is
                applied, all weight values are multiplied by this.
            offset (float): Defaults to 0 (no offset). This number is added
                to all the weight values after they are randomly generated
                as between 0 and 1.

        Returns:
            None
        """
        self.mat = regen_mat(self.width, self.height, self.indim, scale, offset)

    def get_weight(self, x, y):
        """Returns the weight vector of the node at coordinates x, y in the
        node grid.

        Args:
            x (int): x (horizontal) coordinate of the desired node. Must be
                less than grid width.
            y (int): y (vertical) coordinate of the desired node. Must be less
                than grid height.

        Returns:
            np.ndarray: vector of the input weights belonging to node at (x, y).
                Will be of shape (indim,) from the constructor.
        """
        return self.mat[x, y]

    def dump_weight_list(self):
        """Returns the full node matrix of the SOM, shaped as single array
        of weight vectors instead of a grid.

        Args:
            None

        Returns:
            np.ndarray: 2D array of shape (width * height, indim) from the
                constructor. Each entry in the outer array is the weight
                vector of one node in the SOM's output grid.
        """

        return self.mat.reshape((self.width * self.height, self.indim))

    def get_idx_closest(self, example):
        """Given a single input data point, returns coordinates of the node
        in the output grid which is most similar to it.

        Args:
            example (np.ndarray): The input data point to consider. Should be
                of shape (indim,) from the constructor.

        Returns:
            tuple: coordinates of the best matching node in the output grid.
        """

        return get_idx_closest(example, self.mat, self.in_dist_p)

    def learn(self, example, epoch):
        """Given a single input data point, trains the SOM accordingly.
        Which epoch this is must be provided so that appropriate learning rate
        and neighbourhood radius of the BMU can be calculated.

        Args:
            example (np.ndarray): The input data point to train on. Should
                be of shape (indim,) from the constructor.
            epoch (int): Which epoch of training this is. Should be a non-
                negative integer (zero is fine).

        Returns:
            None
        """

        self.set_epoch(epoch)
        self.mat = learn(example, epoch, self.mat, self.mat_coord, self.lr, self.rad, self.in_dist_p, self.out_dist_p)

    def learn_batch(self, batch, epoch):
        """Given a collection of data points, trains the SOM accordingly.
        Which epoch this is must be provided so that appropriate learning rate
        and neighbourhood radius of the BMU can be calculated. This method is
        not the same as looping through all the data points, incrementing
        'epoch' and calling the learn() method for each one. This method
        only computes learning rate and neighbourhood radius once, using the
        given epoch, for the entire batch.

        Args:
            batch (np.ndarray): The batch of data points to train on. Should
                be of shape (n, indim) where indim is from the constructor and
                n can be any positive integer. Each entry of the outer array
                is one data point for training.
            epoch (int): Which epoch of training this is. Should be a non-
                negative integer (zero is fine).

        Returns:
            None
        """

        self.set_epoch(epoch)
        self.mat = som_learn_batch(np.array(batch, dtype=np.float64), self.mat, self.mat_coord, self.lr, self.rad, self.in_dist_p, self.out_dist_p)

    def set_epoch(self, epoch):
        """Given an epoch, calculates and updates the learning rate and
        neighbourhood radius of the BMU accordingly. Called in both the
        learn() and learn_batch() methods; if using them, you don't need to
        call this method yourself.

        Args:
            epoch (int): Which epoch of training this is. Should be a non-
                negative integer (zero is fine).

        Returns:
            None
        """

        lr, rad = set_epoch(epoch, self.lr_max, self.lr_min, self.lr_step, self.lr_func, self.rad_max, self.rad_min, self.rad_step, self.rad_func)
        self.lr = lr
        self.rad = rad
