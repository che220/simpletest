import cv2, numpy as np

img = cv2.imread('/Users/hwang7/tmp/simpletest/OCR/irs1099misc.png', cv2.IMREAD_UNCHANGED)
print(img.shape) # 0 - vertical, 1 - horizontal, 2 - BGR colors

win_name = 'image_orig'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray
win_name = 'image_gray'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, gray)

(thresh, im_bw) = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
print('threshold:', thresh)
win_name = 'image_bw'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, im_bw)

cv2.waitKey(0) & 0xFF # for 64-bit machine
cv2.destroyAllWindows()
