import cv2
import cupy as cp
import numpy as np


def gamma(imagelocation, value):
    image = cv2.imread(imagelocation)
    shape = value * 100
    scale = 1.0

    img_gpu = cp.asarray(image, dtype=cp.float32)
    noise = cp.random.gamma(shape, scale, image.shape)
    noisy = cp.clip(img_gpu + noise, 0, 255)

    return cp.asnumpy(noisy).astype(np.uint8)
