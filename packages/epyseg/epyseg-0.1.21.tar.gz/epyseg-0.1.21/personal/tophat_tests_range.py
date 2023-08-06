from epyseg.img import Img
import traceback
from skimage.morphology import white_tophat, disk
from skimage.morphology import square, ball, diamond, octahedron, rectangle
import numpy as np

# try restore range


'''
single_RGB_16bits.tif
single_RGB_32bits.tif
single_8bits.tif
single_16bits.tif
single_32bits.tif
single_RGB.tif
'''


# img = Img('/D/Sample_images/sample_images_epiguy_pyta/images_with_different_bits/single_8bits.tif')# it is converted to float down the way and range is changed --> be careful
# img = Img('/D/Sample_images/sample_images_epiguy_pyta/images_with_different_bits/single_RGB.tif')# it is converted to float down the way and ange is changed
# img = Img('/D/Sample_images/sample_images_epiguy_pyta/images_with_different_bits/single_32bits.tif')# it is unchanged
# img = Img('/D/Sample_images/sample_images_epiguy_pyta/images_with_different_bits/single_RGB_32bits.tif')# it is unchanged dtype but changed range
img = Img('/D/Sample_images/sample_images_epiguy_pyta/images_with_different_bits/single_16bits.tif')# it is unchanged dtype but changed range

print(img.dtype)
print(img.shape)
print(img.max(), img.min())


# do for single channel in fact --> preserve range

'''
to preserve the initial range

min = orig.min()
max = orig.max()

# print('noise', mode, extra_params, is_mask)

noisy_image = random_noise(orig, mode=mode, clip=True, **extra_params)
if min == 0 and max == 1 or max == min:
    pass
else:
    # we preserve original image range (very important to keep training consistent)
    noisy_image = (noisy_image * (max - min)) + min
'''



img = white_top_hat(img)




print('---> ')
print(img.dtype)
print(img.shape)
print(img.max(), img.min())