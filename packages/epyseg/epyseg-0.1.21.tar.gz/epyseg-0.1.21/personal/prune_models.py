# https://help.github.com/en/github/managing-large-files/about-git-large-file-storage --> to allow to push files larger than limit size

# can I put a hash to force new download

# TODO test below to see if that works because it would suffice most likely
# try reduce by half without losing precision
import pathlib
from zipfile import ZipFile
import os

import tensorflow as tf

from epyseg.deeplearning.deepl import EZDeepLearning

import hashlib


# in colab
#import urllib.request
# import os
# cache_dir = os.path.join(os.path.expanduser('~'), '.keras')
# print(cache_dir)
# %ls /root/.keras

# model_weights = tf.keras.utils.get_file(fname='test.h5', origin='https://gitlab.com/baigouy/models/-/raw/master/model_linknet-vgg16_shells.h5', archive_format=None, extract=False)

# import urllib.request
# url = 'https://gitlab.com/baigouy/models/-/raw/master/model_linknet-vgg16_shells.h5'
# opener = urllib.request.build_opener()
# opener.addheaders = [('User-agent', 'Mozilla/5.0')]
# urllib.request.install_opener(opener)
#
# def show_progress(cur_block, block_size, total_size):
#     downloaded = cur_block * block_size
#     if cur_block % 100 == 0:
#         print(round((downloaded/total_size)*100,1),'%')
#     if downloaded == total_size:
#         print('download complete...')
#
# urllib.request.urlretrieve(url, '/home/aigouy/Bureau/test.h5', reporthook=show_progress) # it works, gitlab blocks bots and require user-agent to be set
#
# # if cache_dir is None:
# cache_dir = os.path.join(os.path.expanduser('~'), '.keras')
# epyseg_path = os.path.join(cache_dir, 'epyseg')
# os.makedirs(epyseg_path, exist_ok=True)
# print(cache_dir, epyseg_path)



# labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')

# if True:
#     import sys
#     sys.exit(0)



def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()



if True:
    import sys

    print(md5('/home/aigouy/mon_prog/Pretrained_models_gitlab/models/models/model_linknet-vgg16_shells_v2.h5'))
    print(md5('/home/aigouy/mon_prog/Pretrained_models_gitlab/models/models/model_linknet-vgg16_shells.h5'))
    sys.exit(0)




#https://keras.io/getting_started/faq/#what-are-my-options-for-saving-models
input_output_files = [('/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Linknet-seresnext101-smloss-256x256/Linknet-seresnext101-smloss-256x256-ep0099-l0.158729.h5', '/home/aigouy/mon_prog/Pretrained_models/model_Linknet-seresnext101.h5'),
                      ('/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/linknet_vgg16_shells_inverted_seeds_inverted_amazing/linknet-vgg16-sigmoid-ep0191-l0.144317.h5','/home/aigouy/mon_prog/Pretrained_models/model_linknet-vgg16_shells.h5')]
# input_output_files = [('/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/FPN-inceptionresnetv2-smloss-256x256','/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/FPN-inceptionresnetv2-smloss-256x256/weights_only.h5')]
# do a list of models to compress

# tflite_model_file = '/tmp/compressed.h5'
# input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/vggunet7/model_1-ep0097-l0.052965.h5'
# input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-smloss-256x256/Unet-inceptionresnetv2-smloss-256x256-ep0099-l0.159963.h5'

# no clue why but hash is different --> WHY ??? --> each save weight seems different
# no matter it's ok anyway...


file2 = open(os.path.join(os.path.dirname(input_output_files[0][1]),'hashes.txt'), "w+")
deepl = EZDeepLearning()

for input_file,output_filename in input_output_files:

    # filename0_without_path = os.path.basename(f)
    # filename0_without_ext = os.path.splitext(filename0_without_path)[0]
    # parent_dir_of_filename0 = os.path.dirname(f)

    # 1d947a0007d87a6372ad2c6eb7bc471d hash example
    # abf84554775db712f188cf7acee967a8 # why not same hash --> pb --> do not zip --> better
    deepl.load_or_build(model=input_file)
    deepl.saveWeights(deepl.model, name=output_filename) # this reduces size by 3 already --> use that --> a much better deal...

    # DUE TO TIME STAMP HASH IS ALWAYS CHANGING DESPITE SAME CONTENT --> not good
    # TODO then zip it and then
    # with ZipFile('/D/datasets_deep_learning/test2.h5.zip', 'w') as myzip:
    #     myzip.write('/D/datasets_deep_learning/test2.h5', arcname=os.path.basename('/D/datasets_deep_learning/test2.h5'))

    # class gzip.GzipFile(filename=None, mode=None, compresslevel=9, fileobj=None, mtime=None)¶ # or set time stamp constant
    # import gzip
    #
    # content = b"Lots of content here"
    # with gzip.open('/home/joe/file.txt.gz', 'wb') as f:
    #     f.write(content)
    # os.remove('/D/datasets_deep_learning/test2.h5')

    # hash = md5('/D/datasets_deep_learning/test2.h5.zip')
    hash = md5(output_filename)
    print(hash)
    #and get hash for the file

    #b2346c5d1ca7d0cda457dc7a29448ab0

    file2.write(output_filename+'\t'+hash+'\n')
file2.close()

# save then reload a .pb model --> need drag n drop the folder --> just try that and add it to my stuff!!!
# Save the entire model as a SavedModel.
# !mkdir -p saved_model
# model.save('saved_model/my_model')
# new_model = tf.keras.models.load_model('saved_model/my_model')
#
# Check its architecture
# new_model.summary()

# TODO do that for a list of files. Also save hashes to a file

# converter = tf.lite.TFLiteConverter.from_keras_model(deepl.model)
# tflite_model = converter.convert()
# with open(tflite_model_file, 'wb') as f:
#   f.write(tflite_model)

# Converting ConcreteFunctions to a TensorFlow Lite model.
# converter = tf.lite.TFLiteConverter.TFLiteConverter.from_concrete_functions([func])
# tflite_model = converter.convert()


if True:
    import sys
    sys.exit(0)


# see here
# https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/performance/post_training_float16_quant.ipynb#scrollTo=3gwhv4lKbYZ4

# c'est ici que je veux faire le hash

input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-smloss-256x256/Unet-inceptionresnetv2-smloss-256x256-ep0099-l0.159963.h5'
deepl = EZDeepLearning()
deepl.load_or_build(model=input_file)

# converter = tf.lite.TFLiteConverter.from_keras_model(deepl.model)
# converter.optimizations = [tf.lite.Optimize.DEFAULT]
# converter.target_spec.supported_types = [tf.float16]


# tflite_model = converter.convert()
tflite_models_dir = pathlib.Path("/tmp/mnist_tflite_models/")
tflite_models_dir.mkdir(exist_ok=True, parents=True)
# tflite_model_file = tflite_models_dir/"mnist_model.tflite"
# tflite_model_file.write_bytes(tflite_model)
converter = tf.lite.TFLiteConverter.from_keras_model(deepl.model)
tflite_model = converter.convert()

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

tflite_fp16_model = converter.convert()
tflite_model_fp16_file = tflite_models_dir/"mnist_model_quant_f16.tflite"
tflite_model_fp16_file.write_bytes(tflite_fp16_model)




# TO load the model
interpreter_fp16 = tf.lite.Interpreter(model_path=str(tflite_model_fp16_file))
interpreter_fp16.allocate_tensors()

if True:
    import sys
    sys.exit(0)

import tensorflow as tf
import sys
from epyseg.deeplearning.deepl import EZDeepLearning

# to get a list of pretrained models
for method in EZDeepLearning.available_model_architectures:
    for backbone in EZDeepLearning.available_sm_backbones:
        for activation in EZDeepLearning.last_layer_activation:
            if 'igmoid' in activation and not 'hard' in activation:
                print("'"+method + '-' + backbone + '-' + activation+"'"+':None,')



# input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-smloss-256x256/Unet-inceptionresnetv2-smloss-256x256-ep0099-l0.159963.h5'
# input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-smloss-256x256/Unet-inceptionresnetv2-smloss-256x256_weights.h5'
input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-smloss-256x256/Unet-inceptionresnetv2-smloss-256x256_weights.zip'
print(md5(input_file))  #1517b6db11f5df93fbdc0bb6dd65ae3e #08734b616959936f64ff90b3492f7207 #233e759ce608202c980d273224573218 --> need hash it myself




# here is how tf can download a file
# labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')

# hack to make it download in model folder
# marche pas si le folder existe pas ... pas tres grave si sauve dans les datasets....
# labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt') # if file exists then it does not download it...

# ça marche if file_hash differs it downloads it again --> exactly what I wanted and needed for upload
# caches it in an epyseg dir --> that is also perfectly what I want and can also extract it
labels_path = tf.keras.utils.get_file('Unet-inceptionresnetv2.h5','file://'+input_file, file_hash='1517b6db11f5df93fbdc0bb6dd65ae3e',cache_subdir='epyseg', hash_algorithm='auto', extract=True, archive_format='auto') # if file exists then it does not download it...

# that's really great because it does really output the file --> ok I'm ready to add pretrain and ideally store files on github if possible if I just use weights --> maybe doable...
# labels_path = tf.keras.utils.get_file('Unet-inceptionresnetv2-epyseg.h5','file://'+input_file, md5_hash='08734b616959936f64ff90b3492f7207') # if file exists then it does not download it...
# par contre si le fichier existe il ne reload pas...
print(labels_path)

# TODO save my weights


# tf.keras.utils.get_file(
#     fname, origin, untar=False, md5_hash=None, file_hash=None,
#     cache_subdir='datasets', hash_algorithm='auto', extract=False,
#     archive_format='auto', cache_dir=None
# )



# /home/aigouy/.keras/models --> c'est là que tf store les modeles --> cool


# model compression https://www.dlology.com/blog/how-to-compress-your-keras-model-x5-smaller-with-tensorflow-model-optimization/ better https://www.tensorflow.org/model_optimization/guide/pruning/pruning_with_keras
# https://www.tensorflow.org/model_optimization/guide/pruning/pruning_with_keras --> best

# TODO try model sparsity --> where can i save stuff in the meantime --> try not saving optimizer ...

# https://www.tensorflow.org/api_docs/python/tf/lite/TFLiteConverter
# ça marche mais j'arrive pas à le rouvrir...

tflite_model_file = '/tmp/compressed.h5'
# input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/vggunet7/model_1-ep0097-l0.052965.h5'
input_file = '/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Unet-inceptionresnetv2-smloss-256x256/Unet-inceptionresnetv2-smloss-256x256-ep0099-l0.159963.h5'
# converter = tf.lite.TFLiteConverter.from_keras_model_file(input_file)
# tflite_model = converter.convert()
# with open(tflite_model_file, 'wb') as f:
#   f.write(tflite_model)



# Converting a SavedModel to a TensorFlow Lite model.
# converter = tf.lite.TFLiteConverter.from_saved_model(input_file)
# tflite_model = converter.convert()

# Converting a tf.Keras model to a TensorFlow Lite model.

# ça marche --> reduit par trois les weights --> cool
if True:
    sys.exit(0)