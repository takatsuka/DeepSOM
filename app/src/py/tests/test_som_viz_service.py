import pytest
from som_viz_service import *

def test_lerp():
    assert lerp(1, 1, 1) == 1

def test_bilinear():
    assert bilinear()