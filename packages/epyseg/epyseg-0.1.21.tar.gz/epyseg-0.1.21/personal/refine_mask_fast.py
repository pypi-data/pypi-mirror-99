# do an average of the 5 masks then segment them

from epyseg.img import Img
import matplotlib.pyplot as plt
from epyseg.postprocess.superpixel_methods import get_optimized_mask2

# windows tests
# img_orig = Img('D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/100708_png06.tif')
# img_orig = Img('D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/11.tif')
# img_orig = Img('D:/Dropbox/stuff_for_the_new_figure/old/predict_avg_hq_correction_ensemble_wshed/5.tif')

# linux
# img_orig = Img('/D/final_folder_scoring/predict_avg_hq_correction_ensemble_wshed/100708_png06.tif')
img_orig = Img('/D/final_folder_scoring/predict_test_of_bg_subtraction/100708_png06.tif') # very good too --> maybe worth a try!!!
# could also run wshed on orig and score bonds --> remove bonds but keep vertices to not destroy other things

if False:

    img_orig[..., 3] = Img.invert(img_orig[..., 3])
    img_orig[..., 4] = Img.invert(img_orig[..., 4])

    # seems to work --> now need to do the projection
    for c in range(1, img_orig.shape[-1] - 2):
        img_orig[..., 0] += img_orig[..., c]

    img_orig[..., 0] /= img_orig.shape[-1] - 2
    img_orig = img_orig[..., 0]

if True:
    img_orig[..., 0]+=img_orig[..., 1]
    img_orig=img_orig[..., 0]/2

plt.imshow(img_orig)
plt.show()

# faire un and entre les 2 ???

# sb = sobel(img_orig)
#
# plt.imshow(sb)
# plt.show()

# segments_quick = find_boundaries(quickshift(img_orig.astype(np.float), kernel_size=3, max_dist=6, ratio=0.5, convert2lab=False))
#
# plt.imshow(segments_quick)
# plt.show()

# from skimage.segmentation import watershed
# segmentation = watershed(segments_quick)

# segments_fz = felzenszwalb(img_orig, scale=100, sigma=1, min_size=50)
# pas mal
# segments_fz = felzenszwalb(img, scale=100, sigma=0.4, min_size=50)
# segments_fz = find_boundaries(felzenszwalb(gray2rgb(img_orig), scale=10, sigma=0.5, min_size=50)) # pas trop mal en fait aussi
#
# plt.imshow(segments_fz)
# plt.show()

# wshed_mask = Wshed.run(img_orig, first_blur=1, second_blur=3)
#
# plt.imshow(wshed_mask)
# plt.show()
#
# final_image = None
# rotations = [0, 2, 3]
# kernels = [1, 1.33, 1.66, 2]
#
# for kern in kernels:
#     for rot in rotations:
#         segments_quick = getQuickseg(img_orig, nb_of_90_rotation=rot, kernel_size=kern)
#         segments_quick = segments_quick.astype(np.uint8)
#         # plt.imshow(segments_quick)
#         # plt.show()
#         if final_image is None:
#             final_image = segments_quick
#         else:
#             final_image = final_image + segments_quick
#
#
# plt.imshow(final_image)
# plt.title("avg")
# plt.show()

# could even wshed it
# maybe need a better threshold there
# maybe do several
# final_image[final_image < final_image.max() * 0.74] = 0
# final_image[final_image >= final_image.max() * 0.74] = 255
# final_image[final_image < final_image.max()] = 0
# final_image[final_image >= final_image.max()] = 1
#
# plt.imshow(final_image)
# plt.show()

# combine felzenswab et autre ou felzenswab ds plein de ditrections comme marche bien

# peut etre que ça marcherait avec des images faites par bg subtraction


# do a score before
seeds, edm,  final_mask = get_optimized_mask2(img_orig, score_before_adding=True, return_seeds=True)

plt.imshow(final_mask)
plt.show()


Img(final_mask, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/final_mask.tif')
# what if I do floodfill by intensity on the raw image --> follow biggest stuff


# if a bond cann connect two unconnecteds then try connect them



# TODO do a find bond by overlap if still unconnected
# or TODO if several paths --> get best path from avg of bonds on orig image --> do this only for last unconnected bonds
# could also take closest vertex irrespective of position if unconnected...

# in the end try reconnect big bonds still unconnected especially if same orientation and score not too bad --> take it
# just take one and in the same orientation
# if still unconnected can try take closest bond and it vertices ...
# TODO
# then need rescore ???
# compare both

# or if two unconnected share same connecting bond then take it --> that is easy to do in fact... --> I really like this one
#



# TODO maybe score added bonds and only keep them if most of their length allows them to be there from the binarized mask
# no need to deblob but score --> could score on addition and decide to add it or not finally


# can I also tophat the mask or the edm ???


# really not great in fact


# what if I compare edm tophat and edm for seeds ??? would that help ???
# do slic * 2
if False:

    final_wshed = watershed(img_orig, markers=seeds, watershed_line=True)
    final_wshed[final_wshed != 0] = 2
    final_wshed[final_wshed == 0] = 1
    final_wshed[final_wshed == 2] = 0

    plt.imshow(final_wshed)
    plt.show()

    # final_wshed = np.logical_and(final_mask,final_wshed)
    #
    # plt.imshow(final_wshed)
    # plt.show()

    # need score the bonds and only keep most likely in fact (super bonds can habe higher score because lots of dark pixels around

    vertices, bonds = split_into_vertices_and_bonds(final_wshed)


    plt.imshow(bonds)
    plt.show()


    Img(bonds, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/cut_bonds.tif')
    Img(final_wshed, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/final_wshed.tif')

    Img(edm, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/edm.tif')



















if False:












    image = img_orig.copy()


    image[image<0.2]=0
    image[image>=0.2]=255

    image = Img.invert(image)

    plt.imshow(image)
    plt.show()

    distance = distance_transform_edt(image)

    plt.imshow(distance)
    plt.show()

    local_maxi = peak_local_max(distance, indices=False,
                                footprint=np.ones((8, 8)),
                                labels=image)  # sinon peut pas segmenter petites cellules --> à tester le tout en fait!!! min_distance does not work

    # take two closest seeds from different cells or from perpendicular site --> how can i do that --> not so hard compute the shape vector and angle then rotate and expand
    # take a bounding box to look around for seeds and if nothing is available then just take the seeds from the superpixel method --> otherwise take seed from the edm...
    # if two seeds and roughly same distance they are likely to be good and that is worth it...
    # can take seed anywhere in closest block maybe ???? --> yhink about it
    # if two independent bonds need be fixed maybe take three in fact should be ok to always take two
    # maybe take all seeds after filtering and get position of closest --> ideally interseed distance should be big --> roughly twice that of the distance to the bond tip unconnected
    # take closest either seed or big seed around --> TODO --> good idea in fact
    # be stingent with threshold then sauvola because useless otherwise

    # footprint and others bypass min_dist --> be careful and check doc
    # local_maxi = peak_local_max(distance, indices=False,     min_distance=5)  # sinon peut pas segmenter petites cellules --> à tester le tout en fait!!! min_distance does not work
    #
    # if seeds are close by then take only one in f

    # if seeds are close by then take only one in fact -> the biggest

    # print(generate_binary_structure(2,2))
    distance = -distance

    markers = ndimage.label(local_maxi, structure=generate_binary_structure(2, 2))[0]

    # if __VISUAL_DEBUG:
    plt.imshow(markers)
    plt.show()

    # maybe one wshed + one quick and compare both to get perfect stuff
    # or just get missing cells at connected stuff with erosion --> good idea maybe and much faster
    # to try

    # if __DEBUG:
        # Img(find_boundaries(segments_quick), dimensions='hw').save(
        #     '/home/aigouy/Bureau/trash/trash4/inner_0.tif')  # , mode='outer'
        # Img(segments_quick, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/quick_0.tif')
    # Img(markers, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/markers_0.tif')

    labels = watershed(distance, markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0
    labels[labels == 255] = 1

    # if __VISUAL_DEBUG:
    plt.imshow(labels)
    plt.title('raw wshed')
    plt.show()


    # ou faire l'autre code classique


    merge = np.logical_and(labels, final_mask)

    plt.imshow(merge)
    plt.title('merge')
    plt.show()