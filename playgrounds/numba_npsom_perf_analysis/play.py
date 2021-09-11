import sys
import numpy as np
from simplesom import simplesom as som
from random import sample as sp
import matplotlib.pyplot as plt
import time

datastr = [l.strip().split(',') for l in open(sys.argv[1]).readlines()]
data = [[float(c) for c in e] for e in datastr]


model = som(100,100,3, init_epoch=16384)

start = time.time()
for _ in range(16384):
    model.learn(sp(data, 1))
end = time.time()

print("Elapsed (with compilation) = %s" % (end - start))

ws = model.dump_weight_list()
print(ws)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

axes = list(zip(*ws))
axes_o = list(zip(*data))
ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))
    
ax.scatter(*axes, marker='o', s=1)
ax.scatter(*axes_o, marker='o', s=1.4, color="magenta")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.savefig(f"som.png")