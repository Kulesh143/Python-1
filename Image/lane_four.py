import cv2
import numpy as np

def canny(image):
    gray=cv2.cvtColor(lane_image,cv2.COLOR_RGB2GRAY)#changes image to gray scale
    blur=cv2.GaussianBlur(gray,(5,5),0)#blurs image using a 5 by 5 kernel and reduces noise
    canny=cv2.Canny(blur,50,150)#image,low threshold,high threshold, a ratio of 1:2 or 1:3 is recommended to get the gradient edges
    return canny

def region_of_interest(image):
    height=image.shape[0]#height of the y axix
    # triangle=np.array([(200,height),(1100,height),(550,250)])#here 200 is the begining of the triangle, and 1100 is the end..
    polygons=np.array([[(200,height),(1100,height),(550,250)]])
    mask=np.zeros_like(image)#will have the same number of pixels as the images as zeros in zero intensity
    cv2.fillPoly(mask,polygons,255)#this will give us a white triangle across the image
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image



image=cv2.imread('test_image.jpg')#reads the image
lane_image=np.copy(image)#copies the image
canny=canny(lane_image)
cropped_image=region_of_interest(canny)
cv2.imshow('result',region_of_interest(cropped_image))#shows gray scale image
cv2.waitKey(0)