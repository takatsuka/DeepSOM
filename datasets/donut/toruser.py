


PLOTTY = True

if PLOTTY: import matplotlib.pyplot as plt
import sys
import numpy as np
from math import sqrt as st
from math import pi, sin, cos
import random
um = random.uniform
umrad = lambda: um(0, 2 * pi)

r = 0.7 #inner radius
a = 0.3 #thickness

def gen_num(n):
    points = []
    for _ in range(n):
        i, o = umrad(), umrad()
        x = (r + a * cos(i)) * cos(o)
        y = (r + a * cos(i)) * sin(o)
        z = a * sin(i)
        points.append((x, y, z))
    
    return points

nn = int(sys.argv[1])

p = gen_num(nn)
open(f"donut_{nn}.txt", 'w').write('\n'.join(['{}, {}, {}'.format(*e) for e in p]))

if PLOTTY:
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    axes = list(zip(*p))
    ax.set_box_aspect((np.ptp(axes[0]), np.ptp(axes[1]), np.ptp(axes[2])))
    
    ax.scatter(*axes, marker='o', s=1, color="magenta")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.savefig(f"donut_{nn}.png")
    
        

