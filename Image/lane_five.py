import cv2
import numpy as np

def canny(image):
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)#changes image to gray scale
    blur=cv2.GaussianBlur(gray,(5,5),0)#blurs image using a 5 by 5 kernel and reduces noise
    canny=cv2.Canny(blur,50,150)#image,low threshold,high threshold, a ratio of 1:2 or 1:3 is recommended to get the gradient edges
    return canny

def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            # print(line)
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image

        



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
canny_image=canny(lane_image)
cropped_image=region_of_interest(canny_image)
lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)#100 is the minimum accpetd threshold,
#THIS IS AN ALGORITHM TO DETECT CROPPED LINES IN  AN IMAGE
# line_image=display_lines(lane_image,lines)
line_image=display_lines(lane_image,lines)
combo_image=cv2.addWeighted(lane_image,0.8,line_image,1,1)# weight of 0.8 decrease pixel intensity, 1 for line _image,the last 1 is the gamma value
cv2.imshow("result",line_image)
# cv2.imshow('result',region_of_interest(cropped_image))#shows gray scale image
cv2.waitKey(0)