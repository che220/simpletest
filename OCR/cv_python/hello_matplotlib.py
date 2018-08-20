import os, sys, cv2, numpy as np
import matplotlib.pyplot as plt

home = os.environ['HOME']
img_file = home + '/Pictures/2017-04-06_23-05-22_000.jpeg'
img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)

b,g,r = cv2.split(img) # openCV2 uses BGR order
img2 = cv2.merge([r,g,b]) # Matplotlib uses RGB order

# same thing, but faster
img2 = img[:,:,::-1]

# or
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(type(img2), img2.shape)
plt.imshow(img2, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()