from PIL import Image, ImageTk
import cv2

def display_cv2_image(img, title):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, img)

def image_cv_to_tk(cv_img):
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    return ImageTk.PhotoImage(img)
