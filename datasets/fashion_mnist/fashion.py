from mnist import MNIST
import numpy as np
from random import sample as sp


mndata = MNIST('./large_bin')
images, labels = mndata.load_training()

images = np.array(images, dtype=np.float64) / 255.0
images = images.reshape((images.shape[0], 28, 28))


def imgrid(imgs, w, h):

    row = np.concatenate(imgs[:w])
    imgs = imgs[w:]

    for r in range(1, h):
        cr = np.concatenate(imgs[:w])
        imgs = imgs[w:]
        row = np.concatenate((row, cr), axis=1)

    return row


W = 50
H = 50
grid = imgrid(images[list(sp(list(range(images.shape[0])), W * H))], W, H, 28, 28)


import matplotlib.pyplot as plt
fig = plt.figure()
plt.imshow(grid, vmin=0.0, vmax=1.0, cmap='PuRd')
plt.axis('off')
fig.savefig('fashion.png', dpi=300, bbox_inches='tight')