from scipy.ndimage import gaussian_filter

from epyseg.img import Img
from skimage.feature import peak_local_max
from skimage.segmentation import watershed, random_walker
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2 as cv
# import imutils
import numpy as np
from matplotlib import pyplot as plt
from skimage.util import invert


from skimage.measure import label

img = Img('/home/aigouy/Dropbox/tests_rewatershed/AVG_5.png')




# img = cv.imread("image.jpg");
# blur = cv.GaussianBlur(img,(7,7),0)


#color space change
# mSource_Hsv = cv.cvtColor(blur,cv.COLOR_BGR2HSV);
# mMask = cv.inRange(mSource_Hsv,np.array([0,0,0]),np.array([80,255,255]));
# output = cv.bitwise_and(img, img, mask=mMask)

#grayscale
# img_grey = cv.cvtColor(output, cv.COLOR_BGR2GRAY)

#thresholding
# ret,th1 = cv.threshold(img_grey,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)

#dist transform
binarized = np.zeros_like(img)
binarized[img>140] = 255
binarized[img<140] = 0

plt.imshow(binarized)
plt.show()

D = ndimage.distance_transform_edt(invert(binarized)) #,sampling=[2, 1]

# D = gaussian_filter(D, 1)


plt.imshow(D)
plt.show()

labels = label(invert(binarized), connectivity=1)

print(labels.shape, labels.dtype)

plt.imshow(labels)
plt.show()

#markers
localMax = peak_local_max(D, indices=False,  min_distance=10) #labels=labels, #, labels=invert(img) , num_peaks_per_label=1 # , footprint=np.ones((3, 3))
markers = label(localMax, connectivity=2)

plt.imshow(markers)
plt.show()

#apply watershed
labels = watershed(img, markers=markers, watershed_line=True)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

# draw label on the mask
mask = np.zeros(img.shape, dtype="uint8")
mask[labels == 0] = 255

plt.imshow(mask)
plt.show()

# labels_rw = random_walker(img, markers)
# plt.imshow(labels_rw)
# plt.show()

# contours = []
#
# # loop over the unique labels, and append contours to all_cnts
# for label in np.unique(labels):
#     if label == 0:
#         continue
#
#
#
#     # detect contours in the mask and grab the largest one
#     cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#     c = max(cnts, key=cv.contourArea)
#
#     ## Ignore small contours
#     #if c.shape[0] < 20:
#     #    continue
#
#     # Get convex hull of contour - it' going to help when merging contours
#     hull = cv.convexHull(c)
#
#     #cv.drawContours(img, c, -1, (0, 255, 0), 2)
#     cv.drawContours(img, [hull], -1, (0, 255, 0), 2, 1)
#
#     # Append hull to contours list
#     contours.append(hull)
#
#
# # Merge the contours that does not increase the convex hull by much.
# # Note: The solution is kind of "brute force" solution, and can be better.
# ################################################################################
# for i in range(len(contours)):
#     c = contours[i]
#
#     area = cv.contourArea(c)
#
#     # Iterate all contours from i+1 to end of list
#     for j in range(i+1, len(contours)):
#         c2 = contours[j]
#
#         area2 = cv.contourArea(c2)
#
#         area_sum = area + area2
#
#         # Merge contours together
#         tmp = np.vstack((c, c2))
#         merged_c = cv.convexHull(tmp)
#
#         merged_area = cv.contourArea(merged_c)
#
#         # Replace contours c and c2 by the convex hull of merged c and c2, if total area is increased by no more then 10%
#         if merged_area < area_sum*1.1:
#             # Replace contour with merged one.
#             contours[i] = merged_c
#             contours[j] = merged_c
#             c = merged_c
#             area = merged_area
# ################################################################################
#
#
# # Draw new contours in red color
# for c in contours:
#     #Ignore small contours
#     if cv.contourArea(c) > 100:
#         cv.drawContours(img, [c], -1, (0, 0, 255), 2, 1)
#
#
# cv.imshow("segmented",img)
# cv.waitKey(0)
# cv.destroyAllWindows()