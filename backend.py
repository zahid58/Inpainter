import cv2
import numpy as np

def inpaint_cv2(image, mask, method="telea", radius=3):

    flags = cv2.INPAINT_NS
    if method == "telea":
        flags = cv2.INPAINT_TELEA
    print(method)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # perform inpainting using OpenCV
    output = cv2.inpaint(image, mask, radius, flags=flags)
    return output




def inpaint_deepfill(image, mask):
    # call your custom algorithm for inpainting here 
    # and pass your image and mask to your algorithm
    # return your output image with format numpy ndarray
    # for now just returning the input image
    print("deepfill")
    return image    