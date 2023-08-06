# TODO train a classic CARE with a Nan filtering --> TODO
# TODO try retrain with that... --> TODO
from matplotlib import pyplot as plt
import numpy as np
from epyseg.img import Img

# TODO keep this for me and not for the users --> in a separate class
from epyseg.deeplearning.augmentation import meta

# fair un minimal dataset en utilisant mon test set et voir si meilleur
from epyseg.tools.logger import TA_logger

logger = TA_logger()  # logging_level=TA_logger.DEBUG

RAPHAEL_FULL_WING_NEED_CROP = '/D/Sample_images/sample_images_PA/trash_test_mem/raphael_fucked_hand_correction/custom_bckup/'
HISTOBLAST_SMALL_DAIKI = '/D/Sample_images/sample_images_PA/trash_test_mem/test_daiki/'
# XENOPUS_COOL = '/D/Sample_images/sample_images_PA/trash_test_mem/test_xenope/' # NEED fix segmentation but cool
# ADD THOSE WHEN READY MAY MAKE THE MODEL MUCH MORE ROBUST
# RIVELINE_CELLS_NEED_CORRECT_MASK_BUT_COOL = '/D/Sample_images/sample_images_PA/riveline_images/'
# ARTIFICIAL_TISSUE = '/D/Sample_images/sample_images_PA/artificial_tissue_images_SampleMovie/' # SHOULD I ADD IT ???
# BALLAND_CELLS_COOL_BUT_NEEDS_CORRECT_MASK = '/D/Sample_images/sample_images_PA/balland/'
DAIKI_HISTO_SMALL = '/D/Sample_images/sample_images_PA/Daiki_histo2/'
NICE_ECAD_STAINING_FULL_WING_DISK = '/D/Sample_images/sample_images_PA/autotdetect_flipout_clone/disc_0003/'  # need take red only
POLARITY_ME = '/D/Sample_images/sample_images_PA/coarse_grain/'
FUCKING_SPOTS = '/D/Sample_images/sample_images_PA/fucking_spots/'
FULL_RAPHAEL_WING_BUT_HOLES_IN_MASK = '/D/Sample_images/sample_images_PA/new_tracking_algorithm/'
KUBA_REAL_CORTEX = '/D/Sample_images/sample_images_PA/kuba_synthetic_cortex/real_cortex/'  # need analyze red channel
ANOTHER_FULL_WING_RAPHAEL = '/D/Sample_images/sample_images_PA/test_complete_wing_raphael/'
HISTOBLAST_ME = '/D/Sample_images/sample_images_PA/test_histo_with_errors/orig_bckup/'  # need only take green channel --> optimize this
# HISTOBLAST_ME_AUG = DataGenerator(HISTOBLAST_ME, input_channel_of_interest=1, REDUCE_LIST_BY_AMOUNT=REDUCE_LIST_BY_AMOUNT, MAX_NB_IMAGES_PER_SET=MAX_NB_IMAGES_PER_SET, augment_methods=SELECTED_AUGMENTATION, mask_dilations=dilation)

# ZEBRAFISH_PEDRO = '/D/Sample_images/sample_images_PA/test_pedro/' # TODO --> do the segmentation but really cool and different zooms too
# DROSOPHILA_SYNTHETIC_POLARITY = '/D/Sample_images/sample_images_PA/test_polarity/' # need check masks but could be cool too
# DROSOPHILA_POLARITY_FULL_WING = '/D/Sample_images/sample_images_PA/test_polarity_coarse/' # single image but full wing --> cool
# DROSOPHILA_WING_CLONE_ANDREAS_MULTICHANNEL = '/D/Sample_images/sample_images_PA/clones_to_ROI_and_back/reta/' # need only take green channel
# DROSOPHILA_WING_CLONE_DAIKI_MULTICHANNEL ='/D/Sample_images/sample_images_PA/clones_to_ROI_and_back/sample_daiki_crash/' # need only take green channel
# DROSOPHILA_WING_CLONE_UNKNOWN_MULTICHANNEL = '/D/Sample_images/sample_images_PA/clones_to_ROI_and_back/mask_to_ROI/'
DROSOPHILA_POLARITY_ANDREAS_SINGLE_COOL_IMAGE = '/D/Sample_images/sample_images_PA/trash_hair_orientation/'
DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_1 = '/D/Sample_images/sample_images_PA/trash_spots_tracking/1/'  # TO CHECK
DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_2 = '/D/Sample_images/sample_images_PA/trash_spots_tracking/2/'  # TO CHECK
DROSOPHILA_EMBRYO_ROSETTES_FULLSET_SPINNING = '/D/Sample_images/sample_images_PA/trash_test_mem/rosettes/rosettes_complete_movie/'  # need crop only the middle cause a lot of errors in claudio's segmentation
DROSOPHILA_PUPAL_WING_L3_ME_FULLSET = '/D/Sample_images/sample_images_PA/trash_test_mem/complete/'  # need convert images to white
DROSOPHILA_PUPAL_WING_DRESDEN_ORIG = '/D/Sample_images/sample_images_denoiseg/train/raw/'
DROSOPHILA_PUPAL_WING_DRESDEN_GT = '/D/Sample_images/sample_images_denoiseg/train/GT/'
# DROSOPHILA_PUPAL_WING_L3_ME_FULLSET_AUG = DataGenerator(DROSOPHILA_PUPAL_WING_L3_ME_FULLSET, input_channel_of_interest=1, REDUCE_LIST_BY_AMOUNT=REDUCE_LIST_BY_AMOUNT, MAX_NB_IMAGES_PER_SET=MAX_NB_IMAGES_PER_SET, augment_methods=SELECTED_AUGMENTATION, mask_dilations=DILATION)
# masks need be cleaned --> ground truth sucks
# DROSOPHILA_EGG_CHAMBERS = '/D/Sample_images/sample_images_PA/trash_test_mem/egg_chambers/' # masks need be cleaned --> ground truth sucks
DROSOPHILA_FULL_WING_PUPA_LATE = '/D/Sample_images/sample_images_PA/trash_test_mem/full_wing_multi/late_stages/'
DROSOPHILA_FULL_WING_PUPA_MID = '/D/Sample_images/sample_images_PA/trash_test_mem/full_wing_multi/mid_stages/'
DROSOPHILA_FULL_WING_PUPA_EARLY = '/D/Sample_images/sample_images_PA/trash_test_mem/full_wing_multi/early_stages/'  # need crop them to images 512*512 for training
DROSOPHILA_WING_DISC = '/D/Sample_images/sample_images_PA/trash_test_natalie/custom_bckup_first10_corrected/'
DROSOPHILA_EMBRYO_SPINNING = '/D/Sample_images/sample_images_PA/claudio_T1s_full_embryo/'  # ---> handCorrection.tif this time --> need make images white if they aren't maybe pop data to avoid pbs
CLEANED_XENOPUS = '/D/Sample_images/new_train_sample/minimal_smart_train_sample/xenopus/'  # ---> handCorrection.tif this time --> need make images white if they aren't maybe pop data to avoid pbs
# DROSOPHILA_EMBRYO_SPINNING_AUG = DataGenerator(DROSOPHILA_EMBRYO_SPINNING, REDUCE_LIST_BY_AMOUNT=REDUCE_LIST_BY_AMOUNT, MAX_NB_IMAGES_PER_SET=MAX_NB_IMAGES_PER_SET, crop_parameters={'x1': 344, 'y1': 182, 'x2': 976, 'y2': 356}, augment_methods=SELECTED_AUGMENTATION, mask_dilations=DILATION) # need crop cause poor seg quality from Claudio's data
PUPAL_WING_WINDOW_DENOISED = '/D/Sample_images/sample_images_PA/trash_test_mem/tracking_test_set_rapha/'
# PUPAL_WING_WINDOW_DENOISED_AUG = DataGenerator(PUPAL_WING_WINDOW_DENOISED, REDUCE_LIST_BY_AMOUNT=REDUCE_LIST_BY_AMOUNT, MAX_NB_IMAGES_PER_SET=MAX_NB_IMAGES_PER_SET, crop_parameters={'x1': 325, 'y1': 420, 'x2': 616, 'y2': 565}, augment_methods=SELECTED_AUGMENTATION, mask_dilations=DILATION)

OVIPO_FROM_MANUE_1 = "/D/Sample_images/sample_images_PA/Analysed Ovipo Jack's paper/07_2/Analyse/T24àT124/Images T24a124/"  # TODO check and add more and clean # and create an augmenter for that
# OVIPO_FROM_MANUE_1_AUG = DataGenerator(OVIPO_FROM_MANUE_1, REDUCE_LIST_BY_AMOUNT=REDUCE_LIST_BY_AMOUNT, MAX_NB_IMAGES_PER_SET=MAX_NB_IMAGES_PER_SET, augment_methods=SELECTED_AUGMENTATION, mask_dilations=dilation)
OVIPO_FROM_MANUE_2 = "TODO AND CLEAN"  # TODO check and add more and clean
OVIPO_FROM_MANUE_3 = "TODO AND CLEAN"  # TODO check and add more and clean

# the output folders
TRAINING_OUTPUT_FOLDER = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/'
TRAINING_IMAGE_SET = TRAINING_OUTPUT_FOLDER + 'images_prepped_train/'
TRAINING_ANNOTATION_SET = TRAINING_OUTPUT_FOLDER + 'annotations_prepped_train/'


# en fait c'est ce truc qui va gerer plusieurs augmenters --> c'est super utile pr entrainer un modele

# all augmentations seem fine for 2D --> but check for 3D


# ALL_AUGMENTATIONS_BUT_INVERT = [None, None, DataGenerator.zoom, DataGenerator.blur, DataGenerator.translate,
#                                 DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]

# can i do true pos and neg based on IOU between ROIs ???? --> yes I think so --> should be doable in fact --> need get same shapes and do IOU on them --> just need to get their mask and compare them without changing image


# augs meta.ALL_AUGMENTATIONS_BUT_INVERT_AND_HIGH_NOISE
# TODO add parameters so that I can handle stuff better such as model input and or output size
def get_epithelia_data_augmenter(input_shape=None, output_shape=None, batch_size=None,
                                 augmentations=meta.MINIMAL_AUGMENTATIONS, mask_dilations=None,
                                 create_epyseg_style_output=None,
                                 **kwargs):

    input_normalization = {'method': 'Rescaling (min-max normalization)', 'range': [0, 1],
                           'individual_channels': True}
    output_normalization = {'method': 'Rescaling (min-max normalization)', 'range': [0, 1],
                            'individual_channels': True}
    # normalization = None
    shuffle = True
    clip_by_frequency = (0.01, 0.01)

    # DILATION = None
    # dilation = None #1

    # print('here', kwargs)

    default_output_tile_width = default_output_tile_height = 128  # 256
    default_input_tile_width = default_input_tile_height = 128  # 256

    # TODO implement below for several inputs and outputs some day
    if input_shape is not None:
        if input_shape[0][-2] is not None:
            default_input_tile_width = input_shape[0][-2]
        if input_shape[0][-3] is not None:
            default_input_tile_height = input_shape[0][-3]

    if output_shape is not None:
        if output_shape[0][-2] is not None:
            default_output_tile_width = output_shape[0][-2]
        if output_shape[0][-3] is not None:
            default_output_tile_height = output_shape[0][-3]

    # if default_input_tile_width is None:
    #     default_input_tile_width = 256
    #
    # if default_output_tile_height is None:
    #     default_output_tile_height = 256

    # batch_size_limit_for_training = 16 # 10  # URGENT TODO --> THAT REALLY SUCKS --> RATHER NEED USE A FIXED BATCH SIZE THAT CAN MIX IMAGES FROM DIFFERENT SETS BY THE WAY
    fixed_batch_size = 32  # 24  # 16  # 16 # 32
    if batch_size is not None:
        fixed_batch_size = batch_size

    # print('default params', batch_size, default_input_tile_width, default_input_tile_height,
    #       default_output_tile_width, default_output_tile_height)

    # input_shape = (None, None, None, 3) #(None, None, None, 3)
    # we set the global parameters for augmentation
    # augment_methods = NO_AUGMENTATION.

    # same bug for zoom/shear/translate not for gaussian nor rotate nor flip nor None --> where is the bug
    # augment_methods = ALL_AUGMENTATIONS_BUT_INVERT  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augmentations = meta.ALL_AUGMENTATIONS  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augment_methods = TEST_AUGMENTATION  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]


    # just for a test --> reactivate below too...
    # MEGA TODO deactivate this ASAP --> but just try for one training
    # MAYBE TRY BCE JACCARD TOO --> do a custom BCE jaccard
    mask_lines_and_cols_in_input_and_mask_GT_with_nans = None # 'id'

    metaAugmenter = meta.MetaAugmenter(augmentations=augmentations,
                                       input_shape=input_shape, output_shape=output_shape,
                                       # input_shape=input_shape, # force 1 or 3 channels input
                                       is_predict_generator=False,
                                       # batch_size_limit_for_training=batch_size_limit_for_training,
                                       batch_size=fixed_batch_size,
                                       input_normalization=input_normalization,
                                       output_normalization=output_normalization,
                                       shuffle=shuffle,
                                       clip_by_frequency=clip_by_frequency,
                                       default_output_tile_width=default_output_tile_width,
                                       default_output_tile_height=default_output_tile_height,
                                       default_input_tile_width=default_input_tile_width,
                                       default_input_tile_height=default_input_tile_height,
                                       mask_dilations=mask_dilations,
                                       create_epyseg_style_output=create_epyseg_style_output,
                                       rotate_n_flip_independently_of_augmentation=True,
                                       mask_lines_and_cols_in_input_and_mask_GT_with_nans=mask_lines_and_cols_in_input_and_mask_GT_with_nans,
                                       )
    # , default_output_tile_width=default_output_tile_width, default_output_tile_height=default_output_tile_height) #

    # TODO URGENT a tester https://github.com/nibtehaz/MultiResUNet/blob/master/MultiResUNet.py
    # augment_methods = ALL_AUGMENTATIONS,

    # add it several different images
    # TODO test it

    # HISTOBLAST_ME_AUG = DataGenerator(HISTOBLAST_ME, input_channel_of_interest=1, augment_methods=SELECTED_AUGMENTATION, mask_dilations=dilation)
    # tester ça

    # infinite=True,

    # we add data to the augmenter

    # TODO add more including zebra and cell culture

    # not bad --> give it a try as a training ???? --> then test

    # BAD/NOT GREAT DATASETS
    # metaAugmenter.append(FULL_RAPHAEL_WING_BUT_HOLES_IN_MASK, input_channel_of_interest=0, crop_parameters={'x1': 324, 'y1': 1548, 'x2': 1728, 'y2': 3716})
    # metaAugmenter.append(DROSOPHILA_POLARITY_ANDREAS_SINGLE_COOL_IMAGE, input_channel_of_interest=1)
    # metaAugmenter.append(KUBA_REAL_CORTEX, input_channel_of_interest=0)  # TODO
    # metaAugmenter.append(HISTOBLAST_SMALL_DAIKI)
    # metaAugmenter.append(NICE_ECAD_STAINING_FULL_WING_DISK, input_channel_of_interest=0, crop_parameters={'x1': 788, 'y1': 868, 'x2': 3036, 'y2': 2300})
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_EARLY, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # NB THERE IS A BUG IN THE DATASET --> THE MASK DOES NOT MATCH THE SEG
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_LATE, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # TODO incomplete wing seg

    # POLARITY DATASETS
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_1, input_channel_of_interest=1)
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_2, input_channel_of_interest=1)
    # metaAugmenter.append(POLARITY_ME, input_channel_of_interest=1, crop_parameters={'x1': 45, 'y1': 291, 'x2': 1716, 'y2': 1596})
    # metaAugmenter.append(FUCKING_SPOTS, input_channel_of_interest=0)  # is that really smart to have the spots ????

    # GOOD DATASETS

    # minimal list of goods
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,

    metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_DRESDEN_ORIG,
                         outputs=DROSOPHILA_PUPAL_WING_DRESDEN_GT)  # is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET, input_channel_of_interest=1,
                         crop_parameters={'x1': 0, 'y1': 64, 'x2': 512 - 64,
                                          'y2': 512})  # is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    metaAugmenter.append(inputs=HISTOBLAST_ME,
                         input_channel_of_interest=1)  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 344, 'y1': 182, 'x2': 976,'y2': 356})  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 625, 'y1': 0, 'x2': 625 + 540,
                                                                             'y2': 0 + 540})  # remove crop to better segment this shit...
    metaAugmenter.append(inputs=CLEANED_XENOPUS, crop_parameters={'x1': 0, 'y1': 0, 'x2': 432,
                                                                  'y2': 532})  # added a simpler crop to better segment this that also includes cells at the perihphery

    # metaAugmenter.append(inputs=PUPAL_WING_WINDOW_DENOISED)

    # full list of good datasets
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_ROSETTES_FULLSET_SPINNING, crop_parameters={'x1': 396, 'y1': 230, 'x2': 1100, 'y2': 396})
    # metaAugmenter.append(inputs=ANOTHER_FULL_WING_RAPHAEL, crop_parameters={'x1': 255, 'y1': 324, 'x2': 3310, 'y2': 1533})
    # metaAugmenter.append(inputs=DAIKI_HISTO_SMALL, input_channel_of_interest=1)
    # metaAugmenter.append(inputs=RAPHAEL_FULL_WING_NEED_CROP, input_channel_of_interest=0, crop_parameters={'x1': 576, 'y1': 501, 'x2': 3456, 'y2': 1332})
    # metaAugmenter.append(inputs=DROSOPHILA_FULL_WING_PUPA_MID, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296})
    # metaAugmenter.append(inputs=DROSOPHILA_WING_DISC, crop_parameters={'x1': 533, 'y1': 196, 'x2': 830, 'y2': 720})

    # metaAugmenter.append(OVIPO_FROM_MANUE_1, crop_parameters={'x1': 325, 'y1': 420, 'x2': 616, 'y2': 565})

    return metaAugmenter


def make_TA_compatible():
    input_folder = '/D/Sample_images/sample_images_denoise_manue/fullset_Manue/Ovipositors/200319/GT/predict/predict_model_nb_0/predict/'
    # list all image files and rename them as handCorrection.tif --> should work
    import os
    import traceback
    from shutil import copyfile

    input1 = os.listdir(input_folder)
    input1 = [os.path.join(input_folder, f) for f in input1]
    for inp in input1:

        if os.path.isfile(inp):
            if inp.lower().endswith('.tif') or inp.lower().endswith('.tiff'):
                filename0_without_path = os.path.basename(inp)
                filename0_without_ext = os.path.splitext(filename0_without_path)[0]
                parent_dir_of_filename0 = os.path.dirname(inp)

                try:
                    print(inp, '-->', os.path.join(parent_dir_of_filename0, filename0_without_ext, 'handCorrection.tif'))
                    img = Img(inp)
                    # output --> same folder but different name
                    Img(img).save(os.path.join(parent_dir_of_filename0, filename0_without_ext, 'handCorrection.tif'))
                except:
                    traceback.print_exc()
                    pass





def copy_clean_files_to_drive():
    import os
    from shutil import copyfile


    data = [DROSOPHILA_PUPAL_WING_DRESDEN_ORIG,
    DROSOPHILA_PUPAL_WING_DRESDEN_GT,
    DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,
    HISTOBLAST_ME,
    DROSOPHILA_EMBRYO_SPINNING,
    CLEANED_XENOPUS]

    output_dir = '/D/Sample_images/_trash_cleaned_training_set'
    extensions=['.tif','.png']

    for folder in data:
        # list folder and copy just some of the files while just keeping the architecture
        # list of files

        input1 = os.listdir(folder)
        input1 = [os.path.join(folder, f) for f in input1]
        # print(input1)

        for inp in input1:

            if os.path.isdir(inp):
                if os.path.exists(os.path.join(inp,'handCorrection.tif')):
                    folder_name = os.path.basename(os.path.dirname(os.path.join(inp,'handCorrection.tif')))
                    folder_name2 = os.path.basename(os.path.dirname(os.path.dirname(os.path.join(inp,'handCorrection.tif'))))
                    # print('folder_name2', folder_name2, 'folder_name', folder_name)

                    os.makedirs(os.path.join(os.path.join(output_dir,folder_name2), folder_name), exist_ok=True)
                    dest = os.path.join(os.path.join(output_dir,folder_name2), folder_name, os.path.basename(os.path.join(inp,'handCorrection.tif')))
                    copyfile(os.path.join(inp,'handCorrection.tif'), dest)
                    print(os.path.join(inp,'handCorrection.tif'),'-->', dest)
                elif os.path.exists(os.path.join(inp,'handCorrection.png')):
                    folder_name = os.path.basename(os.path.dirname(os.path.join(inp, 'handCorrection.png')))
                    folder_name2 = os.path.basename(os.path.dirname(os.path.dirname(os.path.join(inp,'handCorrection.png'))))
                    os.makedirs(os.path.join(os.path.join(output_dir,folder_name2), folder_name), exist_ok=True)

                    dest = os.path.join(os.path.join(output_dir,folder_name2), folder_name,
                                        os.path.basename(os.path.join(inp, 'handCorrection.png')))
                    copyfile(os.path.join(inp, 'handCorrection.png'), dest)
                    print(os.path.join(inp, 'handCorrection.png'), '-->', dest)
            elif inp.lower().endswith(extensions[0]) or inp.lower().endswith(extensions[1]):
                folder_name = os.path.basename(os.path.dirname(inp))
                os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)
                dest = os.path.join(output_dir, folder_name, os.path.basename(inp))
                copyfile(inp, dest)
                print(inp,'-->', dest)

def get_CARESEG_data_augmenter(input_shape=None, output_shape=None, batch_size=None,
                               augmentations=meta.MINIMAL_AUGMENTATIONS, mask_dilations=None,
                               create_epyseg_style_output=None,
                               **kwargs):
    input_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                           'individual_channels': True, 'clip': False}
    output_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                            'individual_channels': True, 'clip': False}
    # normalization = None
    shuffle = True
    clip_by_frequency = None  # (0.02, 0.002) # is that actually the same as CARE ????

    # DILATION = None
    # dilation = None #1

    # print('here', kwargs)

    default_output_tile_width = default_output_tile_height = 128 # 256
    default_input_tile_width = default_input_tile_height = 128 # 256

    # just a hack to try no crop to avoid issues of adding black pixels that may impact learning maybe ???
    # default_output_tile_width = default_input_tile_width = 224
    # default_output_tile_height = default_input_tile_height = 80

    # TODO implement below for several inputs and outputs some day
    if input_shape is not None:
        if input_shape[0][-2] is not None:
            default_input_tile_width = input_shape[0][-2]
        if input_shape[0][-3] is not None:
            default_input_tile_height = input_shape[0][-3]

    if output_shape is not None:
        if output_shape[0][-2] is not None:
            default_output_tile_width = output_shape[0][-2]
        if output_shape[0][-3] is not None:
            default_output_tile_height = output_shape[0][-3]

    # if default_input_tile_width is None:
    #     default_input_tile_width = 256
    #
    # if default_output_tile_height is None:
    #     default_output_tile_height = 256

    # batch_size_limit_for_training = 16 # 10  # URGENT TODO --> THAT REALLY SUCKS --> RATHER NEED USE A FIXED BATCH SIZE THAT CAN MIX IMAGES FROM DIFFERENT SETS BY THE WAY
    fixed_batch_size = 10  # 24  # 16  # 16 # 32
    if batch_size is not None:
        fixed_batch_size = batch_size

    # print('default params', batch_size, default_input_tile_width, default_input_tile_height,
    #       default_output_tile_width, default_output_tile_height)

    # input_shape = (None, None, None, 3) #(None, None, None, 3)
    # we set the global parameters for augmentation
    # augment_methods = NO_AUGMENTATION.

    # same bug for zoom/shear/translate not for gaussian nor rotate nor flip nor None --> where is the bug
    # augment_methods = ALL_AUGMENTATIONS_BUT_INVERT  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augmentations = meta.ALL_AUGMENTATIONS  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augment_methods = TEST_AUGMENTATION  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]

    # SELECTED_AUG = None
    # 'roll along Z (2D + GT ignored)': None,
    # 'shuffle images along Z (2D + GT ignored)': None,

    # is that even better ???
    # fake add images above or below the cell to make CARESEG 
    # but will change also max and min or percentile...
    
    SELECTED_AUG = None # [{'type': 'roll along Z (2D + GT ignored)'}] # just a test to make it less sensitive to signal position
    mask_lines_and_cols_in_input_and_mask_GT_with_nans = 'id' # should be 'id' or 'noid'
    # SELECTED_AUG = [{'type': 'mask_pixels'}] # just for a test to see if becomes even stronger in segmenting and denoising??? # does not exist anymore --> should be an option

    # metaAugmenter = meta.MetaAugmenter(augmentations=None,
    metaAugmenter = meta.MetaAugmenter(augmentations=SELECTED_AUG,
                                       input_shape=input_shape, output_shape=output_shape,
                                       # input_shape=input_shape, # force 1 or 3 channels input
                                       is_predict_generator=False,
                                       # batch_size_limit_for_training=batch_size_limit_for_training,
                                       batch_size=fixed_batch_size,
                                       input_normalization=input_normalization,
                                       output_normalization=output_normalization,
                                       shuffle=shuffle,
                                       clip_by_frequency=clip_by_frequency,
                                       default_output_tile_width=default_output_tile_width,
                                       default_output_tile_height=default_output_tile_height,
                                       default_input_tile_width=default_input_tile_width,
                                       default_input_tile_height=default_input_tile_height,
                                       rotate_n_flip_independently_of_augmentation=True,
                                       mask_lines_and_cols_in_input_and_mask_GT_with_nans=mask_lines_and_cols_in_input_and_mask_GT_with_nans
                                       # mask_dilations=mask_dilations,
                                       # create_epyseg_style_output=create_epyseg_style_output,
                                       )
    # , default_output_tile_width=default_output_tile_width, default_output_tile_height=default_output_tile_height) #

    # TODO URGENT a tester https://github.com/nibtehaz/MultiResUNet/blob/master/MultiResUNet.py
    # augment_methods = ALL_AUGMENTATIONS,

    # add it several different images
    # TODO test it

    # HISTOBLAST_ME_AUG = DataGenerator(HISTOBLAST_ME, input_channel_of_interest=1, augment_methods=SELECTED_AUGMENTATION, mask_dilations=dilation)
    # tester ça

    # infinite=True,

    # we add data to the augmenter

    # TODO add more including zebra and cell culture

    # not bad --> give it a try as a training ???? --> then test

    # BAD/NOT GREAT DATASETS
    # metaAugmenter.append(FULL_RAPHAEL_WING_BUT_HOLES_IN_MASK, input_channel_of_interest=0, crop_parameters={'x1': 324, 'y1': 1548, 'x2': 1728, 'y2': 3716})
    # metaAugmenter.append(DROSOPHILA_POLARITY_ANDREAS_SINGLE_COOL_IMAGE, input_channel_of_interest=1)
    # metaAugmenter.append(KUBA_REAL_CORTEX, input_channel_of_interest=0)  # TODO
    # metaAugmenter.append(HISTOBLAST_SMALL_DAIKI)
    # metaAugmenter.append(NICE_ECAD_STAINING_FULL_WING_DISK, input_channel_of_interest=0, crop_parameters={'x1': 788, 'y1': 868, 'x2': 3036, 'y2': 2300})
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_EARLY, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # NB THERE IS A BUG IN THE DATASET --> THE MASK DOES NOT MATCH THE SEG
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_LATE, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # TODO incomplete wing seg

    # POLARITY DATASETS
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_1, input_channel_of_interest=1)
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_2, input_channel_of_interest=1)
    # metaAugmenter.append(POLARITY_ME, input_channel_of_interest=1, crop_parameters={'x1': 45, 'y1': 291, 'x2': 1716, 'y2': 1596})
    # metaAugmenter.append(FUCKING_SPOTS, input_channel_of_interest=0)  # is that really smart to have the spots ????

    # GOOD DATASETS

    # minimal list of goods
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_DRESDEN_ORIG, outputs=DROSOPHILA_PUPAL_WING_DRESDEN_GT)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1, crop_parameters={'x1': 0, 'y1': 64, 'x2': 512-64, 'y2': 512})# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=HISTOBLAST_ME, input_channel_of_interest=1)# is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 344, 'y1': 182, 'x2': 976,'y2': 356})  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/CARE/raw/',
                         # outputs='/D/Sample_images/sample_images_denoise_manue/CARE/GT/', # doh I was so dumb... I had used the non translated version ...
                         outputs='/D/Sample_images/sample_images_denoise_manue/CARE/denoiseg_fusion/',
                         # doh I was so dumb... I had used the non translated version ...
                         # outputs='/D/Sample_images/sample_images_denoise_manue/CARE/denoiseg_fusion/', # doh I was so dumb... I had used the non translated version ...
                         # crop_parameters={'x1': None, 'y1': None, 'width': 224, 'height': 80}
                         # I have now implement random crop --> with defined width n height # # TODO try a random crop
                         # crop_parameters={'x1': 126, 'y1': 40, 'x2': 254, 'y2': 615} # non random crop for segmentation included
                         )

    # metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/210219/raw/',
    #                      outputs='/D/Sample_images/sample_images_denoise_manue/210219/denoiseg_fusion/',
    #                      # outputs='/D/Sample_images/sample_images_denoise_manue/210219/GT/',
    #                      crop_parameters={'x1': 325, 'y1': 535, 'x2': 549, 'y2': 615})

    # --> ROI x1=325, y1=535, x2=549, y2=615

    # (other stuff not this one, do delete from this file 126, 40, 254, 168)

    # metaAugmenter.append(inputs=CLEANED_XENOPUS, crop_parameters={'x1': 0, 'y1': 0, 'x2': 432, 'y2': 532}) # added a simpler crop to better segment this that also includes cells at the perihphery

    # metaAugmenter.append(inputs=PUPAL_WING_WINDOW_DENOISED)

    # full list of good datasets
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_ROSETTES_FULLSET_SPINNING, crop_parameters={'x1': 396, 'y1': 230, 'x2': 1100, 'y2': 396})
    # metaAugmenter.append(inputs=ANOTHER_FULL_WING_RAPHAEL, crop_parameters={'x1': 255, 'y1': 324, 'x2': 3310, 'y2': 1533})
    # metaAugmenter.append(inputs=DAIKI_HISTO_SMALL, input_channel_of_interest=1)
    # metaAugmenter.append(inputs=RAPHAEL_FULL_WING_NEED_CROP, input_channel_of_interest=0, crop_parameters={'x1': 576, 'y1': 501, 'x2': 3456, 'y2': 1332})
    # metaAugmenter.append(inputs=DROSOPHILA_FULL_WING_PUPA_MID, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296})
    # metaAugmenter.append(inputs=DROSOPHILA_WING_DISC, crop_parameters={'x1': 533, 'y1': 196, 'x2': 830, 'y2': 720})

    # metaAugmenter.append(OVIPO_FROM_MANUE_1, crop_parameters={'x1': 325, 'y1': 420, 'x2': 616, 'y2': 565})

    return metaAugmenter



def get_CARE_data_augmenter(input_shape=None, output_shape=None, batch_size=None,
                               augmentations=meta.MINIMAL_AUGMENTATIONS, mask_dilations=None,
                               create_epyseg_style_output=None,
                               **kwargs):
    input_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                           'individual_channels': True, 'clip': False}
    output_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                            'individual_channels': True, 'clip': False}
    # normalization = None
    shuffle = True
    clip_by_frequency = None  # (0.02, 0.002) # is that actually the same as CARE ????

    # DILATION = None
    # dilation = None #1

    # print('here', kwargs)

    default_output_tile_width = default_output_tile_height = 128 # 256
    default_input_tile_width = default_input_tile_height = 128 # 256

    # just a hack to try no crop to avoid issues of adding black pixels that may impact learning maybe ???
    # default_output_tile_width = default_input_tile_width = 224
    # default_output_tile_height = default_input_tile_height = 80

    # TODO implement below for several inputs and outputs some day
    if input_shape is not None:
        if input_shape[0][-2] is not None:
            default_input_tile_width = input_shape[0][-2]
        if input_shape[0][-3] is not None:
            default_input_tile_height = input_shape[0][-3]

    if output_shape is not None:
        if output_shape[0][-2] is not None:
            default_output_tile_width = output_shape[0][-2]
        if output_shape[0][-3] is not None:
            default_output_tile_height = output_shape[0][-3]

    # if default_input_tile_width is None:
    #     default_input_tile_width = 256
    #
    # if default_output_tile_height is None:
    #     default_output_tile_height = 256

    # batch_size_limit_for_training = 16 # 10  # URGENT TODO --> THAT REALLY SUCKS --> RATHER NEED USE A FIXED BATCH SIZE THAT CAN MIX IMAGES FROM DIFFERENT SETS BY THE WAY
    fixed_batch_size = 10  # 24  # 16  # 16 # 32
    if batch_size is not None:
        fixed_batch_size = batch_size

    # print('default params', batch_size, default_input_tile_width, default_input_tile_height,
    #       default_output_tile_width, default_output_tile_height)

    # input_shape = (None, None, None, 3) #(None, None, None, 3)
    # we set the global parameters for augmentation
    # augment_methods = NO_AUGMENTATION.

    # same bug for zoom/shear/translate not for gaussian nor rotate nor flip nor None --> where is the bug
    # augment_methods = ALL_AUGMENTATIONS_BUT_INVERT  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augmentations = meta.ALL_AUGMENTATIONS  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augment_methods = TEST_AUGMENTATION  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    mask_lines_and_cols_in_input_and_mask_GT_with_nans='id'

    metaAugmenter = meta.MetaAugmenter(augmentations=None,
                                       input_shape=input_shape, output_shape=output_shape,
                                       # input_shape=input_shape, # force 1 or 3 channels input
                                       is_predict_generator=False,
                                       # batch_size_limit_for_training=batch_size_limit_for_training,
                                       batch_size=fixed_batch_size,
                                       input_normalization=input_normalization,
                                       output_normalization=output_normalization,
                                       shuffle=shuffle,
                                       clip_by_frequency=clip_by_frequency,
                                       default_output_tile_width=default_output_tile_width,
                                       default_output_tile_height=default_output_tile_height,
                                       default_input_tile_width=default_input_tile_width,
                                       default_input_tile_height=default_input_tile_height,
                                       rotate_n_flip_independently_of_augmentation=True,
                                       mask_lines_and_cols_in_input_and_mask_GT_with_nans=mask_lines_and_cols_in_input_and_mask_GT_with_nans
                                       # mask_dilations=mask_dilations,
                                       # create_epyseg_style_output=create_epyseg_style_output,
                                       )
    # , default_output_tile_width=default_output_tile_width, default_output_tile_height=default_output_tile_height) #

    # TODO URGENT a tester https://github.com/nibtehaz/MultiResUNet/blob/master/MultiResUNet.py

    # augment_methods = ALL_AUGMENTATIONS,

    # add it several different images
    # TODO test it

    # HISTOBLAST_ME_AUG = DataGenerator(HISTOBLAST_ME, input_channel_of_interest=1, augment_methods=SELECTED_AUGMENTATION, mask_dilations=dilation)
    # tester ça

    # infinite=True,

    # we add data to the augmenter

    # TODO add more including zebra and cell culture

    # not bad --> give it a try as a training ???? --> then test

    # BAD/NOT GREAT DATASETS
    # metaAugmenter.append(FULL_RAPHAEL_WING_BUT_HOLES_IN_MASK, input_channel_of_interest=0, crop_parameters={'x1': 324, 'y1': 1548, 'x2': 1728, 'y2': 3716})
    # metaAugmenter.append(DROSOPHILA_POLARITY_ANDREAS_SINGLE_COOL_IMAGE, input_channel_of_interest=1)
    # metaAugmenter.append(KUBA_REAL_CORTEX, input_channel_of_interest=0)  # TODO
    # metaAugmenter.append(HISTOBLAST_SMALL_DAIKI)
    # metaAugmenter.append(NICE_ECAD_STAINING_FULL_WING_DISK, input_channel_of_interest=0, crop_parameters={'x1': 788, 'y1': 868, 'x2': 3036, 'y2': 2300})
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_EARLY, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # NB THERE IS A BUG IN THE DATASET --> THE MASK DOES NOT MATCH THE SEG
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_LATE, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # TODO incomplete wing seg

    # POLARITY DATASETS
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_1, input_channel_of_interest=1)
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_2, input_channel_of_interest=1)
    # metaAugmenter.append(POLARITY_ME, input_channel_of_interest=1, crop_parameters={'x1': 45, 'y1': 291, 'x2': 1716, 'y2': 1596})
    # metaAugmenter.append(FUCKING_SPOTS, input_channel_of_interest=0)  # is that really smart to have the spots ????

    # GOOD DATASETS

    # minimal list of goods
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_DRESDEN_ORIG, outputs=DROSOPHILA_PUPAL_WING_DRESDEN_GT)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1, crop_parameters={'x1': 0, 'y1': 64, 'x2': 512-64, 'y2': 512})# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=HISTOBLAST_ME, input_channel_of_interest=1)# is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 344, 'y1': 182, 'x2': 976,'y2': 356})  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/CARE/raw/',
                         outputs='/D/Sample_images/sample_images_denoise_manue/CARE/GT/', # doh I was so dumb... I had used the non translated version ...
                         # doh I was so dumb... I had used the non translated version ...
                         # outputs='/D/Sample_images/sample_images_denoise_manue/CARE/denoiseg_fusion/', # doh I was so dumb... I had used the non translated version ...
                         # crop_parameters={'x1': None, 'y1': None, 'width': 224, 'height': 80}
                         # I have now implement random crop --> with defined width n height # # TODO try a random crop
                         # crop_parameters={'x1': 126, 'y1': 40, 'x2': 254, 'y2': 615} # non random crop for segmentation included
                         )

    # metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/210219/raw/',
    #                      # outputs='/D/Sample_images/sample_images_denoise_manue/210219/GT/',
    #                      crop_parameters={'x1': 325, 'y1': 535, 'x2': 549, 'y2': 615})

    # --> ROI x1=325, y1=535, x2=549, y2=615

    # (other stuff not this one, do delete from this file 126, 40, 254, 168)

    # metaAugmenter.append(inputs=CLEANED_XENOPUS, crop_parameters={'x1': 0, 'y1': 0, 'x2': 432, 'y2': 532}) # added a simpler crop to better segment this that also includes cells at the perihphery

    # metaAugmenter.append(inputs=PUPAL_WING_WINDOW_DENOISED)

    # full list of good datasets
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_ROSETTES_FULLSET_SPINNING, crop_parameters={'x1': 396, 'y1': 230, 'x2': 1100, 'y2': 396})
    # metaAugmenter.append(inputs=ANOTHER_FULL_WING_RAPHAEL, crop_parameters={'x1': 255, 'y1': 324, 'x2': 3310, 'y2': 1533})
    # metaAugmenter.append(inputs=DAIKI_HISTO_SMALL, input_channel_of_interest=1)
    # metaAugmenter.append(inputs=RAPHAEL_FULL_WING_NEED_CROP, input_channel_of_interest=0, crop_parameters={'x1': 576, 'y1': 501, 'x2': 3456, 'y2': 1332})
    # metaAugmenter.append(inputs=DROSOPHILA_FULL_WING_PUPA_MID, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296})
    # metaAugmenter.append(inputs=DROSOPHILA_WING_DISC, crop_parameters={'x1': 533, 'y1': 196, 'x2': 830, 'y2': 720})

    # metaAugmenter.append(OVIPO_FROM_MANUE_1, crop_parameters={'x1': 325, 'y1': 420, 'x2': 616, 'y2': 565})

    return metaAugmenter


def get_MINI_test_epithelia_seg(input_shape=None, output_shape=None, batch_size=None,
                               augmentations=meta.MINIMAL_AUGMENTATIONS, mask_dilations=None,
                               create_epyseg_style_output=None,
                               **kwargs):
    input_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                           'individual_channels': True, 'clip': False}
    output_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                            'individual_channels': True, 'clip': False}
    # normalization = None
    shuffle = True
    clip_by_frequency = None  # (0.02, 0.002) # is that actually the same as CARE ????

    # DILATION = None
    # dilation = None #1

    # print('here', kwargs)

    default_output_tile_width = default_output_tile_height = 128 # 256
    default_input_tile_width = default_input_tile_height = 128 # 256

    # just a hack to try no crop to avoid issues of adding black pixels that may impact learning maybe ???
    # default_output_tile_width = default_input_tile_width = 224
    # default_output_tile_height = default_input_tile_height = 80

    # TODO implement below for several inputs and outputs some day
    if input_shape is not None:
        if input_shape[0][-2] is not None:
            default_input_tile_width = input_shape[0][-2]
        if input_shape[0][-3] is not None:
            default_input_tile_height = input_shape[0][-3]

    if output_shape is not None:
        if output_shape[0][-2] is not None:
            default_output_tile_width = output_shape[0][-2]
        if output_shape[0][-3] is not None:
            default_output_tile_height = output_shape[0][-3]

    # if default_input_tile_width is None:
    #     default_input_tile_width = 256
    #
    # if default_output_tile_height is None:
    #     default_output_tile_height = 256

    # batch_size_limit_for_training = 16 # 10  # URGENT TODO --> THAT REALLY SUCKS --> RATHER NEED USE A FIXED BATCH SIZE THAT CAN MIX IMAGES FROM DIFFERENT SETS BY THE WAY
    fixed_batch_size = 10  # 24  # 16  # 16 # 32
    if batch_size is not None:
        fixed_batch_size = batch_size

    # print('default params', batch_size, default_input_tile_width, default_input_tile_height,
    #       default_output_tile_width, default_output_tile_height)

    # input_shape = (None, None, None, 3) #(None, None, None, 3)
    # we set the global parameters for augmentation
    # augment_methods = NO_AUGMENTATION.

    # same bug for zoom/shear/translate not for gaussian nor rotate nor flip nor None --> where is the bug
    # augment_methods = ALL_AUGMENTATIONS_BUT_INVERT  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augmentations = meta.ALL_AUGMENTATIONS  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augment_methods = TEST_AUGMENTATION  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]

    mask_lines_and_cols_in_input_and_mask_GT_with_nans = None # 'id'

    metaAugmenter = meta.MetaAugmenter(augmentations=None,
                                       input_shape=input_shape, output_shape=output_shape,
                                       # input_shape=input_shape, # force 1 or 3 channels input
                                       is_predict_generator=False,
                                       # batch_size_limit_for_training=batch_size_limit_for_training,
                                       batch_size=fixed_batch_size,
                                       input_normalization=input_normalization,
                                       output_normalization=output_normalization,
                                       shuffle=shuffle,
                                       clip_by_frequency=clip_by_frequency,
                                       default_output_tile_width=default_output_tile_width,
                                       default_output_tile_height=default_output_tile_height,
                                       default_input_tile_width=default_input_tile_width,
                                       default_input_tile_height=default_input_tile_height,
                                       rotate_n_flip_independently_of_augmentation=True,
                                       # mask_dilations=mask_dilations,
                                       create_epyseg_style_output=create_epyseg_style_output,
                                       mask_lines_and_cols_in_input_and_mask_GT_with_nans=mask_lines_and_cols_in_input_and_mask_GT_with_nans
                                       )
    # , default_output_tile_width=default_output_tile_width, default_output_tile_height=default_output_tile_height) #

    # TODO URGENT a tester https://github.com/nibtehaz/MultiResUNet/blob/master/MultiResUNet.py

    # augment_methods = ALL_AUGMENTATIONS,

    # add it several different images
    # TODO test it

    # HISTOBLAST_ME_AUG = DataGenerator(HISTOBLAST_ME, input_channel_of_interest=1, augment_methods=SELECTED_AUGMENTATION, mask_dilations=dilation)
    # tester ça

    # infinite=True,

    # we add data to the augmenter

    # TODO add more including zebra and cell culture

    # not bad --> give it a try as a training ???? --> then test

    # BAD/NOT GREAT DATASETS
    # metaAugmenter.append(FULL_RAPHAEL_WING_BUT_HOLES_IN_MASK, input_channel_of_interest=0, crop_parameters={'x1': 324, 'y1': 1548, 'x2': 1728, 'y2': 3716})
    # metaAugmenter.append(DROSOPHILA_POLARITY_ANDREAS_SINGLE_COOL_IMAGE, input_channel_of_interest=1)
    # metaAugmenter.append(KUBA_REAL_CORTEX, input_channel_of_interest=0)  # TODO
    # metaAugmenter.append(HISTOBLAST_SMALL_DAIKI)
    # metaAugmenter.append(NICE_ECAD_STAINING_FULL_WING_DISK, input_channel_of_interest=0, crop_parameters={'x1': 788, 'y1': 868, 'x2': 3036, 'y2': 2300})
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_EARLY, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # NB THERE IS A BUG IN THE DATASET --> THE MASK DOES NOT MATCH THE SEG
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_LATE, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # TODO incomplete wing seg

    # POLARITY DATASETS
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_1, input_channel_of_interest=1)
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_2, input_channel_of_interest=1)
    # metaAugmenter.append(POLARITY_ME, input_channel_of_interest=1, crop_parameters={'x1': 45, 'y1': 291, 'x2': 1716, 'y2': 1596})
    # metaAugmenter.append(FUCKING_SPOTS, input_channel_of_interest=0)  # is that really smart to have the spots ????

    # GOOD DATASETS

    # minimal list of goods
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_DRESDEN_ORIG, outputs=DROSOPHILA_PUPAL_WING_DRESDEN_GT)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1, crop_parameters={'x1': 0, 'y1': 64, 'x2': 512-64, 'y2': 512})# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=HISTOBLAST_ME, input_channel_of_interest=1)# is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 344, 'y1': 182, 'x2': 976,'y2': 356})  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/CARE/raw_super_mini/',
    #                      outputs='/D/Sample_images/sample_images_denoise_manue/CARE/GT_super_mini/', # doh I was so dumb... I had used the non translated version ...
    #                      # outputs='/D/Sample_images/sample_images_denoise_manue/CARE/denoiseg_fusion/',
    #                      # doh I was so dumb... I had used the non translated version ...
    #                      # outputs='/D/Sample_images/sample_images_denoise_manue/CARE/denoiseg_fusion/', # doh I was so dumb... I had used the non translated version ...
    #                      # crop_parameters={'x1': None, 'y1': None, 'width': 224, 'height': 80}
    #                      # I have now implement random crop --> with defined width n height # # TODO try a random crop
    #                      # crop_parameters={'x1': 126, 'y1': 40, 'x2': 254, 'y2': 615} # non random crop for segmentation included
    #                      )

    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_DRESDEN_ORIG,
    #                      outputs=DROSOPHILA_PUPAL_WING_DRESDEN_GT)  # is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET, input_channel_of_interest=1,
    #                      crop_parameters={'x1': 0, 'y1': 64, 'x2': 512 - 64,
    #                                       'y2': 512})  # is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=HISTOBLAST_ME,
    #                      input_channel_of_interest=1)  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 344, 'y1': 182, 'x2': 976,'y2': 356})  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 625, 'y1': 0, 'x2': 625 + 540,
    #                                                                          'y2': 0 + 540})  # remove crop to better segment this shit...
    metaAugmenter.append(inputs=CLEANED_XENOPUS, crop_parameters={'x1': 0, 'y1': 0, 'x2': 432,
                                                                  'y2': 532})  # added a simpler crop to better segment this that also includes cells at the perihphery

    # metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/210219/raw/',
    #                      outputs='/D/Sample_images/sample_images_denoise_manue/210219/denoiseg_fusion/',
    #                      # outputs='/D/Sample_images/sample_images_denoise_manue/210219/GT/',
    #                      crop_parameters={'x1': 325, 'y1': 535, 'x2': 549, 'y2': 615})

    # --> ROI x1=325, y1=535, x2=549, y2=615

    # (other stuff not this one, do delete from this file 126, 40, 254, 168)

    # metaAugmenter.append(inputs=CLEANED_XENOPUS, crop_parameters={'x1': 0, 'y1': 0, 'x2': 432, 'y2': 532}) # added a simpler crop to better segment this that also includes cells at the perihphery

    # metaAugmenter.append(inputs=PUPAL_WING_WINDOW_DENOISED)

    # full list of good datasets
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_ROSETTES_FULLSET_SPINNING, crop_parameters={'x1': 396, 'y1': 230, 'x2': 1100, 'y2': 396})
    # metaAugmenter.append(inputs=ANOTHER_FULL_WING_RAPHAEL, crop_parameters={'x1': 255, 'y1': 324, 'x2': 3310, 'y2': 1533})
    # metaAugmenter.append(inputs=DAIKI_HISTO_SMALL, input_channel_of_interest=1)
    # metaAugmenter.append(inputs=RAPHAEL_FULL_WING_NEED_CROP, input_channel_of_interest=0, crop_parameters={'x1': 576, 'y1': 501, 'x2': 3456, 'y2': 1332})
    # metaAugmenter.append(inputs=DROSOPHILA_FULL_WING_PUPA_MID, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296})
    # metaAugmenter.append(inputs=DROSOPHILA_WING_DISC, crop_parameters={'x1': 533, 'y1': 196, 'x2': 830, 'y2': 720})

    # metaAugmenter.append(OVIPO_FROM_MANUE_1, crop_parameters={'x1': 325, 'y1': 420, 'x2': 616, 'y2': 565})

    return metaAugmenter

def get_MINI_test_CARESEG(input_shape=None, output_shape=None, batch_size=None,
                               augmentations=meta.MINIMAL_AUGMENTATIONS, mask_dilations=None,
                               create_epyseg_style_output=None,
                               **kwargs):
    input_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                           'individual_channels': True, 'clip': False}
    output_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
                            'individual_channels': True, 'clip': False}
    # normalization = None
    shuffle = True
    clip_by_frequency = None  # (0.02, 0.002) # is that actually the same as CARE ????

    # DILATION = None
    # dilation = None #1

    # print('here', kwargs)

    default_output_tile_width = default_output_tile_height = 128 # 256
    default_input_tile_width = default_input_tile_height = 128 # 256

    # just a hack to try no crop to avoid issues of adding black pixels that may impact learning maybe ???
    # default_output_tile_width = default_input_tile_width = 224
    # default_output_tile_height = default_input_tile_height = 80

    # TODO implement below for several inputs and outputs some day
    if input_shape is not None:
        if input_shape[0][-2] is not None:
            default_input_tile_width = input_shape[0][-2]
        if input_shape[0][-3] is not None:
            default_input_tile_height = input_shape[0][-3]

    if output_shape is not None:
        if output_shape[0][-2] is not None:
            default_output_tile_width = output_shape[0][-2]
        if output_shape[0][-3] is not None:
            default_output_tile_height = output_shape[0][-3]

    # if default_input_tile_width is None:
    #     default_input_tile_width = 256
    #
    # if default_output_tile_height is None:
    #     default_output_tile_height = 256

    # batch_size_limit_for_training = 16 # 10  # URGENT TODO --> THAT REALLY SUCKS --> RATHER NEED USE A FIXED BATCH SIZE THAT CAN MIX IMAGES FROM DIFFERENT SETS BY THE WAY
    fixed_batch_size = 10  # 24  # 16  # 16 # 32
    if batch_size is not None:
        fixed_batch_size = batch_size

    # print('default params', batch_size, default_input_tile_width, default_input_tile_height,
    #       default_output_tile_width, default_output_tile_height)

    # input_shape = (None, None, None, 3) #(None, None, None, 3)
    # we set the global parameters for augmentation
    # augment_methods = NO_AUGMENTATION.

    # same bug for zoom/shear/translate not for gaussian nor rotate nor flip nor None --> where is the bug
    # augment_methods = ALL_AUGMENTATIONS_BUT_INVERT  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augmentations = meta.ALL_AUGMENTATIONS  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]
    # augment_methods = TEST_AUGMENTATION  # DataGenerator.translate] #[None, None, DataGenerator.zoom, DataGenerator.gaussian_blur, DataGenerator.translate, DataGenerator.shear, DataGenerator.rotate, DataGenerator.flip]

    metaAugmenter = meta.MetaAugmenter(augmentations=None,
                                       input_shape=input_shape, output_shape=output_shape,
                                       # input_shape=input_shape, # force 1 or 3 channels input
                                       is_predict_generator=False,
                                       # batch_size_limit_for_training=batch_size_limit_for_training,
                                       batch_size=fixed_batch_size,
                                       input_normalization=input_normalization,
                                       output_normalization=output_normalization,
                                       shuffle=shuffle,
                                       clip_by_frequency=clip_by_frequency,
                                       default_output_tile_width=default_output_tile_width,
                                       default_output_tile_height=default_output_tile_height,
                                       default_input_tile_width=default_input_tile_width,
                                       default_input_tile_height=default_input_tile_height,
                                       rotate_n_flip_independently_of_augmentation=True,
                                       # mask_dilations=mask_dilations,
                                       create_epyseg_style_output=create_epyseg_style_output,
                                       )
    # , default_output_tile_width=default_output_tile_width, default_output_tile_height=default_output_tile_height) #

    # TODO URGENT a tester https://github.com/nibtehaz/MultiResUNet/blob/master/MultiResUNet.py

    # augment_methods = ALL_AUGMENTATIONS,

    # add it several different images
    # TODO test it

    # HISTOBLAST_ME_AUG = DataGenerator(HISTOBLAST_ME, input_channel_of_interest=1, augment_methods=SELECTED_AUGMENTATION, mask_dilations=dilation)
    # tester ça

    # infinite=True,

    # we add data to the augmenter

    # TODO add more including zebra and cell culture

    # not bad --> give it a try as a training ???? --> then test

    # BAD/NOT GREAT DATASETS
    # metaAugmenter.append(FULL_RAPHAEL_WING_BUT_HOLES_IN_MASK, input_channel_of_interest=0, crop_parameters={'x1': 324, 'y1': 1548, 'x2': 1728, 'y2': 3716})
    # metaAugmenter.append(DROSOPHILA_POLARITY_ANDREAS_SINGLE_COOL_IMAGE, input_channel_of_interest=1)
    # metaAugmenter.append(KUBA_REAL_CORTEX, input_channel_of_interest=0)  # TODO
    # metaAugmenter.append(HISTOBLAST_SMALL_DAIKI)
    # metaAugmenter.append(NICE_ECAD_STAINING_FULL_WING_DISK, input_channel_of_interest=0, crop_parameters={'x1': 788, 'y1': 868, 'x2': 3036, 'y2': 2300})
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_EARLY, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # NB THERE IS A BUG IN THE DATASET --> THE MASK DOES NOT MATCH THE SEG
    # metaAugmenter.append(DROSOPHILA_FULL_WING_PUPA_LATE, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296}) # TODO incomplete wing seg

    # POLARITY DATASETS
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_1, input_channel_of_interest=1)
    # metaAugmenter.append(DROSOPHILA_SPOT_TRACKING_ANDREAS_CHECK_IMAGES_2, input_channel_of_interest=1)
    # metaAugmenter.append(POLARITY_ME, input_channel_of_interest=1, crop_parameters={'x1': 45, 'y1': 291, 'x2': 1716, 'y2': 1596})
    # metaAugmenter.append(FUCKING_SPOTS, input_channel_of_interest=0)  # is that really smart to have the spots ????

    # GOOD DATASETS

    # minimal list of goods
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_DRESDEN_ORIG, outputs=DROSOPHILA_PUPAL_WING_DRESDEN_GT)# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_PUPAL_WING_L3_ME_FULLSET,  input_channel_of_interest=1, crop_parameters={'x1': 0, 'y1': 64, 'x2': 512-64, 'y2': 512})# is_output_1px_wide=True,) #rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=HISTOBLAST_ME, input_channel_of_interest=1)# is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_SPINNING, crop_parameters={'x1': 344, 'y1': 182, 'x2': 976,'y2': 356})  # is_output_1px_wide=True,) # rebinarize_augmented_output=True,
    metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/CARE/raw_super_mini/',
                         outputs='/D/Sample_images/sample_images_denoise_manue/CARE/GT_super_mini/', # doh I was so dumb... I had used the non translated version ...
                         # outputs='/D/Sample_images/sample_images_denoise_manue/CARE/denoiseg_fusion/',
                         # doh I was so dumb... I had used the non translated version ...
                         # outputs='/D/Sample_images/sample_images_denoise_manue/CARE/denoiseg_fusion/', # doh I was so dumb... I had used the non translated version ...
                         # crop_parameters={'x1': None, 'y1': None, 'width': 224, 'height': 80}
                         # I have now implement random crop --> with defined width n height # # TODO try a random crop
                         # crop_parameters={'x1': 126, 'y1': 40, 'x2': 254, 'y2': 615} # non random crop for segmentation included
                         )

    # metaAugmenter.append(inputs='/D/Sample_images/sample_images_denoise_manue/210219/raw/',
    #                      outputs='/D/Sample_images/sample_images_denoise_manue/210219/denoiseg_fusion/',
    #                      # outputs='/D/Sample_images/sample_images_denoise_manue/210219/GT/',
    #                      crop_parameters={'x1': 325, 'y1': 535, 'x2': 549, 'y2': 615})

    # --> ROI x1=325, y1=535, x2=549, y2=615

    # (other stuff not this one, do delete from this file 126, 40, 254, 168)

    # metaAugmenter.append(inputs=CLEANED_XENOPUS, crop_parameters={'x1': 0, 'y1': 0, 'x2': 432, 'y2': 532}) # added a simpler crop to better segment this that also includes cells at the perihphery

    # metaAugmenter.append(inputs=PUPAL_WING_WINDOW_DENOISED)

    # full list of good datasets
    # metaAugmenter.append(inputs=DROSOPHILA_EMBRYO_ROSETTES_FULLSET_SPINNING, crop_parameters={'x1': 396, 'y1': 230, 'x2': 1100, 'y2': 396})
    # metaAugmenter.append(inputs=ANOTHER_FULL_WING_RAPHAEL, crop_parameters={'x1': 255, 'y1': 324, 'x2': 3310, 'y2': 1533})
    # metaAugmenter.append(inputs=DAIKI_HISTO_SMALL, input_channel_of_interest=1)
    # metaAugmenter.append(inputs=RAPHAEL_FULL_WING_NEED_CROP, input_channel_of_interest=0, crop_parameters={'x1': 576, 'y1': 501, 'x2': 3456, 'y2': 1332})
    # metaAugmenter.append(inputs=DROSOPHILA_FULL_WING_PUPA_MID, input_channel_of_interest=0, crop_parameters={'x1': 696, 'y1': 588, 'x2': 3400, 'y2': 1296})
    # metaAugmenter.append(inputs=DROSOPHILA_WING_DISC, crop_parameters={'x1': 533, 'y1': 196, 'x2': 830, 'y2': 720})

    # metaAugmenter.append(OVIPO_FROM_MANUE_1, crop_parameters={'x1': 325, 'y1': 420, 'x2': 616, 'y2': 565})

    return metaAugmenter

# URGENT TODO IMPLEMENT FIXED BATCH SIZE --> SHOULD BE RELATIVELY SIMPLE AND ADD EMPTY IMAGES IF NOT ENOUGH...
# DOIS-JE FAIRE CA DANS LE METAAUGMENTER --> OUI PLUS DE SENS --> MAY EVEN BE USEFUL FOR TRAIN ON BATCH... --> PREVENTS TOO BIG OF A BATCH
# COMMENT FAIRE --> FAUT UNE SORTE DE MEMOIRE DE BATCH DANS LA CLASSE QUI EST D'ABORD VIDEE AVANT DE PASSER AU NEXT OU DE RELOOPER --> REFLECHIR A CA

# TODO --> Do tests


if __name__ == '__main__':

    if True:
        make_TA_compatible()
        import sys
        sys.exit(0)

    if False:
        copy_clean_files_to_drive()
        import sys
        sys.exit(0)

    # test the function

    # TODO --> add more cause now it's super easy...
    # TODO handle different channels close by

    # logger.setLevel(TA_logger.DEBUG) # log all to see order upon shuffle

    metaAugmenter = get_epithelia_data_augmenter(input_shape=[(None, 256, 512, 1)], output_shape=[(256, 512, 7)],
                                                 create_epyseg_style_output='sevenmaskssave')
    # metaAugmenter = get_CARESEG_data_augmenter(input_shape=[(None, None, None, 1)], output_shape=[(None, None, 1)])

    print('nb of datasets', len(metaAugmenter))  # datasets = 4, total nb of images = 316+200+9+221 = 746
    print('real train',
          metaAugmenter.get_train_length())  # --> 161 --> ça a l'air de vraiment marcher et comme ça j'ai le full set # mais faut faire ça pr tous du coup
    print('real valid', metaAugmenter.get_validation_length())
    print('real test', metaAugmenter.get_test_length())

    # lui faire generer le truc
    # faire des generateurs

    # still a big bug

    # TODO faire un generateur de GUI auto en fonction des parametres des fonctions --> devrait etre assez facile en python et dynamique --> a tester
    # check size and make this produce if possible...
    # test the production to see if possible to see anything

    valid = metaAugmenter.validation_generator()
    test = metaAugmenter.test_generator()
    train_generator = metaAugmenter.train_generator()  # ne marche pas n'est pas infinite

    # plt.ion()
    # i = 0
    # for input, output in train_generator:
    #     if i == 10:
    #         break
    #     i += 1
    #     # print(input)
    #
    #     # input = Img.nomalize(input, method='standardizationch')
    #     # somehow all is reconverted to uint8 here whereas before it was float...
    #     print('in2', input[0].min(), input[0].max())
    #     # print(input)
    #
    #     print(input[0].shape, output[0].shape, input[0].dtype, output[0].dtype)
    #     plt.imshow(np.squeeze(input[0][0]), cmap='gray')
    #     plt.pause(0.3)
    #     plt.imshow(np.squeeze(output[0][0]))
    #     plt.pause(0.3)
    # plt.close(fig='all')
    # plt.ioff()

    # test = metaAugmenter.validation_generator()

    # TODO try FIX THAT

    count = 0
    # for inputs, outputs in test:
    #     # print(inputs, outputs)
    #
    #     print(inputs[0].shape)
    #     print(outputs[0].shape)
    #     count += 1
    #
    # print(count) # --> 167 / 54
    #
    #
    # print('loop 2') # does nothing  --> need reinit the iterator at every run...
    #
    # # print('is empty ', test) # si l'iterateur est empty --> rewind it ???
    #
    # try:
    #     third = next(test)
    # except StopIteration:
    #     print('iterator now empty need reset') # that works --> checks if has next otherwise rewind it --> can be magical
    #
    # # I prefer this version cause it's a smarter way to do I find
    # third = next(test, None)
    # if third is None:
    #     print('iterator now empty need reset')  # that works --> checks if has next otherwise rewind it --> can be magical
    #
    # for inputs, outputs in test:
    #     # print(inputs, outputs)
    #
    #     print(inputs[0].shape)
    #     print(outputs[0].shape)
    #     count += 1

    # can I loop again over it ????

    # TODO really need run it one to count nb of batches --> anyway we don't care for train....
    # try also test or predict

    # bug in one of the augs ???

    # print('loop 3') # --> now working again and just with the right nb of stuff
    # test = metaAugmenter.test_generator()
    plt.ion()
    loop = 0
    for inputs, outputs in train_generator:
        # print(inputs, outputs)

        print('#' * 20, loop)
        loop += 1
        # print(len(inputs), len(outputs))

        print(len(inputs))

        print(inputs[0].shape)
        print(outputs[0].shape)

        print(inputs[0].min(), inputs[0].max(), outputs[0].min(), outputs[0].max())
        count += 1
        try:
            for iii, img in enumerate(inputs):
                plt.imshow(np.squeeze(inputs[iii]), cmap='gray')
                plt.pause(3)
                plt.imshow(np.squeeze(outputs[iii]), cmap='gray')
                plt.pause(3)
            #
            # plt.imshow(np.squeeze(inputs[1]), cmap='gray')
            # plt.pause(10)
            # plt.imshow(np.squeeze(outputs[1]), cmap='gray')
            # plt.pause(10)
        except:
            print(inputs[0][0].shape)

            for i, img in enumerate(inputs[0]):
                print('inner loop', i)
                plt.imshow(np.squeeze(inputs[0][i]), cmap='gray')
                plt.pause(0.2)
                plt.imshow(np.squeeze(outputs[0][i]))
                plt.pause(0.2)
    plt.close(fig='all')
    plt.ioff()

# it all seems ok


# TODO
# metaAugmenter.append()

# sinon faire des infinite iterators --> voir comment faire ????


# # need initial size then loop over it infinitely
# import random
#
# sorted_range = list(range(100))
#
# shuffled = random.sample(range(100), 100)
# print(len(shuffled)) # this is really cool cause it shuffles but without a repick --> then just need loop over shuffled for the index
# print(len(sorted_range)) # this is really cool cause it shuffles but without a repick --> then just need loop over shuffled for the index

