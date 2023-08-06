# des fois ça marche mais pas tt le temps --> est-ce valable essayer le code qui detecte les long bonds et essaie de les connecter à tout prix en utilisant la coordonnée de la droite et dans la meme cellul que le bond --> en utilisant un flood de ttes les cellules --> peut se propager que ds la meme couleur --> evite les pbs...
# à faire

# TODO c'est vraiment mieux mais certains bonds qui sont tres long en WT ont quasiment dipsarus car pas connectes ici malgre les dilats --> faudrait les connecter en les detectant en conparant avec le resultat du watershed et fitter une ellipse pr recup la ligne et essayer de la connecter au bond le plus proche mais francement pas mal

# TODO just make it save bextra bonds and orverlay it on top of original --> don't keep the whole stuff and do several rounds so that it can better handle cells with different sizes --> TODO
# now this sounds like a very good idea... and may be very useful in the end now


# TODO SEGMENTER ET TESTER SUR UNE VRAIE IMAGE D'OLIVIER --> à faire pr un test
# pas une mauvaise idée du tout

# try convert the cellpose model to tensorflow to see if that works
# https://github.com/microsoft/MMdnn


# sudo update-alternatives --config python

# pb some bonds are rescued cause come along with others, pb is that --> can be fixed after by counting nb of real pixels belonging to bonds as a second control after having cut all the bonds --> should be easy
# but maybe a good idea still or change some things in the code to avoid this last step --> TODO

# vraiment pas mal et assez rapides peut etre demander le nb de pass max des dilations
# refaire un controle à la fin pr enlever les bonds qui ne devraient pas etre la --> dont aucun px n'est associé à qq chose sur image originelle, peuyt etre besoin de refaire un wshed dessus par contre


# this is just a test to try to connect bonds
# prendre image originelle
# faire des dilation voir comment empecher les cellules de se boucher par dilation
# puis je faire la dilation sur chaque centoid existant pr empecher de tt boucher
# comparer la longeur du bond sans dilation avec celle avec --> faire un and sur le MASK originel avant dilation et le wshed final apres plein de dilation
# en fait je vais pas utiliser ça pr des seeds mais plutot pr recuperer des bonds donc je m'en fout si je bouche des cellules --> oui en fait


# faire n dilation
# faire tourner un wshed sur la base des seeds de ces dilation
# checker les bonds de ces seeds

# faire un test sur des images

# maybe do several dilation then several watersheds then do an and of the watersheds --> if I do that will not all be 1 px wide --> pb ??? maybe or maybe not
# then try cut bonds and see

# essayer ça
from typing import re

from epyseg.img import Img
import numpy as np
from scipy import ndimage
from skimage.segmentation import watershed
from skimage.measure import regionprops
from skimage.measure import label
from skimage import measure
import os
import sys
from matplotlib import pyplot as plt
import scipy

# this is the default mask that may or may not have been binarized and has hole in it...
# maybe compare to watershed without any other hole in it... to get the bonds that have bee created and maybe do an and to see if I keep them or not
# pas bête en fait et si bcp de px sont blancs dans ce bond alor le garder...
# et peut etre le mettre avec une petite dilation pr permettre de récupérer le bond

# make it a class called FixBonds -->

# essayons
# voir comment rajouter ça dans la main pipeline...

DEBUG = False
VISUAL_DEBUG = False


# nb the rescue of bonds is now excellent but there has to be a bug a bit after

class FixBonds:

    def __init__(self, img_with_holes_binarized, nb_dilations=0):
        self.img_with_holes_binarized = img_with_holes_binarized
        self.nb_dilations = nb_dilations

    def process(self):
        # path = '/D/Sample_images/sample_images_epiguy_pyta/egg_chamber_olivier_ArpI005_3 concat st4-TASrBcEcPNG/predict'  # this is the path to get
        # can it also be done with the other style of images --> make it a class
        # path = 'D:/trained_models/mini_test_bonds/predict'  # this is the path to get

        # orig = Img('/D/Sample_images/sample_images_epiguy_pyta/test_detecting_incomplete_bonds/focused_Series012.png')
        # self.img_with_holes_binarized = Img('/D/Sample_images/sample_images_epiguy_pyta/test_detecting_incomplete_bonds/handCorrection_with_holes.png')

        # orig = Img(os.path.join(path, '30.tif'))[..., 0]

        original = self.img_with_holes_binarized.copy()
        output = np.zeros_like(original)

        # img2 = Img('/D/Sample_images/sample_images_PA/trash_test_mem/mini/focused_Series012/handCorrection.tif')

        # print(self.img_with_holes.min(), self.img_with_holes.max())

        # ça marche mais virer les petits blobs ???
        # print(not_img.max(), not_img.min())

        #
        # if True:
        #     sys.exit(0)

        # do dilation n times
        # self.img_with_holes[self.img_with_holes > 0.5] = 1
        # self.img_with_holes[self.img_with_holes <= 0.5] = 0
        if DEBUG:
            Img(original, dimensions='hw').save(os.path.join(path, 'original.tif'))  # not bad

        inv_bin = Img.invert(original)  # do I need that --> maybe
        labels_gt = measure.label(inv_bin, connectivity=1, background=0)  # FOUR_CONNECTED

        if VISUAL_DEBUG:
            plt.imshow(labels_gt, cmap='gray')
            plt.show()

        # default watershed mask with no filled holes
        self.img_with_holes_wshed = watershed(original, markers=labels_gt, watershed_line=True)  # [..., 0]

        self.img_with_holes_wshed[self.img_with_holes_wshed != 0] = 1  # remove all seeds
        self.img_with_holes_wshed[self.img_with_holes_wshed == 0] = 255  # set wshed values to 255
        self.img_with_holes_wshed[self.img_with_holes_wshed == 1] = 0  # set all other cell content to 0

        if VISUAL_DEBUG:
            plt.imshow(self.img_with_holes_wshed, cmap='gray')
            plt.show()
        # wshed on these dilation
        if DEBUG:
            Img(self.img_with_holes_wshed, dimensions='hw').save(
                os.path.join(path, 'img_with_holes_wshed.tif'))  # not bad

        # now we do a watershed on a dilated image to close holes
        bigger_points = original  # [..., 0]
        s = ndimage.generate_binary_structure(2, 1)
        for _ in range(self.nb_dilations):
            bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)
        # bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)
        # bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)
        # bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)
        # bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)
        # bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)
        # bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)
        # bigger_points = ndimage.grey_dilation(bigger_points, footprint=s)

        # rebinarise image
        bigger_points[bigger_points > 0.3] = 1
        bigger_points[bigger_points <= 0.3] = 0

        inv_bin = Img.invert(bigger_points)  # do I need that --> maybe

        if VISUAL_DEBUG:
            plt.imshow(inv_bin, cmap='gray')
            plt.show()

        labels_gt = measure.label(inv_bin, connectivity=1, background=0)  # FOUR_CONNECTED

        # redo wshed on this binarized image
        labels = watershed(original, markers=labels_gt,
                           watershed_line=True)  # [..., 0] # would be better do do real watershed on orig --> maybe less bugs by the way

        labels[labels != 0] = 1  # remove all seeds
        labels[labels == 0] = 255  # set wshed values to 255
        labels[labels == 1] = 0  # set all other cell content to 0

        if VISUAL_DEBUG:
            plt.imshow(labels, cmap='gray')
            plt.show()

        if DEBUG:
            Img(labels, dimensions='hw').save(os.path.join(path, 'labels.tif'))  # not bad

        comparison = ndimage.grey_dilation(self.img_with_holes_wshed, footprint=s)
        # detect bonds that differ between the two --> these actually are the bonds I want to get
        # not_img = np.logical_not(self.img_with_holes_wshed == labels, self.img_with_holes_wshed != labels)
        not_img = np.logical_not(comparison == labels, comparison != labels)
        # not_img = not_img[not_img==True and labels==255]
        not_img[labels != 255] = 0
        # big bug cause images are shifted should I shrink back after open to get back to original size or do watershed on original
        # not_img = np.logical_xor(self.img_with_holes_wshed != labels, self.img_with_holes_wshed == self.img_with_holes_binarized)
        # not_img = ~not_img
        not_img = not_img / not_img.max()

        if VISUAL_DEBUG:
            plt.imshow(not_img, cmap='gray')
            plt.show()
        # should I skeletonize it --> there is a bug

        # tester et finaliser le truc

        # np.logical_and(x==y, x!=y) --> test if that works --> me
        # np.logical_and(x>1, x<4)
        # np.logical_or np.logical_xor np.logical_not

        # en fait faire uh logical not --> TODO

        # ça a l'air de marcher pas mal --> a tester qd meme
        if DEBUG:
            Img(not_img, dimensions='hw').save(os.path.join(path,
                                                            'bonds_rescued.tif'))  # not bad --> it seems to work so realy keep it like that there is a bug after that hinders the efficiency of the code though

        # just need label all the bonds and count how many white pixels there are in the original image to see if they deserve be labeled or not
        # should I exclude border cells ???

        labels_gt = measure.label(not_img, connectivity=2, background=0)  # FOUR_CONNECTED

        if VISUAL_DEBUG:
            plt.imshow(labels_gt, cmap='gray')
            plt.show()

        if DEBUG:
            Img(labels_gt, dimensions='hw').save(os.path.join(path, 'labels_gt0.tif'))  # not bad

        # then loop over those bonds and see whether they need be rescued or not --> i.e. was the majority of the bond already present in the previous stuff
        # --> give it a try

        props = regionprops(labels_gt)  # , intensity_image=self.img_with_holes

        comparison2 = original.copy()
        comparison2[comparison2 > 0.3] = 1
        comparison2[comparison2 <= 0.3] = 0
        comparison2 = ndimage.grey_dilation(comparison2, footprint=s)

        if VISUAL_DEBUG:
            plt.imshow(comparison2, cmap='gray')
            plt.show()

        if DEBUG:
            Img(comparison2, dimensions='hw').save(os.path.join(path, 'comparison2.tif'))  # not bad

        # faudrait faire ça plusieurs fois ??? ou pas --> check --> probleme risque de creer de la surseg
        # print("2", comparison2.min(), comparison2.max())
        for region in props:
            bd_length = region.area
            count = 0
            if bd_length < 5:
                continue
            for coordinates in region.coords:
                if comparison2[coordinates[0], coordinates[1]] == 1:
                    count += 1
            # print("tetst",count, bd_length, count / bd_length)
            if VISUAL_DEBUG:
                if 0.5 < count / bd_length <= 1.0:
                    print(region.label, bd_length, count, count / bd_length, count / bd_length > 0.5)
            if 0.5 < count / bd_length <= 1.0:
                for coordinates in region.coords:
                    # original[coordinates[0], coordinates[1]] = 255
                    output[coordinates[0], coordinates[1]] = 255

        if VISUAL_DEBUG:
            plt.imshow(output, cmap='gray')
            plt.show()

        if DEBUG:
            Img(output, dimensions='hw').save(os.path.join(path, 'output.tif'))  # not bad

        # all seems ok till here

        # pas mal mais tester sur un vrai exemple maintenant pr voir si ça marche puis connecter le truc si modele preentraine
        # voir comment faire idealement permettre un preprocess

        # vraiment pas mal ce truc --> voir comment faire en fait

        # est ce vraiment un pb de blaster les small cells car sont la plupart du temps bonnes de tte façon
        # voir ce que je peux faire de mieux
        # surtout pour supprimer les false bonds

        # pas mal en fait --> voir si j'ai des astuces
        # peut etre faire un blast des bonds complets existants ? oui mais pas si simple --> comment faire

        # couper l'image en new bonds une fois le tout terminé et les scorer

        # reflechir rapido comment faire ça...

        # faudrait en fait scorer chaque bond par rapport à l'orig et si pas assez de % alors remove

        # split cut image or maybe just check new bonds

        # resegmenter en wshed cette image puis cutter ses bonds puis supprimer les bonds qui n'ont pas assez de px une fois cutté

        # pas trop dur je pense

        # do a dilat and apply onto orig
        tmp = ndimage.grey_dilation(output, footprint=s)

        final_comparison = original.copy()

        original[tmp == 255] = 255
        del tmp

        # tester ça

        final_seeds = label(Img.invert(original), connectivity=1, background=0)

        # from the seeds remove things below x pixels
        for region in regionprops(final_seeds):
            cell_area = region.area
            if cell_area <= 16:
                # remove small seeds
                for coordinates in region.coords:
                    original[coordinates[0], coordinates[1]] = 255
                    final_seeds[coordinates[0], coordinates[1]] = 0

        final_wshed = watershed(original, markers=final_seeds, watershed_line=True)

        final_wshed[final_wshed != 0] = 1  # remove all seeds
        final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        final_wshed[final_wshed == 1] = 0  # set all other cell content to

        if VISUAL_DEBUG:
            plt.imshow(final_wshed, cmap='gray')
            plt.show()

        if DEBUG:
            Img(final_wshed, dimensions='hw').save(os.path.join(path, 'final_wshed.tif'))
        # seems to work now need to cut every bond and compare it to original

        # bond scoring does not work well yet --> deactivate for now
        kernel = np.ones((3, 3))
        mask = scipy.signal.convolve2d(final_wshed, kernel, mode='same', fillvalue=1)

        # specifically detect vertices here too to remove false bonds again
        mask2 = scipy.signal.convolve2d(output, kernel, mode='same', fillvalue=1)

        # mask[mask<1020] = 0
        # mask[mask>=1020] = 255

        # if VISUAL_DEBUG:
        #     plt.imshow(mask)
        #     plt.show()
        #
        # if DEBUG:
        #     Img(result, dimensions='hw').save(os.path.join(path, 'vertices_test.tif'))

        result = np.zeros_like(mask)
        result[np.logical_and(mask >= 1020, output == 255)] = 255
        result[np.logical_and(mask2 >= 1020, output == 255)] = 255
        del mask2

        if VISUAL_DEBUG:
            plt.imshow(result)
            plt.show()

        if DEBUG:
            Img(result, dimensions='hw').save(os.path.join(path, 'vertices_test.tif'))

        # dirty vertex detection but maybe there is hope

        bds = output.astype(np.uint8) - result.astype(np.uint8)

        # get regions and count nb of white pixels in this region and if too low --> blast it...
        bonds = label(bds, connectivity=2, background=0)

        if VISUAL_DEBUG:
            plt.imshow(bonds)
            plt.show()

        if DEBUG:
            Img(bonds, dimensions='hw').save(os.path.join(path, 'bonds.tif'))

        # all is ok now --> just need one last step to do that and I'll be forever done !!!
        # count for every bond wether it should be kept or not --> i.e. if it has enough white pixels below it

        # pb I guess I am scoring all the bonds and not just the ones I just added --> really not a good idea...
        props = regionprops(bonds)  # , intensity_image=self.img_with_holes

        # faudrait faire ça plusieurs fois ??? ou pas --> check --> probleme risque de creer de la surseg
        # print("2", self.img_with_holes.min(), self.img_with_holes.max())
        for region in props:
            bd_length = region.area
            count = 0
            for coordinates in region.coords:
                if final_comparison[coordinates[0], coordinates[1]] == 255:
                    count += 1
            if VISUAL_DEBUG:
                if count / bd_length < 0.3:
                    print(region.label, bd_length, count, count / bd_length, count / bd_length < 0.3)

            # if region.label == 137 or region.label == 138:
            #     print(region.label, bd_length, count, count / bd_length, count / bd_length < 0.3)
            if count / bd_length < 0.3:
                for coordinates in region.coords:
                    output[coordinates[0], coordinates[1]] = 0
                    # output[coordinates[0], coordinates[1]] = 0
            # if count / bd_length >= 0.5:
            #     for coordinates in region.coords:
            #         output[coordinates[0], coordinates[1]] = 255

        if VISUAL_DEBUG:
            plt.imshow(output, cmap='gray')
            plt.show()

        # do a copy of the image at the very beginning ... then will be done
        # tt a l'air mega top ok --> keep it like that and do several tests

        # nb there is a bug in the detection of vertices
        # bug in detection of vertices --> creates some artificial seg of cells in some cases

        if DEBUG:
            Img(output, dimensions='hw').save(os.path.join(path, 'fixed_bonds_final.tif'))

        # pas mal --> faire une dilation de ça une fois et puis fini mais faire ça en recursif avec differents nb de dilation --> TODO
        output = ndimage.grey_dilation(output, footprint=s)

        return output

    def serial(self, min=1, max=8, increment=3):
        # do max proj
        max_proj = None
        for dilat in range(min, max, increment):
            self.nb_dilations = dilat
            output = self.process()
            if max_proj is None:
                max_proj = output
            else:
                # do max proj
                max_proj[output == 255] = 255
            # print('dilat',dilat)
        return max_proj

    def finalize(self, max_proj):
        # try detect last vertices of bonds there and blast if not ok, keep the rest --> pb need do wshed again on mash --> sucks

        # # do wshed on mask ...
        # kernel = np.ones((3, 3))
        # mask = scipy.signal.convolve2d(max_proj, kernel, mode='same', fillvalue=1)
        #
        # result = np.zeros_like(mask)
        # result[np.logical_and(mask >= 1020, max_proj == 255)] = 255
        # del mask
        #
        # # dirty vertex detection but maybe there is hope
        #
        # bds = result.astype(np.uint8) - result.astype(np.uint8)
        # bonds = label(bds, connectivity=2, background=0)
        # props = regionprops(bonds)  # , intensity_image=self.img_with_holes
        #
        # plt.imshow(bonds, cmap='gray')
        # plt.show()
        #
        # # faudrait faire ça plusieurs fois ??? ou pas --> check --> probleme risque de creer de la surseg
        # # print("2", self.img_with_holes.min(), self.img_with_holes.max())
        # for region in props:
        #     bd_length = region.area
        #     count = 0
        #     for coordinates in region.coords:
        #         if self.img_with_holes_binarized[coordinates[0], coordinates[1]] == 255:
        #             count += 1
        #     if VISUAL_DEBUG:
        #         if count / bd_length < 0.3:
        #             print(region.label, bd_length, count, count / bd_length, count / bd_length < 0.3)
        #
        #     # if region.label == 137 or region.label == 138:
        #     #     print(region.label, bd_length, count, count / bd_length, count / bd_length < 0.3)
        #     if count / bd_length < 0.3:
        #         for coordinates in region.coords:
        #             max_proj[coordinates[0], coordinates[1]] = 0

        max_proj[self.img_with_holes_binarized == 255] = 255
        return max_proj


# TODO remove small cells from seeds --> 10 px or less --> remove

# 2pbs some bonds are not grown enough and some appeared bonds do not correspond to anything

# all of this is quite good, can it be used with wshed can I remove cells are some models now better with this than the vgg16 ??? --> really need to check that rapidly --> TODO
if __name__ == '__main__':
    # on dirait que ça perd plus de bonds que ça en gagne peut etre essayer de faire un ensemble avec cellpose pr voir quoi garder --> un jour tester ça --> à faire
    # TODO essayer sur la vraie image --> l'image de la moyenne et pas le reste pr voir si vraiment meilleur peut etre en remplacement du truc d'augmentation d'intensite --> a faire

    # no it's really not outsanding --> except for egg chamber --> offer it as an option only
    # only works well in rare cases with big cells and holes in boundaries ... --> can it be top for embryos ???

    # le finaliser et le mettre en option, peut aussi probablement etre compare
    # path = '/D/Sample_images/sample_images_epiguy_pyta/egg_chamber_olivier_ArpI005_3 concat st4-TASrBcEcPNG/predict'  # this is the path to get
    # path = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729'  # this is the path to get
    # path = '/home/aigouy/Bureau/test_dye/predict_linknet-vgg16-sigmoid-ep0191-l0.144317_default_params'  # this is the path to get
    # path = '/home/aigouy/Bureau/test_dye/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729_default_refine_seg'  # this is the path to get
    path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317'  # this is the path to get

    # img_with_holes = Img(os.path.join(path, '20190924_ecadGFP_400nM20E_000.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX
    # img_with_holes = Img(os.path.join(path, '31.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX
    # img_with_holes = Img(os.path.join(path, 'StackFocused_Endocad-GFP(6-12-13)#19_016.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX
    img_with_holes = Img(os.path.join(path, '5.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX

    img_with_holes[img_with_holes > 0.3] = 255
    img_with_holes[img_with_holes <= 0.3] = 0

    # parfait --> it all seems to work perfectly actually now and better than CP

    # TODO virer les micro erreurs...
    # processed = FixBonds(img_with_holes, nb_dilations=1).process()

    fixer = FixBonds(img_with_holes, nb_dilations=1)

    fixed_bonds = fixer.serial()
    # fixed_bonds = fixer.serial(min=1, max=17, increment=3) # ok
    plt.imshow(fixed_bonds, cmap='gray')
    plt.show()

    Img(fixed_bonds, dimensions='hw').save(os.path.join(path, 'fixed_bonds.tif'))
    print(os.path.join(path, 'fixed_bonds.tif'))

    final_mask = fixer.finalize(fixed_bonds)
    plt.imshow(final_mask, cmap='gray')
    plt.show()
    # pas tjrs mieux --> le mettre comme une option pr certains tissus

    Img(final_mask, dimensions='hw').save(os.path.join(path, 'final_fix.tif'))
    print(os.path.join(path, 'final_fix.tif'))

    # TODO maybe also detect vertices on fixed bonds and delete if associated to  black ---> last ultimate control



    # voir le reultat sur une aile --> à tester
    # apporte pas tjrs grand chose faudrait faire un max en fait et aussi plusieurs dilats
    # TODO tester sur vraies images
