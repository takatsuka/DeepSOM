import numpy as np
from pysom.utils.transition_funcs import concat_binary
from pysom.components.som import Som


def test_concat_binary_basic():
    vector = np.array([1, 2])
    som = Som(3, 3, 2)

    expected = np.zeros(som.width * som.height)
    bmu_coords = som.get_idx_closest(vector)
    expected[bmu_coords[0] * som.height + bmu_coords[1]] = 1

    output = concat_binary(vector, som)

    assert all([a == b for a, b in zip(expected, output)])
    assert len(expected) == len(output)


def test_concat_binary_basic_2():
    vector = np.array([1, 2])
    som = Som(3, 3, 2)

    expected = np.zeros(som.width * som.height)
    bmu_coords = som.get_idx_closest(vector)
    expected[bmu_coords[0] * som.height + bmu_coords[1]] = 1

    output = concat_binary(vector, som)

    assert all([a == b for a, b in zip(expected, output)])
    assert len(expected) == len(output)

# randomnness makes it difficult to test against an expected output, this seems reverse logic
def test_concat_binary_basic_2():
    vector = np.array([9, 21, 3])
    som = Som(3, 3, 3)

    expected = np.zeros(som.width * som.height)
    bmu_coords = som.get_idx_closest(vector)
    expected[bmu_coords[0] * som.height + bmu_coords[1]] = 1

    output = concat_binary(vector, som)

    assert all([a == b for a, b in zip(expected, output)])
    assert len(expected) == len(output)
