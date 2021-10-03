import json
import numpy as np
d = json.loads(open('sample_cp.json').read())

print(np.array(d['weights']))