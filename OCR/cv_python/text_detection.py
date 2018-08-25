import os, sys, numpy as np, pandas as pd, re
from utils import display_cv2_image

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

import cv2

show_imgs = True

img = cv2.imread('/Users/hwang7/tmp/simpletest/OCR/images/irs1099misc.png', cv2.IMREAD_UNCHANGED)

# tesseract cannot deal with slanted images
#img = cv2.imread('/Users/hwang7/tmp/simpletest/OCR/images/1099MISC-slanted.png', cv2.IMREAD_UNCHANGED)

print(img.shape) # 0 - vertical, 1 - horizontal, 2 - BGR colors
if show_imgs:
    display_cv2_image(img, 'Original')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray
dst_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
if show_imgs:
    display_cv2_image(dst_img, 'Gray Thresholded')
