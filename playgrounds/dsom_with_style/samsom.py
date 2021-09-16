import numpy as np
from numba import jit
from numbasom import simplesom as som
from numbasom import som_transform
from multiprocessing import Pool

class samsom:
    def __init__(self, pnx, pny, pw, ph, somdim):
        self.soms = []
        self.nump = pnx * pny
        self.pn = (pnx, pny)
        self.dim = pw * ph
        self.sod = somdim
        for _ in range(self.nump): self.soms.append(som(somdim, somdim, self.dim))

    def set_train_iter(self, n):
        for s in self.soms: s.set_round_epochs(n)

    # @jit(parallel=True)
    def train(self, patches):
        fp = patches.reshape((self.nump, self.dim))
        for i in range(self.nump):
            self.soms[i].learn(fp[i])
        
    def sample(self, patches):
        fp = patches.reshape((self.nump, self.dim))
        samples = np.zeros((self.nump, 1))
        for i in range(self.nump):
            samples[i] = som_transform(self.soms[i].mat, fp[i])
        
        return samples.reshape(self.pn) / (self.sod ** 2)

    def extract(self, patches):
        fp = patches.reshape((self.nump, self.dim))
        samples = np.zeros((self.nump, self.dim))
        for i in range(self.nump):
            samples[i] = self.soms[i].bmu([fp[i]])[0]
        
        return samples


    
    