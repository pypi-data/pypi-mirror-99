# https://www.programmersought.com/article/7671791785/

#https://github.com/opencv/opencv/pull/2392 # should have worked --> check dtype
import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage import data



src = data.coins() #cv2.imread('test27.jpg')
img = src.copy()
gray = data.coins() #cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(
    gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Eliminate noise
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

#
sure_bg = cv2.dilate(opening, kernel, iterations=3)

#
dist_transform = cv2.distanceTransform(opening, 1, 5)
ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

# Get an unknown area
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

#
ret, markers1 = cv2.connectedComponents(sure_fg)

# Make sure the background is 1 is not 0
markers = markers1 + 1

# Unknown area marked as 0
markers[unknown == 255] = 0

markers3 = cv2.watershed(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR), markers)

# img[markers3 == -1] = [0, 0, 255]
# img=markers3

plt.subplot(241), plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB)),
plt.title('Original'), plt.axis('off')
plt.subplot(242), plt.imshow(thresh, cmap='gray'),
plt.title('Threshold'), plt.axis('off')
plt.subplot(243), plt.imshow(sure_bg, cmap='gray'),
plt.title('Dilate'), plt.axis('off')
plt.subplot(244), plt.imshow(dist_transform, cmap='gray'),
plt.title('Dist Transform'), plt.axis('off')
plt.subplot(245), plt.imshow(sure_fg, cmap='gray'),
plt.title('Threshold'), plt.axis('off')
plt.subplot(246), plt.imshow(unknown, cmap='gray'),
plt.title('Unknow'), plt.axis('off')
plt.subplot(247), plt.imshow(np.abs(markers), cmap='jet'),
plt.title('Markers'), plt.axis('off')
# plt.subplot(248), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),
markers3[markers3!=-1]=0
markers3[markers3==-1]=255
plt.subplot(248), plt.imshow(markers3, cmap='gray'),
plt.title('Result'), plt.axis('off')

plt.show()

# not sure it exactly works as I'd like it to though
# pass function and test
