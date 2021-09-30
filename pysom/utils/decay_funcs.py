import numpy as np


def exp_decay(t, val_max, val_min, val_step):
    return max(val_max * np.exp(- t * val_step), val_min)


def linear_step(t, val_max, val_min, val_step):
    return max(val_max - t * val_step, val_min)