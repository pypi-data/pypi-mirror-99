# tricks average over various scalings
# or average heightmap or median filter height map


# test of plant outer surface projection

# detect top of the cell then project n images below that --> probably not so hard in fact but maybe need project above or below
# get max


# finaliser ce code
from scipy.ndimage import median_filter
from skimage.transform import resize
from epyseg.img import Img
import numpy as np
from matplotlib import pyplot as plt
import glob
from natsort import natsorted
import os
from scipy import ndimage
from scipy.ndimage import median_filter

# img = Img('/home/aigouy/Dropbox/7DAG_PM_tdT_leaf4_2_D4.tif')
# img = Img('/home/aigouy/Dropbox/seg_vertebrate_full_resolution_actin/C2-Ventral actinR.tif')
# img = Img('D:/Dropbox/seg_vertebrate_full_resolution_actin/C2-Ventral actinR.tif')
# img = Img('D:/Dropbox/seg_vertebrate_full_resolution_actin/C2-None E9 WT pPKCv Ecqdcy5 actinR 2.tif')
# img = Img('D:/Dropbox/seg_vertebrate_full_resolution_actin/C2-None E9 WT ppMLCv actinR 1.tif')
# img = Img('D:/Dropbox/seg_vertebrate_full_resolution_actin/C2-None E9 WT vangl2V atubcy5 actinR 1.tif') # best 2

# take brightest signal

DEBUG = False

folderpath = '/home/aigouy/Dropbox/seg_vertebrate_full_resolution_actin/'

# loop over list and project
list_of_files = glob.glob(folderpath + "*.png") + glob.glob(folderpath + "*.jpg") + glob.glob(
    folderpath + "*.jpeg") + glob.glob(
    folderpath + "*.tif") + glob.glob(folderpath + "*.tiff")+ glob.glob(folderpath + "*.lsm")+ glob.glob(folderpath + "*.czi") + glob.glob(folderpath + "*.lif")
list_of_files = natsorted(list_of_files)

for file in list_of_files:
    filename0_without_path = os.path.basename(file)
    filename0_without_ext = os.path.splitext(filename0_without_path)[0]
    img = Img(file)  # best

    # print(img.shape)

    mask = np.zeros_like(img[0])
    projection = np.zeros_like(img[0])
    # height_map = np.zeros_like(img[0])
    # final_projection = np.zeros_like(img[0])
    # final_projection2 = np.zeros_like(img[0])
    # min_of_all_stacks = np.zeros_like(img[0])

    # need fill holdes in mask to avoid filling inside

    # threshold_to_be_considered_as_signal = 32  # check if ok
    # maybe need remove salt n peper noise --> median filter on binarised image --> to avoid snp noise in proj

    # print(mask.shape)

    # z_sampling = 1

    # need split the image into chunks in z and then need browse the Z
    # not so hard then store values and create projection

    # take brightest Z then do projection

    # scale or scale down the image

    TILE_SIZE = 16

    mini_height_map = np.empty((img.shape[-2] // TILE_SIZE, img.shape[-1] // TILE_SIZE))
    # print(img.shape[-2]//32, img.shape[-2]/32)

    # TILE_SIZE = 16
    # height_map = np.zeros_like(img[0])
    # projection = np.zeros_like(img[0])
    crops, splits = Img.get_2D_tiles_with_overlap(img, width=TILE_SIZE, height=TILE_SIZE, dimension_h=1, dimension_w=2)

    # print(height_map.shape)
    # crops_height_map, splits_height_map = Img.get_2D_tiles_with_overlap(height_map, width=TILE_SIZE, height=TILE_SIZE,
    #                                                                     dimension_h=0, dimension_w=1)

    # img = img[...,392:392+128,377:377+128]
    # split image into chunks and compute the height map then reconstruct image and do projection

    # plt.imshow(img[0])
    # plt.show()
    # take max along the Z and maybe above or below

    # store max value in an image

    # print(len(splits), len(splits[0]))
    # print(len(splits_height_map), len(splits_height_map[0]))

    # need create gradient or reduces size compared to the other --> think how
    # create files by tile size then scale it with linear interp to reach full size

    for k, r in enumerate(splits):
        for l, chk in enumerate(r):
            mx = -1
            mx_pos = 0

            # print(chk)

            # for tile in splits:
            # first = z_slices.pop(0)

            # plt.imshow(img[i], cmap='gray')
            # plt.show()
            for i, slice in enumerate(chk):
                # print(slice.shape)
                cur = slice.mean()
                cur = slice[slice >= cur].mean() + 30 / 100 * cur

                # print(i, cur)
                mx = max(mx, cur)
                if mx == cur:
                    mx_pos = i
            # compute mean and take max along the Z axis
            # first = img[i]
            # j=i+1
            # for j in range(i + 1, i + z_sampling, 1):
            #     if j < img.shape[0]:
            # proj = np.maximum(img[j], first)
            # first = proj

            # force close bottom most cells hack
            # if j >= img.shape[0] - 3:
            #     threshold_to_be_considered_as_signal /= 4
            #
            # for h in range(first.shape[0]):
            #     for w in range(first.shape[1]):
            # first = median_filter(first, size=2)
            # first[first < threshold_to_be_considered_as_signal] = 0
            # first[mask == True] = 0
            #
            # # plt.imshow(first, cmap='gray')
            # # plt.show()
            # # thresholded[mask==True]=
            # height_map[first != 0] = i  #
            # projection[first != 0] = first[first != 0]
            # mask[first > threshold_to_be_considered_as_signal] = True
            # despeckle
            # mask = median_filter(mask, size=2)

            # need fill holdes in mask to avoid filling inside

            # mask = ndimage.binary_fill_holes(mask)

            # splits_height_map[k][l].fill(mx_pos)
            mini_height_map[l][k] = mx_pos
            # print('final', mx, mx_pos)


    mini_height_map = median_filter(mini_height_map,3)
    mini_height_map = np.round(resize(mini_height_map, (img.shape[-2], img.shape[-1])))

    # crops_height_map, splits_height_map = Img.get_2D_tiles_with_overlap(mini_height_map, width=TILE_SIZE,
    #                                                                     height=TILE_SIZE,
    #                                                                     dimension_h=0, dimension_w=1)

    if DEBUG:
        # en fait meme pas besoin de reassembler les tiles --> du coup tellement plus facile à faire
        # plt.imshow(height_map)
        # plt.show()

        plt.imshow(mini_height_map)
        plt.show()

    # now do max proj from height map
    # basic or could also do better

    # print('shp', mini_height_map.shape)
    nb_z_above = 1 # 2
    nb_z_deeper = 2 # 4


    for h in range(mini_height_map.shape[-2]):
        for w in range(mini_height_map.shape[-1]):
            # get pixel and project it
            zpos = int(mini_height_map[h, w])
            # counter = 0

            # projection[h, w]=mini_height_map[h,w]
            for z in range(zpos - nb_z_above, zpos + (nb_z_deeper+1), 1):
                if z < 0 or z >= img.shape[0]:
                    continue

                # print(z,h,w)
                projection[h, w] = max(img[z, h, w], projection[h, w])  # need take max of that

                # print(z, h, w, '-', projection[h, w], '-->', img[z, h, w])

                # counter+=1
            # if counter!=0:
            #     projection[h][w]=projection[h][w]/counter

    # old way of doing
    # for k, r in enumerate(splits):
    #     for l, chk in enumerate(r):
    #         mx = -1
    #         mx_pos = 0
    #
    #         pos = splits_height_map[k][l][0, 0] # need read every pixel in fact
    #         # for each pixel take appropriate stuff
    #
    #         # need read pos from numpy array
    #         for i, slice in enumerate(chk):
    #             if i >= pos + 3 or i <= pos - 2: #one above one below
    #             # if i != pos: # just slice at height map
    #                 # print(slice.shape)
    #                 slice.fill(0)

    # first = z_slices.pop(0)
    #
    # for slice in img:
    #     plt.imshow(slice)
    #     plt.show()

    # projection = img[0]
    # for slice in img:
    #     projection = np.maximum(slice, projection)
    #
    # if DEBUG:
    #     plt.imshow(projection, cmap='gray')
    #     plt.show()

    # I could maybe use that to color code depth of pixels so that I can get them
    #
    #
    # plt.imshow(projection, cmap='gray')
    # plt.show()
    #
    Img(projection, dimensions='hw').save(
        os.path.join(folderpath, 'optimized_projection', filename0_without_ext + '.tif'))
    if DEBUG:
        Img(mini_height_map, dimensions='hw').save(
            os.path.join(folderpath, 'optimized_projection', filename0_without_ext + '_height_map.tif'))
    #
    # projection = median_filter(projection, size=2)
    # plt.imshow(projection, cmap='gray')
    # plt.show()
    #
    # Img(projection, dimensions='hw').save('/home/aigouy/Dropbox/plant_first_encounter_seg_median_filtered.tif')
    #
    # plt.imshow(mask)  # , cmap='gray'
    # plt.show()
    #
    # Img(mask, dimensions='hw').save('/home/aigouy/Dropbox/plant_signal_mask.tif')
    #
    # plt.imshow(height_map)  # , cmap='gray'
    # plt.show()
    # Img(height_map, dimensions='hw').save('/home/aigouy/Dropbox/plant_height_map.tif')
    #
    # # height_map = median_filter(height_map, size=2)
    # # Img(height_map, dimensions='hw').save('/home/aigouy/Dropbox/plant_height_map_median_filtered.tif')
    # # plt.imshow(height_map)  # , cmap='gray'
    # # plt.show()
    #
    # s = ndimage.generate_binary_structure(2, 1)
    # height_map = ndimage.grey_dilation(height_map, footprint=s)
    # height_map = ndimage.grey_dilation(height_map, footprint=s)
    #
    # # fill final projection with random noise between 8000 and 25000
    # noise = np.random.rand(final_projection.shape[0],final_projection.shape[1])
    # max = 24000
    # min = 8000
    # noise=(noise*(max-min))+min
    #
    # plt.imshow(noise, cmap='gray')
    # plt.show()
    # # maybe get the max proj value for that instead
    # for i in range(0, img.shape[0], z_sampling):
    #     first = img[i]
    #     for j in range(i + 1, i + z_sampling, 1):
    #         if j < img.shape[0]:
    #             proj = np.maximum(img[j], first)
    #             first = proj
    #     # in fact need do max of appropriate size
    #     final_projection[height_map == i] = first[height_map == i]
    #
    #
    # final_projection = np.maximum(noise, final_projection)
    #
    # # TODO nb a gaussian blur 0.5 makes it look more natural --> maybe do that
    #
    # # looks like the best
    #     # fait pas tres naturel en fait
    #
    #
    # print('blip')
    # Img(final_projection, dimensions='hw').save('/home/aigouy/Dropbox/plant_final_projection.tif')
    # plt.imshow(final_projection, cmap='gray')
    # plt.show()
    #
    #
    # if False:
    #
    #     final_mask = np.zeros_like(height_map)
    #     final_mask[height_map > 0] = 255
    #     plt.imshow(final_mask, cmap='gray')  # new mask
    #     plt.show()
    #
    #     # ci dessous fait vraiment pas naturel
    #     #
    #     # min_of_all_stacks.fill(64000)
    #     # for i in range(0, img.shape[0], 1):
    #     #     # min of all stacks = noise
    #     #     first = img[i]
    #     #     first[first==0]=64000
    #     #     min_of_all_stacks = np.minimum(first, min_of_all_stacks)
    #
    #     # take max of all stack for that
    #     for i in range(0, img.shape[0], 1):
    #         # first = img[i]
    #         first = img[i]
    #         first[final_mask==0]=0
    #         final_projection2 = np.maximum(first, final_projection2)
    #
    #
    #     # add noise to all
    #     # final_projection2[final_mask==0]=min_of_all_stacks[final_mask==0]
    #     final_projection2 = np.maximum(noise, final_projection2)
    #
    #     plt.imshow(final_projection2, cmap='gray')# new mask
    #     plt.show()
    #
    #
    #     # just create a mask for this and take max of all stack at this max value else take min if not in mask
    #
    #
    #
    #     # je pourrais utiliser le height map pr faire ça --> pr faire une proj --> tenter de coder ça et de voir le résultat
    #     #
    #
    #
    #     # now use this info to do the max proj
    #
    #
    #     # plt.imshow(first)
    #     # plt.show()
    #     # do a max proj of n images
    #     # pass
    #
    #     # then need use that to do the projection...

    # final_mask = Img.reassemble_tiles(splits, crops)
