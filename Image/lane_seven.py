import cv2
import numpy as np

def make_coordinates(image,line_parameters):
    slope,intercept=line_parameters
    print(image.shape)
    y1=image.shape[0]
    y2=int(y1*(3/5))
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])


def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)
        print(parameters)
        slope=parameters[0]
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average=np.average(left_fit,axis=0)
    right_fit_average=np.average(right_fit,axis=0)
    # print(left_fit_average,'left')
    # print(right_fit_average,'right')
    left_line=make_coordinates(image,left_fit_average)
    right_line=make_coordinates(image,right_fit_average)
    return np.array([left_line,right_line])
        # print(left_fit)
        # print(right_fit)
    

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
averaged_lines=average_slope_intercept(lane_image,lines)
line_image=display_lines(lane_image,averaged_lines)
combo_image=cv2.addWeighted(lane_image,0.8,line_image,1,1)# weight of 0.8 decrease pixel intensity, 1 for line _image,the last 1 is the gamma value
# cv2.imshow("result",combo_image)
# cv2.imshow('result',region_of_interest(cropped_image))#shows gray scale image
# cv2.waitKey(0)
cap=cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _, frame=cap.read()
    canny_image=canny(frame)
    cropped_image=region_of_interest(canny_image)
    lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)#100 is the minimum accpetd threshold,
#THIS IS AN ALGORITHM TO DETECT CROPPED LINES IN  AN IMAGE
# line_image=display_lines(lane_image,lines)
    averaged_lines=average_slope_intercept(frame,lines)
    line_image=display_lines(frame,averaged_lines)
    combo_image=cv2.addWeighted(frame,0.8,line_image,1,1)# weight of 0.8 decrease pixel intensity, 1 for line _image,the last 1 is the gamma value
    cv2.imshow("result",combo_image)
# cv2.imshow('result',region_of_interest(cropped_image))#shows gray scale image
    if cv2.waitKey(1)&0xFF== ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
    
