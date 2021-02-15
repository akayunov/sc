import cv2 as cv

import numpy as np
img_rgb = cv.imread('resources/probes.jpg')

b,g,r = img_rgb[425,636]
# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.
print(b,g,r)
# for i in range(100):
#     for k in range(100):
#         img_rgb[i,k] = (b,g,r)

# set lower and upper color limits
lower_val = np.array([150,190,200])
upper_val = np.array([210,255,255])
# Threshold the HSV image to get only green colors
mask = cv.inRange(img_rgb, lower_val, upper_val)


gray = cv.cvtColor(img_rgb,cv.COLOR_BGR2GRAY)

only_green = cv.bitwise_and(gray,gray, mask= mask)

cv.imwrite('res.jpg',only_green)