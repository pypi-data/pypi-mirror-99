from skimage import exposure  # enhance image contrast

import matplotlib.pyplot as plt
from skimage import data
from skimage.transform import rescale
import warnings
import numpy as np

# https://www.kaggle.com/tomahim/image-manipulation-augmentation-with-skimage
from epyseg.img import Img

# good point they all seem to preserve the range --> really cool



original_image = Img('/home/aigouy/Bureau/final_folder_scoring/122.png')
# original_image = Img.normalization(original_image, method='Rescaling (min-max normalization)', range=[0, 1])
original_image = Img.normalization(original_image, method='Standardization (Z-score Normalization)', range=[-1, 1])

# --> easy to add for
# maybe just ignore them for now if selected in augs and nothing can be done...

# original_image = Img.normalization(original_image, method='Standardization (Z-score Normalization)', range=[0, 1])

# NB DOES NOT WORK FOR NEGATIVE VALUES --> NEED TO WARN IF USER USES THE WRONG NORMALIZATION



# min_val = None
# if original_image.min()<0:
#     min_val = abs(original_image.min())
#
# if min_val is not None:
#     original_image+=min_val



# pbs --> for rescale with standardization -1,1 --> Clipping input data to the valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers).
# not working with negative values --> adjusted_gamma_image, rescale_intensity, adjust_log, adjust_sigmoid



# original_image = Img('/home/aigouy/Bureau/final_folder_scoring/122.png')


warnings.filterwarnings("ignore")


def show_images(before, after, op):
    print(op, before.min(), before.max(), after.min(), after.max())

    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.ravel()
    ax[0].imshow(before, cmap='gray')
    ax[0].set_title("Original image")

    ax[1].imshow(after, cmap='gray')
    ax[1].set_title(op + " image")

    ax[0].axis('off')
    ax[1].axis('off')
    plt.tight_layout()
    plt.show()


v_min, v_max = np.percentile(original_image, (0.2, 99.8))  # preserves scale it seems --> good
better_contrast = exposure.rescale_intensity(original_image, in_range=(v_min, v_max))
# if min_val is not None:
#     better_contrast-=min_val
show_images(original_image, better_contrast, 'Rescale intensity')

v_min, v_max = np.percentile(original_image, (0.9, 98))  # pas mal --> quite strong # maybe put this as a parameter some day but ok for now to have it like that
better_contrast = exposure.rescale_intensity(original_image, in_range=(v_min, v_max))
# if min_val is not None:
#     better_contrast-=min_val
show_images(original_image, better_contrast, 'Rescale intensity')

v_min, v_max = np.percentile(original_image, (5, 95))  # pas mal --> quite strong # maybe put this as a parameter some day but ok for now to have it like that
better_contrast = exposure.rescale_intensity(original_image, in_range=(v_min, v_max))
# if min_val is not None:
#     better_contrast-=min_val
show_images(original_image, better_contrast, 'Rescale intensity')



# gamma and gain parameters are between 0 and 1
adjusted_gamma_image = exposure.adjust_gamma(original_image, gamma=0.4, gain=0.9)  # decreases a bit the max but ok -->
# if min_val is not None:
#     adjusted_gamma_image-=min_val
show_images(original_image, adjusted_gamma_image, 'Adjusted gamma')

# gamma and gain parameters are between 0 and 1
adjusted_gamma_image = exposure.adjust_gamma(original_image, gamma=0.8, gain=0.9)
# if min_val is not None:
#     adjusted_gamma_image-=min_val
show_images(original_image, adjusted_gamma_image, 'Adjusted gamma')

# equalize_adapthist = exposure.equalize_adapthist(original_image, clip_limit=0.03) # too strong I think
# show_images(original_image, equalize_adapthist, 'equalize_adapthist')


# too strong I think
# equalize_histo = exposure.equalize_hist(original_image) # warning does change scale
# show_images(original_image, equalize_histo, 'equalize_hist') # all but this one preserve range --> not much to do then

log_correction_image = exposure.adjust_log(original_image)
# if min_val is not None:
#     log_correction_image-=min_val
show_images(original_image, log_correction_image, 'Logarithmic corrected')

# log_correction_image = exposure.adjust_log(original_image, gain=2)
# show_images(original_image, log_correction_image, 'Logarithmic corrected g=2')

# sigmoid_correction_image = exposure.adjust_sigmoid(original_image, gain=8) # maybe too strong
# show_images(original_image, sigmoid_correction_image, 'Sigmoid corrected g=8')

sigmoid_correction_image = exposure.adjust_sigmoid(original_image, gain=5)
# if min_val is not None:
#     sigmoid_correction_image-=min_val
show_images(original_image, sigmoid_correction_image, 'Sigmoid corrected g=5')

sigmoid_correction_image = exposure.adjust_sigmoid(original_image, gain=2)  # image appears blurred
# if min_val is not None:
#     sigmoid_correction_image-=min_val
show_images(original_image, sigmoid_correction_image, 'Sigmoid corrected g=2')

# TODO check max min
