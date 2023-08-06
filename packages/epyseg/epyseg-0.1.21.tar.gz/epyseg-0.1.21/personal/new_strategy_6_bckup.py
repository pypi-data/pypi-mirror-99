# could offer an option of filtering cells by area --> easy in post process
# how can I do that ???

# TODO convertir ça en classe avec des parametres et le rajouter à la fin peut être fait en post process et mettre des tests


# il y a pas mal de cas où il est mieux de prendre directement le mask mais pas tt le temps --> faudrait proposer ça en option apres --> faire un postprocess qui cree des masks
# qd image contient bcp de bruit mieux vaut ne rien changer
# pr papier ne garder que les autres

# the simpler the model the better ???

# I'm sure that some models would perform better

# TODO faire un truc modulaire  et mettre un systeme de formule qui dit comment sauver les masks etc et faire les calculs
# faire aussi un choix entre dilation et watershed --> TODO
# enuite faire un selecteur de modele en fonction de la surseg de de la sous seg --> pas si facile --> y reflechir

# put a warning for some augs
# add some of these to the HQ mode


# would there be better combinations than just 0+1+2 ??? --> faudrait faire des tests --> souvent 2 et toujours 3 contient vachement de bruit...

# faire un rewatershed du mask et comparer à l'original et voir ce que ça donne

# given speedup I largely prefer this one to the other... but sometimes may perform less well than other
# 57 secs pour Optimized_projection_018 VS 1533 secs pr new_strategy_5 --> forget...

# ça ça va le faire

# can I compute a difference between wshed and original to keep lost cells that need human corrections again --> would be great and very visual and would not affect much my iou while greatly helping the people

# super faster --> that is really what I needed but does it reduce quality ???

# c'est mieux et plus rapide mais faut faire plein de comparaisons pr etre sur
# dans certains cas il vaut mieux choisir le mask directos
# la seg est vraiment top...

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
from scipy import ndimage
from scipy.signal import convolve2d
from skimage import morphology, img_as_uint, img_as_ubyte
from skimage.feature import peak_local_max, corner_harris, corner_peaks
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

# TODO ask if in TA mode or if should be saved in another folder

# add parameters

# maybe need check that the extra pixels do touch the seeds otherwise skip ???? --> how can I do that

# binary closing is really crap so I really need to implement my own connector for stuff really close enough and if area is also big enough in order not to fill small elongated cells
# TODO add binary closing as first step to connect really close by points # scipy.ndimage.binary_closing https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.binary_closing.html
# nb for Bro43_avproj0000.tif --> the wshed mask does not work --> that is maybe why cellpose does not work

# try cellpose with 120 cell size parameter for the Bro43_avproj0000.png image cause is more in line with real cell size --> pb is that it detects 7.5 px diameter (the diam is shown below the image and for this image it should be 120...)

TA_mode = True
extra_filter_by_size = 12
# extra_filter_by_size = 'auto'
factor_below_average_for_extra_filter_by_size=6
# if TA mode save as expected

start = timer()

# get the image invert what needs to be inverted


# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/'
root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_shells/'
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_light_divided_by_2/'
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_paper/'

# path = root_path + 'AVG_070219.lif - Series0020000.tif'
# path = root_path + 'focused_Series239.tif'
# path = root_path + 'focused_Series010.tif'
# path = root_path + 'focused_Series016.tif'
# path = root_path + 'StackFocused_Endocad-GFP(6-12-13)#19_016.tif'
# path = root_path + 'StackFocused_Endocad-GFP(6-12-13)#19_400.tif'
# path = root_path + 'T21a920000.tif'
# path = root_path + 'T21a920069.tif'
# path = root_path + 'Series019.tif'
# path = root_path + 'proj0016.tif'
# path = root_path + 'FocStich_RGB005.tif'
# path = root_path + '5.tif'
# could also do a watershed using the seeds and see if it rescues stuff from the lost cells because if it does so then I could use that --> could give it a try ??? --> TODO test
# TODO do a local whsed tool and I would do the same and I can in addition add it to TA

# path = root_path + '12.tif'
# path = root_path + '100708_png06.tif'
path = root_path + '122.tif'
# path = root_path + 'Optimized_projection_018.tif'
# path = root_path + 'Bro43_avproj0000.tif'
# path = root_path + 'Bro43_avproj0001.tif'
# path = root_path + '100708_png06.tif'
# path = root_path + '5.tif'
# path = root_path + 'disc_0002_DCAD.tif'
img_orig = Img(path)

img_has_seeds = True
if img_orig.has_c():
    img_seg = img_orig[..., 0].copy()

    seeds_1 = img_orig[..., img_orig.shape[-1] - 2]
    seeds_1[seeds_1 >= 0.5] = 255
    seeds_1[seeds_1 < 0.5] = 0

    # for debug
    # s = ndimage.generate_binary_structure(2, 1)
    # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
    # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
    # Img(seeds_1, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'wshed_seeds.tif'))  # not bad




    lab_seeds = label(seeds_1.astype(np.uint8), connectivity=2, background=0)
    #
    # for region in regionprops(lab_seeds):
    #     if region.area<10:
    #         for coordinates in region.coords:
    #             lab_seeds[coordinates[0], coordinates[1]] = 0
    #
    # Img(seeds_1, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'wshed_seeds_deblobed.tif'))  # not bad
    #
    # plt.imshow(lab_seeds)
    # plt.show()

    # should I deblob seeds too ???

    img_orig[..., 3] = invert(img_orig[..., 3])
    img_orig[..., 4] = invert(img_orig[..., 4])

    # seems to work --> now need to do the projection
    for c in range(1, img_orig.shape[-1] - 2):
        img_orig[..., 0] += img_orig[..., 1]

    img_orig[..., 0] /= img_orig.shape[-1] - 2
    img_orig = img_orig[..., 0]

    # test_wshed = watershed(img_orig, markers=lab_seeds, watershed_line=True)
    # test_wshed[test_wshed != 0] = 1  # remove all seeds
    # test_wshed[test_wshed == 0] = 255  # set wshed values to 255
    # test_wshed[test_wshed == 1] = 0  # set all other cell content to 0
    # duration = timer() - start
    # print('duration wshed in secs', duration)
    #
    # Img(test_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'mask_from_seeds.tif'))  # not bad
else:
    img_has_seeds = False

# for debug
# Img(img_orig, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'avg.tif'))  # not bad

img_saturated = img_orig.copy()
if img_has_seeds:
    img_saturated[img_saturated >= 0.5] = 255
    img_saturated[img_saturated < 0.5] = 0
else:
    img_saturated[img_saturated >= 0.3] = 255
    img_saturated[img_saturated < 0.3] = 0

Img(img_saturated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'handCorrection.tif'))

deblob = True
if deblob:
    image_thresh = label(img_saturated, connectivity=2, background=0)

    # plt.imshow(image_thresh)
    # plt.show()

    # deblob
    min_size = 100
    for region in regionprops(image_thresh):
        # take regions with large enough areas
        if region.area < min_size:
            for coordinates in region.coords:
                image_thresh[coordinates[0], coordinates[1]] = 0

    image_thresh[image_thresh > 0] = 255
    img_saturated = image_thresh
    # Img(img_saturated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'deblobed.tif'))
    del  image_thresh

extra_dilations = True
if extra_dilations:
    # do a dilation of 2 to close bonds
    s = ndimage.generate_binary_structure(2, 1)
    dilated = ndimage.grey_dilation(img_saturated, footprint=s)
    dilated = ndimage.grey_dilation(dilated, footprint=s)
    # Img(dilated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'filled_one_px_holes.tif'))

    labs = label(invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)
    for region in regionprops(labs):
        seeds = []

        # exclude tiny cells form dilation because they may end up completely closed
        if region.area >= 10 and region.area < 200:
            for coordinates in region.coords:
                dilated[coordinates[0], coordinates[1]] = 0
            continue
        else:
            # preserve cells at edges because they have to e naturally smaller because they are cut
            if region.bbox[0] <= 1 or region.bbox[1] <= 1 or region.bbox[2] >= labs.shape[-2] - 2 or region.bbox[3] >= \
                    labs.shape[-1] - 2:
                # edge cell detected --> removing dilation
                for coordinates in region.coords:
                    dilated[coordinates[0], coordinates[1]] = 0
                continue

    # pb if there is a very tiny cell need rebuild it # or just ignore
    img_saturated = dilated
    # for debug
    Img(img_saturated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'dilated_further.tif'))
    del dilated

list_of_cells_to_dilate = []
labs = label(invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)

if img_has_seeds:
    for region in regionprops(labs, intensity_image=img_orig):
        seeds = []

        if not extra_dilations and region.area < 10:
            continue

        # if small and no associated seeds --> remove it ??? maybe or not
        for coordinates in region.coords:
            id = lab_seeds[coordinates[0], coordinates[1]]
            if id != 0:
                seeds.append(id)

        seeds = set(seeds)

        if len(seeds) >= 2:
            # we may have found an undersegmented cell --> try segment it better
            list_of_cells_to_dilate.append(region.label)



if len(list_of_cells_to_dilate) != 0:
    props = regionprops(labs, intensity_image=img_orig)
    for run in range(10):
        something_changed = False  # early stop

        for region in props:
            if region.label not in list_of_cells_to_dilate:
                continue

            threshold_values = [100 / 255, 80 / 255, 60 / 255, 40 / 255, 30 / 255,
                                20 / 255, 10 / 255, 5 / 255] # 160 / 255, 140 / 255, 120 / 255, , 1 / 255 , 2 / 255

            try:
                for threshold in threshold_values:
                    mask = region.image.copy()
                    image = region.image.copy()
                    image[region.intensity_image > threshold] = True
                    image[region.intensity_image <= threshold] = False
                    final = np.zeros_like(image, dtype=np.uint8)
                    final = invert(image.astype(np.uint8))
                    final[final < 255] = 0
                    final[mask == False] = 0
                    new_seeds = label(final, connectivity=1, background=0)
                    props2 = regionprops(new_seeds)
                    if len(props2) > 1:  # cell was resplitted into smaller
                        for r in props2:
                            if r.area < 20:
                                raise Exception

                        region.image[mask == False] = False
                        region.image[mask == True] = True
                        region.image[new_seeds > 0] = False
                        something_changed = True
                        for coordinates in region.coords:
                            img_saturated[coordinates[0], coordinates[
                                1]] = 255  # ça a l'air de marcher car garde le truc # ça devrait pas marcher et d'ailleurs ça marche plus dès que je fais une copie
                    region.image[mask == False] = False
                    region.image[mask == True] = True
                    del final
                    del new_seeds
            except:
                traceback.print_exc()
                pass

        if not something_changed:
            # print('no more changes anymore --> quitting')
            break

 # for debug
# Img(img_saturated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'saturated_mask4.tif'))

# plt.imshow(img_saturated)
# plt.show()

final_seeds = label(invert(img_saturated), connectivity=1, background=0)

# TODO this extra size parameter is quite good --> can I automate it --> eg cells 3 times smaller than the average or more
# eg could set it to auto then compute average and adapt thresold

if extra_filter_by_size == 'auto':
    avg_area = 0
    count = 0
    for region in regionprops(final_seeds):
        avg_area+=region.area
        count+=1
    avg_area/=count
    extra_filter_by_size = avg_area/factor_below_average_for_extra_filter_by_size
    print('filter cells below:',extra_filter_by_size)



if extra_filter_by_size != 0:
    for region in regionprops(final_seeds):
        if region.area < extra_filter_by_size:
            for coordinates in region.coords:
                final_seeds[coordinates[0], coordinates[1]] = 0  # do remove the seed

final_seeds[img_saturated == 255] = 0
final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)  # , mask=img_saturated[img_saturated==255]

final_wshed[final_wshed != 0] = 1  # remove all seeds
final_wshed[final_wshed == 0] = 255  # set wshed values to 255
final_wshed[final_wshed == 1] = 0  # set all other cell content to

# plt.imshow(final_wshed)
# plt.show()



# print(parent_path, os.path.join(parent_path, filename0))
Img(final_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'optimized_wshed.tif'))

# inutile leur wshed donne le meme resultat qq soit l'angle...
#
# img_orig=img_orig[::-1,...]
# final_seeds = final_seeds[::-1,...]
# final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)
# final_wshed[final_wshed != 0] = 1  # remove all seeds
# final_wshed[final_wshed == 0] = 255  # set wshed values to 255
# final_wshed[final_wshed == 1] = 0  # set all other cell content to
# Img(final_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'optimized_wshed_inverted.tif'))

del final_wshed

filename0 = os.path.basename(path)
parent_path = os.path.dirname(os.path.dirname(path))
try:
    img_orig = Img(os.path.join(parent_path, filename0))
except:
    img_orig = Img(os.path.join(parent_path, os.path.splitext(filename0)[0]) + '.png')
if img_orig.has_c() and img_orig.shape[-1] != 1:
    img_orig = img_orig[..., 0]

# could even AND optimized_wshed and other watersheds
final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)  # , mask=img_saturated[img_saturated==255]
del final_seeds
# for debug
# Img(img_orig, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'original.tif'))

final_wshed[final_wshed != 0] = 1  # remove all seeds
final_wshed[final_wshed == 0] = 255  # set wshed values to 255
final_wshed[final_wshed == 1] = 0  # set all other cell content to

# plt.imshow(final_wshed)
# plt.show()
Img(final_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'optimized_wshed_real_original.tif'))

duration = timer() - start
print('duration is sec', duration)


# bond scoring does not work well yet --> deactivate for now
# if img_has_seeds:
#     kernel = np.ones((3, 3))
#     mask = convolve2d(final_wshed, kernel, mode='same', fillvalue=1)
#
#     # mask[mask<1020] = 0
#     # mask[mask>=1020] = 255
#
#     plt.imshow(mask)
#     plt.show()
#
#     result = np.zeros_like(mask)
#     result[np.logical_and(mask >= 1020, final_wshed == 255)] = 255
#
#     plt.imshow(result)
#     plt.show()
#
#     Img(result, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'vertices_test.tif'))
#
#     # dirty vertex detection but maybe there is hope
#
#     final_wshed = final_wshed.astype(np.uint8) - result.astype(np.uint8)
#
#     # get regions and count nb of white pixels in this region and if too low --> blast it...
#     bonds = label(final_wshed, connectivity=2, background=0)
#
#     plt.imshow(bonds)
#     plt.show()
#
#     final = final_wshed.copy()
#
#     img_seg[img_seg >= 0.9] = 255
#     img_seg[img_seg < 0.9] = 0
#
#     for region in regionprops(bonds):
#         # if region.area>100:
#         count = 0
#         for coordinates in region.coords:
#             # final[coordinates[0], coordinates[1]]=255
#             if img_seg[coordinates[0], coordinates[1]] == 255:
#                 count += 1
#
#         print(count / region.area)
#
#         if count / region.area <= 0.3:
#
#             for coordinates in region.coords:
#                 # final[coordinates[0], coordinates[1]]=255
#                 final[coordinates[0], coordinates[1]] = 0
#
#     plt.imshow(final)
#     plt.show()

