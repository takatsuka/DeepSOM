
#a simple slow script to generate sphere pc dataset

PLOTTY = True

if PLOTTY: import matplotlib.pyplot as plt
import sys
import numpy as np
from math import sqrt as st
import random
um = random.uniform
umstd = lambda: um(-1,1)



def gen_num(n):
    points = []
    for _ in range(n):
        v = (umstd(), umstd(), umstd())
        lvdv = st(sum([x**2 for x in v]))
        points.append([x / lvdv for x in v])
    
    return points

nn = int(sys.argv[1])

p = gen_num(nn)
open(f"sphere_{nn}.txt", 'w').write('\n'.join(['{}, {}, {}'.format(*e) for e in p]))

if PLOTTY:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    axes = list(zip(*p))
    ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))
    
    ax.scatter(*axes, marker='o', s=1, color="magenta")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.savefig(f"sphere_{nn}.png")
    
        

