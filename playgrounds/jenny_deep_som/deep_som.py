import numpy as np
from numba import jit
import matplotlib
import matplotlib.pyplot as plt
from random import sample as sp
from enum import Enum
import sys
from numbasom import simplesom as SOM


class DeepSom:
    def __init__(self, n_epoch):
        self.n_epoch = n_epoch
        self.soms = set()

    def add_som(self, domain):
        self.soms.add(domain)

    def get_root(self):
        return None

    def train(self, data):
        # Organise soms into queue so they are trained in the right order
        training_queue = self.sort_soms()
        final_som = None
        counter = 0
        # Start training
        print(training_queue)
        while len(training_queue) > 0:
            som = training_queue.pop(0)
            model = som.initialise_som(self.n_epoch)
            
            if som.domain_type is DomainType.LEAF:
                # Extract data with correct dimensions
                training_data = self.extract_input_data(data, som.dimensions)
            else:
                # Extract weight lists from children soms and concatenate them together
                training_data = self.extract_children_data(som).tolist()
            
            for _ in range(self.n_epoch):
                model.learn(sp(training_data, 1))

            # Remember the last model (which would be the root SOM)
            if len(training_queue) == 0:
                final_som = model
            
        # Return root som
        return final_som

    def extract_children_data(self, som):
        weights = []
        for child in som.children:
            child_weights = child.get_som().dump_weight_list()
            weights.append(child_weights)
        concat_weights = np.concatenate(weights)
        return concat_weights

    def extract_input_data(self, data, dimensions):
        final_data = []
        for line in data:
            line_data = [line[index] for index in dimensions]
            final_data.append(line_data)
        return final_data

    # Sort SOMs by DFS
    def sort_soms(self):
        visited = {som : False for som in self.soms}
        queue = []
        for som in self.soms:
            if not visited[som]:
                visited, queue = self.visit_som(som, visited, queue)
        return queue

    def visit_som(self, som, visited, queue):
        visited[som] = True
        # Visit children first
        for child in som.children:
            if not visited[child]:
                visited, queue = self.visit_som(child, visited, queue)
        # Then add self to queue
        queue.append(som)
        return visited, queue


class DomainType(Enum):
    LEAF = 1
    NON_LEAF = 2


class Domain:
    def __init__(self, lattice_width, lattice_height, domain_type):
        self.lattice_width = lattice_width
        self.lattice_height = lattice_height
        self.domain_type = domain_type
        self.som = None

        # Dimensions is an array of indices of which dimensions this domain involves
        self.dimensions = set()

        # Children is a set of Domains that the current Domain is based on
        self.children = set()

    def define_dimensions(self, dimensions):
        for index in dimensions:
            self.dimensions.add(index)

    def add_child(self, domain):
        self.children.add(domain)

    def initialise_som(self, n_epoch):
        if len(self.dimensions) == 0:
            self.som = SOM(self.lattice_width, self.lattice_height, self.find_largest_dimension_in_children(), init_epoch=n_epoch)
        else:
            self.som = SOM(self.lattice_width, self.lattice_height, len(self.dimensions), init_epoch=n_epoch)
        return self.som

    def find_largest_dimension_in_children(self):
        largest_dimension = 0
        for child in self.children:
            if len(child.dimensions) > largest_dimension:
                largest_dimension = len(child.dimensions)
        return largest_dimension

    def get_som(self):
        return self.som


datastr = [l.strip().split(',') for l in open(sys.argv[1]).readlines()]
data = [[float(c) for c in e] for e in datastr]

init_epoch = 200
deep_som = DeepSom(init_epoch)

# User defining domains for the base layer
domain_a = Domain(100, 100, DomainType.LEAF)
domain_a.define_dimensions((0, 1))
deep_som.add_som(domain_a)
print("a:", domain_a)

domain_b = Domain(100, 100, DomainType.LEAF)
domain_b.define_dimensions((1, 2))
deep_som.add_som(domain_b)
print("b:", domain_b)

# User defining domains for upper layers
domain_c = Domain(200, 200, DomainType.NON_LEAF)
domain_c.add_child(domain_a)
domain_c.add_child(domain_b)
deep_som.add_som(domain_c)
print("c:", domain_c)

# domain_d = Domain(init_epoch, 100, 100, DomainType.NON_LEAF)
# domain_d.add_child(domain_a)
# domain_d.add_child(domain_b)
# deep_som.add_som(domain_d)

# domain_e = Domain(init_epoch, 100, 100, DomainType.NON_LEAF)
# domain_e.add_child(domain_c)
# domain_e.add_child(domain_d)
# deep_som.add_som(domain_e)

# Train the deep SOM
root_som = deep_som.train(data)

weights = root_som.dump_weight_list()

# Graph the resulting weights (doesn't work --> bug at line 174 where axes is only size 2)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

axes = list(zip(*weights))
axes_o = list(zip(*data))
print(len(axes_o))
ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))
    
ax.scatter(*axes, marker='o', s=1)
ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.savefig(f"deep_som.png")