import os, sys, numpy as np, pandas as pd, re
from utils import display_cv2_image

import cv2, pytesseract, io

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

show_imgs = True

img = cv2.imread('/Users/hwang7/tmp/simpletest/OCR/images/irs1099misc.png', cv2.IMREAD_UNCHANGED)
if show_imgs:
    display_cv2_image(img, 'Original')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray
if show_imgs:
    display_cv2_image(gray, 'Gray Thresholded')

dst_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
if show_imgs:
    display_cv2_image(dst_img, 'Gray Thresholded - Adp Thresh')
    kernel = np.ones((5,5), np.uint8)

    # erosion expand black area, so actually thickening the black characters
    erosion = cv2.erode(dst_img, kernel, iterations=1)
    display_cv2_image(erosion, 'Gray Thresholded - Adp Thresh Eroded')

    # dilation expand white area, so thinning the black characters
    kernel = np.ones((2,2), np.uint8)
    dilate = cv2.dilate(dst_img, kernel, iterations=1)
    display_cv2_image(dilate, 'Gray Thresholded - Adp Thresh Dilated')

if show_imgs:
    cv2.waitKey(0) & 0xFF # for 64-bit machine
    cv2.destroyAllWindows()
