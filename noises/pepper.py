import cv2
import cupy as cp
import numpy as np


def pepper(img_path, value):
    img = cv2.imread(img_path)
    height, width, _ = img.shape
    img_gpu = cp.asarray(img)

    num_salt = int(height * width * value)
    if num_salt > 0:
        y = cp.random.randint(0, height, size=num_salt)
        x = cp.random.randint(0, width, size=num_salt)
        img_gpu[y, x] = cp.array([255, 255, 255])

    num_pepper = int(height * width * value)
    if num_pepper > 0:
        y = cp.random.randint(0, height, size=num_pepper)
        x = cp.random.randint(0, width, size=num_pepper)
        img_gpu[y, x] = cp.array([0, 0, 0])

    return cp.asnumpy(img_gpu)
