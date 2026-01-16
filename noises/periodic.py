import cv2
import cupy as cp
import numpy as np


def periodic(imagelocation, value):
    img = cv2.imread(imagelocation, 0)
    h, w = img.shape
    noise_freq = 0.05

    img_gpu = cp.asarray(img, dtype=cp.float32)
    y, x = cp.ogrid[0:h, 0:w]

    noise = cp.sin(2 * cp.pi * noise_freq * x + cp.pi * noise_freq * y)
    noise = cp.clip(noise, -1, 1) * value

    noisy = cp.clip(img_gpu + noise * 255, 0, 255)
    return cp.asnumpy(noisy).astype(np.uint8)
