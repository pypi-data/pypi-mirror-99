from scipy import misc, ndimage
from epyseg.deeplearning.deepl import EZDeepLearning
from epyseg.img import Img

def content_aware_projection(deepTA, img, nb_dilat_mask=0):
    # faire la prediction avec le modèle actuel sur chaque image du stack
    #  loop over the Z dimension

    # sliced_image=[]

    full_image_storage = []
    projection_slices = []
    final_table_out = None

    # ça marche mais faut improver les slicer d'images pr obtenir ce que je veux

    # predict on each slice then do stuff I have to do
    # check patches --> big enough then do proj

    for zslice in img:
        # out = self.predict_from_current_model(inp=zslice, force_show=False)
        out = deepTA.predict_from_current_model(inp=zslice, force_show=False)

        # need get the prdiction and resize it to an array that has the desired size

        # print('zoupa', len(projection_slices[0]))
        # print('zoupa', len(projection_slices[0][0]))
        # projection_slices.append(out)

        # slicer le truc et evaluer chaque truc et stocker le max

        # slices = self.get_chunks(out, width=a, height=b)

        # import cv2
        # import numpy as np

        # img = cv2.imread('your_image.jpg')
        # get original image size back to be able to use it as a mask
        # out = cv2.resize(out, dsize=(zslice.shape[1], zslice.shape[0]),
        #                  interpolation=cv2.INTER_NEAREST)  # cv2.INTER_CUBIC
        # import matplotlib.pyplot as plt
        #
        # plt.imshow(out)
        # plt.show()
        # # print(zslice[:,0,0])
        #
        # print(out)

        # numpy.ma.masked_array(data, numpy.logical_not(mask)) --> so cool I love it and it's gonna be a piece of cake now

        # here is an example of getting a mask array
        # x = np.ma.array([1, 2, 3, 4, 5], mask=[0, 0, 1, 0, 1], fill_value=-999)

        # pas mal mais faudrait une ou deux dilatations du mask je pense --> à tester
        # faut faire varier çe en fonction du truc # sinon appliquer ça sur la projection faire la prediction et ne projeter que ce qui est détecte par la projection avec un dilat --> peut etre encore mieux meme --> à tester

        # coule be faster to multiply
        # for i in range(nb_dilat_mask):
        # should I change this with gray dilation
        if nb_dilat_mask > 0:
            out = ndimage.binary_dilation(out, structure=np.ones((3 * nb_dilat_mask, 3 * nb_dilat_mask)))
        # out = ndimage.binary_dilation(out, structure=np.ones((3, 3)))

        filled_mask = np.ma.array(zslice[..., 0], mask=np.logical_not(out), fill_value=0).filled()
        # print(filled_mask[:, 0])
        zslice[..., 0] = filled_mask
        zslice[..., 1] = filled_mask
        zslice[..., 2] = filled_mask

        # import matplotlib.pyplot as plt
        # plt.imshow(zslice)
        # plt.show()

        # zslice.filled()

        # masked_slice = np.ma

        # pas trop mal idealement faurdrait respecter les tailles mais ça devrait aller et faut aussi permettre de faire un truc
        projection_slices.append(zslice)  # not great optimize that

        # store max and store pos
        #
        # max_count = []
        # # max_pos = []
        # # print('O', len(slices))
        # # print('1', len(slices[0]))
        # for r in slices:
        #
        #     values = []
        #     for i in r:
        #         count = 0
        #         for h in range(i.shape[0]):
        #             for w in range(i.shape[1]):
        #                 if i[h, w] != 0:
        #                     count += 1
        #         values.append(count)
        #     max_count.append(values)
        #     # print('slice count', count)
        #
        #     # print('max count', max_count)
        #
        #     # bug in second dimension of this
        # full_image_storage.append(max_count)

    # print('full storage', full_image_storage)
    #
    # print('full', full_image_storage[0] == full_image_storage[1])
    # print('full', full_image_storage[0] == full_image_storage[2])
    # print('full', full_image_storage[0] == full_image_storage[3])
    # print('full', full_image_storage[0][0] == full_image_storage[3][0])

    # all different here --> bug is after
    # print('full', full_image_storage[0] == full_image_storage[4])

    # now flatten it to get max pos

    # flattenedImage = []
    # counter = 0
    # for slice in full_image_storage:
    #     max = 0
    #     max_pos = 0
    #     for r in slice:
    #         for img in r:
    #             if img>=max:
    #                 max = img
    #                 max_pos = counter
    #
    #     counter += 1

    # data = [[None] * 5] * 5
    # data = [[None] * 5 for _ in range(5)]

    # if not final_table_out:
    #     # print('init table once')
    #     final_table_out = [[0] * len(full_image_storage[0][0]) for _ in range(len(full_image_storage[0]))]

    # print(final_table_out)
    # print(len(final_table_out))
    # print(len(final_table_out[0]))
    # print(len(full_image_storage))
    # print(len(full_image_storage[0]))
    # print(len(full_image_storage[0][0]))

    # print('zinbzbbz', final_table_out[0][0][0])

    # print('zinbzbbz', final_table_out)
    # final_table_out[0][0] = 256 # ce truc sette tte la col comme ça
    # # print('zinbzbbz', final_table_out)
    #
    # for row in range(len(full_image_storage[0])):
    #     for i in range(len(full_image_storage[0][0])):
    #         # need loop over Z to get max
    #         intensity_max = 0
    #         max_pos = 0
    #         for z in range(len(full_image_storage)):
    #             # print('z', z)
    #             cur = full_image_storage[z][row][i]
    #             # print('testete', cur, z, row, i, max_pos, intensity_max)
    #
    #             if cur >= intensity_max:
    #                 intensity_max = cur
    #                 max_pos = z
    #                 # if z!=2:
    #                 #     print("here z",z)
    #                 #     print(final_table_out[row][img])
    #
    #                 # print('setting max', cur, max_pos)
    #                 # if z!=2:
    #                 #     print('after', final_table_out[row][img])
    #         final_table_out[row][i] = max_pos
    #         # print('val', intensity_max, max_pos, row, i, final_table_out[row][i])
    # print(final_table_out)
    # print('end of image table', final_table_out)

    # print(final_table_out)

    # ça marche mais maintenant il faut reconstituer l'image

    # print('table', final_table_out[0] == final_table_out[1]) # all tables are same
    # print('table', final_table_out[0] == final_table_out[2])
    # print('table', final_table_out[0] == final_table_out[3])
    # print('table', final_table_out[0] == final_table_out[4])

    # return final_table_out
    return do_max_proj(projection_slices)
    # need slice the stuff and store the max

    # en fait faudrait slicer le truc et faire la projection en ne gardant que le plus en focus
    # count = 0
    # for h in range(out.shape[0]):
    #     for w in range(out.shape[1]):
    #         if out[h, w] != 0:
    #             count += 1
    # print('count', count)

    # pass


import numpy as np

def do_max_proj( z_slices):
    # nb_z_frames = len(sliced_image)  #

    first = z_slices.pop(0)
    for slice in z_slices:
        projection = np.maximum(slice, first)
        first = projection

    # # z = mapper[row][i]
    # # need loop over Z to get max
    # # intensity_max = 0
    # # max_pos = 0
    # # for z in range(len(mapper)):
    # # print('z', z, row, i)
    #
    # # if proj_n_slices_above != 0 or proj_n_slices_above !=0 : #NB could also have used a tuple for that
    # # create max proj from below and above
    # # begin = z
    # # end = z
    # # if proj_n_slices_above != 0:
    # #     begin = z - abs(proj_n_slices_above)
    # #     if begin < 0:
    # #         begin = 0
    # # if proj_n_slices_below != 0:
    # #     end = z + abs(proj_n_slices_below)
    # #     if end >= nb_z_frames:
    # #         end = nb_z_frames - 1
    # # do proj between begin and end
    #
    # # else:
    # # if begin == end:
    # #     projection[row][i] = sliced_image[begin][row][i]  # = mapper[z][row][i]
    # # else:
    #     # do max proj and add max proj data here
    #     # recover all the images and do max proj for all of them
    #     images_to_project = []
    #     print('begin', begin, 'end', end)
    #     for depth in range(begin, end + 1, 1):
    #         images_to_project.append(sliced_image[depth][row][i])
    #     # now that we have all the data we do the max proj
    #     # projection = np.maximum(projection, z)
    #     print('projecting', len(images_to_project), 'images')
    #     first = images_to_project.pop(0)
    #     for img in images_to_project:
    #         projection[row][i] = np.maximum(first, img)
    #         first = projection[row][i]
    # import matplotlib.pyplot as plt
    #
    # plt.imshow(sliced_image[z][row][i])
    # plt.show()

    #        print(projection)

    # final = self.reassemble_chunks(projection) # bug here

    # final = self.reassemble_chunks(projection)  # bug here
    # print('final shape of reconstituted ', final.shape)

    return projection



deepTA = EZDeepLearning()
deepTA.load_or_build(model='/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/Linknet-seresnext101-smloss-256x256/Linknet-seresnext101-smloss-256x256-ep0099-l0.158729.h5')

default_input_width = 256  # 576  # 128 # 64
default_input_height = 256  # 576 # 128 # 64


input_normalization = {'method': 'Rescaling (min-max normalization)', 'range': [0, 1],
                           'individual_channels': True}

predict_generator = deepTA.get_predict_generator(
    inputs=['/home/aigouy/Téléchargements/7DAG_PM_tdT_leaf4_2_D4.tif'], input_shape=deepTA.get_inputs_shape(),
    output_shape=deepTA.get_outputs_shape(), default_input_tile_width=default_input_width,
    default_input_tile_height=default_input_height,
    tile_width_overlap=32,
    tile_height_overlap=32, input_normalization=input_normalization, clip_by_frequency=0.05)


# predict in 2D for each image then done

# predict on all the images of the stack
import os
predict_output_folder = os.path.join('/home/aigouy/Téléchargements/predict')  # 'TA_mode'
deepTA.predict(predict_generator, deepTA.get_outputs_shape(), predict_output_folder=predict_output_folder,
               batch_size=1)


# image_to_project = Img('/home/aigouy/Téléchargements/7DAG_PM_tdT_leaf4_2_D4.tif')
# regenerate image ???

# then load the image

# result = content_aware_projection(deepTA, image_to_project)

# print(result.shape)

