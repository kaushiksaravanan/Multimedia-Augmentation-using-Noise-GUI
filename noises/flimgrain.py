import cv2
import cupy as cp
import numpy as np


def flimgrain(imagelocation, value):
    img = cv2.imread(imagelocation)
    scale = round(value / 10, 2)

    img_gpu = cp.asarray(img, dtype=cp.float32)
    noise = cp.random.normal(loc=0, scale=scale, size=img_gpu.shape)
    noisy = cp.clip(img_gpu + noise * 255, 0, 255)

    return cp.asnumpy(noisy).astype(np.uint8)
