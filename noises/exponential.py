import cv2
import cupy as cp
import numpy as np


def exponential(imagelocation, value):
    image = cv2.imread(imagelocation)
    scale = value * 10

    img_gpu = cp.asarray(image, dtype=cp.float32)
    noise = cp.random.exponential(scale=scale, size=image.shape)
    noisy = cp.clip(img_gpu + noise, 0, 255)

    return cp.asnumpy(noisy).astype(np.uint8)
