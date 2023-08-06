# test of plant outer surface projection

# detect top of the cell then project n images below that --> probably not so hard in fact but maybe need project above or below
# get max



# finaliser ce code
from scipy.ndimage import median_filter

from epyseg.img import Img
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage

img = Img('/home/aigouy/Dropbox/7DAG_PM_tdT_leaf4_2_D4.tif')
# img = Img('/home/aigouy/Dropbox/seg_vertebrate_full_resolution_actin/C2-Ventral actinR.tif')

print(img.shape)

mask = np.zeros_like(img[0])
projection = np.zeros_like(img[0])
height_map = np.zeros_like(img[0])
final_projection = np.zeros_like(img[0])
final_projection2 = np.zeros_like(img[0])
min_of_all_stacks = np.zeros_like(img[0])

# need fill holdes in mask to avoid filling inside

threshold_to_be_considered_as_signal = 40000  # check if ok
# maybe need remove salt n peper noise --> median filter on binarised image --> to avoid snp noise in proj

print(mask.shape)

z_sampling = 6

for i in range(0, img.shape[0], z_sampling):
    # first = z_slices.pop(0)

    first = img[i]
    j=i+1
    for j in range(i + 1, i + z_sampling, 1):
        if j < img.shape[0]:
            proj = np.maximum(img[j], first)
            first = proj

        # force close bottom most cells hack
    if j >= img.shape[0] - 3:
        threshold_to_be_considered_as_signal /= 4

    # for h in range(first.shape[0]):
    #     for w in range(first.shape[1]):
    # first = median_filter(first, size=2)
    first[first < threshold_to_be_considered_as_signal] = 0
    first[mask == True] = 0

    # plt.imshow(first, cmap='gray')
    # plt.show()
    # thresholded[mask==True]=
    height_map[first != 0] = i  #
    projection[first != 0] = first[first != 0]
    mask[first > threshold_to_be_considered_as_signal] = True
    # despeckle
    # mask = median_filter(mask, size=2)

    # need fill holdes in mask to avoid filling inside

    mask = ndimage.binary_fill_holes(mask)

# I could maybe use that to color code depth of pixels so that I can get them


plt.imshow(projection, cmap='gray')
plt.show()

Img(projection, dimensions='hw').save('/home/aigouy/Dropbox/plant_first_encounter_seg.tif')

projection = median_filter(projection, size=2)
plt.imshow(projection, cmap='gray')
plt.show()

Img(projection, dimensions='hw').save('/home/aigouy/Dropbox/plant_first_encounter_seg_median_filtered.tif')

plt.imshow(mask)  # , cmap='gray'
plt.show()

Img(mask, dimensions='hw').save('/home/aigouy/Dropbox/plant_signal_mask.tif')

plt.imshow(height_map)  # , cmap='gray'
plt.show()
Img(height_map, dimensions='hw').save('/home/aigouy/Dropbox/plant_height_map.tif')

# height_map = median_filter(height_map, size=2)
# Img(height_map, dimensions='hw').save('/home/aigouy/Dropbox/plant_height_map_median_filtered.tif')
# plt.imshow(height_map)  # , cmap='gray'
# plt.show()

s = ndimage.generate_binary_structure(2, 1)
height_map = ndimage.grey_dilation(height_map, footprint=s)
height_map = ndimage.grey_dilation(height_map, footprint=s)

# fill final projection with random noise between 8000 and 25000
noise = np.random.rand(final_projection.shape[0],final_projection.shape[1])
max = 24000
min = 8000
noise=(noise*(max-min))+min

plt.imshow(noise, cmap='gray')
plt.show()
# maybe get the max proj value for that instead
for i in range(0, img.shape[0], z_sampling):
    first = img[i]
    for j in range(i + 1, i + z_sampling, 1):
        if j < img.shape[0]:
            proj = np.maximum(img[j], first)
            first = proj
    # in fact need do max of appropriate size
    final_projection[height_map == i] = first[height_map == i]


final_projection = np.maximum(noise, final_projection)

# TODO nb a gaussian blur 0.5 makes it look more natural --> maybe do that

# looks like the best
    # fait pas tres naturel en fait


print('blip')
Img(final_projection, dimensions='hw').save('/home/aigouy/Dropbox/plant_final_projection.tif')
plt.imshow(final_projection, cmap='gray')
plt.show()


if False:

    final_mask = np.zeros_like(height_map)
    final_mask[height_map > 0] = 255
    plt.imshow(final_mask, cmap='gray')  # new mask
    plt.show()

    # ci dessous fait vraiment pas naturel
    #
    # min_of_all_stacks.fill(64000)
    # for i in range(0, img.shape[0], 1):
    #     # min of all stacks = noise
    #     first = img[i]
    #     first[first==0]=64000
    #     min_of_all_stacks = np.minimum(first, min_of_all_stacks)

    # take max of all stack for that
    for i in range(0, img.shape[0], 1):
        # first = img[i]
        first = img[i]
        first[final_mask==0]=0
        final_projection2 = np.maximum(first, final_projection2)


    # add noise to all
    # final_projection2[final_mask==0]=min_of_all_stacks[final_mask==0]
    final_projection2 = np.maximum(noise, final_projection2)

    plt.imshow(final_projection2, cmap='gray')# new mask
    plt.show()


    # just create a mask for this and take max of all stack at this max value else take min if not in mask



    # je pourrais utiliser le height map pr faire ça --> pr faire une proj --> tenter de coder ça et de voir le résultat
    #


    # now use this info to do the max proj


    # plt.imshow(first)
    # plt.show()
    # do a max proj of n images
    # pass

    # then need use that to do the projection...
