import os, sys, cv2, numpy as np, time

print('optimized:', cv2.useOptimized())
home = os.environ['HOME']
img1 = cv2.imread(home + '/Pictures/2017-04-06_23-05-22_000.jpeg', cv2.IMREAD_UNCHANGED)

t0 = time.time()
res = cv2.medianBlur(img1,49)
t1 = time.time()
print('spend:', t1-t0)

img2 = cv2.imread(home + '/Pictures/2017-04-06_23-05-33_000.jpeg', cv2.IMREAD_UNCHANGED)

cv2.setUseOptimized(False)
print('optimized:', cv2.useOptimized())
t0 = time.time()
res = cv2.medianBlur(img2,49)
t1 = time.time()
print('spend:', t1-t0)

img3 = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

# display image
win_name = 'image_0'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, img3)

k = cv2.waitKey(0) & 0xFF # for 64-bit machine
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite(home + '/tmp/1.png',img)
    cv2.destroyAllWindows()

#cv2.waitKey(0) # wait for any keyboard event
#cv2.destroyAllWindows()