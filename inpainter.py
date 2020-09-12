import cv2
import numpy as np

def inpaint(image, mask, method=None, radius=3):

    flags = cv2.INPAINT_TELEA
    if method == "ns":
        flags = cv2.INPAINT_NS

    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)


    # perform inpainting using OpenCV
    output = cv2.inpaint(image, mask, radius, flags=flags)
    return output