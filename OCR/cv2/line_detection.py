import cv2, numpy as np

img = cv2.imread('/Users/hwang7/tmp/simpletest/OCR/irs1099misc.png', cv2.IMREAD_UNCHANGED)
print(img.shape) # 0 - vertical, 1 - horizontal, 2 - BGR colors

a = cv2.adaptiveThreshold()

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

edges = cv2.Canny(im_bw, 50, 150, apertureSize=3)
win_name = 'image_edges'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, edges)

threshold = img.shape[1] // 5
lines = cv2.HoughLines(edges, 1, np.pi/2, threshold)
print(lines.shape)
for i in range(min(lines.shape[0], 5)):
    print(lines[i])

# The below for loop runs till r and theta values
# are in the range of the 2d array
for line in lines:
    for r, theta in line:
        # Stores the value of cos(theta) in a
        a = np.cos(theta)

        # Stores the value of sin(theta) in b
        b = np.sin(theta)

        # x0 stores the value rcos(theta)
        x0 = a * r

        # y0 stores the value rsin(theta)
        y0 = b * r

        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000 * (-b))

        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000 * (a))

        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000 * (-b))

        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000 * (a))

        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
        print('from ({}, {}) to ({}, {})'.format(x1, y1, x2, y2))

# All the changes made in the input image are finally
# written on a new image houghlines.jpg
#cv2.imwrite('linesDetected.jpg', img)
#cv2.circle(img,(0,0), 1044, (0,0,0), -1)

win_name = 'image_4'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, img)

cv2.waitKey(0) & 0xFF # for 64-bit machine
cv2.destroyAllWindows()
