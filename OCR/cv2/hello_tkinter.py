import os, sys, cv2, numpy as np
from tkinter import *
from utils import image_cv_to_tk

home = os.environ['HOME']
img_file = home + '/Pictures/2017-04-06_23-05-22_000.jpeg'
cv_img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

root = Tk()
img = image_cv_to_tk(cv_img)

if True:
    panelA = Label(root, image=img)
    panelA.image = img
    panelA.pack(side='left', padx=10, pady=10)
else:
    canvas = Canvas(root, width=cv_img.shape[1], height=cv_img.shape[0])
    canvas.pack(side='left')
    canvas.create_image(0, 0, anchor=NW, image=img)

mainloop()
