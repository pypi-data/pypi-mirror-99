# list files and do the copy to separate folder

import numpy as np
import matplotlib.pyplot as plt
import glob
import traceback
import os
import re
from natsort import natsorted


# better than denoiseg could learn to reconstitute max proj or better from Z stacks
from epyseg.img import Img

TA_mode = False # if false save in a single output folder, if True, save in TA mode...
# ALSO_SAVE_MASK = True # if true save mask if false ignore mask
ALSO_SAVE_MASK = True # if true save mask if false ignore mask
# excluded_image_nb= [4,324]
excluded_image_nb= []
channel_of_interest = 1


# input_path = '/D/datasets_to_release/long_WT/'
# input_path = '/D/datasets_to_release/080205_WT_63X15h/proj/'
# input_path = '/D/datasets_to_release/dataset_1_segmentation_tmp_recorrected/'
# output_path_originals = '/D/datasets_to_release/dataset_1_originals'
# output_path_segmentation = '/D/datasets_to_release/dataset_1_segmentation'
input_path = '/D/datasets_to_release/histo/'
output_path_originals = '/D/datasets_to_release/dataset_2_originals'
output_path_segmentation = '/D/datasets_to_release/dataset_2_segmentation'




# do a glob to get files

files = glob.glob(input_path + "*.png") + glob.glob(input_path + "*.jpg") + glob.glob(input_path + "*.jpeg") + glob.glob(
    input_path + "*.tif") + glob.glob(input_path + "*.tiff")+ glob.glob(input_path + "*.lsm")+ glob.glob(input_path + "*.czi") + glob.glob(input_path + "*.lif")
files = natsorted(files)

counter = 0

for file in files:
    filename0_without_path = os.path.basename(file)
    filename0_without_ext = os.path.splitext(file)[0]
    # digits_in_name = int(filter(str.isdigit, filename0_without_path))
    digits_in_name = int((re.findall('\d+', filename0_without_path ))[0])
    print(digits_in_name)
    if digits_in_name in excluded_image_nb:
        print('excluding ', filename0_without_path)
        continue
    print(filename0_without_path)

    # do stuff here


    orig = Img(file)
    if orig.has_c():
        orig=orig[...,channel_of_interest]

    # plt.imshow(orig)
    # plt.show()

    exclude_image = False
    if ALSO_SAVE_MASK:
        # check if mask exists
        segmentation_file = os.path.join(filename0_without_ext,'handCorrection.tif')
        if not os.path.exists(segmentation_file):
            segmentation_file = os.path.join(filename0_without_ext, 'handCorrection.png')
        if os.path.exists(segmentation_file):
            segmentation_mask = Img(segmentation_file)
            if segmentation_mask.has_c():
                segmentation_mask = segmentation_mask[...,0]
            if not TA_mode:
                Img(segmentation_mask, dimensions='hw').save(os.path.join(output_path_segmentation, str(counter) + '.tif'), print_file_name=True)
            else:
                Img(segmentation_mask, dimensions='hw').save(os.path.join(output_path_segmentation, str(counter), 'handCorrection.tif'), print_file_name=True)
        else:
            exclude_image = True

    if not exclude_image:
        Img(orig, dimensions='hw').save(os.path.join(output_path_originals, str(counter)+'.tif'), print_file_name=True)


    counter+=1



# check that a mask exist for the file and if so --> copy it --> in fact just copy one channel

# rename by simply having an increment

# also allow it to work without mask and in that case I can substitute for the stuff

# also allow TA mode

# or just translate from one list to the other

# also copy the channel of interest for the input



# match name by digit --> could be a way --> just get digit for matching

