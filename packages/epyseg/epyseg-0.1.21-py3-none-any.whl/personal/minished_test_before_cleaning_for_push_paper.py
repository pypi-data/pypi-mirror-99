from skimage.filters import threshold_sauvola
from skimage.measure import label, regionprops
from scipy.ndimage import generate_binary_structure
from scipy.signal import convolve2d
from skimage.morphology import remove_small_objects
# from skimage.morphology import watershed
from skimage.segmentation import watershed
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.morphology import skeletonize
from skimage import feature
from epyseg.img import Img
import numpy as np
from deprecated_demos.ta.wshed import Wshed
from personal.mini_test_wshed_only_for_unconnected_bonds2 import get_optimized_mask
from epyseg.postprocess.superpixel_methods import get_optimized_mask2


def sauvola(img, window_size=25, min_threshold=0.02):

    k = 0.25
    r = 0.5

    t = threshold_sauvola(img, window_size=window_size, k=k, r=r)
    if min_threshold is not None:
        t[t<=min_threshold]=min_threshold
    return t


def segment_cells(image, score_bonds=True, __DEBUG=False, __VISUAL_DEBUG=False, stop_at_threshold_step=False, min_unconnected_object_size=None, min_threshold=None, window_size=25, real_avg_mode=False):
    original = image.copy()

    t = sauvola(image, min_threshold=min_threshold, window_size=window_size)

    if __VISUAL_DEBUG:
        plt.imshow(t)
        plt.show()

    image[image >= t] = 1
    image[image < t] = 0

    if __VISUAL_DEBUG and min_unconnected_object_size == 12:
        plt.imshow(image)
        plt.title('before')
        plt.show()

    if min_unconnected_object_size is not None and min_unconnected_object_size>=1:
        image = remove_small_objects(image.astype(np.bool),min_size=min_unconnected_object_size, connectivity=2, in_place=True).astype(np.uint8)
        if __VISUAL_DEBUG and  min_unconnected_object_size == 12:
            plt.imshow(image)
            plt.title('after')
            plt.show()

    if stop_at_threshold_step:
        image = image*255
        return image

    if True:
        return get_optimized_mask2(original, sauvola_mask=None, score_before_adding=True) #, orig=original # in fact it's best with mask

    if False:
        return get_optimized_mask(image, orig=None, real_avg_mode=real_avg_mode)#, orig=original # in fact it's best with mask

    if __VISUAL_DEBUG:
        plt.imshow(image)
        plt.show()

    image = Img.invert(image)

    distance = ndimage.distance_transform_edt(image)
    if __VISUAL_DEBUG:
        plt.imshow(distance)
        plt.show()

    local_maxi = feature.peak_local_max(distance, indices=False,
                                        footprint=np.ones((16, 16)), labels=image)
    markers = ndimage.label(local_maxi, structure=generate_binary_structure(2,2))[0]

    if __VISUAL_DEBUG:
        plt.imshow(local_maxi)
        plt.show()

    labels = watershed(-distance, markers, watershed_line=True)
    labels[labels != 0] = 1
    labels[labels == 0] = 255
    labels[labels == 1] = 0

    if __VISUAL_DEBUG:
        plt.imshow(labels)
        plt.show()

        plt.imshow(image)
        plt.show()

    combination = np.logical_or(Img.invert(image), labels)
    if __VISUAL_DEBUG:
        plt.imshow(combination)
        plt.show()

    combination[combination != 0] = 1
    inv_bin = skeletonize(combination)
    if __VISUAL_DEBUG:
        plt.imshow(inv_bin)
        plt.show()

    if __DEBUG:
        Img(inv_bin.astype(np.uint8)*255, dimensions='hw').save('/D/final_folder_scoring/predict_hybrid/test_raw_skel_before_scoring.png')

    inv_bin = Wshed.run(inv_bin, seeds='mask')
    inv_bin[inv_bin!=0]=1

    if __VISUAL_DEBUG:
        plt.title('wshed')
        plt.imshow(inv_bin)
        plt.show()

    kernel = np.ones((3, 3))
    mask = convolve2d(inv_bin, kernel, mode='same', fillvalue=1)

    mask[mask < 4] = 0
    mask[mask >= 4] = 1

    if __VISUAL_DEBUG:
        plt.imshow(mask)
        plt.show()

    bonds = inv_bin - mask
    bonds[bonds < 0] = 0
    if __VISUAL_DEBUG:
        plt.imshow(bonds)
        plt.show()

    seeds_nomal_dilat = label(bonds, connectivity=None, background=0)
    if __VISUAL_DEBUG:
        plt.imshow(seeds_nomal_dilat)
        plt.show()

    image = Img.invert(image)
    if __VISUAL_DEBUG:
        plt.imshow(image)
        plt.show()

    if score_bonds:
        for region in regionprops(seeds_nomal_dilat):
            score = 0
            total = 0
            for coordinates in region.coords:
                total += 1
                if image[coordinates[0], coordinates[1]] != 0:
                    score += 1

            if total != 0:
                score /= total
                if score < 0.5:
                    for coordinates in region.coords:
                        inv_bin[coordinates[0], coordinates[1]] = 0

    if __VISUAL_DEBUG:
        plt.imshow(inv_bin)
        plt.show()

    if __DEBUG:
        Img(inv_bin.astype(np.uint8)*255, dimensions='hw').save('/D/final_folder_scoring/predict_hybrid/test_mask.png')
        Img(image.astype(np.uint8)*255, dimensions='hw').save('/D/final_folder_scoring/predict_hybrid/sauvola_mask.png')

    final_seeds = label(Img.invert(inv_bin), connectivity=1, background=0)
    for region in regionprops(final_seeds):
        if region.area < 10:
            for coordinates in region.coords:
                final_seeds[coordinates[0], coordinates[1]] = 0

    final_wshed = watershed(original, markers=final_seeds, watershed_line=True)
    final_wshed[final_wshed != 0] = 1
    final_wshed[final_wshed == 0] = 255
    final_wshed[final_wshed == 1] = 0
    if __DEBUG:
        Img(final_wshed.astype(np.uint8), dimensions='hw').save('/D/final_folder_scoring/predict_hybrid/final_wshed.png')

    return final_wshed

if __name__ == '__main__':
    from timeit import default_timer as timer

    # image = Img('/D/final_folder_scoring/predict_hybrid/mini_test.tif')
    # image = Img('/D/final_folder_scoring/predict_hybrid/AVG_StackFocused_Endocad-GFP(6-12-13)#19_000.tif')
    # image = Img('/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/122.tif')[...,0]
    # image = Img('/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/image_plant_best-zoomed.tif')[...,0]
    image = Img('/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/5.tif')[...,0]
    # image = Img('/D/final_folder_scoring/predict_hybrid/tmp11.png')
    # image = Img('/D/final_folder_scoring/predict_hybrid/11-1_nuclei_1.tif')
    start = timer()

    final_mask = segment_cells(image, score_bonds=False, __DEBUG=False, __VISUAL_DEBUG=False, stop_at_threshold_step=False)

    duration = timer() - start
    print(duration)

    plt.imshow(final_mask)
    plt.show()
    Img(final_mask, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/final_rewatershed.tif')