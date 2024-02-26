import cv2
import numpy as np

image=cv2.imread('test_image.jpg')#reads the image
lane_image=np.copy(image)#copies the image
gray=cv2.cvtColor(lane_image,cv2.COLOR_RGB2GRAY)#changes image to gray scale
cv2.imshow('result',image)#shows true image
blur=cv2.GaussianBlur(gray,(5,5),0)#blurs image using a 5 by 5 kernel and reduces noise
canny=cv2.Canny(blur,50,150)#image,low threshold,high threshold, a ratio of 1:2 or 1:3 is recommended to get the gradient edges
cv2.imshow('result',canny)#shows gray scale image
cv2.waitKey(0)
