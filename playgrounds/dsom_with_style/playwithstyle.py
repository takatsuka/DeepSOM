import numpy as np
from numba import jit
from numbasom import simplesom as som
import matplotlib.pyplot as plt

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

train_dat = np.array(train_dat, dtype=np.float64).reshape((len(train_dat), 28, 28)) / 255.0
test_dat = np.array(test_dat, dtype=np.float64).reshape((len(test_dat), 28, 28)) / 255.0

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



grid = imgrid(*fast_mini_patch(train_dat[2]))
fig = plt.figure()

plt.imshow(train_dat[2], vmin=0.0, vmax=1.0, cmap='PuRd')
plt.axis('off')
fig.savefig("s.png")

plt.imshow(grid, vmin=0.0, vmax=1.0, cmap='PuRd')
plt.axis('off')
plt.show()
