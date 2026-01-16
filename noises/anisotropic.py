import cupy as cp
import cv2
import numpy as np


def anisotropic(imagelocation, value):
    img = cv2.imread(imagelocation)
    mean = 0
    stddev = value * 100

    noise = cp.random.normal(mean, stddev, img.shape)
    img_gpu = cp.asarray(img)
    noisy = cp.clip(img_gpu + noise.astype(cp.uint8), 0, 255)

    return cp.asnumpy(noisy).astype(np.uint8)
