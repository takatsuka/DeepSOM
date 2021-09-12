# Specify all required imports in requirements.txt

from __future__ import annotations
from typing import *
from random import random, randint
import math

from .Vec import Vec
from .Node import Node

class SOM:  # Abstract base class

    t_lim: int  # Iteration limit

    inp_dim: int  # Number of attributes
    node_id: int  # Number of nodes in the SOM

    def __init__(self, max_iter: int, inp_dim: int):
        self.t_lim = max_iter
        self.inp_dim = inp_dim
        self.node_id = 0

    # Abstract functions:
    def get_nodes(self) -> Iterable[Node]:
        pass

    def neighbor_multiplier(self, best: Node, n2: Node, t: int) -> float:
        pass

    def sigma_f(self, t: int) -> float:
        pass

    def neighbors(self, best: Node, t: int) -> List[Node]:
        pass

    def learning_rate(self, t: int) -> float:
        pass

    def distance(self, v1: Vec, v2: Vec) -> float:  # Euclidean distance
        temp: Vec = Vec.sub_v(v1, v2)
        return Vec.norm(temp)

    def stochastic_train(self, datas: List[Vec], verbose=False) -> None:
            # Train using randomly selected single vectors
        for node in self.get_nodes():  # Initialise spatial position
            node.set_pos(Vec([random() for i in range(self.inp_dim)]))
        t = 0
        while t < self.t_lim:  # Training iteration
            # Includes right endpoint
            to_pick: int = randint(0, len(datas) - 1)  # Random input vector
            data: Vec = datas[to_pick]
            if data.dim != self.inp_dim:
                raise Exception("Data dimension not matching")
            bmu: Node = self.find_bmu(data)  # Closest node to input vector
            for neighbor in self.neighbors(bmu, t):  # Move all neighbors
                    # Neighborhood shrinks with time
                to_change: Vec = Vec.sub_v(data, bmu.get_pos())  # Distance
                n_mult: float = self.neighbor_multiplier(bmu, neighbor, t)
                to_change = Vec.mul_s(to_change, n_mult)  
                    # Nodes further away are moved less
                to_change = Vec.mul_s(to_change, self.learning_rate(t))
                    # Distance moved is decreased over time
                neighbor.add_pos(to_change)
            t += 1
            if verbose:
                print("{:.2f}% complete".format(t/self.t_lim*100))

    def batch_train(self, datas: List[Vec], verbose = False) -> None:  
            # Train on entire dataset of input vectors, in epochs
        for node in self.get_nodes():
            node.set_pos(Vec([random() for i in range(self.inp_dim)]))
        t = 0
        while t < self.t_lim:
            to_changes: List[Vec] = [Vec([0 for i in range(self.inp_dim)]) 
                                        for j in range(self.node_id)]
                # New spatial positions for each node
            for data in datas:  # Iterate over input vectors
                if data.dim != self.inp_dim:
                    raise Exception("Data dimension not matching")
                bmu: Node = self.find_bmu(data)
                for neighbor in self.neighbors(bmu, t):
                    to_change: Vec = Vec.sub_v(data, bmu.get_pos())
                    n_mult: float = self.neighbor_multiplier(bmu, neighbor, t)
                    to_change = Vec.mul_s(to_change, n_mult)
                    to_change = Vec.mul_s(to_change, self.learning_rate(t))
                    to_changes[neighbor.get_id()] = to_change
            for node in self.get_nodes():
                node.add_pos(to_changes[node.get_id()])
            t += 1
            if verbose:
                print("{:.2f}% complete".format(t/self.t_lim*100))

    def node_generator(self, topo_coord: Vec, 
                        init_pos: Optional[Vec] = Vec([])) -> Node:
        self.node_id += 1
        return Node(topo_coord, self.node_id - 1, init_pos)

    def find_bmu(self, inp_vec: Vec) -> Node:
        # we rust now
        mins: Tuple[Optional[Node], float] = (None, math.inf)
        for node in self.get_nodes():
            dist: float = self.distance(node.get_pos(), inp_vec)
            if (dist < mins[1]):
                mins = (node, dist)
        if (mins[0] is None):
            raise Exception("Min not found")
        else:
            return mins[0]
