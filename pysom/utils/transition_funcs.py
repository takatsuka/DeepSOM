import numpy as np

# Transition functions for taking an input to one SOM
# and creating an output in the form of a numeric vector
# ready to be used by another SOM.

# Every transition function must take in the input
# (example) data point, the SOM to use, and must output
# a numeric vector which must always be the same size for
# a given SOM.
# Transition functions should not perform any training on
# the given SOM; they calculate without modifying.
# Transition functions may read, but not write, to SOM
# attributes if necessary.


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


def concat_binary(example, som):
    """A transition function where every entry in the output vector represents
    one node of the SOM. All entries are zero except for the entry
    corresponding to the BMU of the given example, which is 1.

    Args:
        example (np.ndarray): The input data point.
        som (class Som): The SOM to which the data is fed.

    Returns:
        np.ndarray: The output vector.
    """

    output = np.zeros(som.width * som.height)
    bmu_coords = som.get_idx_closest(example)
    output[bmu_coords[0] * som.height + bmu_coords[1]] = 1
    return output


def concat_linear(example, som):
    # TODO: A transition where every entry represents an output node,
    # concatenating rows to rows. Each entry contains a value relating to that
    # node's distance from the input data point, where 1 is identical and
    # value decreases linearly with increase in distance
    pass


def concat_exp(example, som):
    # TODO: A transition where every entry represents an output node,
    # concatenating rows to rows. Each entry contains a value relating to that
    # node's distance from the input data point, where 1 is identical and
    # value decreases exponentially with increase in distance
    pass


def coordinates(example, som):
    """A transition function which simply returns the coordinates of the BMU
    for the given data point, in the SOM's outspace.

    Args:
        example (np.ndarray): The input data point.
        som (class Som): The SOM to which the data is fed.

    Returns:
        np.ndarray: The output vector.
    """

    return np.array(som.get_idx_closest(example))


def coordinates_distance(example, som):
    """A transition function which returns a 3-tuple of coordinates for the
    given data point's BMU in outspace, and distance between the BMU and data
    point in inspace.

    Args:
        example (np.ndarray): The input data point.
        som (class Som): The SOM to which the data is fed.

    Returns:
        np.ndarray: The output vector.
    """

    output = np.zeros(3)
    bmu_coords = som.get_idx_closest(example)
    output[0] = bmu_coords[0]
    output[1] = bmu_coords[1]
    bmu = som.get_weight(bmu_coords[0], bmu_coords[1])
    output[2] = np.linalg.norm(bmu - example, ord=som.in_dist_p)
    return output


def interpolation_linear(example, som):
    # TODO: A transition where the output is coordinates representing the
    # input's position in the SOM's outspace. This is calcuated by linear
    # interpolation between the output nodes closest to the input point
    # according to inspace.
    pass
