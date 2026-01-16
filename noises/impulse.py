import random
import cv2
import cupy as cp


def impulse(imagelocation, value):
    img = cv2.imread(imagelocation, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    row, col = img.shape
    img_gpu = cp.asarray(img)

    num_salt = random.randint(50, 9000 + int(value * 1000))
    y_salt = cp.random.randint(0, row, size=num_salt)
    x_salt = cp.random.randint(0, col, size=num_salt)
    img_gpu[y_salt, x_salt] = 255

    num_pepper = random.randint(0, int(1000 * value))
    if num_pepper > 0:
        y_pepper = cp.random.randint(0, row, size=num_pepper)
        x_pepper = cp.random.randint(0, col, size=num_pepper)
        img_gpu[y_pepper, x_pepper] = 0

    return cp.asnumpy(img_gpu)
