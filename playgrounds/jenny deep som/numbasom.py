import numpy as np
from numba import jit
import matplotlib
import matplotlib.pyplot as plt

@jit(nopython=True)
def som_activate(m, v):
    flat_idx = np.argmin(np.sum((m - v) ** 2, axis=2))
    return (flat_idx // m.shape[0], flat_idx % m.shape[1])

@jit(nopython=True)
def som_learn_batch(m, b, mat_coord, rg, lr):
    mat = m
    w, h, _ = mat.shape
    bnpa = b
    for v in bnpa: 
        winner = som_activate(mat, v)

        dists_mat = np.sum(np.abs(mat_coord - np.array(winner)), axis=2)
        h_mat = np.exp(-(dists_mat * (1 / rg)) ** 2).reshape(w, h, 1)
        mat = mat - ((mat - v)*h_mat * lr)
    
    return mat

class simplesom:
    def __init__(self, width,height, dimin, init_scale=2, init_offset = -0.5, init_epoch=600):

        self.lr = 0.7
        self.lr_min = 0.1

        self.lr_max = self.lr        

        self.rg = width * 0.5
        self.rg_min = 0.7
        self.rg_max = self.rg

        self.set_round_epochs(init_epoch)
        self.width = width
        self.height = height
        self.input_dim = dimin

        self.mat = (np.random.default_rng().random((self.width, self.height, self.input_dim), dtype=np.float64) + init_offset) * init_scale
        idx_mat = np.unravel_index(np.arange(self.width * self.height).reshape(self.width, self.height), (self.width, self.height))
        self.mat_coord = np.stack(idx_mat, 2)



    def __str__(self):
        return str(self.mat)

    def set_round_epochs(self, num):
        self.lr_step = ((self.lr - self.lr_min) / num)
        self.rg_step = ((self.rg - self.rg_min) / num)
        self.lr_max = self.lr     
        self.rg_max = self.rg

    def get_weight(self, x, y):
        return self.mat[x,y]

    def dump_weight_list(self):
        return self.mat.reshape((self.width * self.height, self.input_dim))
        
    
    def get_arg_closest(self, v):
        flat_idx = np.argmin(np.sum((self.mat - v) ** 2, axis=2))
        return (flat_idx // self.width, flat_idx % self.height)

    def get_vector_estimate(self, v, feats):
        flat_idx = np.argmin(np.sum((self.mat[:,:,:feats] - v) ** 2, axis=2))
        return (flat_idx // self.width, flat_idx % self.height)

    def learn(self, v):
        winner = self.get_arg_closest(v)

        dists_mat = np.sum(np.abs(self.mat_coord - np.array(winner)), axis=2)
        h_mat = np.exp(-(dists_mat * (1 / self.rg)) ** 2).reshape(self.width, self.height, 1)
        self.mat = self.mat - ((self.mat - v)*h_mat * self.lr)


        self.lr = max(self.lr_min, self.lr - self.lr_step)
        self.rg = max(self.rg_min, self.rg - self.rg_step)


    def learn_batch(self, b):
        nm = som_learn_batch(self.mat, np.array(b, dtype=np.float64), self.mat_coord, self.rg, self.lr)
        self.mat = nm

        self.lr = max(self.lr_min, self.lr - self.lr_step * len(b))
        self.rg = max(self.rg_min, self.rg - self.rg_step * len(b))
    

    def learn_more(self):
        self.lr = min(self.lr_max, self.lr + self.lr_step)
        self.rg = min(self.rg_max, self.rg + self.rg_step)

    #dataset should be of shape(n, dim(input))
    def error_to_dataset(self, dataset):
        cumerr = 0
        cumidx = 0
        for d in dataset:
            dist = self.mat[self.get_arg_closest(d)] - d
            cumerr += np.sqrt(np.dot(dist, dist.T))
            cumidx += 1
        
        return cumerr / cumidx


    def error_to_dataset_max(self, dataset):
        cumerr = 0
        for d in dataset:
            dist = self.mat[self.get_arg_closest(d)] - d
            cumerr = max(np.sqrt(np.dot(dist, dist.T)), cumerr)
            
        
        return cumerr
