
from scipy.ndimage import distance_transform_edt, generate_binary_structure
from skimage.feature import peak_local_max
from scipy import ndimage

from deprecated_demos.ta.wshed import Wshed
from epyseg.img import Img
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve2d
from skimage.morphology import disk, remove_small_objects
# from skimage.morphology import watershed
from skimage.segmentation import watershed
from skimage.measure import label, regionprops
from skimage import transform as transfo


def get_optimized_mask(img, orig=None, __VISUAL_DEBUG=False, __DEBUG=False, real_avg_mode=False):
    img[img != 0] = 1
    skel = skeletonize(img)

    if __VISUAL_DEBUG:
        plt.imshow(skel)
        plt.show()

    skel = remove_small_objects(skel.astype(np.bool), min_size=10, connectivity=2, in_place=True).astype(np.uint8)

    if __VISUAL_DEBUG:
        plt.imshow(skel)
        plt.title('deblob')
        plt.show()

    labs = label(Img.invert(skel), connectivity=1, background=0)

    if __VISUAL_DEBUG:
        plt.imshow(labs)
        plt.show()

    # EXTRA_SEG_1 = False
    # EXTRA_SEG_3 = True
    # EXTRA_SEG_4 = False
    # EXTRA_SEG_5 = False
    # EXTRA_SEG_6 = False
    # EXTRA_SEG_7 = False

    EXTRA_SEG_1 = False
    EXTRA_SEG_3 = True
    EXTRA_SEG_4 = False
    EXTRA_SEG_5 = True
    EXTRA_SEG_6 = False
    EXTRA_SEG_7 = False

    # EXTRA_SEG_1 = False
    # EXTRA_SEG_3 = False
    # EXTRA_SEG_4 = False
    # EXTRA_SEG_5 = True
    # EXTRA_SEG_6 = False
    # EXTRA_SEG_7 = False

    # EXTRA_SEG_1 = True
    # EXTRA_SEG_3 = True
    # EXTRA_SEG_4 = True
    # EXTRA_SEG_5 = True
    # EXTRA_SEG_6 = True
    # EXTRA_SEG_7 = True

    # EXTRA_SEG_1 = False
    # EXTRA_SEG_3 = False
    # EXTRA_SEG_4 = False
    # EXTRA_SEG_5 = False
    # EXTRA_SEG_6 = False
    # EXTRA_SEG_7 = False

    image = skel.copy()
    image = image.astype(np.uint8) * 255
    # do the wshed on it
    image = Img.invert(image)


    distance = distance_transform_edt(image)

    if __VISUAL_DEBUG:
        plt.imshow(distance)
        plt.show()

    # before --> was that
    local_maxi = peak_local_max(distance, indices=False,
                                footprint=np.ones((8, 8)),
                                labels=image)  # sinon peut pas segmenter petites cellules --> à tester le tout en fait!!! min_distance does not work

    # footprint and others bypass min_dist --> be careful and check doc
    # local_maxi = peak_local_max(distance, indices=False,     min_distance=5)  # sinon peut pas segmenter petites cellules --> à tester le tout en fait!!! min_distance does not work
    #
    # if seeds are close by then take only one in f

    # if seeds are close by then take only one in fact -> the biggest

    # print(generate_binary_structure(2,2))
    distance = -distance
    if orig is not None:
        distance = orig

    markers = ndimage.label(local_maxi, structure=generate_binary_structure(2, 2))[0]

    if __DEBUG:
        Img(distance, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/edm.tif')

    # nb can I try this as wshed on the first image ??? or on other masks
    # can I use this directly if better than others --> just score bonds and if good add them
    if __VISUAL_DEBUG:
        plt.imshow(local_maxi)
        plt.show()

        # plt.imshow(markers)
        # plt.show()

    # there is a lot of noise how can I get rid of that...
    # do I care in fact ???

    # local_maxi = is_local_maximum(distance, image, np.ones((3, 3)))
    # markers = ndimage.label(local_maxi, structure=generate_binary_structure(2,2))[0]
    #
    # plt.imshow(markers)
    # plt.show()

    # plt.imshow(-distance)
    # plt.show()

    # plt.imshow(markers)
    # plt.show()

    if not EXTRA_SEG_1:
        final_watershed_mask = np.zeros_like(skel, dtype=np.int32)

    if EXTRA_SEG_1:
        labels = watershed(distance, markers, watershed_line=True)  # --> maybe implement that too
        # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
        #
        # plt.imshow(labels)
        # plt.title('test')
        # plt.show()
        labels[labels != 0] = 1  # remove all seeds
        labels[labels == 0] = 255  # set wshed values to 255
        labels[labels == 1] = 0  # set all other cell content to 0

        final_watershed_mask = labels.copy()
        # plt.imshow(labels)
        # plt.title('raw wshed')
        # plt.show()

        # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
        if __DEBUG:
            Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed1.tif')
        # sum all wsheds
        # that seems to roughly work --> can I make it better
        # or compare bonds and keep good ones in the two ??? --> maybe...

        # H watershed marche pas tres bien
        # distance2 = distance - 0.5*distance.max()
        # distance2[distance2<0]=0
        # # bis to use the non filtered one or one with a different filter maybe the raw one
        #
        # # pas mal mais bouge un peu les bonds
        # # distance = distance_transform_edt(skel)  # en fait c'est vraiment presque parfait --> à tester
        # # plt.imshow(distance)
        # # plt.show()
        # # TODO could randomly move seeds according
        # labels = watershed(-distance2, markers, watershed_line=True)  # --> maybe implement that too
        # # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
        # #
        # # plt.imshow(labels)
        # # plt.title('test')
        # # plt.show()
        # labels[labels != 0] = 1  # remove all seeds
        # labels[labels == 0] = 255  # set wshed values to 255
        # labels[labels == 1] = 0  # set all other cell content to 0
        # Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed0.tif')

    if __VISUAL_DEBUG:
        plt.imshow(markers)
        plt.title('markers')
        plt.show()

    if __DEBUG:
        Img(markers.astype(np.uint8) * 255, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/markers_normal.tif')

    afine_tf = transfo.AffineTransform(translation=(2, 2))
    shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                   order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
    # plt.imshow(shifted_markers)
    # plt.show()

    labels = watershed(distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0

    final_watershed_mask += labels
    if __DEBUG:
        Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed2.tif')

    if EXTRA_SEG_3:
        afine_tf = transfo.AffineTransform(translation=(-2, -2))
        shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                       order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
        # plt.imshow(shifted_markers)
        # plt.show()

        labels = watershed(distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
        # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
        #
        # plt.imshow(labels)
        # plt.title('test')
        # plt.show()
        labels[labels != 0] = 1  # remove all seeds
        labels[labels == 0] = 255  # set wshed values to 255
        labels[labels == 1] = 0  # set all other cell content to 0
        final_watershed_mask += labels

        if __VISUAL_DEBUG:
            plt.imshow(labels)
            plt.title('raw wshed')
            plt.show()

        if __DEBUG:
            # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
            Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed3.tif')

    if EXTRA_SEG_4:
        afine_tf = transfo.AffineTransform(translation=(-2, 2))
        shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                       order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
        # plt.imshow(shifted_markers)
        # plt.show()

        labels = watershed(distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
        # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
        #
        # plt.imshow(labels)
        # plt.title('test')
        # plt.show()
        labels[labels != 0] = 1  # remove all seeds
        labels[labels == 0] = 255  # set wshed values to 255
        labels[labels == 1] = 0  # set all other cell content to 0
        final_watershed_mask += labels

        if __VISUAL_DEBUG:
            plt.imshow(labels)
            plt.title('raw wshed')
            plt.show()

        if __DEBUG:
            # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
            Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed4.tif')

    if EXTRA_SEG_5:
        afine_tf = transfo.AffineTransform(translation=(2, -2))
        shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                       order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
        # plt.imshow(shifted_markers)
        # plt.show()

        labels = watershed(distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
        # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
        #
        # plt.imshow(labels)
        # plt.title('test')
        # plt.show()
        labels[labels != 0] = 1  # remove all seeds
        labels[labels == 0] = 255  # set wshed values to 255
        labels[labels == 1] = 0  # set all other cell content to 0
        final_watershed_mask += labels

        if __VISUAL_DEBUG:
            plt.imshow(labels)
            plt.title('raw wshed')
            plt.show()

        if __DEBUG:
            # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
            Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed5.tif')

    if EXTRA_SEG_6:
        afine_tf = transfo.AffineTransform(translation=(0, -2))
        shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                       order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
        # plt.imshow(shifted_markers)
        # plt.show()

        labels = watershed(distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
        # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
        #
        # plt.imshow(labels)
        # plt.title('test')
        # plt.show()
        labels[labels != 0] = 1  # remove all seeds
        labels[labels == 0] = 255  # set wshed values to 255
        labels[labels == 1] = 0  # set all other cell content to 0
        final_watershed_mask += labels

        if __VISUAL_DEBUG:
            plt.imshow(labels)
            plt.title('raw wshed')
            plt.show()

        if __DEBUG:
            # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
            Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed6.tif')

    if EXTRA_SEG_7:
        afine_tf = transfo.AffineTransform(translation=(-2, 0))
        shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                       order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
        # plt.imshow(shifted_markers)
        # plt.show()

        labels = watershed(distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
        # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
        #
        # plt.imshow(labels)
        # plt.title('test')
        # plt.show()
        labels[labels != 0] = 1  # remove all seeds
        labels[labels == 0] = 255  # set wshed values to 255
        labels[labels == 1] = 0  # set all other cell content to 0
        final_watershed_mask += labels

        if __VISUAL_DEBUG:
            plt.imshow(labels)
            plt.title('raw wshed')
            plt.show()

        if __DEBUG:
            # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
            Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed7.tif')

    # bug here was random watersheding but that was perfect as it removed most of the noise --> maybe that is my trick
    # could also try filtering with a different filter or after flipping the image --> good idea

    # TODO implement that
    # https://imagej.net/Interactive_Watershed --> fairly easy todo -> can change a bit the input image maybe

    # labels = watershed(Img.interpolation_free_rotation(-distance, 180), Img.interpolation_free_rotation(markers, 180), watershed_line=True)  # --> maybe implement that too
    # # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    # #
    # # plt.imshow(labels)
    # # plt.title('test')
    # # plt.show()
    # labels[labels != 0] = 1  # remove all seeds
    # labels[labels == 0] = 255  # set wshed values to 255
    # labels[labels == 1] = 0  # set all other cell content to 0
    # Img(Img.interpolation_free_rotation(labels,180), dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed2.tif')
    #
    # labels = watershed(np.flip(np.flip(-distance, 0),1), np.flip(np.flip(markers, 0),1),
    #                    watershed_line=True)  # --> maybe implement that too
    # # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    # #
    # # plt.imshow(labels)
    # # plt.title('test')
    # # plt.show()
    # labels[labels != 0] = 1  # remove all seeds
    # labels[labels == 0] = 255  # set wshed values to 255
    # labels[labels == 1] = 0  # set all other cell content to 0
    # Img(np.flip(np.flip(labels, 0),1), dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed3.tif')

    # H maximum wshed
    # distance = distance - 0.5*distance
    # distance[distance<0]=0
    # bis to use the non filtered one or one with a different filter maybe the raw one

    # pas mal mais bouge un peu les bonds
    distance = distance_transform_edt(skel)  # en fait c'est vraiment presque parfait --> à tester
    # plt.imshow(distance)
    # plt.show()
    # TODO could randomly move seeds according
    labels = watershed(distance, markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0
    final_watershed_mask += labels
    if __DEBUG:
        Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed8.tif')

    # distance = distance_transform_edt(skel)  # en fait c'est vraiment presque parfait --> à tester
    # plt.imshow(distance)
    # plt.show()
    # TODO could randomly move seeds according

    # dilation of the stuff but not that great in fact
    # s = ndimage.generate_binary_structure(2, 1)
    # markers = ndimage.grey_dilation(markers, footprint=s)
    #
    # labels = watershed(distance, markers, watershed_line=True)  # --> maybe implement that too
    # # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    # #
    # # plt.imshow(labels)
    # # plt.title('test')
    # # plt.show()
    # labels[labels != 0] = 1  # remove all seeds
    # labels[labels == 0] = 255  # set wshed values to 255
    # labels[labels == 1] = 0  # set all other cell content to 0
    # final_watershed_mask += labels
    # if __DEBUG:
    #     Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed9.tif')

    # distance = distance_transform_edt(img)  # en fait c'est vraiment presque parfait --> à tester
    #
    # # print(markers)
    # # print(type(markers))
    # # print(markers.shape)
    # # print(local_maxi.shape)
    # # plt.imshow(markers)
    # # plt.show()
    # # plt.imshow(distance)
    # # plt.show()
    # # TODO could randomly move seeds according
    # labels = watershed(distance, markers, watershed_line=True)  # --> maybe implement that too
    # # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    # #
    # # plt.imshow(labels)
    # # plt.title('test')
    # # plt.show()
    # labels[labels != 0] = 1  # remove all seeds
    # labels[labels == 0] = 255  # set wshed values to 255
    # labels[labels == 1] = 0  # set all other cell content to 0

    if __DEBUG:
        # Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed9.tif')
        Img(skel.astype(np.uint8) * 255, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/skel.tif')

    # seems ok maybe max it to skel

    # can I fix/keep seeds instead of bonds --> maybe that is simpler --> use overlap to indetify seed and keep the smallest --> not a good idea in fact
    # ok if i lose a few cells maybe
    # sinon scorer les differing bonds et voir lesquels garder peut etre aussi essayer de restaurer les long missing bonds coute que coute

    # end trash this

    # Img(labels.astype(np.uint8), dimensions='hw').save('D:/test_mask.png')

    # if __VISUAL_DEBUG:
    #     plt.imshow(labels)
    #     plt.show()

        # plt.imshow(image)
        # plt.show()

    # if __DEBUG:
    #     # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
    #     Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/rewatershed.tif')

    # should I combine all the masks here and have a very stringent filter and max it in the end to the skel to get mask


    if real_avg_mode:
        # return avg and let the other code do the job
        final_watershed_mask = final_watershed_mask/final_watershed_mask.max()
        # final_watershed_mask[final_watershed_mask < 0.75]=0
        # final_watershed_mask[final_watershed_mask >=0.75] = 1
        # final_watershed_mask[skel != 0] = 1
        # final_watershed_mask[final_watershed_mask != 0] = 255
        return final_watershed_mask

    if __VISUAL_DEBUG:
        plt.imshow(final_watershed_mask)
        plt.title('avg')
        plt.show()

    if __DEBUG:
        Img(final_watershed_mask, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/avg.tif')
        Img(skel, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/skel.tif')

    true_count = sum([EXTRA_SEG_1, EXTRA_SEG_3, EXTRA_SEG_4, EXTRA_SEG_5, EXTRA_SEG_6, EXTRA_SEG_7])

    # print(true_count)
    if true_count >= 1:
        threshold_nb_of_images_diverging = 1
    elif true_count >= 4:
        threshold_nb_of_images_diverging = 2
    else:
        threshold_nb_of_images_diverging = 0

    final_watershed_mask[final_watershed_mask < final_watershed_mask.max() - (threshold_nb_of_images_diverging * 255)] = 0
    final_watershed_mask[skel != 0] = 255
    final_watershed_mask[final_watershed_mask != 0] = 255
    # correct watershed to keep best only
    Img(final_watershed_mask, dimensions='hw').save(
        '/home/aigouy/Bureau/trash/trash4/corrected_whsed.tif')

    # final_watershed_mask[cells_to_resegment!=0]=labels[cells_to_resegment!=0]
    # final_watershed_mask[final_watershed_mask!=0]=255

    final_watershed_mask = Wshed.run(final_watershed_mask.astype(np.uint8), seeds='mask')

    if __VISUAL_DEBUG:
        plt.imshow(final_watershed_mask)
        plt.title('test')
        plt.show()

    if __DEBUG:
        # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
        Img(final_watershed_mask.astype(np.uint8), dimensions='hw').save(
            '/home/aigouy/Bureau/trash/trash4/rewatershed_fixed_secure.tif')

    # maybe also further remove tiny cells from the stuff --> are there tiny cells an artifact of skel --> if so blast them
    # TODO
    # alternatively always take biggest cell of the two ???
    # or remove tiny cells
    # also if new contact not connected to existing vertex it can be removed
    # --> loop over vertices

    if False:
        # get differing bonds and get their tips --> if not connected to an existing stuff then remove them
        differing_bonds = np.logical_xor(final_watershed_mask, skel)
        # plt.imshow(differing_bonds)
        # plt.show()

        if __DEBUG:
            # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
            Img(differing_bonds.astype(np.uint8) * 255, dimensions='hw').save(
                '/home/aigouy/Bureau/trash/trash4/differing_bonds.tif')

        import os
        path = os.path.abspath('/home/aigouy/Bureau/trash/trash4/')
        print(path)
        # si pas un pixel dans les deux pixels à proximité ou au moins dans 2 px radius alos c'est un faux bond et il faut le supprimer
        # again get the tip or bounding box and get if there is a px around
        # ar in fact only keep bonds that do touch an unconnected one --> in fact it's easier thta way and I have everything already
        # of all those remaining bonds check the ones in touch with an unconnected vertex and keep them --> in fact remove them so that they are not substracted --> faire un logical stuff

        labeled_differing_bonds = label(differing_bonds, background=0, connectivity=None)
        differing_bonds_really_connected = []
        for i in range(len(coordinates_x)):
            try:
                try:
                    val = labeled_differing_bonds[coordinates_y[i] - 2:coordinates_y[i] + 3,
                          coordinates_x[i] - 2:coordinates_x[i] + 3].flatten()
                except:
                    val = labeled_differing_bonds[coordinates_y[i] - 1:coordinates_y[i] + 2,
                          coordinates_x[i] - 1:coordinates_x[i] + 2].flatten()
                for val in val[val != 0]:
                    differing_bonds_really_connected.append(val)
            except:
                pass

        for region in regionprops(labeled_differing_bonds):
            if region.label in differing_bonds_really_connected:
                for coordinates in region.coords:
                    differing_bonds[coordinates[0], coordinates[1]] = 0

        if __DEBUG:
            # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
            Img(differing_bonds.astype(np.uint8) * 255, dimensions='hw').save(
                '/home/aigouy/Bureau/trash/trash4/differing_bonds2.tif')

        final_watershed_mask = final_watershed_mask - differing_bonds.astype(np.uint8) * 255

        if __DEBUG:
            # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
            Img(final_watershed_mask.astype(np.uint8), dimensions='hw').save(
                '/home/aigouy/Bureau/trash/trash4/rewatershed_fixed_secure2.tif')

        # TODO clean all unecessary files here

    # now remove tiny cells that are not present in wshed but present in original --> TODO --> in fact that also removes true very tiny cells too
    # faire un code avec ça et essayer de finaliser tt
    if False:
        # maintenant si truc est ok que faire ????
        # dois-je blaster petites cellules ???
        # peut etre en fait aussi

        # faire un np.min entre final wshed et autre pr essayer
        # à tester --> mais voir si ça ne supprime pas les ttes petites cellules

        # not great --> remove that and see if better
        # ne pas faire ça en fait ou alors un bug qq part...
        final_watershed_mask = np.minimum(final_watershed_mask, labels)
        s = ndimage.generate_binary_structure(2, 1)
        final_watershed_mask = ndimage.grey_dilation(final_watershed_mask,
                                                     footprint=s)  # required to fix tiny blurbs but may cause overseg too

        if __VISUAL_DEBUG:
            plt.imshow(labels)
            plt.title('skel')
            plt.show()

            plt.imshow(final_watershed_mask)
            plt.title('final')
            plt.show()

        if __DEBUG:
            # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
            Img(final_watershed_mask.astype(np.uint8), dimensions='hw').save(
                '/home/aigouy/Bureau/trash/trash4/rewatershed_fixed_secure3.tif')

        # fini pr now --> just try on the sample of the other guy on vertebrate cells

    return final_watershed_mask
