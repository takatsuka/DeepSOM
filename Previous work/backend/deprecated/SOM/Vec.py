from __future__ import annotations
from typing import *

from functools import reduce

import numpy as np
np.seterr(divide='raise')  

import math

class Vec:

    def __init__(self, vals: List[float]) -> None:
        self.store = np.asarray(vals, dtype=float)
        self.dim = self.store.size

    #add a scalar to every component of a vector
    @staticmethod
    def add_s(v1: Vec, scalar: float) -> Vec:
        return Vec(v1.store + scalar)

    #add two vectors component wise
    @staticmethod
    def add_v(v1: Vec, v2: Vec) -> Vec:
        return Vec(v1.store + v2.store)

    #subtract a scalar from each component of a vector
    @staticmethod
    def sub_s(v1: Vec, scalar: float) -> Vec:
        return Vec(v1.store - scalar)

    #subtract two vectors component wise
    @staticmethod
    def sub_v(v1: Vec, v2: Vec) -> Vec:
        return Vec(v1.store - v2.store)

    #multiply each component of a vector by a scalar
    @staticmethod
    def mul_s(v1: Vec, scalar: float) -> Vec:
        return Vec(v1.store * scalar)

    #multiply two vectors component wise
    @staticmethod
    def mul_v(v1: Vec, v2: Vec) -> Vec:
        return Vec(v1.store * v2.store)

    #divide each component of a vector by a scalar
    @staticmethod
    def div_s(v1: Vec, scalar: float) -> Vec:
        return Vec(v1.store / scalar)

    #divide two vectors component wise
    @staticmethod
    def div_v(v1: Vec, v2: Vec) -> Vec:
        return Vec(v1.store / v2.store)

    #raise each component of a vector to a scalar power
    @staticmethod
    def pow_s(v1: Vec, scalar: float) -> Vec:
        return Vec(v1.store ** scalar)

    #sum the components of a vector
    @staticmethod
    def sum_v(v1: Vec) -> float:
        return np.add.reduce(v1.store)

    #returns the euclidean norm of a vector
    @staticmethod
    def norm(v1: Vec) -> float:
        return math.sqrt(np.add.reduce(v1.store ** 2))

    def get_coords(self) -> Tuple[float, ...]:
        return tuple(self.store)

    def __str__(self) -> str:
        return str(self.get_coords())

    
