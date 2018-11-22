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

# threshold = 180 was chosen to preserve checkboxes
(thresh, im_bw) = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
print('threshold:', thresh)
win_name = 'image_bw'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, im_bw)

dst = cv2.cornerHarris(gray, 2, 3, 0.04)
print(dst.shape)
print(np.count_nonzero(dst))
print(np.unique(dst, return_counts=True))
dst = cv2.dilate(dst, None)
print(dst.shape)
print(np.count_nonzero(dst))
a = np.unique(dst, return_counts=True)
print(a)
print(np.unique(a[1], return_counts=True))

img[dst>0.05*dst.max()]=[0,0,0,0]

win_name = 'image_4'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, img)

cv2.waitKey(0) & 0xFF # for 64-bit machine
cv2.destroyAllWindows()
