import os, sys, numpy as np, time, cv2, pytesseract, io
from imutils.object_detection import non_max_suppression

project_path = '/Users/huiwang/Google Drive/Job/Machine Learning/CV/opencv-text-detection'
model_path = project_path + '/frozen_east_text_detection.pb'
print("[INFO] loading EAST text detector...")
net = cv2.dnn.readNet(model_path)
print('loaded model from', model_path)

all_angles = []
def detect(image, min_confidence=0.5, get_text=False):
    orig = image.copy()
    (H, W) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    newW = (W // 32 + 1) * 32
    newH = (H // 32 + 1) * 32
    print('original H and W:', (H, W))
    print('new H and W:', (newH, newW))

    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()

    # show timing information on text prediction
    print("[INFO] text detection took {:.6f} seconds".format(end - start))

    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < min_confidence:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            all_angles.append(angle)

            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

        if get_text:
            rec_img = orig[startY : endY, startX : endX, :]
            text = pytesseract.image_to_string(rec_img, lang='eng', config='--psm 3', nice=0,
                                                 output_type=pytesseract.Output.STRING)
            print('>>>', text)

    return orig

def show(image, win_title, loc=0):
    cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_title, image.shape[1], image.shape[0])
    cv2.moveWindow(win_title, loc, loc)
    cv2.imshow(win_title, image)

def detect_and_show(image, win_title, loc=0, get_text=False):
    image = detect(image, get_text=get_text)
    show(image, win_title, loc)

image_dir = project_path + '/images'

# load the input image and grab the image dimensions
image_path = image_dir+ '/car_wash.png'
image_path = '/Users/huiwang/simpletest/OCR/images/irs1099misc.png'
irs1099_path = project_path + '/irs1099'
image_path = irs1099_path + '/1099-partial-slanted.png'

image = cv2.imread(image_path)
print(image.shape)
print('loaded image from', image_path)
#image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
detect_and_show(image, 'Orig')

'''
1. scale the angles from 0.0 to float(buckets)
2. counts in each 1.0 bins
3. pick the bins with top 5 counts. select all angles in this range
4. use mean angle to rotate image
'''
buckets = 100
angles = np.array(all_angles, dtype=np.float32)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
norm_angles = (scaler.fit_transform(angles.reshape(-1,1)) * buckets)[:, 0]
cnts = np.bincount(norm_angles.astype(np.int64))

top_n = 5
idxs = np.argsort(cnts)
top_idxs = idxs[(idxs.shape[0]-top_n):]

# get range of index of the top 5 so we can include all those in between
angles = norm_angles[(norm_angles >= top_idxs.min()) & (norm_angles < top_idxs.max()+1.0)]
angles = angles / buckets * scaler.data_range_ + scaler.data_min_
angle = np.mean(angles)

if True:
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -angle/np.pi*180, 1)
    dst = cv2.warpAffine(image, M, (cols, rows))
    detect_and_show(dst, 'Rotated', get_text=True)

if False:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray image is 2D. Make a 3D image data
    image = np.repeat(image[:, :, np.newaxis], 3, axis=2)
    print(image.shape)
    detect_and_show(image, 'Gray', 50)

# blurring reduces the performance of text detection dramatically!!!
if False:
    image = cv2.GaussianBlur(image,(5,5),0)
    detect_and_show(image, 'Gray Blur', 100)

cv2.waitKey(0)