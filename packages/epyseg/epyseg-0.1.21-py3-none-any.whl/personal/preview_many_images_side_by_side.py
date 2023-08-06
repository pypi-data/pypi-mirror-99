# maybe I should get inspired from that for my own figure creation tool: https://matplotlib.org/3.1.1/tutorials/intermediate/gridspec.html
# almost there now...

import numpy as np
import matplotlib.pyplot as plt
import os

import numpy as np
import matplotlib.pyplot as plt
import math
from docutils.nodes import figure
from natsort import natsorted

from epyseg.img import Img

# even better packing
from numpy.random import rand
import matplotlib.pyplot as plt

# test_data = [[rand(10,10), rand(10,10)],[rand(5,10), rand(5,10)],[rand(2,10), rand(2,10)]]
# cmaps = [['viridis', 'binary'], ['plasma', 'coolwarm'], ['Greens', 'copper']]
#
# heights = [a[0].shape[0] for a in test_data]
# widths = [a.shape[1] for a in test_data[0]]
#
# fig_width = 8.  # inches
# fig_height = fig_width * sum(heights) / sum(widths)
#
# f, axarr = plt.subplots(3,2, figsize=(fig_width, fig_height),
#         gridspec_kw={'height_ratios':heights})
#
# for i in range(3):
#     for j in range(2):
#         axarr[i, j].imshow(test_data[i][j], cmap=cmaps[i][j])
#         axarr[i, j].axis('off')
# plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
# plt.show()

# root_path = '/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/'
# root_path = '/D/Sample_images/sample_images_denoise_manue/test_different_models_210108/predict/'
# root_path = '/D/Sample_images/sample_images_denoise_manue/test_different_models_201104/predict/'
# root_path = '/D/Sample_images/sample_images_denoise_manue/test_segs_200722/predict/'
# root_path = '/D/Sample_images/sample_images_denoise_manue/test_legs_100807/predict/'
# root_path = '/D/Sample_images/sample_images_denoise_manue/test_210128_dpov1/predict/'
root_path = '/D/Sample_images/sample_images_denoise_manue/fullset_Manue/test_200319/predict/'
folders = os.listdir(root_path)
# folders = ['/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/predict_model_nb_0',
#            '/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/predict_model_nb_1',
#            '/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/predict_model_nb_2',
#            '/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/predict_model_nb_3',
#            '/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/predict_model_nb_4',
#            '/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/predict_model_nb_5',
#            '/D/Sample_images/sample_images_denoise_manue/tests_CARE_stack_foc/predict/predict_model_nb_6',
#            ]



folders = [os.path.join(root_path, folder) for folder in folders]
folders = natsorted(folders)

print(folders)





# not bad also for cropping title
# https://stackoverflow.com/questions/10351565/how-do-i-fit-long-title
#

# pas mal --> je pourrais vraiment optimiser ça pr moi... les images sont des dict avec un nom unique et une image mais pourrait aussi implementer pr juste un array d'images...

# pas trop mal mais fianliser ce code et trouver une solution si les images ont un nb de canaux differents ou s'ils contiennent des Z et de t --> peute etre splitte dehors cependant...

# TODO clean and add to the image code cause can be useful --> say it will only accept images with same nb of channels and no t and no Z --> need pre processing
def preview_as_panel(images, rows=1, cols=1, max_nb_cols=None, cmap=None, full_screen=False, hide_white_space=True, title=None, sharex=True, sharey=True):
    if rows*cols<len(images):
        # cols = len(images)

        # alternatively try to make a square
        # cols = len(images)
        if max_nb_cols is None:
            cols = math.sqrt(len(images)) # in fact square is not smart as screen is 16/9 --> more width --> more cols than height
            cols*=16/9 # force to screen AR
            cols=math.ceil(cols)

            # cols+=1

        else:
            cols = max_nb_cols

        rows = int(math.ceil(len(images)/cols))
        if rows<1:
            rows=1
    # heights= []
    # for iii in range(rows):
    #     heights.append(1)

    # fig = pylab.gcf()
    # fig.canvas.set_window_title('Test')

    # print(rows,cols)
    figure, ax = plt.subplots(nrows=rows, ncols=cols,sharex=sharex, sharey=sharey) # sharex=True, sharey=True --> allows same zoom for all

    figure.subplots_adjust(0, 0, 1, 1) # better for size


    # plt.margins(0.1)

    # plt.xlim(0., 1.)
    # plt.ylim(0., 1.)

    # CAN BE USED TO ZOOM ON AN IMAGE!!!!! --> faut en fait des pixels
    # plt.xlim(500, 1000) # cree un zoom mais pas optimal
    # plt.ylim(500, 1000)
    #
    # plt.xlim(0.25, 0.5) # marche pas...
    # plt.ylim(0.25, 0.5)

    # plt.axis('off')
    # ax.margins(0.05)
    # figure.margins(0.05)
    # ax.set_xlim([-0.38, 7.6])
    # ax.set_ylim([-0.71, 3.2])
    # ax.set_aspect(0.85)

    axes = ax.ravel() #--> maybe simpler
    for idx, _legend in enumerate(images):
        # ax.ravel()[idx].get_xaxis().set_visible(False)  # this removes the ticks and numbers for x axis
        # ax.ravel()[idx].get_yaxis().set_visible(False)

        #
        axes[idx].axis('off')
        axes[idx].imshow(images[_legend], cmap=cmap)
        # ax.ravel()[idx].set_title(os.path.basename(os.path.dirname(title))+'\n'+os.path.basename(title), y=-15)
        # ax.ravel()[idx].text(0, -15, os.path.basename(os.path.dirname(title))+'\n'+os.path.basename(title))
        # ax.ravel()[idx].legend([os.path.basename(os.path.dirname(title))+'\n'+os.path.basename(title)],("My explanatory text", "0-10", "10-100"),loc='upper left')
        # try:
        #     # if name is not a path --> just print classical title
        #     legend=axes[idx].legend(title=os.path.basename(os.path.dirname(title))+'\n'+os.path.basename(title),loc='upper left')#, bbox_to_anchor=(1., 1.) , frameon=False
        # except:
        legend = axes[idx].legend(title=_legend, loc='upper left')  # , bbox_to_anchor=(1., 1.) , frameon=False
        # legend.get_frame().set_facecolor('C0') # set frame color requires , frameon=True
        # for text in legend.get_texts():
        #     text.set_color("red")
        # l=ax.ravel()[idx].legend()
        # for text in ax.ravel()[idx].get_texts():
        #     text.set_color("red")
        # legend((line1, line2, line3), ('label1', 'label2', 'label3'))
        # ax.ravel()[idx].set_title(os.path.dirname(title))
        axes[idx].set_axis_off()
    try:
        # removing all axes when no images are associated to it
        for iii in range(idx, len(axes)):
            axes[iii].set_axis_off()
    except:
        pass
    # figure.subplots_adjust()
    # figure.tight_layout()
    plt.tight_layout()
    # plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    if full_screen:
        # show full screen
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()

    # plt.axis([256, 256, 256+128, 256+128])
    if hide_white_space:
        # super tight packing of images --> no space between them...
        plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    # plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)

    if title is not None:
        plt.gcf().canvas.set_window_title(title)
        # print(title)

    plt.show()


# could also hack this to plot all the images in a folder --> can also be useful...
# put name somewhere else
# get path somewhere else...


# can be used to compare the same file in different folders # do one to see all files in one folder

def compare_same_files_in_different_folder():
    force_channel = 0  # None
    files_in_first_folder = os.listdir(folders[0])

    # list all files in first folder and if present in others then add them
    for file in files_in_first_folder:
        images = {}
        for folder in folders:
            final_file = os.path.join(folder, file)
            if os.path.isfile(final_file):
                try:
                    img = Img(final_file)
                    if force_channel is not None:
                        if img.has_c():
                            img = img[..., force_channel]
                    folder_name = os.path.basename(os.path.dirname(final_file))
                    images[folder_name] = img
                    # print(img.shape)
                    # print('valid', final_file)
                except:
                    print('invalid file', final_file)
        # print(len(images))
        if images:
            preview_as_panel(images, cmap='gray', full_screen=True, title=os.path.basename(final_file)) #cmap=None,
    # list



def show_all_images_in_a_folder(folder, sharex=False, sharey=False):
    force_channel = 0  # None
    files_in_first_folder = os.listdir(folder)
    images = {}

    # TODO if all image have same width and height or dims --> could sharex and y to zoom altogether otherwise not smart at all

    for final_file in files_in_first_folder:
        final_file = os.path.join(folder, final_file)
        try:
            img = Img(final_file)
            if force_channel is not None:
                if img.has_c():
                    img = img[..., force_channel]
            folder_name = os.path.basename(final_file)
            images[folder_name] = img
            # print(img.shape)
            # print('valid', final_file)
        except:
            print('invalid file', final_file)
    if images:
            preview_as_panel(images, cmap='gray', full_screen=True, title=folder, sharex=sharex, sharey=sharey) #cmap=No # or maybe just folder --> as a test



# not bad --> can do cool stuff with that...
show_all_images_in_a_folder(folders[0])
compare_same_files_in_different_folder()





#
# total_images = 4
# images = {'Image'+str(i): np.random.rand(100, 100) for i in range(total_images)}
#
# display_multiple_img(images, 2, 2)

# w=10
# h=10
# fig=plt.figure(figsize=(8, 8))
# columns = 4
# rows = 5
# for i in range(1, columns*rows +1):
#     img = np.random.randint(10, size=(h,w))
#     fig.add_subplot(rows, columns, i)
#     plt.imshow(img)
# plt.show()

