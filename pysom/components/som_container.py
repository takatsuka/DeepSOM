import numpy as np


def make_input(vector, inlen, in_set):
    return vector[in_set, ]


# This is the identity transition function from transition_funcs
# We include it here to avoid having to import it via a complicated
# directory path.
def identity(example, som):
    """A transition function which simply returns the input.
    The som variable is not used, but has been included to conform to
    standards for transition functions.

    Args:
        example (np.ndarray): The input data point.
        som (class Som): The SOM to which the data is fed.

    Returns:
        np.ndarray: The output vector.
    """
    return example


class SomContainer:

    def __init__(self, som, transition, in_set=None):
        """Constructor. Holds a SOM, a transition function, and some useful information.

        Args:
            som (class Som): The SOM for the container to hold. If None, the
                som container will be an identity transition, simply returning
                the vector given as input.
            transition (function): The transition function which creates some
                numeric vector by feeding the SOM an input. See the
                'transitions' module for more.
            in_set (tuple): The indices from which this SOM should take data
                to use as inputs, out of the whole layer's input array.
                Should be a tuple of ints only. If not provided, defaults to
                (0, 1, 2, ..., som.indim - 1).

        Returns:
            class SomContainer: The new object.
        """

        self.som = som
        if som == None:
            self.transition_func = identity
        else:
            self.transition_func = transition
        self.inlen = som.indim
        if in_set == None:
            self.in_set = tuple([i for i in range(self.inlen)])
        else:
            self.in_set = in_set
        assert len(self.in_set) == self.inlen, "Input idx set must have the same length as the som's input dimension"

        # The only way to know the output length of the
        # transition function is to run it
        dummy_point = np.zeros(self.inlen)
        self.outlen = len(self.transition_func(dummy_point, self.som))

    def get_in_len(self):
        return self.inlen

    def get_out_len(self):
        return self.outlen

    def get_in_set(self):
        return self.in_set

    def make_input(self, vector):
        """Given the entire input array of the current layer in a deep SOM,
        extract only those indices which this SOM should use as input, and
        make an array out of that data.

        Args:
            vector (np.ndarray): The current state of the entire layer's
                input array.

        Returns:
            np.ndarray: Only those elements of the layer's input array which
                are found at the indices this SOM uses. Will be of shape
                (som.indim,) using the SOM from the constructor.
        """

        return make_input(vector, self.inlen, self.in_set)

    def activate_som(self, example):
        """Runs the SOM on a given input, and returns whatever the transition
        function returns given that SOM and input.

        Args:
            example (np.ndarray): The data point to feed into the SOM. Should
                be of shape (indim,) using the indim of the SOM in question.

        Returns:
            np.ndarray: The output of the transition function for that input
                vector. Will be of shape (outlen,) using the value of
                outlen calculated by running the transition function on this
                SOM.
        """

        return self.transition_func(example, self.som)

    def train_som(self, example, epoch):
        """Trains the SOM on the given input, and returns whatever the
        transition function returns given that SOM and input before training.
        Allows both for the SOM itself to be updated and an output to be
        generated, facilitating training of a larger Deep SOM.

        Args:
            example (np.ndarray): The data point to feed into the SOM. Should
                be of shape (indim,) using the indim of the SOM in question.
            epoch (int): Which epoch of training this is. Should be a non-
                negative integer (zero is fine).

        Returns:
            np.ndarray: The output made by the transition function on this
                input, using this SOM, before the training took place. Will be
                of shape (outlen,) using the value of outlen calculated by
                running the transition function on this SOM.
        """

        output = self.transition_func(example, self.som)
        if som != None:
            self.som.learn(example, epoch)
        return output
