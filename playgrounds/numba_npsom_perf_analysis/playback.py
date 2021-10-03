import sys
import numpy as np
from simplesom import simplesom as som
from random import sample as sp
import matplotlib.pyplot as plt
import time
import json
datastr = [l.strip().split(',') for l in open(sys.argv[1]).readlines()]
data = [[float(c) for c in e] for e in datastr]

SWID = 12
SHEI = 12
model = som(SWID,SHEI,3, init_epoch=16384)
playback_points = []

start = time.time()
for i in range(16384):
    model.learn(sp(data, 1))

    if i % 100 == 0:
        playback_points.append(model.dump_weight_list().tolist())

end = time.time()

print("Elapsed (with compilation) = %s" % (end - start))

# ws = model.dump_weight_list()
pb = {}
for i, v in enumerate(playback_points):
    pb[str(i)] = v

d = {'type':'som_cp', 'som':'simple_not_deep_fashion', 'w': SWID, 'h': SHEI, 
'weights': model.dump_weight_list().tolist(), 
'weightspb': pb}



open('out.json','w').write(json.dumps(d))
