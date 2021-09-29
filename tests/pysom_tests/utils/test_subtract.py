import pytest
from pysom.utils.subtract import subtract


def test_subtract_basic():
    assert pytest.approx(5.0) == subtract(7.0, 2.0)


def test_subtract_good_nonint():
    assert pytest.approx(0.75) == subtract(2.0, 1.25)


def test_subtract_bad():
    assert not pytest.approx(4.0) == subtract(3.0, 2.0)


def test_subtract_type():
    assert isinstance(subtract(2.0, 3.0), float)
