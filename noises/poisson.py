import cv2
import cupy as cp
import numpy as np


def poisson(imagelocation, value):
    image = cv2.imread(imagelocation)
    peak = 1 - value

    img_gpu = cp.asarray(image, dtype=cp.float32)
    noise = cp.random.poisson(img_gpu / 255.0 * peak) / peak * 255

    return cp.asnumpy(noise).astype(np.uint8)
