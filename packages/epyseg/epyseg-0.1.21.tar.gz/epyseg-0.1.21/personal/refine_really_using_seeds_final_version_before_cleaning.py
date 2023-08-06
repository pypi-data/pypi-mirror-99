

# should I autothreshold all ??? would that help ???

# threshold = (average background + average objects)/2 --> how do i do that ???
# take initial threshold then decide if above or below
# try just for fun

# the only default is that the wshed is a bit slow --> how can I improve that ?

# can I use an autolocal thershold to figure out which intensity to keep --> maybe not that hard to do and then would be totally auto
# the auto threshold by IJ is almost what I want
# maybe need a dilat to rescue small holes of 1px or maybe need better stuff

import traceback
from scipy import ndimage
from skimage.filters import threshold_otsu
# from skimage.morphology import watershed
from skimage.segmentation import watershed
from epyseg.img import Img
from matplotlib import pyplot as plt
from skimage.measure import label, regionprops
import os
import numpy as np

# logging
from epyseg.tools.logger import TA_logger

logger = TA_logger()


class RefineMaskUsingSeeds:
    stop_now = False

    # take input image, and provide desired output

    def __init__(self, img_orig, restore_safe_cells=True, _DEBUG=False, _VISUAL_DEBUG=False, **kwargs):

        # print('\nRefining predictions\n')

        # self.stop_now = False
        # self.progress_callback = progress_callback

        # if _DEBUG:
        #     print(input, filter, correction_factor, kwargs, cutoff_cell_fusion, output_folder)
        #
        # TA_mode = False
        # if output_folder == 'TA_mode':
        #     TA_mode = True
        #
        # if output_folder is None:
        #     output_folder = ''
        #
        # start = timer()
        #
        # # si input est dejà une liste alors prendre la liste sinon la créer TODO FIX SOON
        # list_of_files = glob.glob(os.path.join(input, "*.png")) + glob.glob(os.path.join(input, "*.jpg")) + glob.glob(
        #     os.path.join(input, "*.jpeg")) + glob.glob(
        #     os.path.join(input, "*.tif")) + glob.glob(os.path.join(input, "*.tiff"))
        # list_of_files = natsorted(list_of_files)
        #
        # if _DEBUG:
        #     print(list_of_files)

        # TODO maybe put a force list here

        # filename0 = path
        # filename0_without_path = os.path.basename(filename0)
        # filename0_without_ext = os.path.splitext(filename0_without_path)[0]
        # parent_dir_of_filename0 = os.path.dirname(filename0)
        # TA_output_filename = os.path.join(parent_dir_of_filename0, filename0_without_ext,
        #                                   'handCorrection.tif')  # TODO allow custom names here to allow ensemble methods
        # non_TA_final_output_name = os.path.join(output_folder, filename0_without_ext + '.tif')
        #
        # filename_to_use_to_save = non_TA_final_output_name
        # if TA_mode:
        #     filename_to_use_to_save = TA_output_filename
        #
        # if TA_mode:
        #     # try also to change path input name
        #     if os.path.exists(
        #             os.path.join(parent_dir_of_filename0, filename0_without_ext, 'raw_epyseg_output.tif')):
        #         path = os.path.join(parent_dir_of_filename0, filename0_without_ext, 'raw_epyseg_output.tif')

        # img_orig = Img(path)
        # print('analyzing', path, self.stop_now)
        # try:
        #     if self.progress_callback is not None:
        #         self.progress_callback.emit((iii / len(list_of_files)) * 100)
        #     else:
        #         logger.info(str((iii / len(list_of_files)) * 100) + '%')
        # except:
        #     traceback.print_exc()
        #     pass

        # DO A DILATION OF SEEDS THEN AN EROSION TO JOIN CLOSE BY SEEDS

        output_folder = '/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/'

        autothresholds = []

        # nb it works better with manual thresholds

        # test of thresholds for all
        for i in range(img_orig.shape[-1]):
            if i in [3, 4, 6]:
                threshold = self.autothreshold(Img.invert(img[..., i])) / 4
            else:
                threshold = self.autothreshold(img[..., i])
            # if i==0:
            #     threshold = 0.3
            print(i, '-->', threshold)
            autothresholds.append(threshold)
        # manual_thresholds = [0.3, 0.6, 0.7, 0.1, 0.25, 0.5, 0.1]
        # autothresholds = manual_thresholds

        if _DEBUG:
            Img(img_orig, dimensions='hwc').save(os.path.join(output_folder, 'raw_input.tif'))

        Img(img_orig, dimensions='hwc').save(os.path.join(output_folder, 'raw_input.tif'))

        # img_has_seeds = True
        # mask with several channels
        # if img_orig.has_c():

        # TODO in fact rather check that it has channels and the right nb of channels otherwise ignore

        # print(img_orig.shape)

        differing_bonds = np.zeros_like(img_orig)
        bckup_img_wshed = img_orig[..., 0].copy()

        # print(img_orig.shape)

        # should I reimplement that ??? maybe
        # if restore_safe_cells:
        #     raw_wshedlike_segmentation = img_orig[..., 0].copy() #

        # seeds_1 = img_orig[..., img_orig.shape[-1] - 1]
        # seeds_1 = Img.invert(seeds_1)
        # seeds_1[seeds_1 >= 0.5] = 255
        # seeds_1[seeds_1 < 0.5] = 0
        # seeds_1[seeds_1 >= 0.2] = 255 # TODO maybe be more stringent here
        # seeds_1[seeds_1 < 0.2] = 0
        #
        # s = ndimage.generate_binary_structure(2, 1)
        # seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
        # seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
        # seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
        # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
        # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
        # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
        # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)

        # for debug
        # if _DEBUG:
        #     Img(seeds_1, dimensions='hw').save(
        #         os.path.join(output_folder, 'extras', 'wshed_seeds.tif'))  # not bad
        #
        # lab_seeds = label(seeds_1.astype(np.uint8), connectivity=2, background=0)
        #
        # for region in regionprops(lab_seeds):
        #     if region.area < 10:
        #         for coordinates in region.coords:
        #             lab_seeds[coordinates[0], coordinates[1]] = 0

        # if _DEBUG:
        #     Img(seeds_1, dimensions='hw').save(
        #         os.path.join(output_folder, 'extras', 'wshed_seeds_deblobed.tif'))

        # img_orig[..., 0] = raw_wshedlike_segmentation.copy()
        # img_orig[..., 0][img_orig[..., 0] > 0.3] = 255
        # img_orig[..., 0][img_orig[..., 0] <= 0.3] = 0
        # img_orig[..., 0] = self.binarise(img_orig[..., 0],threshold=0.3)
        img_orig[..., 0] = self.binarise(img_orig[..., 0], threshold=autothresholds[0])

        # s = ndimage.generate_binary_structure(2, 1)
        # img_orig[..., 0] = ndimage.grey_dilation(img_orig[..., 0], footprint=s) # we dilate the first
        # img_orig[..., 0] = ndimage.grey_dilation(img_orig[..., 0], footprint=s) # we dilate the first

        # plt.imshow(img_orig[..., 0])
        # plt.show()

        # whsed_no_dilat1_black = img_orig[..., 1]
        # whsed_no_dilat1_black[whsed_no_dilat1_black > 0.5] = 255
        # whsed_no_dilat1_black[whsed_no_dilat1_black <= 0.5] = 0
        # img_orig[..., 1][img_orig[..., 1] > 0.6] = 255
        # img_orig[..., 1][img_orig[..., 1] <= 0.6] = 0
        # img_orig[..., 1] = self.binarise(img_orig[..., 1], threshold=0.6)
        img_orig[..., 1] = self.binarise(img_orig[..., 1], threshold=autothresholds[1])
        # whsed_no_dilat2_black = img_orig[..., 2]
        # whsed_no_dilat2_black[whsed_no_dilat2_black > 0.5] = 255
        # whsed_no_dilat2_black[whsed_no_dilat2_black <= 0.5] = 0
        # img_orig[..., 2][img_orig[..., 2] > 0.7] = 255
        # img_orig[..., 2][img_orig[..., 2] <= 0.7] = 0
        # img_orig[..., 2] = self.binarise(img_orig[..., 2], threshold=0.7)
        img_orig[..., 2] = self.binarise(img_orig[..., 2], threshold=autothresholds[2])

        img_orig[..., 3] = Img.invert(img_orig[..., 3])
        # img_orig[..., 3][img_orig[..., 3] > 0.1] = 255
        # img_orig[..., 3][img_orig[..., 3] <= 0.1] = 0
        # img_orig[..., 3] = self.binarise(img_orig[..., 3], threshold=0.1)
        img_orig[..., 3] = self.binarise(img_orig[..., 3], threshold=autothresholds[3])

        img_orig[..., 4] = Img.invert(img_orig[..., 4])
        # img_orig[..., 4][img_orig[..., 4] > 0.25] = 255
        # img_orig[..., 4][img_orig[..., 4] <= 0.25] = 0
        # img_orig[..., 4] = self.binarise(img_orig[..., 4], threshold=0.25)
        img_orig[..., 4] = self.binarise(img_orig[..., 4], threshold=autothresholds[4])

        # maybe change threshold
        # wshed_white_dilat2=img_orig[..., 3]
        # wshed_white_dilat2[wshed_white_dilat2 > 0.5] = 255
        # wshed_white_dilat2[wshed_white_dilat2 <= 0.5] = 0
        # plt.imshow(wshed_white_dilat2)
        # plt.show()
        #
        # wshed_white_dilat3 = img_orig[..., 4]
        # wshed_white_dilat3[wshed_white_dilat3 > 0.5] = 255
        # wshed_white_dilat3[wshed_white_dilat3 <= 0.5] = 0

        # binarise seeds
        img_orig[..., 5] = img_orig[..., 5]
        # img_orig[..., 5][img_orig[..., 5] > 0.5] = 255
        # img_orig[..., 5][img_orig[..., 5] <= 0.5] = 0
        # img_orig[..., 5] = self.binarise(img_orig[..., 5], threshold=0.5)
        img_orig[..., 5] = self.binarise(img_orig[..., 5], threshold=autothresholds[5])
        # maybe deblob it or keep it like that

        # white seeds
        img_orig[..., 6] = Img.invert(img_orig[..., 6])
        # img_orig[..., 6][img_orig[..., 6] > 0.1] = 255
        # img_orig[..., 6][img_orig[..., 6] <= 0.1] = 0
        # img_orig[..., 6] = self.binarise(img_orig[..., 6], threshold=0.1)
        img_orig[..., 6] = self.binarise(img_orig[..., 6], threshold=autothresholds[6])

        Img(img_orig, dimensions='hwc').save(os.path.join(output_folder, 'thresholded_masks.tif'))

        # seems to work --> now need to do the projection
        # for c in range(1, img_orig.shape[-1] - 2):
        #     img_orig[..., 0] += img_orig[..., 1]
        #
        # img_orig[..., 0] /= img_orig.shape[-1] - 2
        # img_orig = img_orig[..., 0]

        # else:
        #     # mask with single channel
        #     img_has_seeds = False
        #     if restore_safe_cells:
        #         raw_wshedlike_segmentation = img_orig.copy()

        # if restore_safe_cells:
        #     if _DEBUG:
        #         print(os.path.join(output_folder, 'extras', 'img_seg.tif'))
        #         Img(raw_wshedlike_segmentation, dimensions='hw').save(
        #             os.path.join(output_folder, 'extras', 'img_seg.tif'))

        # # for debug
        # if _DEBUG:
        #     Img(img_orig, dimensions='hw').save(os.path.join(output_folder, 'extras', 'avg.tif'))
        #
        # img_saturated = img_orig.copy()
        # # if img_has_seeds:
        #     # this is the binarised mask
        # img_saturated[img_saturated >= 0.5] = 255
        # img_saturated[img_saturated < 0.5] = 0
        # if restore_safe_cells:
        #     # TODO maybe do a safe image
        #     raw_wshedlike_segmentation[raw_wshedlike_segmentation >= 0.3] = 255 # not very stringent to be honest mayeb need more than that
        #     raw_wshedlike_segmentation[raw_wshedlike_segmentation < 0.3] = 0
        #     secure_mask = raw_wshedlike_segmentation
        # else:
        #     img_saturated[img_saturated >= 0.3] = 255
        #     img_saturated[img_saturated < 0.3] = 0
        #     if restore_safe_cells:
        #         raw_wshedlike_segmentation[raw_wshedlike_segmentation >= 0.95] = 255
        #         raw_wshedlike_segmentation[raw_wshedlike_segmentation < 0.95] = 0
        #         secure_mask = raw_wshedlike_segmentation

        # convert it to seeds and make sure they are all present in there
        # if pixel is not labeled then read it
        # if restore_safe_cells:
        #     labels_n_area_rescue_seeds = {}
        #     rescue_seeds = label(Img.invert(secure_mask), connectivity=1, background=0)
        #     for region in regionprops(rescue_seeds):
        #         labels_n_area_rescue_seeds[region.label] = region.area
        #     if _DEBUG:
        #         Img(secure_mask, dimensions='hw').save(os.path.join(output_folder, 'extras', 'secure_mask.tif'))
        # loop over those seeds to rescue

        # for debug
        # if _DEBUG:
        #     Img(img_saturated, dimensions='hw').save(
        #         os.path.join(output_folder, 'extras', 'handCorrection.tif'))

        # do I need deblob ???
        # deblob = True
        # if deblob:
        #     image_thresh = label(img_saturated, connectivity=2, background=0)
        #     # for debug
        #     if _DEBUG:
        #         Img(image_thresh, dimensions='hw').save(
        #             os.path.join(output_folder, 'extras', 'before_deblobed.tif'))
        #     # deblob
        #     min_size = 200
        #     for region in regionprops(image_thresh):
        #         # take regions with large enough areas
        #         if region.area < min_size:
        #             for coordinates in region.coords:
        #                 image_thresh[coordinates[0], coordinates[1]] = 0
        #
        #     image_thresh[image_thresh > 0] = 255
        #     img_saturated = image_thresh
        #     # for debug
        #     if _DEBUG:
        #         Img(img_saturated, dimensions='hw').save(
        #             os.path.join(output_folder, 'extras', 'deblobed.tif'))
        #     del image_thresh
        #
        # # for debug
        # if _DEBUG:
        #     Img(img_saturated, dimensions='hw').save(
        #         os.path.join(output_folder, 'extras', 'deblobed_out.tif'))

        # dilate mask to close holes (shall I now remove that in case of image with seeds ?)

        # do I need that can the seeds do the rescue instead ???
        # extra_dilations = True
        # if extra_dilations:
        #     # do a dilation of 2 to close bonds
        #     s = ndimage.generate_binary_structure(2, 1)
        #     dilated = ndimage.grey_dilation(img_saturated, footprint=s)
        #     dilated = ndimage.grey_dilation(dilated, footprint=s)
        #     # Img(dilated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'filled_one_px_holes.tif'))
        #
        #     # other_seeds = label(invert(np.grey_dilation(dilated, footprint=s).astype(np.uint8)), connectivity=1, background=0)
        #
        #     labs = label(Img.invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)
        #     for region in regionprops(labs):
        #         # seeds = []
        #
        #         # exclude tiny cells form dilation because they may end up completely closed
        #         if region.area >= 10 and region.area < 350:
        #             for coordinates in region.coords:
        #                 dilated[coordinates[0], coordinates[1]] = 0
        #             continue
        #         else:
        #             # pb when big cells around cause connections are not done
        #             # preserve cells at edges because they have to a naturally smaller size because they are cut
        #             # put a size criterion too
        #             if region.area < 100 and (
        #                     region.bbox[0] <= 1 or region.bbox[1] <= 1 or region.bbox[2] >= labs.shape[-2] - 2 or
        #                     region.bbox[
        #                         3] >= \
        #                     labs.shape[-1] - 2):
        #                 # edge cell detected --> removing dilation
        #                 for coordinates in region.coords:
        #                     dilated[coordinates[0], coordinates[1]] = 0
        #                 continue
        #
        #     img_saturated = dilated
        #     # for debug
        #     if _DEBUG:
        #         Img(img_saturated, dimensions='hw').save(
        #             os.path.join(output_folder, 'extras', 'dilated_further.tif'))
        #     del dilated
        #
        # list_of_cells_to_dilate = []
        # labs = label(Img.invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)
        #
        # # c'est cette correction qui fixe bcp de choses mais recree aussi des choses qui n'existent pas... --> voir à quoi sont dus ces lignes blobs
        # # faudrait redeblober
        # # if img_has_seeds:
        # for region in regionprops(labs, intensity_image=img_orig):
        #     seeds = []
        #
        #     if not extra_dilations and region.area < 10:
        #         continue
        #
        #     # if small and no associated seeds --> remove it ??? maybe or not
        #     for coordinates in region.coords:
        #         id = lab_seeds[coordinates[0], coordinates[1]]
        #         if id != 0:
        #             seeds.append(id)
        #
        #     seeds = set(seeds)
        #
        #     if len(seeds) >= 2:
        #         # we may have found an undersegmented cell --> try segment it better
        #         list_of_cells_to_dilate.append(region.label)
        #
        # # this is not great --> keep only for the most basic case where no seeds exist
        # if len(list_of_cells_to_dilate) != 0:
        #     props = regionprops(labs, intensity_image=img_orig)
        #     for run in range(10):
        #         something_changed = False  # early stop
        #
        #         for region in props:
        #             if region.label not in list_of_cells_to_dilate:
        #                 continue
        #
        #             # TODO recheck those values and wether it makes sense
        #             threshold_values = [80 / 255, 60 / 255, 40 / 255, 30 / 255,
        #                                 20 / 255,
        #                                 10 / 255]  # 160 / 255, 140 / 255, 120 / 255, 100 / 255,  1 / 255 , 2 / 255, , 5 / 255
        #
        #             try:
        #                 for threshold in threshold_values:
        #                     mask = region.image.copy()
        #                     image = region.image.copy()
        #                     image[region.intensity_image > threshold] = True
        #                     image[region.intensity_image <= threshold] = False
        #                     final = Img.invert(image.astype(np.uint8))
        #                     final[final < 255] = 0
        #                     final[mask == False] = 0
        #                     new_seeds = label(final, connectivity=1, background=0)
        #                     props2 = regionprops(new_seeds)
        #                     if len(props2) > 1:  # cell was resplitted into smaller
        #                         for r in props2:
        #                             if r.area < 20:
        #                                 raise Exception
        #
        #                         region.image[mask == False] = False
        #                         region.image[mask == True] = True
        #                         region.image[new_seeds > 0] = False
        #                         something_changed = True
        #                         for coordinates in region.coords:
        #                             img_saturated[coordinates[0], coordinates[1]] = 255
        #                     region.image[mask == False] = False
        #                     region.image[mask == True] = True
        #                     del final
        #                     del new_seeds
        #             except:
        #                 traceback.print_exc()
        #                 pass
        #
        #         if not something_changed:
        #             # print('no more changes anymore --> quitting')
        #             break
        #
        # # for debug
        # if _DEBUG:
        #     Img(img_saturated, dimensions='hw').save(
        #         os.path.join(output_folder, 'extras', 'saturated_mask4.tif'))

        # here I need detect all the unconnected bonds and and see if further seeds can rescue that
        # see how I can do that --> need detect bonds that disappear upon whseding of mask --> see how

        # now get seeds from saturated image
        # final_seeds = label(Img.invert(img_saturated), connectivity=1,
        #                     background=0)  # keep like that otherwise creates tiny cells with erroneous wshed
        #
        # # for debug
        # if _DEBUG:
        #     Img(final_seeds, dimensions='hw').save(
        #         os.path.join(output_folder, 'extras', 'final_seeds_before.tif'))
        # final_seeds = label(Img.invert(img_saturated), connectivity=2, background=0)  # is that needed ???
        # # for debug
        # if _DEBUG:
        #     Img(final_seeds, dimensions='hw').save(
        #         os.path.join(output_folder, 'extras', 'final_seeds_before2.tif'))
        #
        # final_seeds[img_saturated == 255] = 0
        # final_wshed = watershed(img_orig, markers=final_seeds,
        #                         watershed_line=True)
        #
        # final_wshed[final_wshed != 0] = 1  # remove all seeds
        # final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        # final_wshed[final_wshed == 1] = 0  # set all other cell content to

        # filename0 = os.path.basename(path)
        # parent_path = os.path.dirname(os.path.dirname(path))

        # here is the last wshed mask
        # after that it is just a refine of the mask can be stored in an independent class to ease things up
        # not so easy to put somewhere else because requires the safe seeds
        # should I simply redo a specific code just for that

        # create a wshed also for the seeds
        # detect bonds that disappeared after wshed and see if can be restored
        # plt.imshow(final_wshed, cmap='gray')
        # plt.show()
        #
        # Img(final_wshed, dimensions='hw').save(os.path.join(output_folder, 'wshed_cells.tif'))

        # do wshed on original image using seeds big enough of the stuff

        # img_orig = bckup_img_wshed
        for i in range(img_orig.shape[-1]):
            if i < 5:
                final_seeds = label(Img.invert(img[..., i]), connectivity=1, background=0)
            else:
                final_seeds = label(img[..., i], connectivity=1, background=0)
            final_wshed = watershed(bckup_img_wshed, markers=final_seeds, watershed_line=True)
            final_wshed[final_wshed != 0] = 1  # remove all seeds
            final_wshed[final_wshed == 0] = 255  # set wshed values to 255
            final_wshed[final_wshed == 1] = 0  # set all other cell content to
            differing_bonds[..., i] = final_wshed

            print(i)

            plt.imshow(img[..., i])
            # plt.imshow(final_wshed)
            plt.show()

            del final_seeds
            del final_wshed

            # final_seeds[img_saturated == 255] = 0
        # final_seeds2 = label(whsed_seeds_black, connectivity=1,                            background=0)
        # final_wshed2 = watershed(img_orig, markers=final_seeds2,                        watershed_line=True)
        # final_wshed2[final_wshed2 != 0] = 1  # remove all seeds
        # final_wshed2[final_wshed2 == 0] = 255  # set wshed values to 255
        # final_wshed2[final_wshed2 == 1] = 0  # set all other cell content to
        #
        # Img(final_wshed2, dimensions='hw').save(os.path.join(output_folder, 'wshed_seeds_black.tif'))
        #
        #
        # plt.imshow(final_wshed2, cmap='gray')
        # plt.show()
        #
        # final_seeds3 = label(whsed_seeds_white, connectivity=1,                            background=0)
        # final_wshed3 = watershed(img_orig, markers=final_seeds3,                        watershed_line=True)
        # final_wshed3[final_wshed3 != 0] = 1  # remove all seeds
        # final_wshed3[final_wshed3 == 0] = 255  # set wshed values to 255
        # final_wshed3[final_wshed3 == 1] = 0  # set all other cell content to
        #
        # Img(final_wshed3, dimensions='hw').save(os.path.join(output_folder, 'wshed_seeds_white.tif'))
        #
        # plt.imshow(whsed_no_dilat_black)
        # plt.show()
        #
        # final_seeds4 = label(Img.invert(whsed_no_dilat_black), connectivity=1, background=0)
        # final_wshed4 = watershed(img_orig, markers=final_seeds4, watershed_line=True)
        # final_wshed4[final_wshed4 != 0] = 1  # remove all seeds
        # final_wshed4[final_wshed4 == 0] = 255  # set wshed values to 255
        # final_wshed4[final_wshed4 == 1] = 0  # set all other cell content to
        #
        # Img(final_wshed4, dimensions='hw').save(os.path.join(output_folder, 'whsed_no_dilat_black.tif'))
        #
        # final_seeds5 = label(Img.invert(whsed_no_dilat1_black), connectivity=1, background=0)
        # final_wshed5 = watershed(img_orig, markers=final_seeds5, watershed_line=True)
        # final_wshed5[final_wshed5 != 0] = 1  # remove all seeds
        # final_wshed5[final_wshed5 == 0] = 255  # set wshed values to 255
        # final_wshed5[final_wshed5 == 1] = 0  # set all other cell content to
        #
        # Img(final_wshed5, dimensions='hw').save(os.path.join(output_folder, 'whsed_no_dilat1_black.tif'))
        #
        # final_seeds6 = label(Img.invert(whsed_no_dilat2_black), connectivity=1, background=0)
        # final_wshed6 = watershed(img_orig, markers=final_seeds6, watershed_line=True)
        # final_wshed6[final_wshed6 != 0] = 1  # remove all seeds
        # final_wshed6[final_wshed6 == 0] = 255  # set wshed values to 255
        # final_wshed6[final_wshed6 == 1] = 0  # set all other cell content to
        #
        # Img(final_wshed6, dimensions='hw').save(os.path.join(output_folder, 'whsed_no_dilat2_black.tif'))
        #
        # final_seeds7 = label(Img.invert(wshed_white_dilat2), connectivity=1, background=0)
        # final_wshed7 = watershed(img_orig, markers=final_seeds7, watershed_line=True)
        # final_wshed7[final_wshed7 != 0] = 1  # remove all seeds
        # final_wshed7[final_wshed7 == 0] = 255  # set wshed values to 255
        # final_wshed7[final_wshed7 == 1] = 0  # set all other cell content to
        #
        # Img(final_wshed7, dimensions='hw').save(os.path.join(output_folder, 'wshed_white_dilat2.tif'))
        #
        # final_seeds8 = label(Img.invert(wshed_white_dilat3), connectivity=1, background=0)
        # final_wshed8 = watershed(img_orig, markers=final_seeds8, watershed_line=True)
        # final_wshed8[final_wshed8 != 0] = 1  # remove all seeds
        # final_wshed8[final_wshed8 == 0] = 255  # set wshed values to 255
        # final_wshed8[final_wshed8 == 1] = 0  # set all other cell content to
        #
        # Img(final_wshed8, dimensions='hw').save(os.path.join(output_folder, 'wshed_white_dilat3.tif'))
        #
        # #  = img_orig[..., 4]
        #
        #
        #
        # plt.imshow(final_wshed3, cmap='gray')
        # plt.show()

        # now maybe just get the differing bonds and score with respect to the original image
        # test

        # or do max proj and compare current to final and if ok then really need score it and if score is good --> rescue stuff otherwise ignore
        # --> remove from max proj then the differeing pixels

        # maxproj = final_wshed4.copy()
        # maxproj =  np.maximum(maxproj, final_wshed)
        # maxproj =  np.maximum(maxproj, final_wshed2)
        # maxproj =  np.maximum(maxproj, final_wshed3)
        # maxproj =  np.maximum(maxproj, final_wshed5)
        # maxproj =  np.maximum(maxproj, final_wshed6)
        # maxproj =  np.maximum(maxproj, final_wshed7)
        # maxproj =  np.maximum(maxproj, final_wshed8)
        #
        # plt.imshow(maxproj, cmap='gray')
        # plt.show()
        # Img(maxproj, dimensions='hw').save(os.path.join(output_folder, 'max_proj.tif'))
        #
        # minproj = maxproj.copy()
        # # minproj.fill(255)
        # minproj = np.minimum(minproj, final_wshed)
        # minproj = np.minimum(minproj, final_wshed2)
        # minproj = np.minimum(minproj, final_wshed3)
        # minproj = np.minimum(minproj, final_wshed5)
        # minproj = np.minimum(minproj, final_wshed6)
        # minproj = np.minimum(minproj, final_wshed7)
        # minproj = np.minimum(minproj, final_wshed8)
        #
        # Img(minproj, dimensions='hw').save(os.path.join(output_folder, 'min_proj.tif'))

        # not_img = np.logical_not(maxproj == final_wshed, maxproj != final_wshed)

        # plt.imshow(not_img, cmap='gray')
        # plt.show()
        #
        # Img(maxproj, dimensions='hw').save(os.path.join(output_folder, 'difference_to_first.tif'))
        # parfait

        # could do that for all and score bonds in an array and see in the
        # if bonds overlap then take smallest --> see how to do that maybe best is to do a stack

        # not_img = np.logical_not(maxproj == final_wshed2, maxproj != final_wshed2)
        # differing_bonds[..., 0] = not_img
        # not_img = np.logical_not(maxproj == final_wshed3, maxproj != final_wshed3)
        # differing_bonds[..., 1] = not_img
        # not_img = np.logical_not(maxproj == final_wshed4, maxproj != final_wshed4)
        # differing_bonds[..., 2] = not_img
        # not_img = np.logical_not(maxproj == final_wshed5, maxproj != final_wshed5)
        # differing_bonds[..., 3] = not_img
        # not_img = np.logical_not(maxproj == final_wshed6, maxproj != final_wshed6)
        # differing_bonds[..., 4] = not_img
        # not_img = np.logical_not(maxproj == final_wshed7, maxproj != final_wshed7)
        # differing_bonds[..., 5] = not_img
        # not_img = np.logical_not(maxproj == final_wshed8, maxproj != final_wshed8)
        # differing_bonds[..., 6] = not_img

        # differing_bonds[..., 7] = not_img

        print(os.path.join(output_folder, 'differences.tif'))
        Img(differing_bonds, dimensions='hwc').save(os.path.join(output_folder, 'differences.tif'))

        # score with respect to this image comppared to safe bonds and see if must be there or not ???
        Img(bckup_img_wshed, dimensions='hw').save(os.path.join(output_folder, 'orig_img.tif'))

        # avg
        avg = np.mean(differing_bonds, axis=-1)
        avg = avg / avg.max()
        Img(avg, dimensions='hw').save(os.path.join(output_folder, 'avg.tif'))

        threshold = self.autothreshold(avg)

        # should I use local thresholds ??? could so the same
        print('threshold', threshold)

        avg = self.binarise(avg, threshold=threshold)
        # avg[avg >= threshold] = 255
        # avg[avg < threshold] = 0
        Img(avg, dimensions='hw').save(os.path.join(output_folder, 'binarized.tif'))

        # TODO just finalize mask and reshed and remove things too small
        # todo

        # or close then get seeds then rerun
        # avg = Wshed.run(avg.astype(np.uint8), seeds='mask')
        # Img(avg, dimensions='hw').save(os.path.join(output_folder, 'binarized_cleaned.tif'))

        s = ndimage.generate_binary_structure(2, 1)
        avg = ndimage.grey_dilation(avg, footprint=s)  # close

        # need get rid of very tiny cells left --> less that 10px

        # remove tiny blobs
        mask = label(Img.invert(avg), connectivity=1, background=0)  # is that needed ???
        for region in regionprops(mask):
            #             region_props_n_size[counter]=region.area # pb unhashable
            #             counter+=1
            #             rgps.append(region)
            #         # labels_n_bbox[region.label] = region.bbox
            if region.area < 5:

                for coordinates in region.coords:
                    avg[coordinates[0], coordinates[1]] = 255
        #             # compute score and add to final mask if above threshold
        #
        #             # labels_n_area[region.label] = region.area
        #
        #             # if (region.bbox[0] <= 3 or region.bbox[1] <= 3 or region.bbox[2] >= final_seeds.shape[-2] - 5 or
        #             #         region.bbox[
        #             #             3] >= \
        #             #         final_seeds.shape[-1] - 5):
        #             #     border_cells.append(region.label)
        #             # if restore_safe_cells:
        #             score = 0
        #             for coordinates in region.coords:
        #                 score+=img_orig[coordinates[0], coordinates[1]]
        #             score/=region.area
        del mask
        avg = label(Img.invert(avg), connectivity=1, background=0)  # is that needed ???

        avg = watershed(bckup_img_wshed, markers=avg,
                        watershed_line=True)

        avg[avg != 0] = 1  # remove all seeds
        avg[avg == 0] = 255  # set wshed values to 255
        avg[avg == 1] = 0  # set all other cell content to
        Img(avg.astype(np.uint8),dimensions='hw').save(os.path.join(output_folder, 'binarized_cleaned2.tif'))

        # qdsqdsqdqsdqsd

        # not bad see others

        # store all in original image so that I can see what to do with that

        # maybe exclude border cells from seeds as the seeds do not work well at the periphery
        # whseds can almost be readily combined but would be good to see the differences especially gained and lost bonds
        # see how I can do that

        # could even do that for all and then find a way to get the best mask by seeingbonds
        # or just take most frequent masks

        # could even run stuff on all and compare to wshed mask and see the best
        # could do wshed for all then combine all
        # see how to fuse cells and compare masks

        # all wsheds and decide
        # should I label all and compare seeds ???

        # should I do a dilate of masks and  sum or avg them
        # should I detect missing bonds from first image and see if can be rescued
        # maybe last is best

        # get all unconnected objects from the images and score them to see if worth adding them or not
        # and if so add them
        # only score if not in final mask otherwise skip it

        # can I label in a 3D stacks

        # or just compute and if above a threshold then keep

        # remove or keep
        #
        # valid_bonds = np.zeros_like(maxproj)
        # invalid_bonds = np.zeros_like(maxproj)

        # faudrait les trier dans l'ordre et faire smart

        # sort region props by size then

        # region_props_n_size = {}
        # rgps = []
        #
        # counter = 0
        # for i in range(differing_bonds.shape[-1]):
        #     difference = differing_bonds[..., i]
        #     # print(difference.shape)
        #     # plt.imshow(difference)
        #     # plt.show()
        #
        #     # get all labels and do stuff with them and create a mask for no repick maybe
        #     # if already scored --> ignore and also ignore if pixels exist
        #     labled_differing_bonds = label(difference, connectivity=None, background=0) # 8 connected
        #     # plt.imshow(labled_differing_bonds)
        #     # plt.show()
        #
        #     # remove dupes regions
        #     # need store regions and region props
        #
        #
        #     rps = regionprops(labled_differing_bonds)
        #     for region in rps:
        #             region_props_n_size[counter]=region.area # pb unhashable
        #             counter+=1
        #             rgps.append(region)
        #         # labels_n_bbox[region.label] = region.bbox
        #         # if region.area>=5:
        #             # compute score and add to final mask if above threshold
        #
        #             # labels_n_area[region.label] = region.area
        #
        #             # if (region.bbox[0] <= 3 or region.bbox[1] <= 3 or region.bbox[2] >= final_seeds.shape[-2] - 5 or
        #             #         region.bbox[
        #             #             3] >= \
        #             #         final_seeds.shape[-1] - 5):
        #             #     border_cells.append(region.label)
        #             # if restore_safe_cells:
        #             score = 0
        #             for coordinates in region.coords:
        #                 score+=img_orig[coordinates[0], coordinates[1]]
        #             score/=region.area
        #
        #             # maybe too stringent --> think about it and check
        #
        #             # should I get local score to see
        #             # pb is when images are from
        #             # should I average stuff
        #             if score>0.5:
        #                 for coordinates in region.coords:
        #                     valid_bonds[coordinates[0], coordinates[1]]=255
        #                     # keep
        #
        #                 # if img_orig[coordinates[0], coordinates[1]] != 0:  # do r
        #                 #     correspondance_between_cur_seeds_and_safe_ones[region.label] = rescue_seeds[coordinates[0], coordinates[1]]
        #                 #     break
        #             else:
        #                 for coordinates in region.coords:
        #                     invalid_bonds[coordinates[0], coordinates[1]] = 255
        #         # else:
        #         #     for coordinates in region.coords:
        #         #         invalid_bonds[coordinates[0], coordinates[1]] = 255
        #
        # print('region props sorted by size', region_props_n_size)
        # print('regionprops', rgps)
        #
        # # import operator
        # #we sort rps by area/length
        # # y = {'carl': 40, 'alan': 2, 'bob': 1, 'danny': 3}
        # # sorted_rps_by_length = dict(sorted(region_props_n_size.items(), key=operator.itemgetter(1)))
        # sorted_rps_by_length = sorted(region_props_n_size.items(), key=lambda x: x[1]) # ça marche --> vraiment top
        # print('Dictionary in ascending order by value : ', sorted_rps_by_length)
        # # print('Dictionary in ascending order by value : ', sorted_rps_by_length.keys())

        # loop in correct order and see how to do

        # sorted = list(region_props_n_size.items())  # convet the given dict. into list
        # sorted.sort()  # sort the list
        # print('Ascending order is', sorted)  # this print the sorted list

        # plt.imshow(valid_bonds, cmap='gray')
        # plt.show()
        # Img(valid_bonds, dimensions='hw').save(os.path.join(output_folder, 'valid_bonds.tif'))
        # Img(invalid_bonds, dimensions='hw').save(os.path.join(output_folder, 'invalid_bonds.tif'))
        #
        # final_mask = np.maximum(minproj, valid_bonds) # reconstitued cells # maybe add a basic filtering by area or alike

        # Img(final_mask, dimensions='hw').save(os.path.join(output_folder, 'final_mask.tif'))
        # plt.imshow(final_mask, cmap='gray')
        # plt.show()

        # si des cellules sont incompletes open faudrait qd mm les fermer... --> c'est surtout au bord qu'il y a des pbs

        # maybe put the filtering of mask in another class is that even needed with the new correction

    #         if filter is None or filter == 0:
    #             # raw mask
    #             # TODO maybe offer the choice between saving wshed on predict or on orig
    #             # Img(final_wshed, dimensions='hw').save(os.path.join(output_folder, os.path.splitext(filename0)[
    #             #     0]) + '.tif')  # need put original name here  TODO put image default name here
    #             print('saving', filename_to_use_to_save)
    #             Img(final_wshed.astype(np.uint8), dimensions='hw').save(filename_to_use_to_save)
    #         else:
    #             # filtered mask to remove small cells or outliers from a wshed mask
    #             if isinstance(filter, int):
    #                 filter_by_size = filter
    #             else:
    #                 filter_by_size = None
    #             avg_area = 0
    #             count = 0
    #             if _DEBUG:
    #                 Img(final_wshed, dimensions='hw').save(os.path.join(output_folder, 'extras', 'test_size_cells.tif'))
    #
    #             final_seeds = Img.invert(final_wshed)
    #             final_seeds = label(final_seeds, connectivity=1, background=0)
    #
    #             if _VISUAL_DEBUG:
    #                 plt.imshow(final_seeds)
    #                 plt.show()
    #
    #             removed_seeds = []
    #             keep_seeds = []
    #
    #             labels_n_bbox = {}
    #             labels_n_area = {}
    #             border_cells = []
    #             ids_n_local_median = {}
    #             correspondance_between_cur_seeds_and_safe_ones = {}
    #
    #             if isinstance(filter, str) and 'local' in filter:
    #                 rps = regionprops(final_seeds)
    #
    #                 for region in rps:
    #                     labels_n_bbox[region.label] = region.bbox
    #                     labels_n_area[region.label] = region.area
    #                     if (region.bbox[0] <= 3 or region.bbox[1] <= 3 or region.bbox[2] >= final_seeds.shape[-2] - 5 or
    #                             region.bbox[
    #                                 3] >= \
    #                             final_seeds.shape[-1] - 5):
    #                         border_cells.append(region.label)
    #                     if restore_safe_cells:
    #                         for coordinates in region.coords:
    #                             if rescue_seeds[coordinates[0], coordinates[1]] != 0:  # do r
    #                                 correspondance_between_cur_seeds_and_safe_ones[region.label] = rescue_seeds[
    #                                     coordinates[0], coordinates[1]]
    #                                 break
    #                             break
    #
    #                 _, tiles = Img.get_2D_tiles_with_overlap(final_seeds, overlap=64, dimension_h=-2, dimension_w=-1)
    #
    #                 for r in tiles:
    #                     for tile in r:
    #                         rps2 = regionprops(tile)
    #                         for region in rps2:
    #                             if self.stop_now:
    #                                 return
    #
    #                             if region.label in border_cells:
    #                                 continue
    #
    #                             if (region.bbox[0] <= 3 or region.bbox[1] <= 3 or region.bbox[2] >= final_seeds.shape[
    #                                 -2] - 5 or
    #                                     region.bbox[
    #                                         3] >= \
    #                                     final_seeds.shape[-1] - 5):
    #                                 continue
    #
    #                             area_of_neighboring_cells = []
    #                             for region2 in rps2:
    #                                 if region2.label == region.label:
    #                                     continue
    #                                 # find all cells with
    #                                 if self.rect_distance(region.bbox, region2.bbox) <= 1:
    #                                     area_of_neighboring_cells.append(labels_n_area[region2.label])
    #
    #                             if area_of_neighboring_cells:
    #                                 median = statistics.median_low(area_of_neighboring_cells)
    #                                 ids_n_local_median[
    #                                     region.label] = median / correction_factor
    #                                 if region.area <= median / correction_factor:
    #                                     removed_seeds.append(region.label)
    #                                 else:
    #                                     keep_seeds.append(region.label)
    #                 removed_seeds = [x for x in removed_seeds if x not in keep_seeds]
    #
    #                 # TODO offer the things below as an option --> prevent removal of sure seeds or something like that
    #                 if restore_safe_cells:
    #                     removed_seeds_to_restore = []
    #                     for region in regionprops(final_seeds):
    #                         if region.label in removed_seeds:
    #                             first = True
    #                             for coordinates in region.coords:
    #                                 if first and rescue_seeds[coordinates[0], coordinates[1]] != 0:
    #                                     percent_diff = min(labels_n_area[region.label], labels_n_area_rescue_seeds[
    #                                         rescue_seeds[coordinates[0], coordinates[1]]]) / max(
    #                                         labels_n_area[region.label], labels_n_area_rescue_seeds[
    #                                             rescue_seeds[coordinates[0], coordinates[1]]])
    #
    #                                     if (percent_diff >= 0.7 and percent_diff < 1.0) or (
    #                                             labels_n_area[region.label] <= 200 and (
    #                                             percent_diff >= 0.3 and percent_diff < 1.0)):
    #                                         if _DEBUG:
    #                                             print('0 finally not removing seed, safe seed', region.label,
    #                                                   percent_diff,
    #                                                   labels_n_area[region.label],
    #                                                   labels_n_area_rescue_seeds[
    #                                                       rescue_seeds[coordinates[0], coordinates[1]]],
    #                                                   labels_n_area[region.label] / labels_n_area_rescue_seeds[
    #                                                       rescue_seeds[coordinates[0], coordinates[1]]],
    #                                                   region.centroid)
    #                                         removed_seeds_to_restore.append(region.label)
    #                                         break
    #                                     break
    #                     removed_seeds = [x for x in removed_seeds if x not in removed_seeds_to_restore]
    #             else:
    #                 areas = []
    #
    #                 for region in regionprops(final_seeds):
    #                     if (region.bbox[0] <= 3 or region.bbox[1] <= 3 or region.bbox[2] >= final_seeds.shape[-2] - 5 or
    #                             region.bbox[3] >= final_seeds.shape[-1] - 5):
    #                         continue
    #                     avg_area += region.area
    #                     count += 1
    #                     areas.append(region.area)
    #                 avg_area /= count
    #
    #                 median = statistics.median_low(areas)
    #
    #                 if isinstance(filter, int):
    #                     filter_by_size = filter
    #                 elif 'avg' in filter:
    #                     filter_by_size = avg_area / correction_factor
    #                 elif 'median' in filter:
    #                     filter_by_size = median / correction_factor
    #                 # TODO maybe use stdev or alike to see if cell should really be removed
    #                 if _DEBUG:
    #                     print('filter cells below=', filter_by_size, 'avg cell area=', avg_area, 'median=',
    #                           median)  # , 'median', median
    #
    #                 if filter_by_size is not None and filter_by_size != 0:
    #
    #                     if _VISUAL_DEBUG:
    #                         plt.imshow(final_seeds)
    #                         plt.show()
    #
    #                     for region in regionprops(final_seeds):
    #                         labels_n_bbox[region.label] = region.bbox
    #                         labels_n_area[region.label] = region.area
    #                         if region.area < filter_by_size:
    #                             if (region.bbox[0] <= 2 or region.bbox[1] <= 2 or region.bbox[2] >= labs.shape[
    #                                 -2] - 3 or
    #                                     region.bbox[
    #                                         3] >= \
    #                                     labs.shape[
    #                                         -1] - 3):
    #                                 continue
    #                             removed_seeds.append(region.label)
    #
    #             if cutoff_cell_fusion is not None and cutoff_cell_fusion > 1:
    #                 cells_to_fuse = []
    #
    #                 for idx, removed_seed in enumerate(removed_seeds):
    #                     current_cells_to_fuse = set()
    #                     closest_pair = None
    #                     smallest_distance = None
    #
    #                     for idx2 in range(idx + 1, len(removed_seeds)):
    #                         removed_seed2 = removed_seeds[idx2]
    #
    #                         if closest_pair is None:
    #                             if self.rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2]) <= 1:
    #                                 closest_pair = removed_seed2
    #                                 smallest_distance = self.rect_distance(labels_n_bbox[removed_seed],
    #                                                                        labels_n_bbox[removed_seed2])
    #                         elif self.rect_distance(labels_n_bbox[removed_seed],
    #                                                 labels_n_bbox[removed_seed2]) <= smallest_distance:
    #                             closest_pair = removed_seed2
    #                             smallest_distance = self.rect_distance(labels_n_bbox[removed_seed],
    #                                                                    labels_n_bbox[removed_seed2])
    #
    #                         if self.rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2]) <= 1:
    #                             current_cells_to_fuse.add(removed_seed)
    #                             current_cells_to_fuse.add(removed_seed2)
    #
    #                     if current_cells_to_fuse:
    #                         cells_to_fuse.append(current_cells_to_fuse)
    #
    #                 cells_to_fuse = [frozenset(i) for i in cells_to_fuse]
    #                 cells_to_fuse = list(dict.fromkeys(cells_to_fuse))
    #
    #                 cells_to_keep = []
    #                 if cutoff_cell_fusion is not None and cutoff_cell_fusion > 0:
    #                     superfuse = []
    #
    #                     copy_of_cells_to_fuse = cells_to_fuse.copy()
    #                     for idx, fuse in enumerate(copy_of_cells_to_fuse):
    #                         current_fusion = set(fuse.copy())
    #                         changed = True
    #                         while changed:
    #                             changed = False
    #                             for idx2 in range(len(copy_of_cells_to_fuse) - 1, idx, -1):
    #                                 fuse2 = copy_of_cells_to_fuse[idx2]
    #                                 if idx2 == idx:
    #                                     continue
    #                                 if fuse2.intersection(current_fusion):
    #                                     current_fusion.update(fuse2)
    #                                     del copy_of_cells_to_fuse[idx2]
    #                                     changed = True
    #                         superfuse.append(current_fusion)
    #
    #                     for sf in superfuse:
    #                         if len(sf) > cutoff_cell_fusion:
    #                             for val in sf:
    #                                 cells_to_keep.append(val)
    #
    #                 seeds_to_fuse = []
    #
    #                 cells_to_fuse = sorted(cells_to_fuse, key=len)
    #                 for fuse in cells_to_fuse:
    #                     cumulative_area = 0
    #                     for _id in fuse:
    #                         if _id in cells_to_keep:
    #                             if _id in removed_seeds:
    #                                 removed_seeds.remove(_id)
    #                             continue
    #                         cumulative_area += labels_n_area[_id]
    #                     if filter_by_size is not None:
    #                         if cumulative_area >= filter_by_size: #: #1200: #filter_by_size: # need hack this to get local area
    #                             seeds_to_fuse.append(fuse)
    #                             for _id in fuse:
    #                                 if _id in removed_seeds:
    #                                     removed_seeds.remove(_id)
    #                     else:
    #                         if cumulative_area >= ids_n_local_median[_id]:
    #                             seeds_to_fuse.append(fuse)
    #                             for _id in fuse:
    #                                 if _id in removed_seeds:
    #                                     removed_seeds.remove(_id)
    #
    #                 # need recolor all the seeds in there with the new seed stuff
    #                 for fuse in seeds_to_fuse:
    #                     for _id in fuse:
    #                         break
    #                     for region in regionprops(final_seeds):
    #                         if region.label in fuse:
    #                             for coordinates in region.coords:
    #                                 final_seeds[coordinates[0], coordinates[1]] = _id
    #
    #             if _VISUAL_DEBUG:
    #                 plt.imshow(final_seeds)
    #                 plt.show()
    #
    #             for region in regionprops(final_seeds):
    #                 if region.label in removed_seeds:
    #                     for coordinates in region.coords:
    #                         final_seeds[coordinates[0], coordinates[1]] = 0
    #             if _VISUAL_DEBUG:
    #                 plt.imshow(final_seeds)
    #                 plt.show()
    #
    #             if _VISUAL_DEBUG:
    #                 plt.imshow(final_seeds)
    #                 plt.show()
    #
    #             final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)
    #
    #             final_wshed[final_wshed != 0] = 1  # remove all seeds
    #             final_wshed[final_wshed == 0] = 255  # set wshed values to 255
    #             final_wshed[final_wshed == 1] = 0  # set all other cell content to
    #             if _VISUAL_DEBUG:
    #                 plt.imshow(final_wshed)
    #                 plt.show()
    #             print('saving', filename_to_use_to_save)
    #             Img(final_wshed.astype(np.uint8), dimensions='hw').save(filename_to_use_to_save)
    #
    #             duration = timer() - start
    #             if _DEBUG:
    #                 print('final duration wshed in secs', duration)
    #
    # def rect_distance(self, bbox1, bbox2):
    #     width1 = abs(bbox1[3] - bbox1[1])
    #     width2 = abs(bbox2[3] - bbox2[1])
    #     height1 = abs(bbox1[2] - bbox1[0])
    #     height2 = abs(bbox2[2] - bbox2[0])
    #     return max(abs((bbox1[1] + width1 / 2) - (bbox2[1] + width2 / 2)) - (width1 + width2) / 2,
    #                abs((bbox1[0] + height1 / 2) - (bbox2[0] + height2 / 2)) - (height1 + height2) / 2)
    def autothreshold(self, single_2D_img, initial_threshold=0.5):

        # fig, ax = try_all_threshold(single_2D_img, figsize=(10, 8), verbose=False)
        # plt.show()

        return threshold_otsu(single_2D_img)  # this is exactly the same as imageJ

        # test auto threshold à la imageJ

        # bg = (avg < initial_threshold) * avg
        # average_background = np.mean(bg)
        # fg = (avg > initial_threshold) * avg
        # average_objects = np.mean(fg)
        # average_background = single_2D_img[single_2D_img <= initial_threshold].mean()
        # average_objects = single_2D_img[single_2D_img > initial_threshold].mean()
        # threshold = (average_background + average_objects) / 2
        # print('threshold', threshold, average_objects, average_background)

        # threshold/=2
        # return threshold

    # TODO improve and allow for copy of image and move to the Img class or at least file
    def binarise(self, single_2D_img, threshold=0.5, bg_value=0, fg_value=255):
        single_2D_img[single_2D_img > threshold] = fg_value
        single_2D_img[single_2D_img <= threshold] = bg_value
        return single_2D_img


if __name__ == '__main__':
    # get the image invert what needs to be inverted

    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/'
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_shells/'
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict/'
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_light_divided_by_2/'
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_paper/'
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/'  # 1
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729_rot_HQ_only/' #2
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/'  # 3
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/' #3
    # input = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317_rot_HQ_only/' #4

    from timeit import default_timer as timer

    start = timer()

    # check but this is most likely better than any other code I made --> TODO
    # check for real and finalize the code but looks like the best I ever had
    # maybe need simpler model to capture less noise or signal

    # everything seems to work now finalize the GUI...
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/0.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/cellpose_img22.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/cellpose_img07.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/cellpose_img08.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/cellpose_img18.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/cellpose_img21.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/122.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/5.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/Bro43_avproj0000.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/100708_png06.tif') # quite bad...
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/proj0016.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/StackFocused_Endocad-GFP(6-12-13)#19_000.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/StackFocused_Endocad-GFP(6-12-13)#19_400.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/image_plant_best-zoomed.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/T21a920000.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_ok_2.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_2c.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/16.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/Series019.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/FocStich_RGB008.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/focused_Series194.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/focused_Series316.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/MAX_ECadGFP_120410_2_094.tif')

    # should I keep the old codes can the secure cells be those of
    img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/20190924_ecadGFP_400nM20E_000.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/disc_0002_DCAD.tif')

    # pas mal trouver comment thresholder et aussi suppimer les ttes petites cellules
    # sauver ces fichiers en fichiers.score et les ouvrir --> peut etre fait en post process
    # maybe offer score
    # faire un score browser maybe --> TODO

    post_proc = RefineMaskUsingSeeds(img_orig=img,
                                     restore_safe_cells=True,
                                     _DEBUG=False, _VISUAL_DEBUG=False)

    print('local max', timer() - start)

    # should I check and fix neo disconnected bonds --> maybe not hard due to vertices
    # also bring back wshed and removal of small cells as a parameter

    # pure size based stuff
    # post_proc = EPySegPostProcess(input=input, output_folder='/home/aigouy/Bureau/final_folder_scoring/epyseg_tests',
    #                               filter=150,
    #                               correction_factor=2, TA_name=None, cutoff_cell_fusion=None,
    #                               restore_safe_cells=False,
    #                               _DEBUG=False, _VISUAL_DEBUG=False)
