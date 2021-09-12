from __future__ import annotations
from typing import *

from .Vec import Vec


class Node:

    topo_coord: Vec
    position: Vec
    neighbors: List[Node]
    id_v: int

    def __init__(self, topo_coord: Vec, id_v: int, 
                    init_pos: Optional[Vec] = None) -> None:
        self.topo_coord = topo_coord
        if init_pos is None:
            self.position = Vec([])
        else:
            self.position = init_pos
        self.neighbors = []
        self.id_v = id_v 

    def add_neighbor(self, neighbor: Node) -> None:
        self.neighbors.append(neighbor)

    def add_pos(self, delta: Vec) -> None:
        self.position = Vec.add_v(self.position, delta)

    def set_pos(self, loc: Vec) -> None:
        self.position = loc

    def mult_pos(self, scalar: float) -> None:
        self.position = Vec.mul_s(self.position, scalar)

    def get_pos(self) -> Vec:
        return self.position

    def get_topo(self) -> Vec:
        return self.topo_coord

    def get_id(self) -> int:
        return self.id_v

    def fetch_neighbors(self) -> List[Node]:
        return list(self.neighbors)
