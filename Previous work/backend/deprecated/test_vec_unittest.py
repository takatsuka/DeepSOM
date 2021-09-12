import unittest
import os
import random
import math
import sys

from src import *
import numpy as np

# from backend.src.SOM.Vec import Vec

# Run script from its containing directory
class TestVec(unittest.TestCase):

    #generic case, test the construction of an input with 100 dimensions.
    def test_constructor_list(self):
        vals: Iterable[float] = [random.uniform(-100, 100) for i in range(100)]
        vec: Vec = Vec(vals)
        self.assertTrue(vec.dim == 100)
    
    #boundary case, test the parsing of an empty input
    def test_constructor_empty(self):
        vals: Iterable[float] = ()
        vec: Vec = Vec(vals)
        self.assertTrue(vec.dim == 0)

    #simple generic case, initialise a small vector and 1 to each component.
    #Test values and dimension of output.
    def test_add_s(self):
        vals: Iterable[float] = [-1, 0, 1]
        scaler: float = 1.0
        v1: Vec = Vec(vals)
        result: Vec = Vec.add_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([0, 1, 2]))
        self.assertEqual(result.dim, 3)
    
    #boundary case, add 1 to each component of an empty vector.
    def test_add_s_empty(self):
        vals: Iterable[float] = []
        scaler: float = 1.0
        v1: Vec = Vec(vals)

        result: Vec = Vec.add_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)
    
    #generic test case, adding two simple vectors.
    #checking dimension and values of output
    def test_add_v(self):
        vals: Iterable[float] = [-1, 0, 1]
        v1: Vec = Vec(vals)
        v2: Vec = Vec([x - 10 for x in vals])

        result: Vec = Vec.add_v(v1, v2)
        np.testing.assert_almost_equal(result.store, [-12, -10, -8])
        self.assertEqual(result.dim, 3)
    
    #testing bad inputs, adding two vectors of differing sizes
    #checking that the correct error is raised
    def test_add_v_different_size(self):
        vals: Iterable[float] = [random.uniform(-100, 100) for i in range(100)]
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals + [random.randint(-100, 100)])

        self.assertRaises(ValueError, Vec.add_v, v1, v2)
    
    #testing a boundary case, adding two empty vectors.
    #checking that result is empty with correct dimension attribute
    def test_add_v_empty(self):
        vals: Iterable[float] = []
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals)

        result: Vec = Vec.add_v(v1, v2)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)
    
    #generic test case, subtracting a scalar from a simple vector
    #checking that values are correct and dimension is unchanged
    def test_sub_s(self):
        vals: Iterable[float] = [-1, 0, 1]
        scaler: float = 1.0
        v1: Vec = Vec(vals)

        result: Vec = Vec.sub_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([-2, -1, 0]))
        self.assertEqual(result.dim, 3)
    
    #boundary case, subtracting a scalar from an empty vector
    #checking that result is empty and dimension is unchanged
    def test_sub_s_empty(self):
        vals: Iterable[float] = []
        scaler: float = 1.0
        v1: Vec = Vec(vals)

        result: Vec = Vec.sub_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)
    
    #generic test case, subtraction of two simple vectors
    #checking that values and dimension are correct
    def test_sub_v(self):
        vals: Iterable[float] = [-1, 0, 1]
        v1: Vec = Vec(vals)
        v2: Vec = Vec([x - 10 for x in vals])

        result: Vec = Vec.sub_v(v1, v2)
        np.testing.assert_almost_equal(result.store, np.array([10, 10, 10]))
        self.assertEqual(result.dim, 3)
    
    #bad input case, subtracting two vectors with differing dimension
    #checking that the correct error case is raised
    def test_sub_v_different_size(self):
        vals: Iterable[float] = [random.uniform(-100, 100) for i in range(100)]
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals + [random.randint(-100, 100)])

        self.assertRaises(ValueError, Vec.sub_v, v1, v2)

    #boundary case, subtraction of two empty vectors
    #checking that result is empty and has dimension zero
    def test_sub_v_empty(self):
        vals: Iterable[float] = []
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals)

        result: Vec = Vec.sub_v(v1, v2)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)

    #generic test case, multiplying a simple vector by a scalar
    #checking that result has correct values and dimension
    def test_mul_s(self):
        vals: Iterable[float] = [-1, 0, 1]
        scaler: float = 10.0
        v1: Vec = Vec(vals)

        result: Vec = Vec.mul_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([-10, 0, 10]))
        self.assertEqual(result.dim, 3)
    
    #boundary case, multiply empty vector by a scalar
    #checking that result is empty and has dimension zero
    def test_mul_s_empty(self):
        vals: Iterable[float] = []
        scaler: float = 1.0
        v1: Vec = Vec(vals)

        result: Vec = Vec.mul_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)

    #generic test case, multiply two simple vectors
    #checking that values are correct and output has correct dimension
    def test_mul_v(self):
        vals: Iterable[float] = [-1, 0, 1]
        v1: Vec = Vec(vals)
        v2: Vec = Vec([x - 10 for x in vals])

        result: Vec = Vec.mul_v(v1, v2)
        np.testing.assert_almost_equal(result.store, np.array([11, 0, -9]))
        self.assertEqual(result.dim, 3)

    #bad input case, multiplying two vectors of different size
    #checking that correct error is raised
    def test_mul_v_different_size(self):
        vals: Iterable[float] = [random.uniform(-100, 100) for i in range(100)]
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals + [random.randint(-100, 100)])

        self.assertRaises(ValueError, Vec.mul_v, v1, v2)

    #bad input case, attempting to multiply two vectors of different dimensions
    #checking that the correct error is raised
    def test_mul_v_empty(self):
        vals: Iterable[float] = []
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals)

        result: Vec = Vec.mul_v(v1, v2)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)
    
    #generic test case, dividing a simple vector by a scalar
    #checking that values are correct and dimension is preserved
    def test_div_s(self):
        vals: Iterable[float] = [-1, 0, 1]
        scaler: float = 10.0
        v1: Vec = Vec(vals)

        result: Vec = Vec.div_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([-0.1, 0, 0.1]))
        self.assertEqual(result.dim, 3)
    
    #boundary case, dividing the empty vector by a scalar
    #checking that the vector remains empty and its dimension is preserved
    def test_div_s_empty(self):
        vals: Iterable[float] = []
        scaler: float = 1.0
        v1: Vec = Vec(vals)

        result: Vec = Vec.div_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)

    #generic case, dividing two simple vectors
    #checking output vector has correct values and dimension
    def test_div_v(self):
        vals: Iterable[float] = [-1, 0, 1]
        v1: Vec = Vec(vals)
        v2: Vec = Vec([x - 10 for x in vals])

        result: Vec = Vec.div_v(v1, v2)
        # comparing floats
        np.testing.assert_almost_equal(result.store, np.array([1/11, 0, -1/9]))
        self.assertEqual(result.dim, 3)
    
    #bad input case, attempting to divide by zero
    #checking that the correct error is raised
    def test_div_v_zero_division_error(self):
        vals: Iterable[float] = [-1, 0, 1]
        v1: Vec = Vec(vals)
        v2: Vec = Vec([x - 10 for x in vals])

        self.assertRaises(FloatingPointError, Vec.div_v, v2, v1)

    #bad input case, attempting to divide vectors of different dimension
    #checking that the correct error is raised
    def test_div_v_different_size(self):
        vals: Iterable[float] = [random.uniform(-100, 100) for i in range(100)]
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals + [random.randint(-100, 100)])

        self.assertRaises(ValueError, Vec.div_v, v1, v2)

    #boundary case, dividing the empty vector by itself
    #checking that the output is the empty vector and has dimension 0
    def test_div_v_empty(self):
        vals: Iterable[float] = []
        v1: Vec = Vec(vals)
        v2: Vec = Vec(vals)

        result: Vec = Vec.div_v(v1, v2)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)

    #generic test case, raising a simple vector to a scalar power
    #checking that values are correct and dimension is preserved
    def test_pow_s(self):
        vals: Iterable[float] = [-10, 0, 10]
        scaler: float = 3
        v1: Vec = Vec(vals)

        result: Vec = Vec.pow_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([-1000, 0, 1000]))
        self.assertEqual(result.dim, 3)
    
    # is this how we do this?
    def test_pow_s_decimal_scaler(self):
        vals: Iterable[float] = [0, 10]
        scaler: float = 2
        v1: Vec = Vec(vals)

        result: Vec = Vec.pow_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([0.0, 100]))
        self.assertEqual(result.dim, 2)
        
    #boundary case, raising vector to scalar power zero
    #checking that all inputs are 1 and dimension is preserved
    #perhaps we should have another test case testing 0 to the 0th power?
    def test_pow_s_zero_scaler(self):
        vals: Iterable[float] = [-10, 0, 10]
        scaler: float = 0
        v1: Vec = Vec(vals)

        result: Vec = Vec.pow_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([1, 1, 1]))
        self.assertEqual(result.dim, 3)
    
    #boundary case, raising the empty vector to a scalar power
    #checking that the vector remains empty and dimension is preserved
    def test_pow_s_empty(self):
        vals: Iterable[float] = []
        scaler: float = 1.5
        v1: Vec = Vec(vals)

        result: Vec = Vec.pow_s(v1, scaler)
        np.testing.assert_almost_equal(result.store, np.array([]))
        self.assertEqual(result.dim, 0)

    #generic test case, computing the sum of a simple vector's components
    #checking that the sum is correct (0)
    def test_sum_v(self):
        vals: Iterable[float] = [-10, 0, 10]
        v1: Vec = Vec(vals)

        result: Vec = Vec.sum_v(v1)
        self.assertEqual(result, 0)
    
    #boundary case, computing the sum of the empty vector's components
    #checking that the sum is correct (0)
    def test_sum_v_empty(self):
        vals: Iterable[float] = []
        v1: Vec = Vec(vals)

        result: Vec = Vec.sum_v(v1)
        self.assertEqual(result, 0)

    #generic test case, computing the norm of a simple vector
    #checking that the value is correct
    def test_norm(self):
        vals: Iterable[float] = [-10, 0, -10]
        v1: Vec = Vec(vals)

        result: Vec = Vec.norm(v1)
        self.assertEqual(result, math.sqrt(200))

    #genetic test case, getting the coords of a vector
    #checking that they're correct
    def test_get_coords(self):
        vals: Iterable[float] = [-10, 0, -10]
        v1: Vec = Vec(vals)

        result = v1.get_coords()

        self.assertTrue(isinstance(result, tuple))
    
    #boundary case, getting the coords of an empty vector
    #checking that the result is empty
    def test_get_coords_empty(self):
        vals: Iterable[float] = []
        v1: Vec = Vec(vals)

        result = v1.get_coords()

        self.assertTrue(isinstance(result, tuple))



if __name__ == '__main__':
    unittest.main()