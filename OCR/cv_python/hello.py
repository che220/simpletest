import os, sys, cv2, numpy as np

home = os.environ['HOME']
img_file = home + '/Pictures/2017-04-06_23-05-22_000.jpeg'
img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)

# display image
win_name = 'image_0'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, img)

# display RGB components of the image
# Note openCV is BGR
for i in range(3):
    win_name = 'image_{}'.format(i)
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    img2 = np.matrix.copy(img[0:1000, 0:1000])
    for j in range(3):
        if j != i:
            img2[:, :, j] = 0
    cv2.imshow(win_name, img2)

k = cv2.waitKey(0) & 0xFF # for 64-bit machine
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite(home + '/tmp/1.png',img)
    cv2.destroyAllWindows()

#cv2.waitKey(0) # wait for any keyboard event
#cv2.destroyAllWindows()