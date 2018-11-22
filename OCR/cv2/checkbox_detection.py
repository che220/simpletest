import cv2, numpy as np, pytesseract
from utils import display_cv2_image

def getBWImage(img):
    (thresh, img_bw) = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
    print('threshold:', thresh)
    #img_bw = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return img_bw

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 100 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return img, squares

img = cv2.imread('/Volumes/toshiba/simpletest/OCR/images/checkboxes.png', cv2.IMREAD_UNCHANGED)
print(img.shape) # 0 - vertical, 1 - horizontal, 2 - BGR colors
img = img[:, :, 0:3]
print(img.shape) # 0 - vertical, 1 - horizontal, 2 - BGR colors
display_cv2_image(img, 'image_orig')

new_img, squares = find_squares(img)
print(squares)
cv2.drawContours(new_img, squares, -1, (0, 255, 0), 3)
display_cv2_image(new_img, 'squares')

#img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray
#display_cv2_image(img_gray, 'image_gray')
#img_bw = getBWImage(img_gray)
#display_cv2_image(img_bw, 'image_bw')

cv2.waitKey(0) & 0xFF # for 64-bit machine
cv2.destroyAllWindows()
