from Som import Som
import json
import numpy as np
import matplotlib.pyplot as plt


width = 100
height = 100
indim = 3

som = Som(width, height, indim)
som.regen_mat(scale=2, offset=-0.5)

datastr = [l.strip().split(',') for l in open("sphere_64.txt", "r").readlines()]
dataset = [[float(c) for c in e] for e in datastr]

data = np.array(dataset)
print(len(data))

js = {}

step = 0

for i in range(16001):
    point = data[np.random.randint(0, len(data))]
    som.learn(point, i)

    if i % 800 == 0:
        sw = som.dump_weight_list()
        fw = [elem for l in sw for elem in l]
        
        js[step] = fw
        """
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        axes = list(zip(*sw))
        axes_o = list(zip(*dataset))
        ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))

        ax.scatter(*axes, marker='o', s=1)
        ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.savefig("sphere64_{}.png".format(step))
        """
        step += 1

with open('vis20_sphere64.txt', 'w') as outfile:
    json.dump(js, outfile)
