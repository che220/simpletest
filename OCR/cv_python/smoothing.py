import os, sys, numpy as np, pandas as pd, re
from utils import display_cv2_image
import cv2

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

show_imgs = True

img = cv2.imread('/Users/hwang7/tmp/simpletest/OCR/images/smeared_opencv_image.jpg', cv2.IMREAD_UNCHANGED)
print(img.shape) # 0 - vertical, 1 - horizontal, 2 - BGR colors
print(img[0:5, 0:5, :])
if show_imgs:
    display_cv2_image(img, 'Original')
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    display_cv2_image(edges, 'Original Edge')

blur = cv2.blur(img, (5,5))
if show_imgs:
    display_cv2_image(blur, 'Average Blur')

blur = cv2.GaussianBlur(img,(5,5),0)
if show_imgs:
    display_cv2_image(blur, 'Gaussian Blur')

blur = cv2.medianBlur(img, 5)
if show_imgs:
    display_cv2_image(blur, 'Median Blur')

for sigma in range(75, 100, 50):
    blur = cv2.bilateralFilter(img, 9, sigma, sigma)
    if show_imgs:
        display_cv2_image(blur, 'Bilateral Blur sigma={}'.format(sigma))
        edges = cv2.Canny(blur, 50, 150, apertureSize=3)
        display_cv2_image(edges, 'Bilateral Blur Edge sigma={}'.format(sigma))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray
dst_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
if show_imgs:
    display_cv2_image(dst_img, 'Gray Thresholded')


if show_imgs:
    cv2.waitKey(0) & 0xFF # for 64-bit machine
    cv2.destroyAllWindows()
