import unittest
from pysom.utils.divide import divide


class DivideTester(unittest.TestCase):
    def test_divide_basic(self):
        self.assertAlmostEqual(7.0, divide(14.0, 2.0))
        
    def test_divide_good_nonint(self):
        self.assertAlmostEqual(1.5, divide(3.0, 2.0))

    def test_divide_bad(self):
        self.assertNotAlmostEqual(2.0, divide(3.0, 2.0))

    def test_divide_type(self):
        self.assertIsInstance(divide(2.0, 3.0), float)
