# ça a l'air de marcher ... --> juste connecter le truc pr tt finir

# average or max or... the outputs of deep learning
# allow it to work with folders or with files and in TA mode or in another mode --> in fact just need to save the files processed --> TODO
# TODO maybe allow post processing of the file... --> TODO
# need get the parameters and



# si c'est un dossier --> loop inside the folder
from PyQt5.QtWidgets import QApplication

import sys
from epyseg.img import Img
import numpy as np
import traceback
import os
import matplotlib.pyplot as plt


# est ce que je rajoute des images ou pas ???
# idealement devrait verifier que les noms des fichiers soient les memes
# for output I also need check whether TA mode or not...

# if single folder increment
from epyseg.postprocess.filtermask import simpleFilter
from epyseg.postprocess.gui import PostProcessGUI
from epyseg.postprocess.refine import EPySegPostProcess
from epyseg.postprocess.refine_v2 import RefineMaskUsingSeeds


def ensemble(input, output=None, mode='average', TA_mode=False):
    # if folder then list files in it
    # load all files then do average or alike
    # for avg or max can be done two by two images
    # should I always average

    # if input is folder then

    output_files = []

    for iii in range(len(input[0])):
        print('#' * 60)
        try:
            first = None
            output_name = None
            dimensions = None
            counter = 1
            if 'med' in mode.lower():
                # add all images to an array and do the median of it
                images = []
                first_run = True
                for folder in input:
                    file = folder[iii]
                    print(file)
                    img = Img(file)
                    if first_run:
                        dimensions = img.metadata['dimensions']
                        first_run = False
                        output_name = os.path.basename(file)
                        output_name = os.path.splitext(output_name)[0]
                        if TA_mode:
                            output_name = os.path.join(os.path.basename(os.path.dirname(file)), output_name)
                            print(TA_mode, output_name)
                    images.append(img)
                first = np.median(np.stack(images), axis=0)
                print('computing median')
            else:
                for folder in input:
                    file = folder[iii]
                    print(file)
                    img = Img(file)
                    if first is None:
                        dimensions = img.metadata['dimensions']
                        output_name = os.path.basename(file)
                        output_name = os.path.splitext(output_name)[0]
                        if TA_mode:
                            output_name = os.path.join(os.path.basename(os.path.dirname(file)), output_name)
                            print(TA_mode, output_name)
                        first = img
                        if 'av' in mode.lower():
                            first = first.astype(np.float32)
                        del img
                    elif 'av' in mode.lower():
                        # images must be of the same type
                        first += img
                        counter += 1
                    elif 'max' in mode.lower():
                        first = np.maximum(img, first)  # do the max proj --> should be ok
                    elif 'min' in mode.lower():
                        first = np.minimum(img, first)  # do the max proj --> should be ok
                if 'av' in mode.lower():
                    first /= float(counter)
                    print('computing average')
                elif 'max' in mode.lower():
                    print('computing max')
                elif 'min' in mode.lower():
                    print('computing min')
            if output is None:
                # preview
                try:
                    plt.imshow(first)
                    plt.show()
                except:
                    print("can't preview")
                    pass
            else:
                # saving file according to user definition
                # output will be different if in TA mode vs another mode --> TODO
                # need recover
                print('saving...', os.path.join(output, output_name)+'.tif') # perfect --> can be used to average files and or folders... --> TODO
                Img(first, dimensions=dimensions).save(os.path.join(output, output_name)+'.tif')
                output_files.append(os.path.join(output, output_name)+'.tif')
        except:
            traceback.print_exc()
            print('Error something went wrong, skipping projection for file', file, 'and related...')
    return output_files

# TODO warn the user that this is work in progress and they use it at their own risk...
# that rougly seems ok but need deep check
def post_process(input, post_process_algorithm=None, **kwargs):

    print('post_process_algorithm', post_process_algorithm)

    for inp in input:
        img = Img(inp)
        #
        # run_post_process
        # TODO --> do that
        print(input, kwargs)
        # method = post_process_algorithm



        if isinstance(post_process_algorithm, str):

            # print('chosen', post_process_algorithm)

            if 'imply' in post_process_algorithm:
                # print('simply')
                img = simpleFilter(img, **kwargs)
                # plt.imshow(img)
                # plt.show()

                Img(img).save(inp)
                continue

            if 'ld' in post_process_algorithm:
                method = EPySegPostProcess
            else:  # MEGA TODO add parameters with partial according to input
                method = RefineMaskUsingSeeds

        img = method().process(input=img, mode=post_process_algorithm, **kwargs,
                                progress_callback=None)

        # TODO see how to handle dimensions in a smart way...

        # plt.imshow(img)
        # plt.show()

        #TODO save the image --> just overwrite the original... then done!!!
        Img(img).save(inp)


        # pass


# almost done, then just connect the GUI and push updates
# TODO maybe also return the list of saved files --> by concatenating output
if __name__ == "__main__":

    # also allow post process of the image maybe put non by default ????
    app = QApplication(sys.argv)
    parameters, ok = PostProcessGUI.getDataAndParameters(parent_window=None, _is_dialog=True)
    # print(parameters, ok)
    # enable_post_process = PostProcessGUI(parent_window=None)

    # en fait jusyte no post process in that case
    # if not ok:
    #     sys.exit(0)


    # '/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed'

    input = []

    # for i in range(30):
    #     if i in [22, 27, 28]:
    #         continue
    #     path1 = '/D/Sample_images/sample_images_denoise_manue/test_legs_100807/predict/predict_model_nb_' + str(i)
    #     input1 = os.listdir(path1)
    #     input1 = [os.path.join(path1, f) for f in input1]
    #     input.append(input1)
    #     # path2 = '/D/Sample_images/sample_images_denoise_manue/test_legs_100807/predict/predict_model_nb_1'
    #     # input2 = os.listdir(path2)
    #     # input2 = [os.path.join(path2, f) for f in input2]

    path1 = '/D/Sample_images/sample_raw_epyseg_output'
    input1 = os.listdir(path1)
    input1 = [os.path.join(path1, f) for f in input1]
    input.append(input1)

    # seems to work also for very complex image structures
    # input = [['/D/Sample_images/sample_images_denoise_manue/out4_2ch.tif'],['/D/Sample_images/sample_images_denoise_manue/out4_2ch.tif']]


    # ensemble(input)
    # ensemble(input, mode='min')
    processed_files = ensemble(input, mode='avg',output='/D/Sample_images/sample_images_denoise_manue/test_legs_100807/predict/test_avg', TA_mode=True) # in fact can overwrite the output --> quite a good idea I guess!!!
    # ensemble(input, mode='min') # nb min a des fois des artefacts de box mais n'est pas mal
    # ensemble(input, mode='median')

    if ok:
        # do the post process for all of the files
        print('Post processing') # in that case I also need an output folder for the post process... --> TODO
        post_process(processed_files, **parameters)
        # need specify an output folder...

    # TODO test if that works with several channels
