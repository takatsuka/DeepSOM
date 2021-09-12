from __future__ import annotations
from typing import *
from random import random, randint
import math
import matplotlib.pyplot as plt
from collections import deque 

from .SOM import SOM
from .Vec import Vec
from .Node import Node

class Map(SOM):

    # Assume input variables are standardized in [-1, 1] using MinMaxScalar()

    nodes: List[Node]  # 1D SOM nodes
    node_2D: List[List[Node]]  # 2D SOM nodes
        # I didn't want to remove nodes
        # I also didn't want to introduce bugs by trying to convert 1D to 2D
    side_len: int  # Number of nodes per side (square SOM)

    sigma: int  # Starting radius of neighborhood (default: 3)
    l: float  # Lambda: Time constant for learning rate and neighbor radius
        # Larger values lead to slower decay (default: max_iter)
    alpha: float  # Initial learning rate (default: 1)

    def __init__(self, max_iter: int, inp_dim: int, side_len: int, 
                       sigma: int = 0, l: float = 0,
                       alpha: float = 1):
        if (sigma == 0):  # sigma is the initial neighborhood radius
            sigma = max(side_len // 3, 3)
        if (l == 0):  # lambda (l) is the time constant
            l = max_iter

        self.sigma = sigma
        self.l = l
        self.alpha = alpha

        SOM.__init__(self, max_iter, inp_dim)

        self.side_len = side_len
        self.nodes = []
        self.node_2D = []
        for i in range(side_len):  # Generate all the nodes
            temp_node_list: List[Node] = []
            for j in range(side_len):
                temp_node = self.node_generator(Vec([i, j]))
                self.nodes.append(temp_node)
                temp_node_list.append(temp_node)
            self.node_2D.append(temp_node_list)
        
        for node in self.nodes:  # Link nodes as neighbors (grid linkage)
            topo: Tuple = node.get_topo().get_coords()
            topo_x: int = int(topo[0])
            topo_y: int = int(topo[1])
            if topo_x != 0:
                node.add_neighbor(self.node_2D[topo_x - 1][topo_y])
            if topo_x != side_len - 1:
                node.add_neighbor(self.node_2D[topo_x + 1][topo_y])
            if topo_y != 0:
                node.add_neighbor(self.node_2D[topo_x][topo_y - 1])
            if topo_y != side_len - 1:
                node.add_neighbor(self.node_2D[topo_x][topo_y + 1])

    def get_nodes(self) -> Iterable[Node]:
        return self.nodes

    def sigma_f(self, t: int) -> float:
        # Sigma function for neighborhood size
        return self.sigma * math.exp(-t/ self.l)

    def neighbor_multiplier(self, best: Node, n2: Node, t: int) -> float:
        # Closer nodes to best should return higher values
        # Consider a ceiling-like function of distance (sigmoid?)

        dist: float = self.distance(best.get_pos(), n2.get_pos())
            # Distance in space, not topological distance
        dist_mult = math.exp((-dist**2)/(2 * ((self.sigma_f(t)**2))))  
            # Consider alternate functions, this one is from towardsdatascience
        if (dist_mult < 0.001):
            dist_mult = 0
        return dist_mult

    def neighbors(self, best: Node, t: int) -> List[Node]:
        radius = math.floor(self.sigma_f(t))
        max_num = (2 * radius + 1)** 2

        res = [None] * max_num
        q = deque(maxlen=max_num)
        traversed = set()
        count = 0
        depth = 1

        current_num = 1
        res[count] = best
        count += 1
        traversed.add(best.get_id())
        q.append(best)
        while len(q) != 0:
            cur = q.popleft()
            current_num -= 1
            to_set = current_num == 0
            for neighbor in cur.fetch_neighbors():
                if neighbor.get_id() not in traversed:
                    if (depth < radius):
                        q.append(neighbor)
                    res[count] = neighbor
                    count += 1
                    traversed.add(neighbor.get_id())
            if to_set:
                current_num = len(q)
                depth += 1
        return res[:count]

        # radius: float = math.floor(self.sigma_f(t))
        
        # ret_nodes: List[Node] = [best]
        # current_layer: List[Node] = [best]
        # next_layer: List[Node] = []

        # count: int = 1
        # while len(current_layer) > 0 and count <= radius:
        #     for node in current_layer:
        #         for neighbor in node.fetch_neighbors():
        #             if neighbor not in ret_nodes:
        #                 ret_nodes.append(neighbor)
        #                 next_layer.append(neighbor)
        #     current_layer = next_layer
        #     next_layer = []
        #     count += 1
        # return ret_nodes

    def learning_rate(self, t: int) -> float: 
        time_mult: float = self.alpha * math.exp(-t / self.l)
            # Consider alternate alpha function
        return time_mult

    def norm_out(self) -> List[List[float]]:  # Output 2D list of Node norms
            # Consider a functional (map) implementation for efficiency
        ret_vals: List[List[float]] = []
        for i in range(self.side_len):
            temp_row: List[float] = []
            for j in range(self.side_len):
                temp_norm = Vec.norm(self.node_2D[i][j].get_pos())
                temp_row.append(temp_norm)
            ret_vals.append(temp_row)
        return ret_vals
    
    def visualise(self):
        # Calculate average distance of all nodes from its immediate neighbours
        neuron_distances: List[List[float]] = []
        for i in range(self.side_len):
            temp_row: List[float] = []
            for j in range(self.side_len):
                n = self.node_2D[i][j]
                neighbors: List[Node] = n.fetch_neighbors()
                temp_row.append(
                    sum(map(lambda x: Vec.norm(Vec.sub_v(n.get_pos(),x)),
                            map(lambda x: x.get_pos(), neighbors)))/len(neighbors))
            neuron_distances.append(temp_row)
        
        plt.clf()
        plt.imshow(neuron_distances, cmap="RdBu_r")
        plt.colorbar()
        plt.savefig("test.png")

        