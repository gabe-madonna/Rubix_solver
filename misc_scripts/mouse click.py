# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:09:49 2017

@author: Gabe Madonna
"""

import cv2
import numpy as np

# mouse callback function
def get_pos(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("(x, y):", (x, y))

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',get_pos)

while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()