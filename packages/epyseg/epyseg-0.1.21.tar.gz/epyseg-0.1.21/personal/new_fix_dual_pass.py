# is there a bug somewhere ?
# bug ???

# should I rerun the wshed to better compare both --> in this way that would be exactly the same bonds and seeds --> maybe best stuff TODO



# this is a test of the dual pass
# do the classical stuff at two scales and get the masks normally, check that if there are size parameters they are scaled down in the sclaed image --> such as palin size for example --> see how to automate that
# get list of processed files
from epyseg.img import Img
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.segmentation import watershed
from skimage.measure import regionprops
from skimage.measure import label
from skimage import measure
from skimage.transform import rescale, resize, downscale_local_mean
import numpy as np
import scipy

s = ndimage.generate_binary_structure(2, 1)

# full_scale_mask = Img('/home/aigouy/Bureau/trash/test_dezoomed/predict/refined_predictions/cellpose_img22.tif')
# downscaled_mask = Img('/home/aigouy/Bureau/trash/test_dezoomed/predict/refined_predictions/cellpose_img22-1.tif')
full_scale_mask = Img('/home/aigouy/Bureau/trash/test_dezoomed/predict/refined_predictions/100708_png06.tif')
downscaled_mask = Img('/home/aigouy/Bureau/trash/test_dezoomed/predict/refined_predictions/100708_png06-1_bilinear.tif')

# get differing bonds then score them with respect to original and get rid of stuff
# need reapplys same scale to both --> how do I do that
# dilate orig mask then downscale it
# then upscale


# image_rescaled = rescale(image, 0.25, anti_aliasing=False)
# image_resized = resize(image, (image.shape[0] // 4, image.shape[1] // 4), anti_aliasing=True)


# full_scale_mask = rescale(full_scale_mask, 0.5, anti_aliasing=False)
full_scale_mask = resize(full_scale_mask, (full_scale_mask.shape[-2] // 2, full_scale_mask.shape[-1] // 2), anti_aliasing=False)
# plt.imshow(full_scale_mask, cmap='gray')
# plt.show()

full_scale_mask[full_scale_mask != 0] = 255
# plt.imshow(full_scale_mask, cmap='gray')
# plt.show()


# now we compare both ways...

# way 1


# do the comparison both ways and score to see ideally need split by vertices to avoid issues
# but then if ok try to rescue also the vertices back
# TODO --> just try it

# now dilate and compare to other mask and restore bonds when ok
# get real original bond from vertices and score them

# comparison = ndimage.grey_dilation(full_scale_mask, footprint=s)
comparison = full_scale_mask
# plt.imshow(comparison, cmap='gray')
# plt.show()



# need detect vertices on non dilated
# pb is comparison sucks can I invert
# kernel = np.ones((3, 3))
# vertices1 = scipy.signal.convolve2d(downscaled_mask, kernel, mode='same', fillvalue=1)
# result = np.zeros_like(vertices1)
# # result[np.logical_and(mask >= 1020, output == 255)] = 255
# result[np.logical_and(vertices1 >= 1020, downscaled_mask == 255)] = 255
# # result[vertices1 >= 1020] = 255
# plt.imshow(result, cmap='gray')
# plt.show()

# no in fact just dilate one not the two
comparison2 = ndimage.grey_dilation(downscaled_mask, footprint=s)
# comparison2 = downscaled_mask #ndimage.grey_dilation(downscaled_mask, footprint=s)
# plt.imshow(comparison2, cmap='gray')
# plt.show()

# seems to work --> perform scoring to decide if keep bond or not and it keep then add to orig or if remove then


# TODO check if bidirectional or make it that way
not_img = np.logical_not(comparison2 == comparison, comparison2 != comparison)
# not_img = not_img[not_img==True and labels==255]
not_img[comparison != 255] = 0
# not_img[not_img!=0]=255
# not_img[result!=0]=0# remove vertices --> sucks in fact
plt.imshow(not_img, cmap='gray')
plt.show()

# way 2
comparison = ndimage.grey_dilation(full_scale_mask, footprint=s)
# comparison = full_scale_mask
# plt.imshow(comparison, cmap='gray')
# plt.show()

# no in fact just dilate one not the two
# comparison2 = ndimage.grey_dilation(downscaled_mask, footprint=s)
comparison2 = downscaled_mask  # ndimage.grey_dilation(downscaled_mask, footprint=s)
# plt.imshow(comparison2, cmap='gray')
# plt.show()

kernel = np.ones((3, 3))
vertices1 = scipy.signal.convolve2d(downscaled_mask, kernel, mode='same', fillvalue=1)
result = np.zeros_like(vertices1)
# result[np.logical_and(mask >= 1020, output == 255)] = 255
result[np.logical_and(vertices1 >= 1020, downscaled_mask == 255)] = 255
# result[vertices1 >= 1020] = 255
plt.imshow(result, cmap='gray')
plt.show()

# seems to work --> perform scoring to decide if keep bond or not and it keep then add to orig or if remove then

# TODO check if bidirectional or make it that way
not_img2 = np.logical_not(comparison2 == comparison, comparison2 != comparison)
# not_img = not_img[not_img==True and labels==255]
not_img2[comparison2 != 255] = 0
# not_img2[result!=0]=0# remove vertices --> sucks in fact
# not_img2[not_img2!=0]=255
plt.imshow(not_img2, cmap='gray')
plt.show()

# l'image est du binaire pr je ne sais quelle raison --> bug qd compare à 255
# combined mask
# en effer
not_img[not_img2 ==True] = True
plt.imshow(not_img, cmap='gray')
plt.show()


# faudrait splitter par vertex et scorer
# voir comment faire ça et si facile ou pas...




# try to do the reverse
#
# not2_img = np.logical_not(comparison2 == comparison, comparison != comparison2)
# not2_img[comparison2 != 255] = 0
# plt.imshow(not2_img, cmap='gray')
# plt.show()
# should
