import unittest
from pysom.utils.add import add


class AddTester(unittest.TestCase):
    def test_add_basic(self):
        self.assertAlmostEqual(5.0, add(2.0, 3.0))

    def test_add_bad(self):
        self.assertNotAlmostEqual(3.0, add(1.0, 7.0))

    def test_add_type(self):
        self.assertIsInstance(add(2.0, 3.0), float)
