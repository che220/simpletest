import os, sys, numpy as np, pandas as pd, re, datetime as dt, subprocess
from utils import display_cv2_image

import cv2, pytesseract, io

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

show_imgs = True

img_file = os.environ['HOME'] + '/simpletest/OCR/images/checkboxes.png'
cmd = ['/usr/local/bin/tesseract', img_file, 'stdout', '--oem', '1', '-l', 'eng', '--psm',  '3', 'tsv']
t0 = dt.datetime.now()
text_loc = subprocess.check_output(cmd).decode('utf-8')
t1 = dt.datetime.now()
print(text_loc)
print(t1 - t0)
exit(0)
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
