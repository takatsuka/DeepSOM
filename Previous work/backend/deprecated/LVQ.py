from __future__ import annotations
from typing import *
from random import random, randint
import math
import numpy as np
import numpy.random as nprng
import matplotlib.pyplot as plt

from .imports import *

class LVQ:
    inp_dim: int  # Number of attributes
    alpha: float  # Initial learning rate (default 0.3)
    n_class: int  # Number of classes for classification
    class_map: Dict[int: Any] = {}  # Mapping of class index to class label
    nodes: List[np.ndarray] = []
    
    def __init__(self, epochs: int, inp_dim: int, classes: Any, alpha = 0.3):
        self.inp_dim = inp_dim
        self.alpha = alpha
        self.n_class = len(classes)
        self.class_map = {idx:item for idx,item in enumerate(classes)}
        self.nodes = [nprng.random(self.inp_dim) for i in range(self.n_class)]
            # TODO : Decide node position based on class mean
    
    def fit(self, datas: List[np.ndarray], labels: List[Any], epochs: int) -> None:
        if (len(datas) != len(labels)):
            raise Exception("Data and class dimensions don't match")
        e: int = 0 
        while e < epochs:
            for idx in range(len(datas)):
                data = datas[idx]
                label = labels[idx]
                bmu_idx = self.find_bmu_idx(data)
                bmu_node = self.nodes[bmu_idx]

                if labels[bmu_idx] == label:
                    mult = 1
                else:
                    mult = -1

                diff: float = data - bmu_node
                self.nodes[bmu_idx] = mult * diff * self.learning_rate(e, epochs)
                
            e += 1

    def predict(self, data): # Predict class for input vector
        bmu_index = self.find_bmu_idx(data)  
        return self.class_map[bmu_index]

    def test(self, testData: List[Any], labels: List[Any]):
        if (len(testData) != len(labels)):
            raise Exception("Data and class dimensions don't match")
        error: int = 0
        for idx, data in enumerate(testData):
            pred = self.class_map[self.find_bmu_idx(data)]
            if pred != labels[idx]:
                error += 1
        return error/len(testData)

    def learning_rate(self, e: int, epochs: int) -> float:
        # From https://machinelearningmastery.com/learning-vector-quantization-for-machine-learning/
        return self.alpha * (1 - (e/epochs))
          
    def find_bmu_idx(self, inp_vec: np.ndarray) -> int:   # Thanks allen
            # Find closest matching node to item, returns index
        mins: Tuple[Optional[Node], float] = (None, math.inf)
            # Stores (node index, euclidean distance) pair
            # Index is for self.nodes, unlike find_bmu in SOM.py
        for idx, node in enumerate(self.nodes):
            dist: float = np.linalg.norm(node - inp_vec)
            if (dist < mins[1]):
                mins = (idx, dist)
        if (mins[0] is None):
            raise Exception("Min not found")
        else:
            return mins[0]
                





