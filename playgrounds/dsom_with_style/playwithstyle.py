import numpy as np
from numba import jit
from numbasom import simplesom as som
from samsom import samsom
from random import randint as ri
from random import sample as sp
import matplotlib.pyplot as plt
from sklearn.svm import SVC
# @jit(nopython=True)
def imgrid(imgs, w, h):

    row = np.concatenate(imgs[:w])
    imgs = imgs[w:]

    for r in range(1, h):
        cr = np.concatenate(imgs[:w])
        imgs = imgs[w:]
        row = np.concatenate((row, cr), axis=1)

    return row

from mnist import MNIST
mndata = MNIST('../../datasets/fashion_mnist/large_bin')
train_dat, train_lab = mndata.load_training()
test_dat, test_lab = mndata.load_testing()


train_lab = np.array(train_lab, dtype=np.float64)
test_lab = np.array(test_lab, dtype=np.float64)
train_dat = np.array(train_dat, dtype=np.float64).reshape((len(train_dat), 28, 28)) / 255.0
test_dat = np.array(test_dat, dtype=np.float64).reshape((len(test_dat), 28, 28)) / 255.0

train_dat = train_dat[:20000]
train_lab = train_lab[:20000]

test_dat = test_dat[:1500]
test_lab = test_lab[:1500]

@jit(nopython=True)
def fast_mini_patch(img, kernel=10, stride=2, fill=0.0):
    w, h = img.shape[:2]
    num_h, num_v = (w-kernel)//stride + 1, (h-kernel)//stride + 1
    # img = np.pad(img,(0,kernel), 'constant', constant_values=(0.0, fill))

    patches = np.zeros((num_h, num_v, kernel, kernel))
    for i in range(num_h):
        for j in range(num_v):
            patches[j][i] = img[i * stride: i * stride + kernel, j * stride: j * stride + kernel]

    return patches.reshape((num_v * num_h, kernel, kernel)), num_h, num_v

@jit(nopython=True, parallel=True)
def batch_mini_patch(imgs, kernel=10, stride=2, fill=0.0):
    w, h = imgs.shape[1:3]
    num_h, num_v = (w-kernel)//stride + 1, (h-kernel)//stride + 1
    chunk = np.zeros((imgs.shape[0], num_v * num_h, kernel, kernel))
    for i in range(imgs.shape[0]): 
        p,_,_ = fast_mini_patch(imgs[i], kernel=kernel, stride=stride)
        chunk[i] = p
    return chunk


def draw_sample(samsom, sam, img, prefix='_'):
    print(sam.shape)
    ex = samsom.extract(sam).reshape(sam.shape[0], sam.shape[1], sam.shape[2])
    g = imgrid(ex, 10, 10)
    tr = samsom.sample(sam)
    fig = plt.figure()
    plt.imshow(g, vmin=0.0, vmax=1.0, cmap='PuRd')
    plt.axis('off')
    plt.savefig(f'activation_{prefix}.png', dpi=300, bbox_inches='tight')

    fig = plt.figure()
    plt.imshow(tr, vmin=0.0, vmax=1.0, cmap='PuRd')
    plt.axis('off')
    plt.savefig(f'sample_{prefix}.png', dpi=300, bbox_inches='tight')

    fig = plt.figure()
    plt.imshow(img, vmin=0.0, vmax=1.0, cmap='PuRd')
    plt.axis('off')
    plt.savefig(f'img_{prefix}.png', dpi=300, bbox_inches='tight')
    
    


exp, x, y = fast_mini_patch(train_dat[45])
train_dat_p = batch_mini_patch(train_dat)
test_dat_p = batch_mini_patch(test_dat)

hidden1 = samsom(x, y, exp.shape[1], exp.shape[2], 20)



print("train start")
hidden1.set_train_iter(20000)
for i in range(20000):
    idx = ri(0, train_dat.shape[0]-1)
    hidden1.train(train_dat_p[idx])
    if i % 1000 == 0: print(f"iter {i}")


all = np.zeros((train_dat.shape[0], x * y))
for i in range(train_dat.shape[0]):
    all[i] = hidden1.sample(train_dat_p[i]).reshape([x * y])
    if i % 1000 == 0: print(f"sampled count: {i}")


tall = np.zeros((test_dat_p.shape[0], x * y))
for i in range(test_dat_p.shape[0]):
    tall[i] = hidden1.sample(test_dat_p[i]).reshape([x * y])
    if i % 1000 == 0: print(f"sampled count: {i}")

print(all.shape)
svm = SVC(gamma='scale', kernel='rbf')
svm.fit(all, train_lab)
print(svm.score(tall, test_lab))


pics_2_draw = sp(list(range(10000)), 10)
for i, v in enumerate(pics_2_draw):
    draw_sample(hidden1, train_dat_p[v], train_dat[v], prefix=str(i))

# grid = imgrid(*fmp)
# fig = plt.figure()

# plt.imshow(train_dat[45], vmin=0.0, vmax=1.0, cmap='PuRd')
# plt.axis('off')
# fig.savefig("s.png")

# plt.imshow(samh1, vmin=0.0, vmax=1.0, cmap='PuRd')
# plt.axis('off')
# plt.show()
