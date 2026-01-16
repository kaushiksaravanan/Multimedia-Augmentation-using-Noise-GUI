import cv2
import cupy as cp
import numpy as np


def speckle(imagelocation, value):
    img = cv2.imread(imagelocation, 0)

    img_gpu = cp.asarray(img, dtype=cp.float32)
    noise = cp.random.normal(loc=1, scale=value, size=img_gpu.shape)
    noisy = cp.clip(img_gpu * noise, 0, 255)

    return cp.asnumpy(noisy).astype(np.uint8)
