# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:00:21 2017

@author: Gabe Madonna
"""

import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)
color = []

def nothing(x):
    pass

def get_pos(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("(x, y):", (x, y))
        print("av pixel:")
        print("av pixel:", get_av_pixel(blur, (y, x), radius = 20, num = 5))

def get_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[y][x])

def get_color_values(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        color.append(list(cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)[y][x]))

# Create a black image, a window
img = np.zeros((200,512,3), np.uint8)
cv2.namedWindow('image')
cv2.namedWindow('frame')
cv2.namedWindow('blur')
cv2.setMouseCallback('blur',get_pos)

# create trackbars for color change
cv2.createTrackbar('Hue Upper','image',0,255,nothing)
cv2.createTrackbar('Sat Upper','image',0,255,nothing)
cv2.createTrackbar('Val Upper','image',0,255,nothing)
cv2.createTrackbar('Hue Lower','image',0,255,nothing)
cv2.createTrackbar('Sat Lower','image',0,255,nothing)
cv2.createTrackbar('Val Lower','image',0,255,nothing)

while(1):
    
    _, frame = cap.read()
    blur = cv2.blur(frame,(15,15))
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # get current positions of four trackbars
    hu = cv2.getTrackbarPos('Hue Upper','image')
    su = cv2.getTrackbarPos('Sat Upper','image')
    vu = cv2.getTrackbarPos('Val Upper','image')
    hl = cv2.getTrackbarPos('Hue Lower','image')
    sl = cv2.getTrackbarPos('Sat Lower','image')
    vl = cv2.getTrackbarPos('Val Lower','image')

    lower = np.array([hl,sl,vl])
    upper = np.array([hu,su,vu])
    
    s1 = int(1/3 * len(img))
    s2 = int(2/3 * len(img))
    img[:s1] = [hl,sl,vl]
    img[s1:s2] = [(hl + hu) // 2,(sl + su) // 2,(vl + vu) // 2]
    img[s2:] = [hu,su,vu]
    img[:s1] = cv2.cvtColor(img[:s1], cv2.COLOR_HSV2BGR)
    img[s1:s2] = cv2.cvtColor(img[s1:s2], cv2.COLOR_HSV2BGR)
    img[s2:] = cv2.cvtColor(img[s2:], cv2.COLOR_HSV2BGR)   
    
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame,frame, mask = mask)

    cv2.imshow('image', img)
#    cv2.imshow('frame',frame)
    cv2.imshow('blur', blur)
#    cv2.imshow('mask',mask)
#    cv2.imshow('res',res)
    
    px = hsv[len(blur) // 2,len(blur[0]) // 2]
#    print(px[0] >= sl and px[0] >= su, px[1] >= hl and px[1] >= hu, px[2] >= vl and px[2] >= vu)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

print(color)
cv2.destroyAllWindows()
cap.release()



def get_av_pixel(image, center, radius, num):
    '''
    make array of pixels at center that is radius wide 
    and has num pixels to a side
    throw out highest and lowest value, 
    average remaining values,
    return averaged pixel
    
    img: frame
    center: 2d list (y, x)
    radius: int
    num: int
    
    returns pxls_av
    '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#    pxls = pd.DataFrame({'h': 0, 's': 0, 'v': 0}, index = [1])
    pxls = []
    for y in range(-num, num + 1):
        for x in range(-num, num + 1):
            x_coord = int(center[1] + x * radius / num)
            y_coord = int(center[0] + y * radius / num)
            pxl = image[y_coord][x_coord]
            print(pxl)
            print({'h': pxl[0], 's': pxl[1], 'v': pxl[2]})
            pxls.append({'h': pxl[0], 's': pxl[1], 'v': pxl[2]})
    pxls = pd.DataFrame(pxls)
    return list(pxls.apply(np.mean))