import cv2
import cupy as cp
import numpy as np


def rayleigh(img_path, value):
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None

    scale = value * 100
    img_gpu = cp.asarray(image, dtype=cp.float32)
    noise = cp.random.rayleigh(scale, size=img_gpu.shape)
    noisy = cp.clip(img_gpu + noise, 0, 255)

    return cp.asnumpy(noisy).astype(np.uint8)
