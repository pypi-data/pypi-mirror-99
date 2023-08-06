# is that optimal as the cell region keeps on decreasing --> should I run a wshed in between ??? TO fix for that ??? or should I not care ??? --> it may decrease cell size
# faudrait aussi pouvoir recuperer les trucs qui existent --> à voir
# will that now be slower than

# skeletonize image
# detect free ends and their direction from the closest vertex of from an endpoint and try to connect it by drawing a line away from the hole
# alternative fill the cell then detect its empty edges --> having the same color on both sides and try to connect it to point away... --> is that sio hard to do ???
# alternative skeletonize then prune and compare before and after prune to get the vertices and the direction of the line then draw it --> quite easy I think


# si je fill une cell et deux free ends close to one another then I can connect them rather than drawing a line for each of them # --> first pass then do a second one for those that couldn't be connected

# or get all smallest possible ROIs by different thresholdings and blast things not associated to strong line --> then use those as seeds --> convert wshed back to seeds and run wshed...
# how can I do that ????


# try run those seeds on original again --> see how I can do that
# just keep seeds and nothing else
# binarise and get seeds with different thresholds if several seeds split an existing one --> keep smallest # maybe with a cutoff and run wshed on orig with those seeds --> should work???
# then blast lines that have almost 0% of white below them
# --> can be doable


import traceback
# from skimage.morphology import flood
# skimage.morphology.flood_fill(image, …[, …])
from skimage.util import invert
from skimage.draw import line_aa
from skimage.morphology import skeletonize
import math
from deprecated_demos.ta.wshed import Wshed
from epyseg.img import Img
from matplotlib import pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from timeit import default_timer as timer

# take orig label it and get seeds
# count colors of one seed and split it

# if no new seed below then ignore it
# can this be done all at once with recursive changing of seeds on orig --> maybe and would not cost much memory then


# TODO think if that's really optimal as it may not work


start = timer()

img_orig = Img('/home/aigouy/Bureau/AVG_FocStich_RGB005-1.png')
# img_saturated = Img('D:/Dropbox/AVG_FocStich_RGB005-1.png')
plt.imshow(img_orig)
plt.show()

img_saturated = img_orig.copy()
img_saturated[img_saturated > 230] = 255
img_saturated[img_saturated <= 230] = 0

Img(img_saturated, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/saturated_mask.tif')

# early stop when don't change ... maybe --> otherwise do it 2 or 3 times

for run in range(10):
    print('run', run)
    cytoplasm = label(invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)

    # plt.imshow(cytoplasm)
    # plt.show()
    something_changed = False # early stop

    for region in regionprops(cytoplasm, intensity_image=img_orig):
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

        threshold_values = [230, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 30, 20, 10, 5, 2,1]

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
                props = regionprops(new_seeds)
                if len(props) > 1:  # cell was resplitted into smaller
                    # print('new split = ', len(props))
                    for r in props:
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
                        img_saturated[coordinates[0], coordinates[1]] = 255  # ça a l'air de marcher car garde le truc # ça devrait pas marcher et d'ailleurs ça marche plus dès que je fais une copie
                region.image[mask == False] = False
                region.image[mask == True] = True
        except:
            traceback.print_exc()
            pass

    if not something_changed:
        print('no more changes anymore --> quitting')
        break

# not so bad but how can I do that ??? properly --> need check splits are big enough otherwise ignore
# should I do this recursively ???


plt.imshow(img_saturated)
plt.show()

Img(img_saturated, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/saturated_mask2.tif')



# handCorrection_strong = Wshed.run(img_saturated, seeds='mask')
#
# Img(handCorrection_strong, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/wshed_saturated.tif')
# Img(handCorrection_strong, dimensions='hw').save('D:/Dropbox/AVG_FocStich_RGB005-1/wshed_saturated.tif')

# #
# # vertices_hand_corr =np.zeros_like(handCorrection_strong)
# # TODO need get the vertices of handCorrection_strong to cut the bonds and recover them
# # see how
# for i in range(1, handCorrection_strong.shape[-1] - 1, 1):
#     for j in range(1, handCorrection_strong.shape[-2] - 1, 1):
#
#         # if matches a free edge --> ad it to a list and connect to closest one
#         #
#
#         if handCorrection_strong[j][i] != 0:
#             count_white = 0
#             count_dark = 0
#             if handCorrection_strong[j - 1][i] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if handCorrection_strong[j + 1][i] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if handCorrection_strong[j][i - 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if handCorrection_strong[j][i + 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if handCorrection_strong[j - 1][i - 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if handCorrection_strong[j - 1][i + 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if handCorrection_strong[j + 1][i - 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if handCorrection_strong[j + 1][i + 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if count_white >= 3:
#                 vertices_hand_corr[j][i] = 255
#
#
# # remove vertices to allow for floodfill 8 connected
# handCorrection_strong[vertices_hand_corr!=0]=0
#
# bonds = label(handCorrection_strong, connectivity=2, background=0)
#
#
# # now get all the regionprops and check if they exist
#
#
#
#
# #tester un wshed sur un truc tres fortement thresholde --> a tester
#
# img = Img('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/handCorrection.tif')
# # img = Img('D:/Dropbox/AVG_FocStich_RGB005-1/handCorrection.tif')
#
# img[img > 0] = 1  # TODO do that more wisely
#
# skeleton = skeletonize(img.copy())
# plt.imshow(skeleton)
# plt.show()
# Img(skeleton, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/skel.tif')
# # Img(skeleton, dimensions='hw').save('D:/Dropbox/AVG_FocStich_RGB005-1/skel.tif')
# # vertices = Wshed.detect_vertices(skeleton) # this shit is super slow --> do I really need that ???
# # plt.imshow(vertices)
# # plt.show()
#
#
# img[img>0]=255
# # wshed = Wshed.r
# handCorrection = Wshed.run(img, seeds='mask')
#
# # best would be to recover original just to fill the missing stuff --> is that easy or not ???
#
# Img(handCorrection, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/wshed.tif')
# # Img(handCorrection, dimensions='hw').save('D:/Dropbox/AVG_FocStich_RGB005-1//wshed.tif')
#
# plt.imshow(handCorrection)
# plt.show()
#
#
# labels_to_indentify_cell = label(invert(handCorrection.astype(np.uint8)), connectivity=1, background=0)
#
# # final_copy = img.copy()
# # skel, final_copy = Wshed.run_fix_mask(final_copy)
#
# # print('skel2')
# # plt.imshow(skel)
# # plt.show()
# # print('end')
#
# # img[img>0]=255
# # final_mask = Wshed.run_dist_transform_watershed(img)
#
# # plt.imshow(final_mask)
# # plt.show()
#
# # Img(final_mask, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/EDT.tif') # c'est nul en fait ça ne marche pas du tout...
#
#
# # facile de detecter les vertices car trois points blancs autour de lui --> easy
#
# # detecter l'ending point et remonter jusqu'au vertex --> ensuite lui faire calculer l'angle et lui faire etendre dans la direction opposee --> facile doit s'etendre dans les pixels de la meme couleur de la surrounding cell
# # nb c'est pas tjrs le plus proche point qui doit etre connecte
#
#
# out = np.zeros_like(skeleton)
# vertices = np.zeros_like(skeleton)
# #
# free_edges = []
# #
# #
# #
# # detect free edges
# # NB skeleton is not as precise as wshed for vertices....
# for i in range(1, skeleton.shape[-1] - 1, 1):
#     for j in range(1, skeleton.shape[-2] - 1, 1):
#
#         # if matches a free edge --> ad it to a list and connect to closest one
#         #
#
#         if skeleton[j][i] != 0:
#             count_white = 0
#             count_dark = 0
#             if skeleton[j - 1][i] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if skeleton[j + 1][i] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if skeleton[j][i - 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if skeleton[j][i + 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if skeleton[j - 1][i - 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if skeleton[j - 1][i + 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if skeleton[j + 1][i - 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if skeleton[j + 1][i + 1] != 0:
#                 count_white += 1
#             else:
#                 count_dark += 1
#             if count_dark >= 7:
#                 # print('isolated_pixel', i, j)
#                 free_edges.append((i, j))
#                 out[j][i] = 255
#             if count_dark == 5:
#                 vertices[j][i] = 255
#
# # Img(out, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/unconnected.tif')
#
# # TODO create a cut image at vertices and try to cut it
# skeleton[vertices!=0]=0
#
# # do I need that ??? now need find closest bond to the vertex and restore it
# # maybe with a dilation too or need also restore its vertices --> just try
#
# corrected = np.zeros_like(handCorrection_strong)
#
# # class BreakOutOfALoop(Exception): pass
#
# look_around_radius = 20 # less than 4 percent of non detected --> ok I think
# counter_miss = 0
#
# # new attempt --> flood splitted cell and recover mask from the non strong binarized stuff
# # --> loop over stuff and get id
#
# # do label all in 4 connected then loop over them and if they interact with
# # i could easily determine whether point is within bounding box and or bounding box + a few extra pixels in w and height --> probably not so hard
#
# # comment en faire une dilation # maybe check if coord is in
#
# # le code inverse serait il plus facile
#
# # super slow --> can I find a better trick maybe using seeds detected with label at different thresholds and --> think about it
#
# # reverse stuff
#
# # j'y suis presque mais qu'est ce que c'est lent inverser le truc ou faire un test plus efficace
# # maybe check if intersects with a bond with a free edge
# # how can I do the limit stuff
# # should not fill too much the stuff
#
# # COMPARISON WITH THE OpenCV WATERSHED IMPLEMENTATION:
# #
# #    If your main interest is in just the final output --- good-quality
# #    watershed segmentations based on user-supplied seeds --- then this
# #    Python module is not for you and you should use the OpenCV
# #    implementation. With regard to the speed of execution, a pure Python
# #    module such as this cannot hope to compete with the C-based
# #    implementation in the OpenCV library. --> maybe change it
#
#
# # for region in regionprops(bonds):
# props = regionprops(labels_to_indentify_cell)
#
# for (i,j) in reversed(free_edges):
#     for i1 in range(look_around_radius):
#         for j1 in range(look_around_radius):
#             try:
#                 if labels_to_indentify_cell[j + j1][i + i1] != 0: # we found a cell --> get its id
#                     id = labels_to_indentify_cell[j + j1][i + i1]
#
#                     # now use that to fill stuff with original # how can I preserve gradient --> simply by keeping original watershed highest --> keep white pixels then add on top of them the pixels I need
#
#                     # print('id', props[id-1].label, id) # check the same
#                     for coordinates in props[id-1].coords:
#                         corrected[coordinates[0], coordinates[1]] = 255
#
#                     # need take bond closest to the vertex and paste it in the other image and connect it
#                     # could also get the bond by flooding outside
#                     # just try
#                     # corrected[j+j1][i+i1] = 255
#                     # local_id = flood(handCorrection_strong, (j+j1,i+i1))  # met le pixel a True
#                     # print(local_id[510, 510])
#                     # print("here I am:", local_id)
#                     # TOP COOL THIS GETS THE INDICES OF THE MASKED STUFF
#                     # floodX, floodY = np.nonzero(local_id) # so fucking slow I hate it --> need an alternative --> cause not possible...
#                     # corrected[floodX, floodX] = 255
#                     # success = True
#                     # raise Exception # first pixel found get out
#                     pass
#                 elif labels_to_indentify_cell[j-j1][i-i1] != 0:
#                     # need take bond closest to the vertex and paste it in the other image and connect it
#                     # could also get the bond by flooding outside
#                     # just try
#                     # corrected[j-j1][i-i1] = 255
#                     # success = True
#                     # raise Exception # first pixel found get out
#                     pass
#                 elif labels_to_indentify_cell[j-j1][i+i1] != 0:
#                     # corrected[j - j1][i + i1] = 255
#                     # success = True
#                     # raise Exception  # first pixel found get out
#                     pass
#                 elif labels_to_indentify_cell[j+j1][i-i1] != 0:
#                     # if (j+j1,i+i1) in region.bbox or (j-j1,i-i1)in region.bbox or (j-j1,i+i1)in region.bbox or (j+j1,i-i1)in region.bbox :
#                     #     for coordinates in region.coords:
#                     #         corrected[coordinates[0], coordinates[1]] = 255
#                     #         success = True
#                     #         free_edges.remove((i,j))
#                     #     raise Exception
#                     pass
#             except:
#                 pass
#
# # min_size = 300
# # for region in regionprops(bonds):
# #     # take regions with large enough areas
# #     # if region.area < min_size:
# #         # slow faudrait vider les free edges pr gagner du temps... mais rien n'est plus mauvais que le floodfill de scipy... tout de meme...
# #         success = False
# #         try:
# #             for (i,j) in reversed(free_edges):
# #                 for i1 in range(look_around_radius):
# #                     for j1 in range(look_around_radius):
# #                         if (j+j1,i+i1) in region.bbox or (j-j1,i-i1)in region.bbox or (j-j1,i+i1)in region.bbox or (j+j1,i-i1)in region.bbox :
# #                             for coordinates in region.coords:
# #                                 corrected[coordinates[0], coordinates[1]] = 255
# #                                 success = True
# #                                 free_edges.remove((i,j))
# #                                 raise Exception
# #         except:
# #             pass
# #         # if not success:
#         #     print('no bound found --> ignoring', i, j)
#         #     counter_miss+=1
#
# # Look from closest to furthest to avoid errors
# # for (i,j) in free_edges:
# #     # look in mask to see if I can find one
# #
# #     # maybe I could also take the image
# #     # look around within a defined radius if it finds a bond and if so --> take it
# #     success = False
# #     try:
# #         for i1 in range(look_around_radius):
# #             for j1 in range(look_around_radius):
# #                 try:
# #                     if handCorrection_strong[j+j1][i+i1] != 0:
# #                         # need take bond closest to the vertex and paste it in the other image and connect it
# #                         # could also get the bond by flooding outside
# #                         # just try
# #                         corrected[j+j1][i+i1] = 255
# #                         # local_id = flood(handCorrection_strong, (j+j1,i+i1))  # met le pixel a True
# #                         # print(local_id[510, 510])
# #                         # print("here I am:", local_id)
# #                         # TOP COOL THIS GETS THE INDICES OF THE MASKED STUFF
# #                         # floodX, floodY = np.nonzero(local_id) # so fucking slow I hate it --> need an alternative --> cause not possible...
# #                         # corrected[floodX, floodX] = 255
# #                         # success = True
# #                         raise Exception # first pixel found get out
# #                     elif handCorrection_strong[j-j1][i-i1] != 0:
# #                         # need take bond closest to the vertex and paste it in the other image and connect it
# #                         # could also get the bond by flooding outside
# #                         # just try
# #                         corrected[j-j1][i-i1] = 255
# #                         success = True
# #                         raise Exception # first pixel found get out
# #                     elif handCorrection_strong[j-j1][i+i1] != 0:
# #                         corrected[j - j1][i + i1] = 255
# #                         success = True
# #                         raise Exception  # first pixel found get out
# #                     elif handCorrection_strong[j+j1][i-i1] != 0:
# #                         corrected[j + j1][i - i1] = 255
# #                         success = True
# #                         raise Exception  # first pixel found get out
# #                 except:
# #                     # out of bonds exception --> ignore
# #                     pass
# #         if not success:
# #             print('no bound found --> ignoring', i, j)
# #             counter_miss+=1
# #     except:
# #         continue
#
#
# print('final correx', counter_miss, counter_miss/len(free_edges))
# plt.imshow(corrected)
# plt.show()
#
# Img(corrected, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/final_corrections_masks.tif')
#
#
# # si deux sont vraiment tres pres alors faut les connecter
# # loop over edges
#
#
# # test = np.zeros_like(skeleton)
# # for idx, (i1, j1) in enumerate(reversed(free_edges)):
# #     if idx+1<len(free_edges):
# #         for i2, j2 in reversed(free_edges[idx+1:]):
# #             dist = math.sqrt((i2 - i1) ** 2 + (j2 - j1) ** 2)
# #             if dist <= 6 and dist>0: # why can it be 0
# #                 # draw line
# #                 rr, cc, val = line_aa(j1, i1, j2, i2)
# #                 test[rr, cc] = val*255
# #                 img[rr, cc] = val*255
# #                 free_edges.remove((i1, j1))
# #                 break
#
#
#             # flood it until I encounter a vertex then compute line
#             # flood_fill(bonds, (i1, j1), 127, inplace=True)
#             # if i1 >= bonds.shape[1] - 3 or j1 >= bonds.shape[0] - 3:
#             #     free_edges.remove((i1, j1))
#             #     continue
#             # if i1 <= 2 or j1 <= 2:
#             #     free_edges.remove((i1, j1))
#             #     continue
#
#     # if bonds[j1][i1] != 0:
#     #     # flood_fill(bonds, (j1, i1), 127, inplace=True)
#     #     flood.flood(bonds, i1, j1, 2, connectivity=Floodfill.EIGHT_CONNECTED)
#     #     if flood.get_area() < 4:
#     #         free_edges.remove((i1, j1))
#
# # plt.imshow(test)
# # plt.show()
#
#
# # plt.imshow(skeleton)
# # plt.show()
# # skeleton[vertices == 255] = 0
#
# # Img(skeleton, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/cut_skel.tif')
# # Img(test, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/fixed_small.tif')
# img[img > 0]=255
# # Img(img, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/fixed_on_skel.tif')
#
# # That really sucks because the skeletonize algorithm is creating the holes --> really dumb to use it
# #  need another way to detect it and ideally increase threshold until the line gets connected to the neighbor and take this line as the default --> would make no mistake--> how to do that
# # how can I identify those lines ???
# # DO a dilation on vertices to cut them
# # maybe I can detect the repair by not having the two cells
#
# # best would be to increase the threshold untill the two edges are connected while keeping the cells --> should ne doable --> in fact need get the labels around the bonds without the connection and see when they become two in the image --> gets splitted
# # sinon faire la liste de ttes les cellules splittees qu'on peut obtenir avec differents thresholds et voir ceux qui me permettent d'obtenir des cellules separees et alors recup ce contact --> facile --> copier la region floodee afin d'obtenir le truc qu'il faut...
# # comment faire...
# # faut faire un skeleton de chaque image thresholdee ? --> ÇA VA ETRE SLOW  --> reflechir
# # check all
# # think about it...
#
# # almost there
# # need check when cytoplasms on both sides aren't connected anymore... --> when do we have 2 cells instead of 1 --> on either side of the bond --> how can i check that --> with a floodfill ????
# # how can I do that practically ... --> there has to be an easy way
#
#
#
#
#
# # detect vertices
# # for i in range(1, skeleton.shape[-1] - 1, 1):
# #     for j in range(1, skeleton.shape[-2] - 1, 1):
# #
# #         # if matches a vertex label it as such
# #
# #         if skeleton[j][i] != 0:
# #             count_white = 0
# #             count_dark = 0
# #             if skeleton[j - 1][i] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             if skeleton[j + 1][i] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             if skeleton[j][i - 1] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             if skeleton[j][i + 1] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             if skeleton[j - 1][i - 1] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             if skeleton[j - 1][i + 1] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             if skeleton[j + 1][i - 1] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             if skeleton[j + 1][i + 1] != 0:
# #                 count_white += 1
# #             else:
# #                 count_dark += 1
# #             # if count_white == 4: # 4 dans skel
# #                 # print('isolated_pixel', i, j)
# #                 # free_edges.append((i, j))
# #             # pas top mais ça fera les vertices sont elargis
# #             if count_dark == 5:
# #                 vertices[j][i] = 255
#
# # Img(vertices, dimensions='hw').save('/home/aigouy/Bureau/AVG_FocStich_RGB005-1/vertices.tif')
#
# print("total time:", timer() - start)
#
# import sys
#
# sys.exit(0)
#
# # this is to draw line between points
# import scipy.misc
# import numpy as np
# from skimage.draw import line_aa
#
# img = np.zeros((10, 10), dtype=np.uint8)
# rr, cc, val = line_aa(1, 1, 8, 4)
# img[rr, cc] = val * 255
# scipy.misc.imsave("out.png", img)
#
# # second_point = None
# # counter = 0
# # for (i1, j1) in free_edges:
# #     # min_pair.append(i1, j1)
# #     min_dist = 1_000_000
# #     for (i2, j2) in free_edges[counter:]:
# #         if i1 != i2 and j1 != j2:
# #             dist = math.sqrt((i1-i2)**2 + (j1-j2)**2)
# #             # print(dist)
# #             if dist < min_dist:
# #                 min_dist = dist
# #                 second_point = (i2, j2)
# #     if min_dist < 50:
# #         rr, cc, val = line_aa(j1, i1, second_point[1], second_point[0])
# #         out[rr, cc] = val * 255
# #         counter += 1
#
#
# # sometimes also need to connect the vertices if belong to same cell cause does not make sense...
