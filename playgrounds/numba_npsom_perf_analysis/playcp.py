import numpy as np
import time
from simplesom import simplesom as som
import json
from random import randint as ri
from random import sample as sp



from mnist import MNIST
mndata = MNIST('../../datasets/fashion_mnist/large_bin')
train_dat, train_lab = mndata.load_training()
test_dat, test_lab = mndata.load_testing()


train_lab = np.array(train_lab, dtype=np.float64)
test_lab = np.array(test_lab, dtype=np.float64)
train_dat = np.array(train_dat, dtype=np.float64).reshape((len(train_dat), 28, 28)) / 255.0
test_dat = np.array(test_dat, dtype=np.float64).reshape((len(test_dat), 28, 28)) / 255.0

train_dat = train_dat
train_lab = train_lab
train_dat = train_dat.reshape((train_dat.shape[0], 28*28))

SWID = 15
SHEI = 15

model = som(SWID,SHEI,train_dat.shape[1], init_epoch=70000)
print("train started")
start = time.time()
for i in range(70000):
    model.learn(train_dat[ri(0, train_dat.shape[0]-1)])
    if i % 1000 == 0: print(i)

end = time.time()


data = {'type':'som_cp', 'som':'simple_not_deep_fashion', 'w': SWID, 'h': SHEI, 'weights': model.dump_weight_list().tolist()}
jdata = json.dumps(data, indent=4)

open("sample_cp.json", 'w').write(jdata)
