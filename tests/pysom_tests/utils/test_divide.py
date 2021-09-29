import pytest
from pysom.utils.divide import divide


def test_divide_basic():
    assert pytest.approx(7.0) == divide(14.0, 2.0)


def test_divide_good_nonint():
    assert pytest.approx(1.5) == divide(3.0, 2.0)


def test_divide_bad():
    assert not pytest.approx(2.0) == divide(3.0, 2.0)


def test_divide_type():
    assert isinstance(divide(2.0, 3.0), float)
