# need a binarised image as an input
from scipy.ndimage import distance_transform_edt, generate_binary_structure
from skimage.feature import peak_local_max
from scipy import ndimage
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


# should I run wshed on original rather than on mask ???
def get_optimized_mask(img, __VISUAL_DEBUG = False, __DEBUG = False):

    #
    # img = Img('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/binarised_mask.png')
    # img = Img('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/C3-E9 WT ppMLCV YAPcy5 actinR 2-1.png')

    # skeletonize it
    img[img != 0] = 1
    skel =skeletonize(img)

    # TODO maybe also remove super tiny bonds or just try like that
    # do wshed every where but keep seeds only for stuff of interest

    if __VISUAL_DEBUG:
        plt.imshow(skel)
        plt.show()
    # ça marche peut etre juste faire un petit deblob avant
    skel = remove_small_objects(skel.astype(np.bool),min_size=10, connectivity=2, in_place=True).astype(np.uint8)

    if __VISUAL_DEBUG:
        plt.imshow(skel)
        plt.title('deblob')
        plt.show()



    # now detect unconnected bonds and do stuff with them
    # bond scoring does not work well yet --> deactivate for now
    kernel = np.ones((3, 3))
    mask = convolve2d(skel, kernel, mode='same', fillvalue=1)


    # plt.imshow(mask)
    # plt.show()

    # specifically detect vertices here too to remove false bonds again
    # mask2 = convolve2d(output, kernel, mode='same', fillvalue=1)

    mask[mask != 2] = 0
    mask[mask == 2] = 1

    mask = np.logical_and(skel, mask).astype(np.uint8)

    # mask = mask.astype(np.bool)
    # if VISUAL_DEBUG:
    if __VISUAL_DEBUG:
        plt.imshow(mask)
        plt.show()

    labs = label(Img.invert(skel), connectivity=1, background=0)
    # for region in regionprops(mask):
    #     if region.area < 5:
    #         for coordinates in region.coords:
    #             final_mask[coordinates[0], coordinates[1]] = 255

    if __VISUAL_DEBUG:
        plt.imshow(labs)
        plt.show()

    # skel=skel+mask
    if __VISUAL_DEBUG:
        plt.imshow(skel+mask)
        plt.show()


    # mask[mask!=0]=0
    # mask[256,512]=1

    # allow watershed but in fact only keep those ones


    # get cells allowed to be changed --> cells having a fot in them
    # loop over all pixel having a value
    coords_unconnected_bonds = mask.nonzero()

    # print(coords_unconnected_bonds)
    # cells allowed to change
    cells_allowed_to_change = []
    coordinates_y= coords_unconnected_bonds[0]
    coordinates_x= coords_unconnected_bonds[1]

    for i in range(len(coordinates_x)):
        # en fait faut regarder autour sinon ça ne marche pas

        # look around and get id

        # @numba.stencil(neighborhood=((-1, 1), (-1, 1)))
        # def _average(arr):
        #     return np.mean(arr[-1:2, -1:2])
        # print(np.median(labs[coordinates_y[i]-1:coordinates_y[i]+1, coordinates_x[i]-1:coordinates_x[i]+1]))
        try:
            # cells_allowed_to_change.append(int(np.median(labs[coordinates_y[i]-1:coordinates_y[i]+1, coordinates_x[i]-1:coordinates_x[i]+1])))
            #
            # if int(np.median(labs[coordinates_y[i]-1:coordinates_y[i]+1, coordinates_x[i]-1:coordinates_x[i]+1])) == 124:
                # print(labs[coordinates_y[i]-1:coordinates_y[i]+1, coordinates_x[i]-1:coordinates_x[i]+1].flatten())
                val = labs[coordinates_y[i]-1:coordinates_y[i]+2, coordinates_x[i]-1:coordinates_x[i]+2].flatten()
                # print(val)
                # val = val[val!=0]
                # print(labs[coordinates_y[i]-1:coordinates_y[i]+1, coordinates_x[i]-1:coordinates_x[i]+1].flatten().nonzero())
                # a = np.array([1, 2, 3, 1, 2, 1, 1, 1, 3, 2, 2, 1])
                counts = np.bincount(val[val!=0])
                # print('most frequent',np.argmax(counts))
                cells_allowed_to_change.append(np.argmax(counts))

                # occurances = np.bincount(x)
                # print(np.argmax(occurances))
        except:
            pass
        # remove dupes
    cells_allowed_to_change = list(dict.fromkeys(cells_allowed_to_change))
    if 0 in cells_allowed_to_change:
        cells_allowed_to_change.remove(0)

    if __VISUAL_DEBUG:
        print(cells_allowed_to_change)
        print('n',len(cells_allowed_to_change))

    # print(len(cells_allowed_to_change)) # 56

    cells_to_resegment = np.zeros_like(mask)

    for region in regionprops(labs):
        if region.label in cells_allowed_to_change:
            for coordinates in region.coords:
                    # if region.label != labs[coordinates[0], coordinates[1]]:
                    #     print(region.label, 'vs', labs[coordinates[0], coordinates[1]])
                    cells_to_resegment[coordinates[0], coordinates[1]] = 1

    if __VISUAL_DEBUG:
        plt.imshow(cells_to_resegment)
        plt.show()

    # ça a l'air de marcher en fait
        plt.imshow(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2)
        plt.show()

    if __DEBUG:
        Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
        Img(labs, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_labs.tif')

    # là c'est parfait
    # simply run the wshed then just get what I want

    # just restore those cells on the mask
    # easy in fact use this mask to restore part of cells then compare

    image = skel.copy()
    image = image.astype(np.uint8)*255
    # do the wshed on it
    image = Img.invert(image)

    distance = distance_transform_edt(image)
    if __VISUAL_DEBUG:
        plt.imshow(distance)
        plt.show()
    # local_maxi = is_local_maximum(distance, image, np.ones((3, 3)))
    # local_maxi = ndimage.maximum_filter(distance, size=1) == distance

    # --> à voir en fait peut etre ok ???
    #

    local_maxi = peak_local_max(distance, indices=False,
                                        footprint=np.ones((8, 8)), labels=image) # sinon peut pas segmenter petites cellules --> à tester le tout en fait!!!
    # print(generate_binary_structure(2,2))
    markers = ndimage.label(local_maxi, structure=generate_binary_structure(2,2))[0]

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


    labels = watershed(-distance, markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0

    plt.imshow(labels)
    plt.title('raw wshed')
    plt.show()

    # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed1.tif')
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




    plt.imshow(markers)
    plt.title('markers')
    plt.show()

    afine_tf = transfo.AffineTransform(translation=(2, 2))
    shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                             order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
    # plt.imshow(shifted_markers)
    # plt.show()

    labels = watershed(-distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed2.tif')

    afine_tf = transfo.AffineTransform(translation=(-2, -2))
    shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                   order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
    # plt.imshow(shifted_markers)
    # plt.show()

    labels = watershed(-distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0

    plt.imshow(labels)
    plt.title('raw wshed')
    plt.show()

    # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed3.tif')

    afine_tf = transfo.AffineTransform(translation=(-2, 2))
    shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                   order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
    # plt.imshow(shifted_markers)
    # plt.show()

    labels = watershed(-distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0

    plt.imshow(labels)
    plt.title('raw wshed')
    plt.show()

    # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed4.tif')


    afine_tf = transfo.AffineTransform(translation=(2, -2))
    shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                   order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
    # plt.imshow(shifted_markers)
    # plt.show()

    labels = watershed(-distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0

    plt.imshow(labels)
    plt.title('raw wshed')
    plt.show()

    # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed5.tif')

    afine_tf = transfo.AffineTransform(translation=(0, -2))
    shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                   order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
    # plt.imshow(shifted_markers)
    # plt.show()

    labels = watershed(-distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0

    plt.imshow(labels)
    plt.title('raw wshed')
    plt.show()

    # trash this that is almost perfect just need score the remaining bonds c'est parfait peut etre une combination basique de 3 ou 4 trucs ferait un job parfait en fait --> à tester -->
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed6.tif')

    afine_tf = transfo.AffineTransform(translation=(-2, 0))
    shifted_markers = transfo.warp(markers, inverse_map=afine_tf,
                                   order=0, preserve_range=True)  # removed 2 cause not yet properly implemented
    # plt.imshow(shifted_markers)
    # plt.show()

    labels = watershed(-distance, shifted_markers, watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0

    plt.imshow(labels)
    plt.title('raw wshed')
    plt.show()

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
    distance = distance_transform_edt(skel) # en fait c'est vraiment presque parfait --> à tester
    # plt.imshow(distance)
    # plt.show()
    # TODO could randomly move seeds according
    labels = watershed(distance, markers,   watershed_line=True)  # --> maybe implement that too
    # labels = watershed(-image, markers, watershed_line=True)  # --> maybe implement that too
    #
    # plt.imshow(labels)
    # plt.title('test')
    # plt.show()
    labels[labels != 0] = 1  # remove all seeds
    labels[labels == 0] = 255  # set wshed values to 255
    labels[labels == 1] = 0  # set all other cell content to 0
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed8.tif')

    distance = distance_transform_edt(img)  # en fait c'est vraiment presque parfait --> à tester

    # print(markers)
    # print(type(markers))
    # print(markers.shape)
    # print(local_maxi.shape)
    # plt.imshow(markers)
    # plt.show()
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
    Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/wshed9.tif')
    Img(skel.astype(np.uint8)*255, dimensions='hw').save('/home/aigouy/Bureau/trash/trash4/skel.tif')

    # seems ok maybe max it to skel



    # can I fix/keep seeds instead of bonds --> maybe that is simpler --> use overlap to indetify seed and keep the smallest --> not a good idea in fact
    # ok if i lose a few cells maybe
    # sinon scorer les differing bonds et voir lesquels garder peut etre aussi essayer de restaurer les long missing bonds coute que coute

    # end trash this

    # Img(labels.astype(np.uint8), dimensions='hw').save('D:/test_mask.png')

    if __VISUAL_DEBUG:
        plt.imshow(labels)
        plt.show()

        # plt.imshow(image)
        # plt.show()

    if __DEBUG:
        # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
        Img(labels, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/rewatershed.tif')

    # correct watershed to keep best only
    final_watershed_mask = skel.copy()
    final_watershed_mask[cells_to_resegment!=0]=labels[cells_to_resegment!=0]
    final_watershed_mask[final_watershed_mask!=0]=255

    if __DEBUG:
        # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
        Img(final_watershed_mask.astype(np.uint8), dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/rewatershed_fixed_secure.tif')


    # maybe also further remove tiny cells from the stuff --> are there tiny cells an artifact of skel --> if so blast them
    # TODO
    # alternatively always take biggest cell of the two ???
    # or remove tiny cells
    # also if new contact not connected to existing vertex it can be removed
    # --> loop over vertices

    # get differing bonds and get their tips --> if not connected to an existing stuff then remove them
    differing_bonds = np.logical_xor(final_watershed_mask, skel)
    # plt.imshow(differing_bonds)
    # plt.show()

    if __DEBUG:
        # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
        Img(differing_bonds.astype(np.uint8)*255, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/differing_bonds.tif')

    import os
    path = os.path.abspath('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/')
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
                val = labeled_differing_bonds[coordinates_y[i]-2:coordinates_y[i]+3, coordinates_x[i]-2:coordinates_x[i]+3].flatten()
            except:
                val = labeled_differing_bonds[coordinates_y[i]-1:coordinates_y[i]+2, coordinates_x[i]-1:coordinates_x[i]+2].flatten()
            for val in val[val!=0]:
                differing_bonds_really_connected.append(val)
        except:
            pass

    for region in regionprops(labeled_differing_bonds):
        if region.label in differing_bonds_really_connected:
            for coordinates in region.coords:
                differing_bonds[coordinates[0], coordinates[1]] = 0

    if __DEBUG:
        # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
        Img(differing_bonds.astype(np.uint8)*255, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/differing_bonds2.tif')

    final_watershed_mask = final_watershed_mask-differing_bonds.astype(np.uint8)*255


    if __DEBUG:
        # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
        Img(final_watershed_mask.astype(np.uint8), dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/rewatershed_fixed_secure2.tif')

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
        final_watershed_mask = ndimage.grey_dilation(final_watershed_mask, footprint=s) # required to fix tiny blurbs but may cause overseg too

        if __VISUAL_DEBUG:
            plt.imshow(labels)
            plt.title('skel')
            plt.show()

            plt.imshow(final_watershed_mask)
            plt.title('final')
            plt.show()



        if __DEBUG:
            # Img(cells_to_resegment.astype(np.uint8) + mask.astype(np.uint8) * 2, dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/cells_to_reshed.tif')
            Img(final_watershed_mask.astype(np.uint8), dimensions='hw').save('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/rewatershed_fixed_secure3.tif')

        # fini pr now --> just try on the sample of the other guy on vertebrate cells

    return final_watershed_mask