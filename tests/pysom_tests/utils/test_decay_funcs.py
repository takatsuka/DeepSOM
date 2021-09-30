import pytest
from pysom.utils.decay_funcs import exp_decay, linear_step


def test_exp_decay_basic():
    assert pytest.approx(0.6958125748377546) == exp_decay(1, 0.7, 0.1, (0.7 - 0.1) / 100)


def test_linear_step_basic():
    assert pytest.approx(0.694) == linear_step(1, 0.7, 0.1, (0.7 - 0.1) / 100)
