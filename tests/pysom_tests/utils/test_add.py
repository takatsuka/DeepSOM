import pytest
from pysom.utils.add import add


def test_add_basic():
    assert pytest.approx(5.0) == add(2.0, 3.0)


def test_add_bad():
    assert not pytest.approx(3.0) == add(1.0, 7.0)


def test_add_type():
    assert isinstance(add(2.0, 3.0), float)
