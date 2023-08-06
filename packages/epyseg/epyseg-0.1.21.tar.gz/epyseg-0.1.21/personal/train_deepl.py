# TODO maybe use Nans to pass ROIs ??? --> see how to do that


# check what this does K.maximum(margin - y_pred, 0)


# and no need to do dilation --> remove single pixel stuff and dilation options
# all is ok in fact...
import traceback

import os
from epyseg.img import Img, mask_rows_or_columns

# from personal.tools.losses.custom_losses_tst import denoise_and_segmentation_loss
# from personal.tools.losses.custom_losses_tst import denoise_and_segmentation_loss

os.environ['SM_FRAMEWORK'] = 'tf.keras'  # set env var for changing the segmentation_model framework
# the bug comes from keras tensorflow
import segmentation_models as sm
from tensorflow.keras.losses import mean_squared_error, binary_crossentropy, mean_absolute_error
from epyseg.deeplearning.augmentation import meta
from personal.epithelia_augmenter import get_epithelia_data_augmenter, get_CARESEG_data_augmenter, \
    get_MINI_test_CARESEG, get_MINI_test_epithelia_seg, get_CARE_data_augmenter
from epyseg.deeplearning.augmentation.meta import MetaAugmenter
from epyseg.deeplearning.deepl import EZDeepLearning
import tensorflow as tf
import numpy as np
from tensorflow import nn # imports softmax and alike

#TODO --> do install this
# pip install tensorflow-addons
# import tensorflow_addons as tfa
# import tfa.losses.giou_loss # tensorflow addons
# https://www.tensorflow.org/addons/api_docs/python/tfa/losses/GIoULoss
#tfa.losses.GIoULoss(
#eucid = tfa.image.euclidean_dist_transform(gray)
#https://www.tensorflow.org/addons/tutorials/image_ops --> really cool too and cool to look at how it's made too...
# https://www.tensorflow.org/addons/api_docs/python/tfa/image/translate

# https://github.com/tensorflow/addons --> check for version compatibility



# import tensorflow.keras.backend as K

# logger
from epyseg.tools.logger import TA_logger

logger = TA_logger()  # logging_level=TA_logger.DEBUG

# pkoi marche plus en inversé ???

# TO KEEP
# def custom_call_back_code():
#     # TODO really need an augmenter there because i need same normalization and parameters etc or need to pass in just one image and corresponding post process code!!!
#     # code to paste in saver callback to view progress dynamically --> good
#     # TODO ça marche mais le rendre portable un jour faire un truc qui fait ça avec un test generator sur un folder entier et de manière intelligente
#     try:
#         # if I pass a test it could save result in a folder --> maybe a good idea just test now
#         x = Img('/D/Sample_images/sample_images_denoise_manue/CARE/raw/session_7_P01.tif')[::, 0:128, 0:128]
#         import numpy as np
#         print('bef', x.shape)
#         x = np.reshape(x, (1, *x.shape, 1))
#         print(x.shape)
#         results = self.model.predict(x, verbose=1,
#                                      batch_size=1)  # ça marche !!!!! --> so cool but would need the cutters and stuff like that to be passed
#         # results = self.model.predict(files, verbose=1, batch_size=batch_size)
#         # print(results)
#         print(len(results))
#         print(results[0].shape)
#         Img(results[0], dimensions='hwc').save('/tmp/test_current.tif')
#     except:
#         # traceback.print_exc()
#         print('failed to predict')


if __name__ == '__main__':
    from timeit import default_timer as timer

    start = timer()

    # tf.compat.v1.enable_eager_execution()  #
    deepTA = EZDeepLearning()

    # deepTA.load_or_build(architecture='Unet', backbone='vgg19', activation='sigmoid', classes=1)
    # deepTA.load_or_build(architecture='linknet', backbone='vgg19', activation='sigmoid', classes=6)
    # deepTA.load_or_build(architecture='linknet', backbone='vgg19', activation='sigmoid', classes=7)
    # deepTA.load_or_build(architecture='linknet', backbone='seresnext101', activation='sigmoid', classes=7)
    # deepTA.load_or_build(architecture='linknet', backbone='inceptionresnetv2', activation='sigmoid', classes=7)
    # deepTA.load_or_build(architecture='linknet', backbone='vgg16', activation='sigmoid', classes=7)

    # deepTA.load_or_build(architecture='linknet', backbone='vgg16', activation='sigmoid', classes=7)

    # bizarre --> il ne voit pas les memes choses en blanc et en noir --> jouer la dessus en mettant un dans un sens puis un dans l'autre puis une strong dilation comme centroid
    # deepTA.load_or_build(architecture='linknet', backbone='vgg19', activation='sigmoid', classes=4)

    # super slow
    # best seed --> take centroid or pixel inside and
    # deepTA.load_or_build(architecture='linknet', backbone='vgg19', activation='sigmoid', classes=6)
    # deepTA.load_or_build(architecture='linknet', backbone='seresnext101', activation='sigmoid', classes=4)

    # deepTA.load_or_build(architecture='Unet', backbone='seresnext101', activation='sigmoid', classes=1)
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Linknet-inceptionresnetv2-smloss/Linknet-inceptionresnetv2-smloss-ep0100-l0.194848.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/unet-vgg19-sigmoid-min-max-adam10exp-3_loss_binary_focal_dice_loss_1px_wide/model_1-ep0099-l0.275704.h5')
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/epyseg_pkg/personal/model_1-ep0099-l0.445036_weights.h5')
    # deepTA.load_or_build(model='/home/aigouy/Dropbox/Unet-vgg19-sigmoid-ep0100-l0.061860_invert_aug.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/unet-vgg19-retrain_from_inverted-new-training/Unet-vgg19-sigmoid-ep0100-l0.061860_invert_aug-ep0150-l0.453209.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Linknet-seresnext101-smloss-256x256/Linknet-seresnext101-smloss-256x256-ep0099-l0.158729.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_seresnext101_retrained_dice_loss_invert/Linknet-seresnext101-smloss-256x256-ep0099-l0.158729-ep0150-l0.272165.h5')
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/epyseg_pkg/personal/Linknet-seresnext101-smloss-256x256-ep0099-l0.158729-ep0150-l0.272165-ep0149-l0.287795.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_seresnext101_retrained_dice_loss_invert/Linknet-seresnext101-smloss-256x256-ep0099-l0.158729-ep0148-l0.269997.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknete_seresnext_retrain_including_invert_150_200times/Linknet-seresnext101-smloss-256x256-ep0099-l0.158729-ep0150-l0.272165-ep0149-l0.287795.h5') #
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/unet-vgg19-retrain_from_inverted-new-training/300epochs_training/Unet-vgg19-sigmoid-ep0100-l0.061860_invert_aug-ep0150-l0.453209-ep0245-l0.304019.h5') # super good model very little extra noise --> could use this one --> tends to oversse SOPs though
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/unet-vgg19-bce-augmentation-invert/Unet-vgg19-sigmoid-ep0094-l0.061129.h5') # old --> less good --> ok
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-sigmoid-aug-invert-bce/Unet-inceptionresnetv2-sigmoid-aug-invert-bce-ep0100-l0.047122.h5') # old --> less good --> ok
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg19_dice_loss_neo_no_interp_training/linknet-vgg19-sigmoid-ep0149-l0.294375.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg19_neo_model_dilation_shell/linknet-vgg19-sigmoid-ep0180-l0.233807.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg19_shells_inverted_cellpose_like_seeds/linknet-vgg19-sigmoid-ep0014-l0.254005.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg19_shells_inverted_cellpose_like_seeds_and_inverted/linknet-vgg19-sigmoid-ep0195-l0.151429.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg16_shells_inverted_seeds_inverted_amazing/linknet-vgg16-sigmoid-ep0191-l0.144317_lighter_model_test.json')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg16_shells_inverted_seeds_inverted_amazing/linknet-vgg16-sigmoid-ep0191-l0.14431_reduced_by_4.json')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-sigmoid-aug-invert-bce_good_but_lots_of_noise_in_noisy_images_maybe_retrain/Unet-inceptionresnetv2-sigmoid-aug-invert-bce-ep0100-l0.047122.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg16_shells_inverted_seeds_inverted_amazing/linknet-vgg16-sigmoid-ep0191-l0.144317.json', model_weights='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg16_shells_inverted_seeds_inverted_amazing/linknet-vgg16-sigmoid-ep0191-l0.144317_weights.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg19_shells_inverted_cellpose_like_seeds_and_inverted/retrained_100_more_epochs_clearly_not_better/linknet-vgg19-sigmoid-ep0195-l0.151429-ep0094-l0.142760_reduced_by_4_but_last-1_filters.json')
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/epyseg_pkg/personal/linknet-vgg19-sigmoid-ep0011-l0.292312.h5')
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/deepl_3rd_party/CARESEG_model.json')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/201205_retrained_model_deep_vgg16_200epochs_with_shuffle_n_intensity_aug_good/linknet-vgg16-sigmoid-0.h5')
    # deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/201205_retrained_model_deep_vgg16_200epochs_with_shuffle_n_intensity_aug_good/retrained_100_epochs/linknet-vgg16-sigmoid-0-0.h5')

    # CARE on two sample sets is really CRAP --> shall I try a higher LR to start with ???

    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/deepl_3rd_party/CARE_model.json')
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/RAUNet-tumor-segmentation/att_resunet_2d_fixed7.json') #
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/RAUNet-tumor-segmentation/att_resunet_2d_filter8_fixed7.json') #
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/RAUNet-tumor-segmentation/att_resunet_2d_filter16_fixed7.json') #
    deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/pytorch_to_tensorflow/unetplusplus-vgg16_channel_last_7_classes.json') #
    # deepTA.load_or_build(model='/home/aigouy/mon_prog/Python/epyseg_pkg/personal/CARE_model-0_nice_start_with_CARE_data_first_in_train.h5')


    deepTA.get_loaded_model_params()
    deepTA.summary()
    # print(deepTA.model.name, deepTA.model._name)

    # deepTA.model._name += '_standardization'

    print(deepTA._get_inputs())
    print(deepTA._get_outputs())

    print('input shapes', deepTA.get_inputs_shape())
    print('output shapes', deepTA.get_outputs_shape())

    input_shape = deepTA.get_inputs_shape()
    output_shape = deepTA.get_outputs_shape()

    input_normalization = {'method': 'Rescaling (min-max normalization)', 'range': [0, 1],
                           'individual_channels': True}

    # input_normalization = {'method': Img.normalization_methods[7], 'range': [2, 99.8],
    #                        'individual_channels': True, 'clip':False}

    # input_normalization = {'method': 'Standardization (Z-score Normalization)', 'range': [-1, 1],
    #                        'individual_channels': True}

    # metaAugmenter = get_epithelia_data_augmenter(augmentations=meta.ALL_AUGMENTATIONS_BUT_HIGH_NOISE)
    # metaAugmenter = get_epithelia_data_augmenter(augmentations=meta.STRETCHED_AUG_EPITHELIA)
    # metaAugmenter = get_epithelia_data_augmenter(augmentations=meta.STRETCHED_AUG_EPITHELIA_4)
    # metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.ALL_AUGMENTATIONS_BUT_INVERT_AND_NOISE, mask_dilations=7) #this training is very good for single images
    # metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.ALL_AUGMENTATIONS_BUT_INVERT_AND_NOISE, mask_dilations=7,  batch_size=6) #this training is very good for single images
    # metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.ALL_AUGMENTATIONS_BUT_INVERT_AND_NOISE, mask_dilations=7) #this training is very good for single images
    # metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.ALL_AUGMENTATIONS_BUT_INVERT_AND_NOISE, mask_dilations=7, batch_size=40) #this training is very good for single images
    # metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.ALL_AUGMENTATIONS_BUT_INVERT_AND_NOISE, mask_dilations=1, batch_size=8 ) #this training is very good for single images

    # ça marche vraiment mais il me faut des controles

    # metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.MINIMAL_AUGMENTATIONS, mask_dilations=0, batch_size=32, create_epyseg_style_output='sevenmaskssave') #this training is very good for single images

    # metaAugmenter = get_CARESEG_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=None, batch_size=10) #this training is very good for single images
    # metaAugmenter = get_CARE_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=None, batch_size=10) #this training is very good for single images
    # metaAugmenter = get_MINI_test_CARESEG(input_shape=input_shape, output_shape=output_shape, augmentations=None, batch_size=10 ) #this training is very good for single images
    # metaAugmenter = get_MINI_test_epithelia_seg(input_shape=input_shape, output_shape=output_shape, augmentations=meta.MINIMAL_AUGMENTATIONS,mask_dilations=0, batch_size=32, create_epyseg_style_output='sevenmaskssave') #this training is very good for single images
    metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.MINIMAL_AUGMENTATIONS, mask_dilations=0, batch_size=32, create_epyseg_style_output='sevenmaskssave')  # this training is very good for single images

    ## metaAugmenter = get_epithelia_data_augmenter(input_shape=input_shape, output_shape=output_shape, augmentations=meta.ALL_AUGMENTATIONS_BUT_INVERT_AND_NOISE, mask_dilations=4, batch_size=6) # batch size 6 is for the linknet seresnext101 256x256 #this training is very good for single images
    # try refine now


    # optimizer = tf.keras.optimizers.Adam(lr=1e-4) # 'adam'  # 'adadelta' # 'adam' #Adam() #keras.optimizers.Adam() #Adam(lr=1e-4) #optimizer='rmsprop' #'sgd' #keras.optimizers.SGD(learning_rate=learning_rate_fn)
    # optimizer = 'adam'
    # optimizer = tf.keras.optimizers.Adam(lr=1e-4)
    # optimizer = 'Adam' #'Adam' # tf.keras.optimizers.Adam(lr=1e-4) #'adam' # 'SGD' #tf.keras.optimizers.SGD
    # optimizer = tf.keras.optimizers.Adam(lr=0.0004) #'Adam' # tf.keras.optimizers.Adam(lr=1e-4) #'adam' # 'SGD' #tf.keras.optimizers.SGD
    optimizer = tf.keras.optimizers.Adam(lr=0.001) #'Adam' # tf.keras.optimizers.Adam(lr=1e-4) #'adam' # 'SGD' #tf.keras.optimizers.SGD

    # loss = sm.losses.bce_jaccard_loss # sm.losses.bce_dice_loss # sm.losses.bce_jaccard_loss # sm.losses.bce_dice_loss #sm.losses.bce_jaccard_loss #sm.losses.binary_focal_dice_loss #sm.losses.jaccard_loss #'binary_crossentropy'  #'categorical_crossentropy' #'mean_squared_error'#'mean_squared_error' #sm.losses.bce_jaccard_loss #'binary_crossentropy' #'mean_squared_error'
    # # loss = sm.losses.bce_dice_loss # sm.losses.bce_dice_loss # sm.losses.bce_jaccard_loss # sm.losses.bce_dice_loss #sm.losses.bce_jaccard_loss #sm.losses.binary_focal_dice_loss #sm.losses.jaccard_loss #'binary_crossentropy'  #'categorical_crossentropy' #'mean_squared_error'#'mean_squared_error' #sm.losses.bce_jaccard_loss #'binary_crossentropy' #'mean_squared_error'
    # metrics = [sm.metrics.iou_score, 'accuracy'] # 'accuracy' # ['binary_accuracy'] #[sm.metrics.iou_score] #['accuracy'] ['binary_accuracy'] ['mae']

    # NB for CARESEG learning rate may have been too high initially as reduce LR on plateau seems to help globally


    # entrainement desastreux et vachement long pr le nouveau CARESEG avec la normalisation par percentile à la CARE... --> need love --> but I had a bug because I had forgotten to convert to float32 before normalization
    # some of the codes were much better

    # TODO check also that https://stackoverflow.com/questions/60582448/custom-loss-function-access-tensor-channels

    # in fact could and should maybe initialize it with the real tensor or find tricks --> infinite loop with catch


    #dirty hack but functional -> TODO try do that better
    # nb cette custom loss ne marche pas du tout en fait


    # i must have a bug because some values are crazy...
    from tensorflow.keras import backend as K

    def jaccard_distance(y_true, y_pred, smooth=100):
        intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
        sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
        jac = (intersection + smooth) / (sum_ - intersection + smooth)
        return (1 - jac) * smooth



    #https://github.com/keras-team/keras-contrib/blob/master/keras_contrib/losses/jaccard.py

    # https://github.com/tensorflow/addons
    #https://www.tensorflow.org/addons/api_docs/python/tfa/losses/giou_loss
    #https://stackoverflow.com/questions/49284455/keras-custom-function-implementing-jaccard
    # maybe I need that
    #https://gist.github.com/wassname/f1452b748efcbeb4cb9b1d059dce6f96
    def jaccard_distance_loss(y_true, y_pred, smooth=1e-5):
        """
        Jaccard = (|X & Y|)/ (|X|+ |Y| - |X & Y|)
                = sum(|A*B|)/(sum(|A|)+sum(|B|)-sum(|A*B|))

        The jaccard distance loss is usefull for unbalanced datasets. This has been
        shifted so it converges on 0 and is smoothed to avoid exploding or disapearing
        gradient.

        Ref: https://en.wikipedia.org/wiki/Jaccard_index

        @url: https://gist.github.com/wassname/f1452b748efcbeb4cb9b1d059dce6f96
        @author: wassname
        """
        intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
        sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
        jac = (intersection + smooth) / (sum_ - intersection + smooth)
        return (1 - jac) * smooth


    def new_mse(y_true, y_pred):
        # swapping elements 1 and 3 - concatenate slices of the original tensor
        swapped = K.concatenate([y_pred[:1], y_pred[3:], y_pred[2:3], y_pred[1:2]])
        # actually, if the tensors are shaped like (batchSize,4), use this:
        # swapped = K.concatenate([y_pred[:,:1],y_pred[:,3:],y_pred[:,2:3],Y_pred[:,1:2])

        # losses
        regularLoss = mean_squared_error(y_true, y_pred)
        swappedLoss = mean_squared_error(y_true, swapped)

        # concat them for taking a min value
        concat = K.concatenate([regularLoss, swappedLoss])

        # take the minimum
        return K.min(concat)

        # below does not work and maybe it's not possible


    def dice_coef(y_true, y_pred, smooth=1):
        """
        Dice = (2*|X & Y|)/ (|X|+ |Y|)
             =  2*sum(|A*B|)/(sum(A^2)+sum(B^2))
        ref: https://arxiv.org/pdf/1606.04797v1.pdf
        """
        intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
        return (2. * intersection + smooth) / (K.sum(K.square(y_true), -1) + K.sum(K.square(y_pred), -1) + smooth)


    def dice_coef_loss(y_true, y_pred):
        return 1 - dice_coef(y_true, y_pred)


    #https://lars76.github.io/2018/09/27/loss-functions-for-segmentation.html

    # example of a combined loss
    def combined_loss(y_true, y_pred):
        def dice_loss(y_true, y_pred):
            y_pred = tf.math.sigmoid(y_pred)
            numerator = 2 * tf.reduce_sum(y_true * y_pred)
            denominator = tf.reduce_sum(y_true + y_pred)

            return 1 - numerator / denominator

        y_true = tf.cast(y_true, tf.float32)
        o = tf.nn.sigmoid_cross_entropy_with_logits(y_true, y_pred) + dice_loss(y_true, y_pred)
        return tf.reduce_mean(o)

    def combined_loss2(y_true, y_pred):
        def dice_loss(y_true, y_pred):

            y_pred = tf.math.sigmoid(y_pred) # cool donc on peut faire ça!!!
            numerator = 2 * tf.reduce_sum(y_true * y_pred)
            denominator = tf.reduce_sum(y_true + y_pred)

            return 1 - numerator / denominator

        y_true = tf.cast(y_true, tf.float32)
        # o = tf.nn.sigmoid_cross_entropy_with_logits(y_true, y_pred) + dice_loss(y_true, y_pred)
        o = mean_absolute_error(y_true[...,0], y_pred[...,0]) + dice_loss(y_true[...,1], y_pred[...,1])+ dice_loss(y_true[...,2], y_pred[...,2])
        return tf.reduce_mean(o)



    # or ...--> easy to implement with channels I guess
    # model.compile(loss=lambda y_true, y_pred: (1 - alpha) * mse(y_true, y_pred) + alpha * gse(y_true, y_pred),
    #     ...)

    alpha = 0.2
    # another combined loss
    # def my_loss(y_true, y_pred):
    #     return (1 - alpha) * mse(y_true, y_pred) + alpha * gse(y_true, y_pred)


    # def make_my_loss(alpha):
    #     def my_loss(y_true, y_pred):
    #         return (1 - alpha) * mse(y_true, y_pred) + alpha * gse(y_true, y_pred)
    #
    #     return my_loss

    # def make_my_loss(alpha):
    #     def my_loss(y_true, y_pred):
    #         return (1 - alpha) * mse(y_true, y_pred) + alpha * gse(y_true, y_pred)
    #
    #     return my_loss


    # should I shake it more ???


    #  maybe try

    # could use split and make this a CARESEG specific loss
    # assume mask

    # the loss seems to work but the learning seems slower in a way... because mae is reduced more slowly but in fact it's hard to compare

    def bce_jaccard_loss_only_in_mask(y_true, y_pred):
        try:
            # tf.print('final step', 'in there')
            masked_true = tf.boolean_mask(y_true, tf.math.is_finite(y_true))
            masked_pred = tf.boolean_mask(y_pred, tf.math.is_finite(y_true))
            # tf.print('second step')
            # bce_jaccard = sm.losses.bce_jaccard_loss(masked_true, masked_pred) # bug is here --> why and where


            jaccard = jaccard_distance_loss(masked_true, masked_pred)
            # tf.print('final step', jaccard)
            jaccard = tf.reduce_mean(jaccard)

            bce = binary_crossentropy(masked_true, masked_pred)
            # tf.print('final step', jaccard)
            bce = tf.reduce_mean(bce)

            bce_jaccard=bce+jaccard

            # tf.print('final step', bce_jaccard)
            # ça marche ça va jusque là...
            return bce_jaccard
        except:
            bce_jaccard = sm.losses.bce_jaccard_loss(y_true, y_pred)
            bce_jaccard = tf.reduce_mean(bce_jaccard)
        return bce_jaccard  # n

    def loss_only_in_mask2(y_true, y_pred):
        try:
            # get mask from y_true and apply it to y_pred before quantif
            # mask = tf.zeros(dims)  # now bug here cause

            # tf.print('finite', tf.math.is_finite(y_true)) # always the case

            masked_true = tf.boolean_mask(y_true, tf.math.is_finite(y_true))
            masked_pred = tf.boolean_mask(y_pred, tf.math.is_finite(y_true))

            # now that works no clue what I had done
            # tf.print(tf.shape(mask_true), "masked shape")
            #
            # y_true = tf.boolean_mask(y_true, mask)
            # y_pred = tf.boolean_mask(y_pred, mask)

            # always crashes here
            # tf.print(tf.shape(masked_true), "masked size")
            # tf.print(tf.size(y_true), 'original size') # seems ok

            # why different
            mae = mean_absolute_error(masked_true, masked_pred)
            mae = tf.reduce_mean(mae)

            # tf.print(mae, tf.reduce_mean(mean_absolute_error(y_true, y_pred))) # ok
            # tf.print('to the end')
            return mae
        except:
            mae = mean_absolute_error(y_true, y_pred)
            mae = tf.reduce_mean(mae)
            return mae  # n

    def loss_only_in_mask(y_true, y_pred):
        tf.print(tf.shape(y_true), "Inside mask loss function true")
        tf.print(tf.shape(y_pred), "Inside mask loss function pred") # fails
        tf.print(tf.keras.backend.int_shape(y_true), "Inside mask loss function")
        tf.print(tf.keras.backend.int_shape(y_pred), "Inside mask loss function")

        # do a simple mae but only in masked array
        # generate empty mask in the same way

        # do create a mask for all arrays with nans then just extract the nan part
        # en fait prendre le negatif d'un mask car plus simple

        try:
            tf.print('in me')
            # tf.print(type(tf.make_ndarray(tf.shape(y_true))))
            # type(np.array(y_true))

            # dims =np.array(y_true).shape # now crash is here???

            # for v in tf.shape(y_true):
            #     tf.print(v)
            #     tf.print(type(v))

            # dims = [v for v in tf.shape(y_true)]
            # tf.compat.v1.enable_eager_execution()
            tf.print('dimsi')

            # tf.print(tf.shape(y_true).get_shape().as_list()) # ok --> not ok
            # tf.print(tf.shape(y_true).as_list()) # ok --> not ok --> marche pas --> too bad --> how can I get this right
            tf.print(str(tf.shape(y_true))) # not ok

            tf.print(type(y_true.get_shape().as_list())) # --> crash
            tf.print(y_true.get_shape().as_list()) # ok but next is a bug

            # dims = tf.shape(y_true).numpy() # bug is really there --> WHY ??? --> because no eager execution because no eager in compile


            dims=y_true.get_shape().as_list() # why bug
            # fuck it...
            tf.print('dims2', dims) # ok --> bug is in the conversion below

            # bug here
            # dims = tuple(map(tuple, dims))

            # tup = tf.tuple(tf.shape(y_true))
            # tf.print('dims3', tup)

            tf.print('shape', tf.shape(y_true))
            tf.print('shape2', type(tf.keras.backend.shape(y_true))) #pas mal ?
            # kvar = tf.keras.backend.variable(value=y_true)
            # tf.print('shape3', tf.keras.backend.int_shape(kvar)) # always none ??? --> why

            tf.print('shape4',tf.keras.backend.shape(y_true)[0]) # --> is ok --> how can I get it then


            shapeeee = tf.keras.backend.shape(y_true)
            # dims = [v for shapeeee in range(len(shapeeee))]
            dims=[]
            for shapee in range(len(shapeeee)):
                dims.append(shapeeee[shapee])

            tf.print('neo dims', dims)
            tf.print('neo dims', type(dims))

            tf.print('neo dims3', tuple(dims)) #perfect

            tf.print('shape3', tf.keras.backend.int_shape(y_true)) # always none ??? --> why

            tf.print('static', tf.get_static_value(dims[1])) # gives me none

            # tf.print(y_true.shape.as_list()) # not ok all is None
            # tf.print(tf.int_shape(y_pred))
            # tf.print(y_pred.int_shape)

            # tf.print('shape', tf.shape(y_true).eval())

            # tf.print(tf.shape(y_true).as_list())
            # tf.print(tf.shape(y_true)[0].value)
            # tf.print('shape', tf.shape(y_true))

            # dims = tf.shape(y_true)
            # dims = tuple([dims[i].value for i in range(0, len(dims))])

            # NB USE Y_PRED BECAUSE Y TRUE IS ONLY KNOWN DURING
            #I think this is because y_true is only known during training, whereas when you are compiling your model, y_pred is known from the model

            # dims = tuple(dims)
            tf.print('dims', dims)
            tf.print(type(dims[0])) # it is again a fucking tensor --> how do i get an int
            # tf.print(tf.get_static_value(dims[0])) # gives none
            # tf.print(type(dims[0].eval())) # it is again a fucking tensor --> how do i get an int # crashes

            # tf.keras.backend.int_shape(y_true)[0]

            # tf.print(tf.keras.backend.eval(dims[0]) )
            #
            # dims =y_true.tensor_shape.dim
            # shape = tuple(d.size for d in dims)
            # tf.print(shape)

            # tf.print(type(dims[0].as_list())) # it is again a fucking tensor --> how do i get an int # bug here
            # tf.print(type(dims[0].as_list()[0])) # it is again a fucking tensor --> how do i get an int
            dims = tuple(dims)

            tf.print('in me2')
            # crash is here...

            # tf.print(dims) # maybe it cannot print a tuple ???
            # bug is here but why
            tf.print('dims3', dims)
            # need implement function in there ??? --> best is to pass directly the mask to the output ?--> how can I do that
            # mask = mask_rows_or_columns(dims, spacing_X=2, spacing_Y=5, return_boolean_mask=True) # crash is here --> can it be fixed --> ok I'll never manage --> just fix it

            # if isinstance(img, tuple):
            mask = tf.zeros(dims) # now bug here cause
            # trop compliqué --> generer le mask dehors et l'appliquer ici --> assez facile en plus --> car si j'applique un mask sur l'original alors je prend le negatif pour l'autre --> peut donner une fonction simple en fait


            tf.print('dims4')
            # else:
            #     mask = np.zeros(img.shape, dtype=np.bool)

            # if mask.ndim < 3:  # assume no channel so add one
            #     mask = mask[..., np.newaxis]

            spacing_X = 2
            spacing_Y = 5
            random_start = False

            initial_shiftX = 0
            initial_shiftY = 0

            if spacing_X is not None:
                if spacing_X <= 1:
                    spacing_X = None
            if spacing_Y is not None:
                if spacing_Y <= 1:
                    spacing_Y = None

            import random
            if random_start:
                if spacing_X is not None:
                    initial_shiftX = random.randint(0, spacing_X)
                if spacing_Y is not None:
                    initial_shiftY = random.randint(0, spacing_Y)

            tf.print('dims5')
            # bug was here


#https://towardsdatascience.com/how-to-replace-values-by-index-in-a-tensor-with-tensorflow-2-0-510994fe6c5f --> maybe the solution
            # assume all images are with a channel --> probably the best way to do things
            for c in range( y_pred.get_shape().as_list()[-1]):# bug is here
                # rentre et crashe
                tf.print('cccccccc',c)
                tf.print('cccccccc2', len(y_pred.get_shape().as_list()))
                # ok
                if spacing_Y is not None:

                    # if len(y_pred.get_shape().as_list()) > 3:
                    tf.print('ddd', len(mask.shape))
                    tf.print(type(mask)) # c'est un tenseur --> pkoi
                    tf.print(spacing_Y)
                    tf.print(spacing_X)
                    tf.print(initial_shiftX)
                    tf.print(initial_shiftY)
                    tf.print(c)
                    if len(mask.shape) > 3:
                        tf.print('cccccccc3')
                        # mask[..., initial_shiftY::spacing_Y, :, c] = 1 # bug is here but why ??? # les doubles ne marchent pas ???
                        tf.fill(mask[..., initial_shiftY::spacing_Y, :, c],1.)
                        tf.print('cccccccc4')
                    else:
                        mask[initial_shiftY::spacing_Y, :, c] = 1
                if spacing_X is not None:
                    mask[..., initial_shiftX::spacing_X, c] = 1

            # tf.fill([2, 3], 9)

            tf.print('dims6')

            # if return_boolean_mask or isinstance(img, tuple):
            #     return mask

            # if img.ndim < 3:  # assume no channel so add one
            #     img = img[..., np.newaxis]
            #
            # # apply mask to image
            # img[mask] = masking_value

            # return img
            tf.print('maskeee', mask)

            tf.print('dims2', dims)
            tf.print('in me3')
            y_true = tf.boolean_mask(y_true, mask)
            y_pred = tf.boolean_mask(y_pred, mask)

            # always crashes here
            tf.print(tf.shape(y_true), "masked size")

            mae = mean_absolute_error(y_true, y_pred)
            mae = tf.reduce_mean(mae)
            return mae
        except:
            mae = mean_absolute_error(y_true, y_pred)
            mae = tf.reduce_mean(mae)
            return mae # need return a tensor ... otherwise can't compute the gradient TODO do this more smartly at some point


    # TODO instead of the for loop --> just split all channels but the first to a new thing --> faster and more elegant
    # before I had plenty of bugs because I was not having arrays instead of single values the tf.print helped me a lot fix all the issues...
    def denoise_and_segmentation_loss(y_true, y_pred):
        # if y_true is None:
        #     return 1000000
        # if not isinstance(y_true, list):
        #     y_true = [y_true]
        # if not isinstance(y_true, list):
        #     y_true = [y_true]
        # TODO just do that but split by channels now

        # ça ça marche
        # if True:
        # return mean_absolute_error(y_true, y_pred)
        # return sm.losses.bce_jaccard_loss(y_true, y_pred) # ça ça marche

        tf.print(tf.shape(y_true), "Inside loss function") # only way to print inside a loss function...
        # could have one random init per round so that the mask position changes always or one random seed per stuff --> just try it

        # if True:
        #     return
        # print(y_true.numpy().shape)
        # ytrue_shape = tf.shape(y_true)
        # multiples = tf.concat((tf.shape(ytrue_shape)[:2], [1]), axis=0)
        # print(ytrue_shape)

        # print(ytrue_shape.as_list()) --> marche pas
        # print(y_true.get_shape().as_list())
        # print(K.int_shape(y_true)[-1]) # that is probably what I wnat in fact !!!
        # print(K.int_shape(y_true)) # this is what I want ... --> not working --> all none
        # print(K.int_shape(y_pred)) # this is what I want ... --> not working --> all none
        # putain ça marche je sais pas pkoi
        # print(K.int_shape(y_pred)[-1]) # putain ça marche!!!
        # print(y_pred.get_shape().as_list()[-1]) # ça aussi ça marche --> these are my channels

        # try:
        eps = 1e-8
        # c= 0
        # print('2', y_true.shape)
        # tensor_shape[0].value
        # print(y_true.shape.value[-1])
        # mae = mean_absolute_error(y_true[:,:,:, c], y_pred[:,:,:, c])

        # maybe really put mae here -->

        # TO use tf.split here
        # TODO maybe keep extras for the GT even if mismatch --> maybe assume always the last image is the masking data and the rest is consistent --> that is a good idea I think I need to change my code dramatically in the channel handler part of it...

        # mae = tf.keras.losses.MeanAbsoluteError()
        # mae(y_true, y_pred).numpy()


        # before
        mae = mean_absolute_error(y_true[..., 0], y_pred[..., 0])
        mae = tf.reduce_mean(mae)

        # now is that better ???
        # mae = tf.keras.losses.MeanAbsoluteError(y_true[..., 0], y_pred[..., 0])
        # tf.print('first mae', mae)
        # mae = tf.reduce_mean(mae)



        # mae = tf.reduce_mean(tf.abs(y_true[..., 0] - y_pred[..., 0]))
        # print('mae', mae)
        # mae = mean_absolute_error(y_true[..., 0], y_true[..., 0])
        # print('mae', mae)
        iou_loss = 0

        channels_to_concat = []
        # concat = K.concatenate([mae])
        # concat = K.concatenate([iou_loss, concat])
        # c+=1
        for c in range(1, y_pred.get_shape().as_list()[-1]):
            # print('bce_jaccard_loss', sm.losses.bce_jaccard_loss(y_true[..., c], y_pred[..., c]))
            # while True:
            #     try:
            # iou_loss += sm.losses.bce_jaccard_loss(y_true[:,:,:, c], y_pred[:,:,:, c]) # to avoid Nans since not a binary output
            # iou_loss += sm.losses.bce_jaccard_loss(y_true[..., c], y_pred[..., c]) # to avoid Nans since not a binary output # maybe need use jaccard
            # iou_loss += sm.losses.jaccard_loss(y_true[..., c], y_pred[..., c]) # to avoid Nans since not a binary output # maybe need use jaccard
            # iou_loss += sm.losses.bce_jaccard_loss(y_true[..., c], y_pred[..., c]) # to avoid Nans since not a binary output # maybe need use jaccard

            # iou_loss+=1.-tf.keras.metrics.MeanIoU(y_true[..., c], y_pred[..., c])
            # iou_loss+=jaccard_distance(y_true[..., c], y_pred[..., c])

            # intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
            # sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
            # jac = (intersection + smooth) / (sum_ - intersection + smooth)
            #
            # #  it's probably a tensor and so I should not do that but something smarter
            #
            # iou_loss = (1 - jac) * smooth
            # iou_loss =tf.reduce_mean(iou_loss)

            # TODO maybe try bce as in denoiseg since it works for them
            # iou_loss = binary_crossentropy(y_true[..., c], y_pred[..., c])
            iou_loss = sm.losses.bce_jaccard_loss(y_true[..., c], y_pred[..., c])
            channels_to_concat.append(tf.reduce_mean(iou_loss))

            # iou_loss += sm.losses.jaccard_loss(y_true[..., c], y_true[..., c]) # to avoid Nans since not a binary output # maybe need use jaccard
            # c+=1
        # except:
        #     break
        # sm.losses.bce_jaccard_loss
        # sm.losses.jaccard_loss
        # sm.losses.bce_dice_loss
        # sm.metrics.iou_score

        # if iou_loss !=0:
        #     iou_loss/=y_pred.get_shape().as_list()[-1]-1 + eps

        # equally weigh segmentation and iou
        # concat = tf.concat(channels_to_concat, axis=0) #
        # concat = K.concatenate(channels_to_concat)
        # concat =tf.stack(channels_to_concat)
        # return K.mean(concat)

        # I guess that is what I want !!!
        iou_loss = sum(channels_to_concat) / len(channels_to_concat)



        # could even append mask on the fly to read GT image in order to increase its size --> very good idea and maybe not that hard

        tf.print('iou', iou_loss)
        tf.print('mae', mae)


        total = iou_loss+mae # could divide by 2 but useless in fact... # I do give more weight here to denoise compared to seg --> about half half so far...
         # is this a tensor ??? there is a bug here

        # total = tf.reduce_mean(total)
        tf.print('total', total)

        return total



    # what about that https://lars76.github.io/2018/09/27/loss-functions-for-segmentation.html
    # TODO essayer de faire des masked arrays et de quantifier que dans les masks??? --> see how to do that


    # I think I fixed the loss now but test it
    # mon denoise_and_segmentation_loss ne marche pas du tout --> pourtant c'était smart, je comprends vraiment pas ... !!!
    loss = sm.losses.bce_jaccard_loss # loss_only_in_mask2 # bce_jaccard_loss_only_in_mask  # denoise_and_segmentation_loss # combined_loss2 #combined_loss # denoise_and_segmentation_loss # 'mae' # sm.losses.bce_dice_loss # 'mae' # sm.losses.bce_dice_loss # sm.losses.bce_jaccard_loss # sm.losses.bce_dice_loss #sm.losses.bce_jaccard_loss #sm.losses.binary_focal_dice_loss #sm.losses.jaccard_loss #'binary_crossentropy'  #'categorical_crossentropy' #'mean_squared_error'#'mean_squared_error' #sm.losses.bce_jaccard_loss #'binary_crossentropy' #'mean_squared_error'
    metrics = ['mae','mse', sm.metrics.iou_score, 'bce']



    FORCE_RECOMPILE = True
    # TRAIN SETTINGS
    if not deepTA.is_model_compiled() or FORCE_RECOMPILE:
        print('compiling model')
        deepTA.compile(optimizer=optimizer, loss=loss, metrics=metrics) # here that would be smart to allow for eager execution or not depending on what I want --> think about it

    # try a CARE hybrid training...
    NB_EPOCHS = 150 #100 # 200 # 100 #180  # 80 # 100 # 10 # 150

    deepTA.get_loaded_model_params()

    print('before training')

    deepTA.train(metaAugmenter, epochs=NB_EPOCHS, steps_per_epoch=-1, batch_size_auto_adjust=False, upon_train_completion_load='best', reduce_lr_on_plateau=0.5, patience=10)

    print('before training')


    deepTA.saveModel()
    deepTA.saveAsJsonWithWeights()
    deepTA.plot_graph(deepTA.model._name + '_graph.png')

    if True:
        import sys
        sys.exit(0)

    default_input_width = 256 # 256  # 576  # 128 # 64
    default_input_height = 256 # 256  # 576 # 128 # 64

    # input_folder = '/home/aigouy/Bureau/last_model_not_sure_that_works/tmp/'
    # input_folder = '/D/Confocal_le_bivic/160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia/proj/'
    # input_folder = '/D/Confocal_le_bivic/160608_test_allula_or_costa_invagination/proj'
    # input_folder = '/D/Confocal_le_bivic/140415_tests/Projections/max_projs'
    # input_folder = '/D/Confocal_le_bivic/141209_EcadKI_clones_19h30APF/Projections/max_projs'
    # input_folder = '/home/aigouy/Bureau/last_model_not_sure_that_works/test_images_for_paper'
    # input_folder = '/D/Confocal_le_bivic/160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia/proj'
    # input_folder = '/home/aigouy/Bureau/final_folder_scoring'

    input_folder = '/D/final_folder_scoring/'

    predict_generator = deepTA.get_predict_generator(
        inputs=[input_folder], input_shape=input_shape,
        output_shape=output_shape, default_input_tile_width=default_input_width, default_input_tile_height=default_input_height, # default_tile_height
        tile_width_overlap=32,
        tile_height_overlap=32, input_normalization=input_normalization, clip_by_frequency=0.01)

    # predict_output_folder = os.path.join('/home/aigouy/mon_prog/Python/Deep_learning/unet/data/membrane/test',
    #                                      deepTA.model._name if deepTA.model._name is not None else 'model')  # 'TA_mode'
    predict_output_folder = os.path.join(input_folder, 'predict')
    deepTA.predict(predict_generator, output_shape, predict_output_folder=predict_output_folder,
                   batch_size=1)

    print("total time", timer() - start) # --> 404 secs for 4 normal images --> 7 mins --> a lot too. also a lot even just showing the image takes forever... --> 5184.843459615s pr la mega aile de raphael --> 1h30 heures pour ces 3 images mais c'est entierement du a la derniere --> but it uses cpu --> no clue why ???

