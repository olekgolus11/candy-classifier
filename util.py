import numpy as np
import cv2
from Colors import Colors as CLR

def get_limits(color, colorName):

    if(colorName == CLR.RED.name):
        lowerLimitBGR = np.array([0, 0, 200])
        upperLimitBGR = np.array([10, 10, 255])
    elif(colorName == CLR.PINK.name):
        lowerLimitBGR = np.array([160, 50, 50])
        upperLimitBGR = np.array([180, 255, 255])
    elif(colorName == CLR.ORANGE.name):
        lowerLimitBGR = np.array([11, 100, 100])
        upperLimitBGR = np.array([25, 255, 255])
    else:
        lowerLimitBGR = np.array([0, 0, 120])
        upperLimitBGR = np.array([70, 255, 200])

    return lowerLimitBGR, upperLimitBGR
