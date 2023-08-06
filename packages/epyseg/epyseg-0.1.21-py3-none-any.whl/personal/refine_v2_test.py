from epyseg.img import Img
from matplotlib import pyplot as plt
import os

# logging
from epyseg.postprocess.refine_v2 import RefineMaskUsingSeeds
from epyseg.tools.logger import TA_logger

logger = TA_logger()

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
