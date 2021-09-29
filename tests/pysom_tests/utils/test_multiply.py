import pytest
from pysom.utils.multiply import multiply


def test_multiply_basic():
    assert pytest.approx(14.0) == multiply(7.0, 2.0)


def test_multiply_good_nonint():
    assert pytest.approx(4.5) == multiply(2.0, 2.25)


def test_multiply_bad():
    assert not pytest.approx(4.0) == multiply(3.0, 2.0)


def test_multiply_type():
    assert isinstance(multiply(2.0, 3.0), float)
