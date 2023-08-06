# le watershed est lent --> could all be done in post process
# can I do a seed blaster as seeds seem always perfect --> put black below
# maybe prevent seeding if only one seed ???? --> does that help
# blaster n'aide pas mais compter les seeds peut supprimer un peu d'overseg... --> le tenter ???


# TODO detecter par multiseed pui utiliser le bazooka habituel pr améliorer l'image --> gain de temps ??? --> à tester
# a tester car bcp plus rapide

# TODO can also do a dekink to remove the small 1px long bonds that stick out from bonds --> but may be slow...

# TODO can I also invert the seed mask to see if it detects it better in one of the channels
# TODO ignore sticking out pixels close to boundary --> how can I detect  that --> watershed followed by a binary dialtion of 1 ???

# check if I can detect free edges even when not there made with skel or wshed since it is largely 1 px wide anyway
# try keep original info of white pixel --> just add a gradient to it --> e.g. add half the value
# or rerun wshed on orig  using the seeds I have --> that will be smaller
# in fact can detect free edgees by six pixels and 2 different ids around --> not that


# faudrait mesurer la distance de la seed à la racine du bond car si trop pres alors forget 
# peut aussi compter le nb de seeds pr savoir si doit resegmenter # try the wshed locally too --> using the nice label tool of scipy --> can probably be done # need enlarge a bit the region to get the bond --> copy the mask but only add the whsed data inside

# plenty of things to test ...
# it's quite good but need control


# suis vraiment pret a essayer
# tester aussi le local wshed
# compter le nb de seeds per stuff and check distance between seeds --> if seeds are too close to one another --> ignore --> at least 5-10 px distance

# try connect seeds to anything 1 px away from them if possible --> see how can do that --> should be done at the very last step

# ça marche je peux detecter les free vertices et donc ne flooder que les cellules associees+

# URGENT TODO really need a blob remover before doing the augmentation --> TODO would make a huge difference for 100708_png06.tif --> I have it somewhere --> copy it in here -->
# can be tried as a post process too


from timeit import default_timer as timer
import traceback
# from skimage.morphology import flood
# skimage.morphology.flood_fill(image, …[, …])
from skimage import morphology
from skimage.util import invert
from skimage.draw import line_aa
from skimage.morphology import skeletonize, watershed
import math
from deprecated_demos.ta.wshed import Wshed
from epyseg.img import Img
from matplotlib import pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from timeit import default_timer as timer
from scipy.ndimage import binary_closing
import os
import numpy as np

# maybe need check that the extra pixels do touch the seeds otherwise skip ???? --> how can I do that

# binary closing is really crap so I really need to implement my own connector for stuff really close enough and if area is also big enough in order not to fill small elongated cells
# TODO add binary closing as first step to connect really close by points # scipy.ndimage.binary_closing https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.binary_closing.html
# nb for Bro43_avproj0000.tif --> the wshed mask does not work --> that is maybe why cellpose does not work

# try cellpose with 120 cell size parameter for the Bro43_avproj0000.png image cause is more in line with real cell size --> pb is that it detects 7.5 px diameter (the diam is shown below the image and for this image it should be 120...)

start = timer()

# get the image invert what needs to be inverted



# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/AVG_070219.lif - Series0020000.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/focused_Series010.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/focused_Series016.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/StackFocused_Endocad-GFP(6-12-13)#19_016.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/StackFocused_Endocad-GFP(6-12-13)#19_400.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/focused_Series239.tif'
path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/T21a920000.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/Series019.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/proj0016.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/StackFocused_Endocad-GFP(6-12-13)#19_400.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/FocStich_RGB005.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/5.tif'
# could also do a watershed using the seeds and see if it rescues stuff from the lost cells because if it does so then I could use that --> could give it a try ??? --> TODO test
#TODO do a local whsed tool and I would do the same and I can in addition add it to TA

# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/12.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/100708_png06.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/Bro43_avproj0000.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/122.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/5.tif'
# path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/Optimized_projection_018.tif'
img_orig = Img(path)

seeds_1 = img_orig[..., img_orig.shape[-1] - 2]
seeds_1[seeds_1 >= 0.5]=255
seeds_1[seeds_1 < 0.5]=0

# plt.imshow(seeds)
# plt.show()

Img(seeds_1, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'wshed_seeds.tif')) # not bad

# TODO --> do a label of the seeds and


lab_seeds = label(seeds_1.astype(np.uint8), connectivity=2, background=0)

# TODO try create a watershed seg based on seeds

# plt.imshow(lab_seeds)
# plt.show()


# need invert channels 3 and 4
# then do average of channel 0-4

# print('before', img_orig[..., 3].max(), img_orig[..., 3].min())

img_orig[..., 3] = invert(img_orig[..., 3])
img_orig[..., 4] = invert(img_orig[..., 4])

# print('after', img_orig[..., 3].max(), img_orig[..., 3].min())

# img_saturated = Img('D:/Dropbox/AVG_FocStich_RGB005-1.png')
# plt.imshow(img_orig)
# plt.show()


# seems to work --> now need to do the projection
for c in range(1, img_orig.shape[-1] - 2):
    # print(c)
    img_orig[..., 0] += img_orig[..., 1]

# print('size avg', img_orig.shape[-1] - 2)

img_orig[..., 0] /= img_orig.shape[-1] - 2
img_orig = img_orig[..., 0]

# plt.imshow(img_orig)
# plt.show()

Img(img_orig, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'avg.tif')) # not bad
# very good idea too --> count the seeds to know if needs further segmenting --> could even rerun the wshed in here

# TODO maybe remove very tiny seeds

test_wshed = watershed(img_orig, markers=lab_seeds, watershed_line=True)
test_wshed[test_wshed != 0] = 1  # remove all seeds
test_wshed[test_wshed == 0] = 255  # set wshed values to 255
test_wshed[test_wshed == 1] = 0  # set all other cell content to 0


Img(test_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'mask_from_seeds.tif')) # not bad

# should I average black and white before adding it to the first



# then do the rest


# import sys
# sys.exit(0)


# peut etre aussi essayer de patcher certains de ces bonds avec une petite distance de contact --> si un pixel tres pres et dans la meme cellule alors peut le connecter --> à tester peut etre
# faut vraiment aussi faire un proximity connector  qui relie des points tres proches d'une meme cellule --> danger boucher les petites cellules --> s'assurer peut etre que la cellule est assez grande
# vraiment à faire ...
# not so easy but think how to do that ????

# also when two seeds are very close could try to connect them

img_saturated = img_orig.copy()
img_saturated[img_saturated >= 0.5] = 255
img_saturated[img_saturated < 0.5] = 0

Img(img_saturated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'handCorrection.tif'))


# selem = morphology.disk(radius=3)
# selem=np.ones((1, 4))
# selem=np.ones((6, 1)) # c'est null
# img_saturated = binary_closing(img_saturated, selem)


# test = morphology.convex_hull_image(img_saturated)

# Img(test, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'convex_hull.tif'))
# Img(img_saturated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'handCorrection_closed.tif'))

# peut etre 0.5 0.4 0.3 0.2 0.1 0.05 0.02

labs = label(invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)

# colors_around = {0}
# colors_around = []
free_edges = []
#
out = np.zeros_like(img_saturated)

list_of_cells_to_dilate = []
#
# detect free edges
# NB skeleton is not as precise as wshed for vertices....
for i in range(1, img_saturated.shape[-1] - 1, 1):
    for j in range(1, img_saturated.shape[-2] - 1, 1):

        # if matches a free edge --> ad it to a list and connect to closest one
        #

        if img_saturated[j][i] != 0:
            count_white = 0
            count_dark = 0

            # colors_around = , , ,  ]

            if img_saturated[j - 1][i] != 0:
                count_white += 1
            else:
                count_dark += 1
            if img_saturated[j][i - 1] != 0:
                count_white += 1
            else:
                count_dark += 1
            if img_saturated[j][i + 1] != 0:
                count_white += 1
            else:
                count_dark += 1
            if img_saturated[j + 1][i] != 0:
                count_white += 1
            else:
                count_dark += 1
            if img_saturated[j - 1][i - 1] != 0:
                count_white += 1
            else:
                count_dark += 1
            if img_saturated[j - 1][i + 1] != 0:
                count_white += 1
            else:
                count_dark += 1
            if img_saturated[j + 1][i - 1] != 0:
                count_white += 1
            else:
                count_dark += 1
            if img_saturated[j + 1][i + 1] != 0:
                count_white += 1
            else:
                count_dark += 1
            if count_dark >= 5:
                colors_around = [labs[j - 1][i], labs[j + 1][i], labs[j][i - 1], labs[j][i + 1], labs[j - 1][i - 1],
                                 labs[j - 1][i + 1], labs[j + 1][i - 1], labs[j + 1][i + 1]]

                # print(colors_around)
                # if 0 in colors_around:
                #     colors_around.remove(0)

                colors_left = set(colors_around)

                # print(colors_left)
                if len(colors_left) == 2:
                    free_edges.append((i, j))
                    out[j][i] = 255
                    for v in colors_left:
                        list_of_cells_to_dilate.append(v)
                # print('isolated_pixel', i, j)
                # free_edges.append((i, j))
                # out[j][i] = 255
            # if count_dark == 5:
            #     img_saturated[j][i] = 255

# if 0 in list_of_cells_to_dilate:
#     list_of_cells_to_dilate.remove(0)
print(len(set(list_of_cells_to_dilate)))  # just dilate those to avoid overseg

# then fix the bonds just for those

Img(out, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'free_edges_test.tif'))

props = regionprops(labs, intensity_image=img_orig)

# faudrait faire ça plusieurs fois ??? ou pas --> check --> probleme risque de creer de la surseg

for run in range(10):
    print('run', run)
    # cytoplasm = label(invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)

    # plt.imshow(cytoplasm)
    # plt.show()
    something_changed = False  # early stop

    for region in props:
        if region.label not in list_of_cells_to_dilate:
            continue

        # if contact is too small then do not try to restore bonds
        if list_of_cells_to_dilate.count(
                region.label) < 2:  # faudrait un check plus malin je pense --> style la longueur du bond depuis le vertex...
            continue
        # if id == 0:
        #     continue
        # print(id)
        # region = props[id - 1]

        # take regions with large enough areas
        # if region.area < min_size:
        # slow faudrait vider les free edges pr gagner du temps... mais rien n'est plus mauvais que le floodfill de scipy... tout de meme...
        # for coordinates in region.coords:
        #     corrected[coordinates[0], coordinates[1]] = 255

        # try splitting these as much as I can
        #

        # if region.label == 10:

        # print(region.label)
        #
        # plt.imshow(region.image)
        # plt.show()
        #
        # plt.imshow(region.intensity_image)
        # plt.show()

        # TODO try reprocess it

        # img_orig[region.coords > 32] = 255
        # img_orig[region.coords < 32] = 0

        # region.intensity_image[region.intensity_image > 16] = 255
        # region.intensity_image[region.intensity_image <= 16] = 0

        #
        # diminuer threshold progressivement --> à faire

        # threshold = 36

        # can probably decrease fast then more slowly... --> give it a try...
        # really need to go to the max because some are really detected only there...
        # 230/255, 220/255, 200/255, 180/255,
        threshold_values = [160 / 255, 140 / 255, 120 / 255, 100 / 255, 80 / 255, 60 / 255, 40 / 255, 30 / 255,
                            20 / 255, 10 / 255, 5 / 255, 2 / 255, 1 / 255]

        try:
            # for threshold in range(230, 1, -1):
            for threshold in threshold_values:
                # print(threshold)

                # plt.imshow(region.image)
                # plt.show()
                # print(region.image.dtype)
                mask = region.image.copy()

                # image = np.zeros_like(region.image.copy(), dtype=np.bool)
                # image = np.array(region.image, copy=True)
                image = region.image.copy()

                # print(image)

                # ça a l'air de marcher

                # probably the key is here
                image[region.intensity_image > threshold] = True
                image[region.intensity_image <= threshold] = False

                # plt.imshow(image)
                # plt.show()

                # mask = region.image

                # TODO reseg image and if changed do something --> keep new things or replace mask in orig --> could be a good idea and quite doable

                # can I use any of the shape parameters to decide whether I want to split cell or not --> for example if cell shape is complex it's probably oversegmentation

                # print(region.image) # ce truc est un mask
                # print(image)

                final = np.zeros_like(image, dtype=np.uint8)
                final = invert(image.astype(np.uint8))
                final[final < 255] = 0

                # print(final.dtype, final.max(), final.min())

                # print('final',final) # false became true --> not what I want
                # ça marche maintenant
                final[mask == False] = 0

                # plt.imshow(final)
                # plt.show()

                # print('final2',final)
                new_seeds = label(final, connectivity=1, background=0)

                # print(new_seeds.dtype)

                # plt.imshow(new_seeds)
                # plt.show()

                # print(new_seeds)
                props2 = regionprops(new_seeds) # , intensity_image=region.intensity_image
                if len(props2) > 1:  # cell was resplitted into smaller
                    # print('new split = ', len(props))
                    for r in props2:
                        if r.area < 20:
                            # cell too small --> ignore
                            # print('cell too small --> ignoring', r.area)
                            raise Exception

                    # print('there are more cells', len(props)) # but need prevent cells outside mask to be reselected again --> need a remask ??? but how

                    # then reinject new seeds in mask

                    # plt.imshow(new_seeds)
                    # plt.show()

                    # plt.imshow(region.intensity_image)
                    # plt.show()

                    # plt.imshow(region.image)
                    # plt.show()

                    # plt.imshow(img_orig)
                    # plt.show()

                    # reinject the image in the original mask

                    # voir comment supprimer des seeds
                    region.image[mask == False] = False
                    region.image[mask == True] = True
                    region.image[new_seeds > 0] = False
                    # region.image[new_seeds == 0] = False
                    # print(region.bbox)
                    # print('changing')
                    something_changed = True
                    for coordinates in region.coords:
                        img_saturated[coordinates[0], coordinates[
                            1]] = 255  # ça a l'air de marcher car garde le truc # ça devrait pas marcher et d'ailleurs ça marche plus dès que je fais une copie
                region.image[mask == False] = False
                region.image[mask == True] = True
        except:
            traceback.print_exc()
            pass

    if not something_changed:
        print('no more changes anymore --> quitting')
        break

Img(img_saturated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'saturated_mask3.tif'))
# not so bad but how can I do that ??? properly --> need check splits are big enough otherwise ignore
# should I do this recursively ???


# maybe increasing a bit the contrast would work
duration = timer() - start
print('duration is sec', duration)  # --> 198secs --> still much faster than cellpose --> can do comparison

# may need a check of the quality of the new bonds to see if that works --> need revive my scoring stuff --> I know the cells that have new bonds --> I can count them
# otherwise make sure there are several free edges in the cell --> and only in such case try to fix things...

# TODO maybe need repeat once

plt.imshow(img_saturated)
plt.show()
