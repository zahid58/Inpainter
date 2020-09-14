import cv2
import numpy as np

def inpaint(image, mask, method="telea", radius=3):

    flags = cv2.INPAINT_NS
    if method == "telea":
        flags = cv2.INPAINT_TELEA
    print(method)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # perform inpainting using OpenCV
    output = cv2.inpaint(image, mask, radius, flags=flags)
    return output