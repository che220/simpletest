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

kernel = np.ones((2,2),np.float32)/4
blur_bw = cv2.filter2D(im_bw,-1,kernel)
win_name = 'image_bw_blur'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, blur_bw)

edges = cv2.Canny(im_bw, 150, 150, apertureSize=3)
win_name = 'image_edges'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, edges)

kernel = np.ones((3,3),np.float32)/9
blur_edges = cv2.filter2D(edges,-1,kernel)
win_name = 'image_edges_blur'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, blur_edges)

edges = cv2.Canny(blur_edges, 150, 150, apertureSize=3)
win_name = 'image_edges_2'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, edges)

threshold = img.shape[0] // 10
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, np.array([]), minLineLength=100, maxLineGap=5)
print(lines.shape)
for i in range(min(lines.shape[0], 5)):
    print(lines[i])

# The below for loop runs till r and theta values
# are in the range of the 2d array
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
        print('from ({}, {}) to ({}, {})'.format(x1, y1, x2, y2))

win_name = 'image_4'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, img)

cv2.waitKey(0) & 0xFF # for 64-bit machine
cv2.destroyAllWindows()
