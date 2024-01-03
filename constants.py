import numpy as np

RED_VALUE = (np.array([0, 50, 100]), np.array([10, 200, 255]))
PINK_VALUE = (np.array([160, 50, 50]), np.array([180, 255, 255]))
ORANGE_VALUE = (np.array([11, 100, 100]), np.array([25, 255, 255]))
GREEN_VALUE = (np.array([30, 80, 50]), np.array([60, 255, 255]))

import cv2
import numpy as np

def get_hex_from_opencv_hsv(tab):
    [h,s,v] = tab
    as_rgb = cv2.cvtColor(np.uint8([[[h,s,v]]]), cv2.COLOR_HSV2RGB)
    as_hex = '#%02x%02x%02x' % tuple(as_rgb[0][0])
    return as_hex

print('Red')
print(get_hex_from_opencv_hsv(RED_VALUE[0]))
print(get_hex_from_opencv_hsv(RED_VALUE[1]))

print('Pink')
print(get_hex_from_opencv_hsv(PINK_VALUE[0]))
print(get_hex_from_opencv_hsv(PINK_VALUE[1]))

print('Orange')
print(get_hex_from_opencv_hsv(ORANGE_VALUE[0]))
print(get_hex_from_opencv_hsv(ORANGE_VALUE[1]))

print('Green')
print(get_hex_from_opencv_hsv(GREEN_VALUE[0]))
print(get_hex_from_opencv_hsv(GREEN_VALUE[1]))

RED_KEY = "Red"
PINK_KEY = "Pink"
ORANGE_KEY = "Orange"
GREEN_KEY = "Green"

INFO_COLOR = (0, 255, 0)

MIN_CONTOUR_AREA = 30000

Y_THRESHOLD = 40
X_THRESHOLD = 15

LINE_THICKNESS = 2
TEXT_THICKNESS = 3