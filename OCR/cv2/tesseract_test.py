import os, sys, numpy as np, pandas as pd, re, datetime as dt, subprocess
from utils import display_cv2_image

import cv2, pytesseract, io

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

show_imgs = True

img_file = os.environ['HOME'] + '/simpletest/OCR/images/checkboxes.png'
img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)

# tesseract cannot deal with slanted images
#img = cv2.imread('/Users/hwang7/tmp/simpletest/OCR/images/1099MISC-slanted.png', cv2.IMREAD_UNCHANGED)

print(img.shape) # 0 - vertical, 1 - horizontal, 2 - BGR colors
if show_imgs:
    display_cv2_image(img, 'Original')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray
dst_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
if show_imgs:
    display_cv2_image(dst_img, 'Gray Thresholded')

#text = pytesseract.image_to_string(dst_img)
#print(text)

text_loc = pytesseract.image_to_data(dst_img, lang='eng', config='--psm 3', nice=0, output_type=pytesseract.Output.STRING)
print(text_loc)
lines = re.split('\n', text_loc)
headers = re.split('\t', lines[0])
print(headers)
cols = ['block_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'text']
#cols = headers
idxs = []
text_idx = headers.index('text')
for col in cols:
    idxs.append(headers.index(col))

rs = []
for line in lines[1:]:
    flds = np.array(re.split('\t', line))
    if len(flds) <= text_idx:
        print('>>> DISCARD:', line)
        continue
    flds[text_idx] = flds[text_idx].strip()
    if len(flds[text_idx]) == 0:
        continue
    rs = np.concatenate((rs, flds[idxs]))
rs = np.reshape(rs, (-1, len(cols)))
df = pd.DataFrame(rs, columns=cols)
for col in cols:
    if col == 'text':
        continue
    df[col] = df[col].astype('int')
df['gap'] = 0 # default to no gap
print(df)

#tmp_file = os.environ['HOME'] + '/tmp/1.csv'
#df.to_csv(tmp_file, index=False)

# calculate word's gap from previous word in same block and same line
last_block = -1
last_line = -1
last_row = None
gaps = []
for i, row in df.iterrows():
    block = row.block_num
    line = row.line_num
    if block == last_block and line == last_line:
        last_row_end = last_row.left + last_row.width
        gap = row.left - last_row_end
        gaps.append(gap)
    else:
        gaps.append(0)

    last_block = block
    last_line = line
    last_row = row

df.gap = gaps
print('------------------'); print(df)
print(df.gap.value_counts().sort_index())

tmp_file = os.environ['HOME'] + '/tmp/2.csv'
df.to_csv(tmp_file, index=False)

if show_imgs:
    cv2.waitKey(0) & 0xFF # for 64-bit machine
    cv2.destroyAllWindows()
