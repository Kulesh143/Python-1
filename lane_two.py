import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    gray=cv2.cvtColor(lane_image,cv2.COLOR_RGB2GRAY)#changes image to gray scale
    blur=cv2.GaussianBlur(gray,(5,5),0)#blurs image using a 5 by 5 kernel and reduces noise
    canny=cv2.Canny(blur,50,150)#image,low threshold,high threshold, a ratio of 1:2 or 1:3 is recommended to get the gradient edges
    return canny

image=cv2.imread('test_image.jpg')#reads the image
lane_image=np.copy(image)#copies the image
canny=canny(lane_image)
plt.imshow(canny)#shows canny as matplotlib
plt.show()#shows matplotlib image of the canny image with axises