import os, sys, numpy as np, pandas as pd, re, datetime as dt, subprocess
from utils import display_cv2_image

import cv2, pytesseract, io

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

def to_dataframe(text_loc):
    '''
    Turn tesseract TSV output into pandas Dataframe, and remove lines without texts

    :param text_loc:
    :return:
    '''
    lines = re.split('\n', text_loc)
    headers = re.split('\t', lines[0])
    print('Headers:', headers)
    text_idx = headers.index('text')
    n_cols = len(headers)

    rs = []
    for line in lines[1:]:
        flds = np.array(re.split('\t', line))
        if len(flds) != n_cols:
            continue

        if len(flds) <= text_idx:
            # these lines have no text. Discard them.
            continue
        flds[text_idx] = flds[text_idx].strip()
        if len(flds[text_idx]) == 0:
            # these lines have empty strings as text. Discard them.
            continue
        rs = np.concatenate((rs, flds))
    rs = np.reshape(rs, (-1, len(headers)))
    df = pd.DataFrame(rs, columns=headers)
    for col in headers:
        if col == 'text':
            continue
        df[col] = df[col].astype('int')
    df['bottom'] = df.top + df.height
    df['right'] = df.left + df.width
    return df

def form_lines(extracted_df):
    """
    Adjacent words form lines. Every element of returned list is [left_top, bottom_right, text]

    :param extracted_df:
    :return: list
    """
    word_1_df = extracted_df[extracted_df.word_num == 1]
    rs = []
    for i, row in enumerate(word_1_df.index):
        end_row = extracted_df.shape[0]
        if i < word_1_df.index.shape[0] - 1:
            end_row = word_1_df.index[i + 1]

        a_df = extracted_df.iloc[row:end_row].copy().reset_index(drop=True)
        a_df['last_right'] = [-10000] + list(a_df.right[0:-1])
        a_df['gap'] = a_df.left - a_df.last_right

        # use the longest word to figure out the width of 2 letters. That will be max gap allowed between words
        # Otherwise break up line into multiple lines
        max_text_row = a_df[a_df.width == a_df.width.max()].iloc[0, :]
        two_letter_width = max_text_row['width'] // len(max_text_row['text']) * 2
        a_df.loc[a_df.gap > two_letter_width, 'word_num'] = 1 # set multiple 1s to indicate multiple lines
        #print(a_df)
        #print('max allowed gap:', max_word_gap)

        if a_df[a_df.word_num == 1].shape[0] > 1:
            sub_rs = form_lines(a_df)
            rs += sub_rs
        else:
            # Box: top, left, bottom, right
            left_top = (a_df.left.min(), a_df.top.min())
            right_bott = (a_df.right.max(), a_df.bottom.max())
            text = ' '.join(a_df.text)
            rs.append([left_top, right_bott, text])
        #print('texts:', rs)
    return rs

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

show_imgs = True

img_file = os.environ['HOME'] + '/simpletest/OCR/images/checkboxes.png'
cmd = ['/usr/local/bin/tesseract', img_file, 'stdout', '--oem', '1', '-l', 'eng', '--psm',  '3', 'tsv']
t0 = dt.datetime.now()
text_loc = subprocess.check_output(cmd).decode('utf-8')
t1 = dt.datetime.now()
print('OCR:', t1 - t0)
df = to_dataframe(text_loc)
lines = form_lines(df)
t1 = dt.datetime.now()
print('OCR+post processing:', t1 - t0)

img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
display_cv2_image(img, 'Original')

t0 = dt.datetime.now()
_, squares = find_squares(img)
t1 = dt.datetime.now()
print('find squares:', t1 - t0)
#cv2.drawContours(img, squares, -1, (0, 255, 0), 3)
sqs = []
for sq in squares:
    left_top = tuple(sq.min(axis=0))
    right_bott = tuple(sq.max(axis=0))
    #cv2.rectangle(img, left_top, right_bott, (0, 255, 0), 2)
    sqs.append([left_top, right_bott])
t1 = dt.datetime.now()
print('find squares+post processing:', t1 - t0)

# text line segmentations are boxed in red
for line in lines:
    cv2.rectangle(img, line[0], line[1], (0, 0, 255), 2)

# all squares are boxed in green
for sq in sqs:
    cv2.rectangle(img, sq[0], sq[1], (0, 255, 0), 2)

display_cv2_image(img, 'Text & Checkbox')
print('displayed')
cv2.waitKey(0) & 0xFF # for 64-bit machine
cv2.destroyAllWindows()
