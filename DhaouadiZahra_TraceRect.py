#Dhaouadi Zohra Trace rectangle Recognition, simple version
#zohra.dhaouadi@esprit.tn
#Verion 3.7.1 latest version
#The Python Standard Library
#OpenCV library 3.4.1

#Biblio declaration
#System-specific parameters and functions package
import sys
#PY3 for the third version of python info
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range
#import OpenCV module for binding and array conversion
import cv2 as cv
#Numpy is a optimized library for fast array calculations
#Numpy provides a large set of numeric datatypes
#used to construct arrays.
#np is to rename the numerical python package 
import numpy as np

#Angle definition 
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )
#Square detection
def find_squares(img):
#Smoothing Images
#Blur the images with various low pass filters
    img = cv.GaussianBlur(img, (5, 5), 0)
	#List declaration
    squares = []
	#Loop 
	#Split to access pixel values and modify them to set the region of the image tp ROI
    for gray in cv.split(img):
	#Python 3’s range is more powerful than Python 2’s xrange with a start,stop and step scales
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
			#Canny Edge Detection
                binary = cv.Canny(gray, 0, 50, apertureSize=5)
				#Apply morphology operators just like Dilation and Erosion.
                binary = cv.dilate(binary, None)
            else:
                _retval, binary = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            binary, contours, _hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 100 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares


caption = cv.VideoCapture(0)

while(1):

#Display Frame
    _,frame = caption.read()
#Call for find_squares function
    squares = find_squares(frame)

    cv.imshow('frame',frame)
	#Contour trace
    cv.drawContours( frame, squares, -1, (0, 255, 0), 3 )
    cv.imshow('squares', frame)

    
#Wait to quite
    if cv.waitKey(33)== 27:
        break

# Clean up everything before leaving
cv.destroyAllWindows()
caption.release()
