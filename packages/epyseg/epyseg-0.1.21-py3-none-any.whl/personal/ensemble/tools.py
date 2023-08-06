# worst case --> reinstall tensorflow-GPU with its deps...
# recursive list models ls -R **/CARE*model-0*h5 TODO remove the dupes of the models... etc...

# TODO merge several files --> think how to do --> just merge same files in different folders or saves all files tbe merged and merge those --> think how this can be done and sometimes offer post process in case that was not done by the user --> it's a quite good idea in fact...
# offer average of several images , etc --> of cours images need be of the same type or offer max proj again images need be the same otherwise warn for errors.

# codes to check
# https://github.com/junyanz/interactive-deep-colorization --> TODO--> just to see how they made the things...
# TODO chek the model zoo https://github.com/BVLC/caffe/wiki/Model-Zoo

# create a bunch of ensemble tools
# one of them should just be tool to project several images with average or max from several models
# another should allow save predictions for each model
# need prevent redundant names though...

# the tool should just loop over an existing stuff while just changing one parameter
# then fusing the things
# should I also allow the same for TA version --> that would be overcompLex to do or need a smart way to do that
# really need a log to avoid issues because there can be so many in that case

# ça marche à peu près voir quoi rajouter et comment gérer le changement d'image dans le truc
# batcher trucs pr aller plus vite

import os
import traceback
import logging
from epyseg.deeplearning.docs.doc2html import markdown_file_to_html, browse_tip
from epyseg.gui.defineROI import DefineROI
from epyseg.postprocess.gui import PostProcessGUI
from epyseg.uitools.blinker import Blinker
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QToolTip, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QTabWidget
from PyQt5 import QtCore
from epyseg.deeplearning.augmentation.generators.data import DataGenerator
from epyseg.gui.open import OpenFileOrFolderWidget
from epyseg.gui.preview import crop_or_preview
from PyQt5.QtWidgets import QSpinBox, QComboBox, QVBoxLayout, QLabel, QCheckBox, QRadioButton, QButtonGroup, QGroupBox, \
    QDoubleSpinBox
from PyQt5.QtCore import Qt, QPoint
from epyseg.img import Img, white_top_hat, black_top_hat
import sys
import os
import json

# logging
from epyseg.tools.logger import TA_logger

logger = TA_logger()

# do stuff to keep only first output of a model --> good idea --> can be useful for the codes that generate surface projections and in practice is very easy to do

# will load several models and have them predict then generate several outputs

# a tester mais peut marcher... en fait
# faudrait hacker l'outil pr eviter les pbs


# TODO self.set_custom_predict_parameters.get_parameters_directly() --> make this popup so that all parameters can be set at once given the input folder --> that should be unique

# QWidget widget = new QWidget(this);
# To "duplicate" set the same properties on the new widget as in the old.

# ensemble tools
from epyseg.deeplearning.deepl import EZDeepLearning
from epyseg.gui.img import image_input_settings


# almost there but bug here

# URGENT TODO remove z_frames_to_add if added to the predict parameters

# TODO add time estimation --> TODO because then I would get a good estimate of how good this is

def model_tester(models, deepTA, predict_parameters, progress_callback=None, mode_single_folder_output=False,
                 z_frames_to_add=None):
    # could popup for the parameters here directly --> no big change to the GUI
    # load the classical prediction tool but just loop over several models before that and change output prediction folder --> should be easy

    default_output_folder = None
    if 'predict_output_folder' in predict_parameters:
        default_output_folder = predict_parameters['predict_output_folder']

    # print(default_output_folder)

    for idx, model in enumerate(models):
        try:
            print('Loading model: "', model, '"')

            # remove model parameters from that ???

            # load model
            # nb models need not be compiled as this is just for prediction so just load model without compile, thereby removing errors

            # TODO maybe skip compile
            deepTA.model = deepTA.load_model(model=model,
                                             skip_comile=True)  # TODO need prevent compilation --> see if there is a parameter for that and need no other parameter than model name...

            # def _predict_using_model
            deepTA.get_loaded_model_params()
            deepTA.summary()

            print(deepTA._get_inputs())
            print(deepTA._get_outputs())

            input_shape = deepTA.get_inputs_shape()
            output_shape = deepTA.get_outputs_shape()

            # logger.debug('inp, out ' + str(input_shape) + ' ' + str(output_shape))
            # logger.debug('test values ' + str(input_shape) + ' ' + str(output_shape))
            # logger.debug('predict params' + str(predict_parameters))

            predict_generator = deepTA.get_predict_generator(input_shape=input_shape, output_shape=output_shape,
                                                             z_frames_to_add=z_frames_to_add,
                                                             # TODO maybe remove if added to the predict_parameters
                                                             **predict_parameters)

            # predict_parameters['predict_output_folder'] = default_output_folder+'_'+str(idx)
            # pas mal save in default folder but then save all modes in their own folder --> would also be compatible with TA
            # print('path',predict_parameters['predict_output_folder'])
            if not mode_single_folder_output:
                predict_parameters['predict_output_folder'] = os.path.join(default_output_folder,
                                                                           'predict_model_nb_' + str(idx))

                # save model name in folder
                if not os.path.exists(predict_parameters['predict_output_folder']):
                    os.makedirs(predict_parameters['predict_output_folder'])

                f = open(os.path.join(predict_parameters['predict_output_folder'], "model_used.txt"), "w+")
                f.write(model)
                f.close()

            # that should do the job in fact...

            deepTA.predict(predict_generator, output_shape, progress_callback=progress_callback, batch_size=1,
                           append_this_to_save_name='' if not mode_single_folder_output else '_model_nb_' + str(
                               idx) + '.tif',
                           **predict_parameters)
        except:
            traceback.print_exc()
            print('An error occurred, please check your model/files...')

        # en gros c'est ça et j'ai juste besoin de sauver le nom du modele dedans ou bien le path dans un fichier de log... ou dans le nom du fichier
        # sauver aussi model nb so that I can have several times the same model name
        # would be good to log model used as a text file inside the stuff
        # maybe just increment model inside

        # def get_predict_parameters(self):


# TODO permettre aussi la selection de modeles --> ça aiderait en fait et aussi la selection depuis un fichier de config... --> réfléchir à ça...
if __name__ == '__main__':

    # TODO faire aussi une version qui sauve tout dans un meme folder avec uen extension le nom du modele ou plutot son numero --> moins bon mais plus facile à gérer et à comparer sans autres outils

    ######################profiling mem#####################################
    # import cProfile
    #
    # pr = cProfile.Profile()
    # pr.enable()
    ######################profiling mem#####################################

    app = QApplication(sys.argv)

    # KEEP ME!!!!!!!!!!! tested models = 0,2,3,13,14,17,21,24,25 for 210108
    # KEEP ME !!!!! tested models = 0,1,2,5,6,13,14,18,24,31 for 201104_armGFP_different_lines_tila
    # keep me !!!! tested models = 0,1,3, 5,6,11,12,13,17,18,21,25,30 ,31 for 200722

    # KEEP ME new default tests = 0, 1, 2, 5, 13, 14, 17, 18, 24, 25, 27, 31

    # Keep me 0,1,2,4,5,12,13,14,17,18,20,21,23,26,29,31,32 for 100807 legs and 080205 old stuff

    # TODO --> first ask for all models...
    # KEEP CAUSE all in the same order...

    # TODO would really be good to clean this because a lot are similar
    models = [
        'CARE_model_trained_MAE_in_epyseg_29-1_50steps_per_epoch_not_outstanding_though/CARE_model-0.h5',  # 0 #####
        # 'CARE_model_trained_MSE_error_instead_MAE_in_epyseg_29-1/CARE_model-0.h5', #1
        # 'CARESEG3D_models_trained_on_colab_201214/CARESEG3D_model-0.h5', #2
        # 'CARESEG_another_normal_training_201216_colab_but_gave_crap/CARESEG_model-0.h5', # 3 # not bad in fact especially when there is an amazing amount of noise because it is an amazing denoiser...
        # 'CARESEG/CARESEG_model-0.h5', #4
        # 'CARESEG_first_correct_test/CARESEG_model-0-0-0.h5', #5
        ## 'CARESEG_first_correct_test/CARESEG_model-0-0-4.h5', #6
        # 'CARESEG_first_successful_retrain_on_CARE_data_very_very_good_surface_proj_but_not_for_all/CARESEG_model-0-0.h5', #7
        ## 'CARESEG_first_successful_retrain_on_CARE_data_very_very_good_surface_proj_but_not_for_all/CARESEG_model-0-1.h5', #8
        ## 'CARESEG_first_successful_retrain_on_CARE_data_very_very_good_surface_proj_but_not_for_all/CARESEG_model-0-2.h5', #9
        ## 'CARESEG_first_successful_retrain_on_CARE_data_very_very_good_surface_proj_but_not_for_all/CARESEG_model-0-3.h5',#10
        ## 'CARESEG_first_successful_retrain_on_CARE_data_very_very_good_surface_proj_but_not_for_all/CARESEG_model-0-4.h5',#11
        # 'CARESEG_masked_data_and_masked_loss_to_prevent_identity_v1_210107_good/CARESEG_model-0.h5',#12
        'CARESEG_masked_data_and_partial_masked_loss_to_limit_identity_but_not_remove_it_v1_210107_outstanding_on_some_just_good_on_others/CARESEG_model-0.h5', #####
        # 13
        'CARESEG_masked_data_and_partial_masked_loss_to_limit_identity_but_not_remove_it_v2_zRoll_stack_210108_quite_good_but_a_bit_low_signal/CARESEG_model-0.h5', #####
        # 14
        # 'CARESEG_my_loss_mae_first_chan_dice_other_chans/CARESEG_model-0.h5',#15
        # 'CARESEG_RETRAINED_NEW_LOSS_DICE_201215/CARESEG_model-0.h5',#16
        'CARESEG_retrained_normally_201216/CARESEG_model-0.h5',#17 #####
        'CARESEG_second_correct_tested_210219_outstanding_denoise/CARESEG_model-0.h5',  # 18 #####
        # 'CARESEG_second_successful_retrain_on_CARE_data_better_than_previous_need_longer_training_and_more_diverse_one_too/CARESEG_model-0.h5',#19
        # 'CARESEG_shuffle_n_roll_models_trained_on_colab_201215/CARESEG_model-0.h5',#20
        # 'CARESEG_test_combined_loss_properly_made_with_reduce_mean_220105/CARESEG_model-0.h5',#21
        # 'CARESEG_test_combined_mae_jaccard_loss_properly_made_with_reduce_mean_220105_terrible_no_clue_why/CARESEG_model-0.h5',# 22
        # 'CARESEG_trained_different_losses_for_channels_mae_bce/CARESEG_model-0.h5', # 23
        # 'CARESEG_trained_on_CARE_data_with_dilation_good/CARESEG_model-0.h5',# 24
        # 'CARESEG_Zroll_models_trained_on_colab_201215/CARESEG_model-0.h5',# 25
        # 'CARE_trained_on_its_data_and_mine_not_working_on_its/CARE_model-0.h5',# 26
        # 'CARE_training_on_its_own_data_with_CARESEG/CARESEG_model-0-0.h5',# 27
        ## 'CARE_training_on_its_own_data_with_CARESEG/CARESEG_model-0-4.h5',# 28
        # 'retrained_CARE_my_soft_fixed_normalization_not_outstanding_but_improving/CARE_model-0.h5',# 29
        # 'CARE_finally_working_retrain_with_CARE_normalization/CARE_model-0.h5',  # 30
        'CARE_models_trained_on_colab_201214/CARE_model-0.h5',  # 31 #####
        # 'CARE_masked_data_and_partial_masked_loss_to_limit_identity_but_not_remove_it_v1_210120_not_outstanding_CARESEG_is_better/CARE_model-0.h5',# 32
    ]

    for idx, model in enumerate(models):
        models[idx] = os.path.join('/home/aigouy/mon_prog/Python/deepl_3rd_party/models/my_model/bckup/', model)

    print(models)

    use_cpu = False
    deepTA = EZDeepLearning(use_cpu=use_cpu)

    # augment, ok = image_input_settings.getDataAndParameters(parent_window=None,
    #                                                         show_normalization=True,
    #                                                         show_preview=True,
    #                                                         show_predict_output=True,
    #                                                         show_overlap=True, show_input=True,
    #                                                         show_output=True,
    #                                                         show_preprocessing=True,
    #                                                         show_tiling=True,
    #                                                         show_channel_nb_change_rules=True,
    #                                                         show_HQ_settings=True,
    #                                                         show_run_post_process=True,
    #                                                         allow_bg_subtraction=True)
    #
    #
    # print(augment, ok)

    # TODO change default parameters there

    # predict_parameters, ok = image_input_settings.getDataAndParameters(show_input=True,
    #                                                               show_channel_nb_change_rules=True,
    #                                                               show_normalization=True,
    #                                                               show_tiling=True,
    #                                                               show_overlap=True,
    #                                                               show_predict_output=True,
    #                                                               input_mode_only=True,
    #                                                               show_preview=True,
    #                                                               show_HQ_settings=True,
    #                                                               show_run_post_process=True,
    #                                                               allow_bg_subtraction=True,
    #                                                               show_preprocessing=True)

    # offer maybe a nb of channels to allow for selection, in fact more complex... ???
    # can't show preview as model is not available --> does not know if must do something --> how can I circumvent that and in any case it is a smart idea to show the image --> fix it
    dialog = image_input_settings(show_input=True,
                                  _is_dialog=True,
                                  show_channel_nb_change_rules=True,
                                  show_normalization=True,
                                  show_tiling=True,
                                  show_overlap=True,
                                  show_predict_output=True,
                                  input_mode_only=True,
                                  show_preview=True,
                                  show_HQ_settings=True,
                                  show_run_post_process=True,
                                  allow_bg_subtraction=True,
                                  show_preprocessing=True)
    dialog.enable_post_process.setChecked(False)  # by default do not show this but may be useful in some cases still...
    # TODO see why no preview and why COI is not updated...

    result = dialog.exec_()
    predict_parameters = dialog.get_parameters()
    if result != QDialog.Accepted:
        print('user canceled --> quitting')
        sys.exit(0)

    # print('predict parameters', predict_parameters)

    # try json load
    predict_parameters = json.loads(predict_parameters)

    # TODO copy and edit those parameters in order to predict for colab --> big gain of time
    # try predict for the leg on colab

    # print(type(predict_parameters))

    # --> à tester
    z_frames_to_add = (
    5, 5)  # None #TODO URGENT REMOVE z_frames_to_add and add it to the predict parameters --> TODO...
    model_tester(models, deepTA, predict_parameters, mode_single_folder_output=False,
                 z_frames_to_add=z_frames_to_add)  # TODO URGENT REMOVE z_frames_to_add and add it to the predict parameters --> TODO...

    ######################profiling mem#####################################
    # pr.disable()
    # # after your program ends
    # pr.print_stats(sort="calls")
    # # Back in outer section of code
    # pr.dump_stats('profile.pstat')
    ######################profiling mem#####################################

    sys.exit(0)
