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
import tempfile

from epyseg.postprocess.filtermask import FilterMask
from epyseg.postprocess.edmshed import segment_cells

logger = TA_logger()


class RefineMaskUsingSeeds:

    # store in temp dir by default
    def __init__(self):
        pass

    def process(self, input=None, mode=None, _DEBUG=False, _VISUAL_DEBUG=False, output_folder=tempfile.gettempdir(), output_name='handCorrection.tif', threshold=None,
                 filter=None,
                 correction_factor=2,
                 # cutoff_cell_fusion=None, # do not keep this in the new version and simplify my code
                 # restore_safe_cells=False, # do not keep this in the new version and simplify my code
                 **kwargs):

        # dispatch between fast or full depending on mode
        # fast --> do it on avg of one + two just once
        # full --> do it on all and time stuff
        # see if I can do all in a single code or if I need more


        if input is None:
            logger.error('no input image --> nothing to do')
            return

        img_orig = input

        if not img_orig.has_c() or img_orig.shape[-1] != 7:
            logger.error('image must have 7 channels to be used for post process')
            return img_orig
        # autothresholds = []

        # autothreshold all masks
        # for i in range(img_orig.shape[-1]):
            # white bg masks need very low threshold
            # if i in [0, 3, 4, 6]: # before [3, 4, 6]
            #     auto_threshold = self.autothreshold(Img.invert(img[..., i])) / 4
            # else:
            # auto_threshold = self.phansalkarthreshold(img[..., i])
            # autothresholds.append(auto_threshold)
            # autothresholds.append(0.15)

        # new corrections (avg on HQ pred)
        # autothresholds[0]/=7
        # autothresholds[1]/=2.5
        # autothresholds[2] = 10/100*autothresholds[2]+autothresholds[2]
        # autothresholds[3]/=5
        # autothresholds[4]/=3
        # autothresholds[5]/=2
        # autothresholds[6]/=6
        # bckup2
        # autothresholds[0] = 0.05
        # autothresholds[1] = 0.14
        # autothresholds[2] = 0.16
        # autothresholds[3] = 0.14
        # autothresholds[4] = 0.1
        # autothresholds[5] = 0.2
        # autothresholds[6] = 0.25
        # test 3
        # autothresholds[0] = 0.01
        # autothresholds[1] = 0.1
        # autothresholds[2] = 0.2
        # autothresholds[3] = 0.2
        # autothresholds[4] = 0.125
        # autothresholds[5] = 0.1
        # autothresholds[6] = 0.2


        # bckup
        # autothresholds[0] /= 6
        # autothresholds[1] /= 3
        # autothresholds[3] /= 6
        # autothresholds[4] /= 4
        # autothresholds[5] /= 2
        # autothresholds[6] /= 6

        # old correction (max on HQ pred)
        # autothresholds[3] /= 4
        # autothresholds[4] /= 4
        # autothresholds[6] /= 4

        # keep because manual is sometimes better
        # manual_thresholds = [0.3, 0.6, 0.7, 0.1, 0.25, 0.5, 0.1] # normal
        # manual_thresholds = [0.075, 0.25, 0.5, 0.15, 0.4, 0.25, 0.25] # for avg --> better take those # pas mal mais tester sur d'autres image
        # print(autothresholds, 'vs', manual_thresholds)

        # print(autothresholds, 'vs', manual_thresholds)
        # autothresholds = manual_thresholds

        if _DEBUG:
            Img(img_orig, dimensions='hwc').save(os.path.join(output_folder, 'raw_input.tif'))

        bckup_img_wshed = img_orig[..., 0].copy()
        if mode is not None and isinstance(mode, str):
            # if 'fault' in mode:
            #     img_orig = img_orig[...,:-4]
            #     # print('3', img_orig.shape)
            # el
            if 'ast' in mode:
                print('fast mode')
                # img_orig = img_orig[..., :-2]
                img_orig[..., 0] += img_orig[..., 1]
                img_orig[..., 0] += img_orig[..., 2]
                img_orig = img_orig[..., 0] / 3
                # img_orig = img_orig[..., 0] / 2
                img_orig = np.reshape(img_orig, (*img_orig.shape, 1))
                # print('4', img_orig.shape)
            else:
                print('normal mode')
            #else nothing to do --> full mode
        else:
            print('normal mode')



        differing_bonds = np.zeros_like(img_orig)


        # if False:
        # binarise dark bg watershed masks
        # if mode is not None and 'ast' in mode:
        #     img_orig = segment_cells(img_orig, min_threshold=0.02,
        #                                      min_unconnected_object_size=3)  # self.binarise(img_orig[..., 0], threshold=autothresholds[0])
        # else:
        img_orig[..., 0] = segment_cells(img_orig[..., 0], min_threshold=0.02, min_unconnected_object_size=3) #self.binarise(img_orig[..., 0], threshold=autothresholds[0])

        if img_orig.shape[-1]>=5:
            # print('2', img_orig.shape)
            img_orig[..., 1] = segment_cells(img_orig[..., 1], min_threshold=0.06, min_unconnected_object_size=6) #self.binarise(img_orig[..., 1], threshold=autothresholds[1])
            img_orig[..., 2] = segment_cells(img_orig[..., 2],min_threshold=0.15, min_unconnected_object_size=12) #, __VISUAL_DEBUG=True #self.binarise(img_orig[..., 2], threshold=autothresholds[2])
            #
            # plt.imshow(img_orig[..., 2])
            # plt.title('deblob')
            # plt.show()


            # plt.imshow(img_orig[..., 1])
            # plt.show()
            # plt.imshow(img_orig[..., 2])
            # plt.show()

            # binarise white bg watershed masks
            img_orig[..., 3] = Img.invert(img_orig[..., 3])
            img_orig[..., 3] = segment_cells(img_orig[..., 3],min_threshold=0.06, min_unconnected_object_size=6)#self.binarise(img_orig[..., 3], threshold=autothresholds[3])
            img_orig[..., 4] = Img.invert(img_orig[..., 4])
            img_orig[..., 4] = segment_cells(img_orig[..., 4],min_threshold=0.15, min_unconnected_object_size=12)#self.binarise(img_orig[..., 4], threshold=autothresholds[4])

        if img_orig.shape[-1]==7:
            # binarise dark bg seeds
            # img_orig[..., 5] = segment_cells(img_orig[..., 5], stop_at_threshold_step=True, window_size=59)#self.binarise(img_orig[..., 5], threshold=autothresholds[5])
            img_orig[..., 5] = self.binarise(img_orig[..., 5], threshold=0.15)
            # block_size = 59
            # from skimage.filters import threshold_otsu, threshold_local
            # img_orig[..., 5] = (img_orig[..., 5] > threshold_local(img_orig[..., 5], block_size)).astype(np.uint8)*255

            # plt.imshow(img_orig[..., 5])
            # plt.show()

            # binarise white bg seeds
            img_orig[..., 6] = Img.invert(img_orig[..., 6])
            # img_orig[..., 6] = segment_cells(img_orig[..., 6], stop_at_threshold_step=True, window_size=59)#self.binarise(img_orig[..., 6], threshold=autothresholds[6])
            img_orig[..., 6] = self.binarise(img_orig[..., 6], threshold=0.1)
            # img_orig[..., 6] = (img_orig[..., 6] > threshold_local(img_orig[..., 6], block_size)).astype(np.uint8)*255
            # plt.imshow(img_orig[..., 6])
            # plt.show()

        if _DEBUG:
            Img(img_orig, dimensions='hwc').save(os.path.join(output_folder, 'thresholded_masks.tif'))

        # get watershed mask for all images
        for i in range(img_orig.shape[-1]):
            if i < 5:
                final_seeds = label(Img.invert(img_orig[..., i]), connectivity=1, background=0)
            else:
                final_seeds = label(img_orig[..., i], connectivity=None, background=0)
            final_wshed = watershed(bckup_img_wshed, markers=final_seeds, watershed_line=True)
            final_wshed[final_wshed != 0] = 1
            final_wshed[final_wshed == 0] = 255
            final_wshed[final_wshed == 1] = 0

            # s = ndimage.generate_binary_structure(2, 1)
            # final_wshed = ndimage.grey_dilation(final_wshed, footprint=s)
            differing_bonds[..., i] = final_wshed

            if _VISUAL_DEBUG:
                plt.imshow(img[..., i])
                plt.show()

            del final_seeds
            del final_wshed

        if _DEBUG:
            print(os.path.join(output_folder, 'differences.tif'))
            Img(differing_bonds, dimensions='hwc').save(os.path.join(output_folder, 'differences.tif'))
            Img(bckup_img_wshed, dimensions='hw').save(os.path.join(output_folder, 'orig_img.tif'))

        # avg
        # if differing_bonds.shape[-1]>1:
        avg = np.mean(differing_bonds, axis=-1)
        # else:
        #     avg = differing_bonds
        avg = avg / avg.max()

        if _DEBUG:
            Img(avg, dimensions='hw').save(os.path.join(output_folder, output_name+ str('avg.tif')))


        if threshold is None:
            threshold = self.autothreshold(avg)


        # should I use local thresholds ??? could so the same
        logger.info('threshold used for producing the final mask=' + str(threshold))

        final_mask = avg.copy()
        final_mask = self.binarise(final_mask, threshold=threshold)

        if _DEBUG:
            Img(final_mask, dimensions='hw').save(os.path.join(output_folder, 'binarized.tif'))

        # close wshed mask to fill super tiny holes
        s = ndimage.generate_binary_structure(2, 1)
        final_mask = ndimage.grey_dilation(final_mask, footprint=s)

        # remove super tiny artificial cells (very small value cause already dilated)
        mask = label(Img.invert(final_mask), connectivity=1, background=0)
        for region in regionprops(mask):
            if region.area < 5:
                for coordinates in region.coords:
                    final_mask[coordinates[0], coordinates[1]] = 255
        del mask

        final_mask = label(Img.invert(final_mask), connectivity=1, background=0)
        final_mask = watershed(bckup_img_wshed, markers=final_mask, watershed_line=True)

        final_mask[final_mask != 0] = 1
        final_mask[final_mask == 0] = 255
        final_mask[final_mask == 1] = 0

        # remove all post process to keep things simpler
        # fast enough anyway that nothing needs be done
        # finalize doc fully

        # finalize full code
        if filter is None or filter==0:
        # if _DEBUG:
        #     print('saving', os.path.join(output_folder, output_name))
        #     Img(final_mask.astype(np.uint8), dimensions='hw').save(os.path.join(output_folder, output_name))
            return final_mask.astype(np.uint8)

        # return avg

        # not clear the code works well but it's ok
        # pas clair que ça marche bien --> le cutoff par taille donne pas mal d'erreurs en fait
        # faudrait regarder le code ne profondeur et voir ce que je garde
        # voir comment faire mais je pense que je vais faire comme ça, mais est ce que je garde le vieux modèle ou pas ??? --> il est globalement bien plus mauvais en tout points
        # est-ce que je tente de garder le filtering ou pas ???

        # get the filter parameters and see
        else:
            logger.debug('Further filtering image')
            return FilterMask(bckup_img_wshed, final_mask, filter=filter, correction_factor=correction_factor) # en fait le filtre domine sur le restore most likely cells but maybe change that some day??? --> see how I can do that and restore the code

        # TODO maybe recreate a watershed after heavily thresholding to restore damaged bonds and use that after score of the original --> good idea --> à tester

        # pas trop mal

    def autothreshold(self, single_2D_img):
        return threshold_otsu(single_2D_img)

    # TODO improve and allow for copy of image and move to the Img class or at least file
    def binarise(self, single_2D_img, threshold=0.5, bg_value=0, fg_value=255):
        # TODO may change this to >= and < try it
        single_2D_img[single_2D_img > threshold] = fg_value
        single_2D_img[single_2D_img <= threshold] = bg_value
        return single_2D_img


# now run for all and see what it does
# TODO need add output name --> allow it to loop over several images
if __name__ == '__main__':
    from timeit import default_timer as timer

    start = timer()

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
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/20190924_ecadGFP_400nM20E_000.tif')
    # img = Img('/home/aigouy/Bureau/tests_dual_resolution/predict/disc_0002_DCAD.tif')
    # should I keep the old codes can the secure cells be those of

    # root_path = '/home/aigouy/Bureau/test_plants/raw_images_denoiseg/predict/'  # 3
    # root_path = '/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/predict2/'  # 3
    # root_path = '/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/predict2/predict/'  # 3
    # root_path = '/D/final_folder_scoring/predict/'  # 3
    # root_path = '/home/aigouy/Bureau/test_plants/predict/'  # 3
    # root_path = '/D/final_folder_scoring/predict_hybrid/'  # 3
    # root_path = '/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/'  # 3
    root_path = '/D/final_folder_scoring/predict_test_of_bg_subtraction/'  # 3
    # root_path = '/home/aigouy/Dropbox/seg_vertebrate_full_resolution_actin/optimized_projection_1above_2_below/predict/'  # 3
    # root_path = '/home/aigouy/Bureau/test_plants/predict/'  # 3
    # root_path = '/D/Sample_images/sample_images_PA/test_pedro/predict/'  # 3
    # root_path = '/home/aigouy/Dropbox/seg_vertebrate_full_resolution_actin/optimized_projection_2above_4_below/predict/'  # 3
    # root_path = '/home/aigouy/Dropbox/seg_vertebrate_full_resolution_actin/optimized_projection_1above_2_below/predict/'  # 3
    # root_path = '/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/'  # 3
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317_rot_HQ_only/' #4

    import glob
    from natsort import natsorted

    list_of_files = glob.glob(root_path + "*.png") + glob.glob(root_path + "*.jpg") + glob.glob(
        root_path + "*.jpeg") + glob.glob(
        root_path + "*.tif") + glob.glob(root_path + "*.tiff")+ glob.glob(root_path + "*.lsm")+ glob.glob(root_path + "*.czi") + glob.glob(root_path + "*.lif")
    list_of_files = natsorted(list_of_files)

    # list_of_files=['/home/aigouy/Bureau/test_plants/raw_images_denoiseg/predict/0.tif']
    # list_of_files=['/home/aigouy/Bureau/test_plants/raw_images_denoiseg/predict/10.tif']
    # list_of_files=['/home/aigouy/Bureau/test_plants/raw_images_denoiseg/predict/6.tif']
    # list_of_files=['/home/aigouy/Bureau/test_plants/raw_images_denoiseg/predict/16.tif'] # pas trop mal non plus --> meme si threshold un peu plus haut serait bien...
    #
    # list_of_files=['/home/aigouy/Bureau/tests_dual_resolution/predict/0.tif']
    # list_of_files=['/D/Sample_images/sample_images_PA/test_pedro/predict/100708_png06_mean_all.tif', '/D/Sample_images/sample_images_PA/test_pedro/predict/100708_png06_max_all.tif', '/D/Sample_images/sample_images_PA/test_pedro/predict/Bro43_avproj0000.tif']
    # list_of_files=['/D/Sample_images/sample_images_PA/test_pedro/predict/100708_png06_mean_all.tif']# not so much better now in fact --> is that really better ???
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_ok_2.tif']


    # fig 1 paper test list_of_files=['/D/VirtualBox/final_paper_deep_learning/new_figures/new_figure_model/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_ok_2.tif'] # paper fig one

    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/5.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/100708_png06.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/100708_png07.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/Bro43_avproj0000.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/Bro43_avproj0001.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/Optimized_projection_018.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/MAX_ECadGFP_120410_2_090.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/11.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/12.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/122.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/focused_Series194.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/focused_Series010.tif'] # qq micros erreurs --> can I fix that withthe other algo ???
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/focused_Series016.tif'] # qq micros erreurs --> can I fix that withthe other algo ???
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/focused_Series031.tif'] # qq micros erreurs --> can I fix that withthe other algo ??? # maybe try reconnect very long bonds --> check
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/20190924_ecadGFP_400nM20E_000.tif'] # qq micros erreurs --> can I fix that withthe other algo ??? # maybe try reconnect very long bonds --> check
    # TODO --> probably need further fix of the stuff that creates fake watershed errors --> TODO

    # avec score 0.22 --> pas si mal en fait
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/cellpose_img22.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/T21a920000.tif']
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/StackFocused_Endocad-GFP(6-12-13)#19_000.tif'] # terrible # it is kinda ok!!!
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/Bro43_avproj0000.tif'] # terrible # it is kinda ok!!!
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/Bro43_avproj0001.tif'] # terrible # it is kinda ok!!!
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/StackFocused_Endocad-GFP(6-12-13)#19_400.tif'] # not that bad
    # ce truc est vraiment pas mal mais est-ce que je peux avoir ça
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/C3-E9 WT ppMLCV YAPcy5 actinR 2.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    # list_of_files=['/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/image_plant_best-zoomed.tif'] # very good already

    # windows tests
    # list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/5.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    # list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/11.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    # list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/12.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    # list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/122.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/100708_png06.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    # list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/cellpose_img22.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    # list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/focused_Series194.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix
    # list_of_files=['D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/Bro43_avproj0000.tif'] # new is a bit more sensitive --> compare old n new maybe --> if I can get rid of wshed artifacts then new would be better --> see how --> maybe super tiny bonds --> to fix

#     list_of_files=['/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png06.tif',
# '/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png07.tif',
# '/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/AVG_070219.lif - Series0020000.tif',
# '/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/cellpose_img08.tif',
# '/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/cellpose_img18.tif',
# '/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/cellpose_img21.tif']

    # list_of_files = ['/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/AVG_070219.lif - Series0020000.tif']
    # list_of_files = ['/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/AVG_070219.lif - Series0020000.tif']
    # list_of_files = ['/D/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/cellpose_img08.tif']

    # call it from other code

    # maybe dissociate the code for thresholding and the code for the avg so that I can produce what I need and ease stuff
    # ask whether interactive

    # test glob and quantif all

    for file in list_of_files:
        loop_time = timer()
        img = Img(file)
        # print(img.shape)
        print('processing', file)
        filename0_without_path = os.path.basename(file)

        # maybe always use this default threshold
        # pas mal mais perd bcp des super tiny cells!!!
        # 'fault' --> 6 secs # 275 secs
        # None --> 8 secs # 258 --> faster than the other ????
        # 'fast' --> 2 secs # 58 secs

        # full is better and fast average of 3 is a good alternative
        
        post_proc = RefineMaskUsingSeeds().process(input=img, mode=None, restore_safe_cells=True, _DEBUG=True, _VISUAL_DEBUG=True,
                                         output_folder='/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/', output_name=filename0_without_path, threshold=None)# threshold=0.24 # threshold=0.42773438

        print('\n\nloop duration', timer() - loop_time)
        plt.imshow(post_proc)
        plt.show()
        Img(post_proc, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/final_wshed.tif')
    # tester les scores pr voir si ok ou pas

    print('total duration', timer() - start)

    # nouvel algo est meilleur que ancien

    # TODO run the score for all but seems great

    # should I remove all other codes and model
    # if always better then remove all other parameters
    # then really need do the score and offer parameter selection
    # maybe offer three or 4 thresholds and ask user to select one
    # maybe plot the image too so that people can see score
    # try original wshed


    # it does not work better for the vertebrate epiboly stuff --> maybe due to threshold --> try with better default parameters
