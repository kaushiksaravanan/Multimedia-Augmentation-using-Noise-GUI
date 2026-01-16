import cv2
import cupy as cp


def gaussian(imagelocation, value):
    image = cv2.imread(imagelocation)
    peak = 1 - value
    image_gpu = cp.asarray(image)
    noise = cp.random.normal(image_gpu / 30 * peak) / peak * 100
    return cp.asnumpy(noise)
