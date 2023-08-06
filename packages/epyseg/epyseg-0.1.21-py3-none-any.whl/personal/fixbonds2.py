# TODO check using excentricity or compactness or alike that it is really a line and not a cell contour maybe a stretch nematic would help

# vraiment pas top qd tt un contour cellulaire est montré
# peut etre meme que l'autre est mieux

# des fois ça marche mais pas tt le temps --> est-ce valable essayer le code qui detecte les long bonds et essaie de les connecter à tout prix en utilisant la coordonnée de la droite et dans la meme cellul que le bond --> en utilisant un flood de ttes les cellules --> peut se propager que ds la meme couleur --> evite les pbs...
# à faire

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

DEBUG = False
VISUAL_DEBUG = False

# nb the rescue of bonds is now excellent but there has to be a bug a bit after

class FixBonds:

    def __init__(self, img_with_holes_binarized, nb_dilations=0):
        self.img_with_holes_binarized = img_with_holes_binarized
        self.nb_dilations = nb_dilations

    def process(self):
        original = self.img_with_holes_binarized.copy()
        output = np.zeros_like(original)

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
        thresholded = original  # [..., 0]

        # rebinarise image
        thresholded[thresholded > 0.3] = 1
        thresholded[thresholded <= 0.3] = 0

        # inv_bin = Img.invert(thresholded)  # do I need that --> maybe

        # take wshed and blast using it and see which bonds remain
        # need apply a dilation to blast using the mask

        s = ndimage.generate_binary_structure(2, 1)

        #
        # if VISUAL_DEBUG:
        #     plt.imshow(inv_bin, cmap='gray')
        #     plt.show()
        #
        # labels_gt = measure.label(inv_bin, connectivity=1, background=0)  # FOUR_CONNECTED
        #
        # # redo wshed on this binarized image
        # labels = watershed(original, markers=labels_gt,
        #                    watershed_line=True)  # [..., 0] # would be better do do real watershed on orig --> maybe less bugs by the way
        #
        # labels[labels != 0] = 1  # remove all seeds
        # labels[labels == 0] = 255  # set wshed values to 255
        # labels[labels == 1] = 0  # set all other cell content to 0

        # if VISUAL_DEBUG:
        #     plt.imshow(labels, cmap='gray')
        #     plt.show()
        #
        # if DEBUG:
        #     Img(labels, dimensions='hw').save(os.path.join(path, 'labels.tif'))  # not bad

        comparison = ndimage.grey_dilation(self.img_with_holes_wshed, footprint=s)
        # detect bonds that differ between the two --> these actually are the bonds I want to get
        # not_img = np.logical_not(self.img_with_holes_wshed == labels, self.img_with_holes_wshed != labels)
        not_img = original.copy()
        not_img[comparison == 255] = 0

        plt.imshow(not_img, cmap='gray')
        plt.show()

        # now need segment it get line coords and finc closest pixel on the path --> TODO
        labels_gt = measure.label(not_img, connectivity=2, background=0)
        props = regionprops(labels_gt)  # , intensity_image=self.img_with_holes

        # remove bonds get their line

        # def find_ellipses(img):  # img is grayscale image of what I want to fit
        #     ret, thresh = cv2.threshold(img, 127, 255, 0)
        #     _, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        #
        #     if len(contours) != 0:
        #         for cont in contours:
        #             if len(cont) < 5:
        #                 break
        #             elps = cv2.fitEllipse(cont)
        #             return elps  # only returns one ellipse for now
        #     return None
        # try fit ellipse or create my own version of it

        # line coords
        # from numpy import ones, vstack
        # from numpy.linalg import lstsq
        # points = [(1, 5), (3, 4)]
        # x_coords, y_coords = zip(*points)
        # A = vstack([x_coords, ones(len(x_coords))]).T
        # m, c = lstsq(A, y_coords)[0]
        # print("Line Solution is y = {m}x + {c}".format(m=m, c=c))

        # maybe the last one is what I want ???
        # import numpy as np
        # import matplotlib.pyplot as plt
        #
        # # Define the known points
        # x = [100, 400]
        # y = [240, 265]
        #
        # # Calculate the coefficients. This line answers the initial question.
        # coefficients = np.polyfit(x, y, 1)
        #
        # # Print the findings
        # print
        # 'a =', coefficients[0]
        # print
        # 'b =', coefficients[1]
        #
        # # Let's compute the values of the line...
        # polynomial = np.poly1d(coefficients)
        # x_axis = np.linspace(0, 500, 100)
        # y_axis = polynomial(x_axis)
        #
        # # ...and plot the points and the line
        # plt.plot(x_axis, y_axis)
        # plt.plot(x[0], y[0], 'go')
        # plt.plot(x[1], y[1], 'go')
        # plt.grid('on')
        # plt.show()

        # Python3 Implementation to find the line passing
        # through two points

        # This pair is used to store the X and Y
        # coordinate of a point respectively
        # define pdd pair<double, double>

        # https://www.geeksforgeeks.org/program-find-line-passing-2-points/
        # # Function to find the line given two points
        # def lineFromPoints(P, Q):
        #
        #     a = Q[1] - P[1]
        #     b = P[0] - Q[0]
        #     c = a * (P[0]) + b * (P[1])
        #
        #     if (b < 0):
        #         print("The line passing through points P and Q is:",
        #               a, "x ", b, "y = ", c, "\n")
        #     else:
        #         print("The line passing through points P and Q is: ",
        #               a, "x + ", b, "y = ", c, "\n")
        #
        #         # Driver code
        #
        # if __name__ == '__main__':
        #     P = [3, 2]
        #     Q = [2, 6]
        #     lineFromPoints(P, Q)

        # This code is contributed by ash264

        # check also line_equation.py

        # Eccentricity
        # orientation in regionprops

        output = np.zeros_like(not_img)

        for region in props:
            bd_length = region.area
            count = 0
            if bd_length < 6:
                for coordinates in region.coords:
                    not_img[coordinates[0], coordinates[1]] = 0
            else:
                # compute line coords
                coords = region.coords
                # print(coords.shape)
                # print(coords[:,0].shape)
                # print(coords [0])
                # print(self.estimate_coef(coords[:,0], coords[:,1]))
                a, b = self.estimate_coef(coords[:, 0], coords[:, 1])

                # try draw line from coords --> does that work now

                x = np.linspace(0, original.shape[-1], original.shape[-1])
                y = a * x + b

                print(x)
                print(y)

                for i in range(len(x)):
                    try:
                        output[int(y[i]), int(x[i])] = 255

                    except:
                        pass

        output[not_img!=0]=255
        plt.imshow(output, cmap='gray')
        plt.show()

        plt.imshow(not_img, cmap='gray')
        plt.show()




        # for coordinates in region.coords:
        #     if comparison2[coordinates[0], coordinates[1]] == 1:
        #         count += 1
        # # print("tetst",count, bd_length, count / bd_length)
        # if VISUAL_DEBUG:
        #     if 0.5 < count / bd_length <= 1.0:
        #         print(region.label, bd_length, count, count / bd_length, count / bd_length > 0.5)
        # if 0.5 < count / bd_length <= 1.0:
        #     for coordinates in region.coords:
        #         # original[coordinates[0], coordinates[1]] = 255
        #         output[coordinates[0], coordinates[1]] = 255
        #     np.logical_not(comparison == labels, comparison != labels)
        # # not_img = not_img[not_img==True and labels==255]
        # not_img[labels != 255] = 0
        # # big bug cause images are shifted should I shrink back after open to get back to original size or do watershed on original
        # # not_img = np.logical_xor(self.img_with_holes_wshed != labels, self.img_with_holes_wshed == self.img_with_holes_binarized)
        # # not_img = ~not_img
        # not_img = not_img / not_img.max()
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(not_img, cmap='gray')
        #     plt.show()
        # should I skeletonize it --> there is a bug

        # tester et finaliser le truc

        # np.logical_and(x==y, x!=y) --> test if that works --> me
        # np.logical_and(x>1, x<4)
        # np.logical_or np.logical_xor np.logical_not

        # en fait faire uh logical not --> TODO

        # ça a l'air de marcher pas mal --> a tester qd meme
        # if DEBUG:
        #     Img(not_img, dimensions='hw').save(os.path.join(path,
        #                                                     'bonds_rescued.tif'))  # not bad --> it seems to work so realy keep it like that there is a bug after that hinders the efficiency of the code though
        #
        # # just need label all the bonds and count how many white pixels there are in the original image to see if they deserve be labeled or not
        # # should I exclude border cells ???
        #
        # labels_gt = measure.label(not_img, connectivity=2, background=0)  # FOUR_CONNECTED
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(labels_gt, cmap='gray')
        #     plt.show()
        #
        # if DEBUG:
        #     Img(labels_gt, dimensions='hw').save(os.path.join(path, 'labels_gt0.tif'))  # not bad
        #
        # # then loop over those bonds and see whether they need be rescued or not --> i.e. was the majority of the bond already present in the previous stuff
        # # --> give it a try
        #
        # props = regionprops(labels_gt)  # , intensity_image=self.img_with_holes
        #
        # comparison2 = original.copy()
        # comparison2[comparison2 > 0.3] = 1
        # comparison2[comparison2 <= 0.3] = 0
        # comparison2 = ndimage.grey_dilation(comparison2, footprint=s)
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(comparison2, cmap='gray')
        #     plt.show()
        #
        # if DEBUG:
        #     Img(comparison2, dimensions='hw').save(os.path.join(path, 'comparison2.tif'))  # not bad
        #
        # # faudrait faire ça plusieurs fois ??? ou pas --> check --> probleme risque de creer de la surseg
        # # print("2", comparison2.min(), comparison2.max())
        # for region in props:
        #     bd_length = region.area
        #     count = 0
        #     if bd_length < 5:
        #         continue
        #     for coordinates in region.coords:
        #         if comparison2[coordinates[0], coordinates[1]] == 1:
        #             count += 1
        #     # print("tetst",count, bd_length, count / bd_length)
        #     if VISUAL_DEBUG:
        #         if 0.5 < count / bd_length <= 1.0:
        #             print(region.label, bd_length, count, count / bd_length, count / bd_length > 0.5)
        #     if 0.5 < count / bd_length <= 1.0:
        #         for coordinates in region.coords:
        #             # original[coordinates[0], coordinates[1]] = 255
        #             output[coordinates[0], coordinates[1]] = 255
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(output, cmap='gray')
        #     plt.show()
        #
        # if DEBUG:
        #     Img(output, dimensions='hw').save(os.path.join(path, 'output.tif'))  # not bad
        #
        # # all seems ok till here
        #
        # # pas mal mais tester sur un vrai exemple maintenant pr voir si ça marche puis connecter le truc si modele preentraine
        # # voir comment faire idealement permettre un preprocess
        #
        # # vraiment pas mal ce truc --> voir comment faire en fait
        #
        # # est ce vraiment un pb de blaster les small cells car sont la plupart du temps bonnes de tte façon
        # # voir ce que je peux faire de mieux
        # # surtout pour supprimer les false bonds
        #
        # # pas mal en fait --> voir si j'ai des astuces
        # # peut etre faire un blast des bonds complets existants ? oui mais pas si simple --> comment faire
        #
        # # couper l'image en new bonds une fois le tout terminé et les scorer
        #
        # # reflechir rapido comment faire ça...
        #
        # # faudrait en fait scorer chaque bond par rapport à l'orig et si pas assez de % alors remove
        #
        # # split cut image or maybe just check new bonds
        #
        # # resegmenter en wshed cette image puis cutter ses bonds puis supprimer les bonds qui n'ont pas assez de px une fois cutté
        #
        # # pas trop dur je pense
        #
        # # do a dilat and apply onto orig
        # tmp = ndimage.grey_dilation(output, footprint=s)
        #
        # final_comparison = original.copy()
        #
        # original[tmp == 255] = 255
        # del tmp
        #
        # # tester ça
        #
        # final_seeds = label(Img.invert(original), connectivity=1, background=0)
        #
        # # from the seeds remove things below x pixels
        # for region in regionprops(final_seeds):
        #     cell_area = region.area
        #     if cell_area <= 16:
        #         # remove small seeds
        #         for coordinates in region.coords:
        #             original[coordinates[0], coordinates[1]] = 255
        #             final_seeds[coordinates[0], coordinates[1]] = 0
        #
        # final_wshed = watershed(original, markers=final_seeds, watershed_line=True)
        #
        # final_wshed[final_wshed != 0] = 1  # remove all seeds
        # final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        # final_wshed[final_wshed == 1] = 0  # set all other cell content to
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(final_wshed, cmap='gray')
        #     plt.show()
        #
        # if DEBUG:
        #     Img(final_wshed, dimensions='hw').save(os.path.join(path, 'final_wshed.tif'))
        # # seems to work now need to cut every bond and compare it to original
        #
        # # bond scoring does not work well yet --> deactivate for now
        # kernel = np.ones((3, 3))
        # mask = scipy.signal.convolve2d(final_wshed, kernel, mode='same', fillvalue=1)
        #
        # # specifically detect vertices here too to remove false bonds again
        # mask2 = scipy.signal.convolve2d(output, kernel, mode='same', fillvalue=1)
        #
        # # mask[mask<1020] = 0
        # # mask[mask>=1020] = 255
        #
        # # if VISUAL_DEBUG:
        # #     plt.imshow(mask)
        # #     plt.show()
        # #
        # # if DEBUG:
        # #     Img(result, dimensions='hw').save(os.path.join(path, 'vertices_test.tif'))
        #
        # result = np.zeros_like(mask)
        # result[np.logical_and(mask >= 1020, output == 255)] = 255
        # result[np.logical_and(mask2 >= 1020, output == 255)] = 255
        # del mask2
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(result)
        #     plt.show()
        #
        # if DEBUG:
        #     Img(result, dimensions='hw').save(os.path.join(path, 'vertices_test.tif'))
        #
        # # dirty vertex detection but maybe there is hope
        #
        # bds = output.astype(np.uint8) - result.astype(np.uint8)
        #
        # # get regions and count nb of white pixels in this region and if too low --> blast it...
        # bonds = label(bds, connectivity=2, background=0)
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(bonds)
        #     plt.show()
        #
        # if DEBUG:
        #     Img(bonds, dimensions='hw').save(os.path.join(path, 'bonds.tif'))
        #
        # # all is ok now --> just need one last step to do that and I'll be forever done !!!
        # # count for every bond wether it should be kept or not --> i.e. if it has enough white pixels below it
        #
        # # pb I guess I am scoring all the bonds and not just the ones I just added --> really not a good idea...
        # props = regionprops(bonds)  # , intensity_image=self.img_with_holes
        #
        # # faudrait faire ça plusieurs fois ??? ou pas --> check --> probleme risque de creer de la surseg
        # # print("2", self.img_with_holes.min(), self.img_with_holes.max())
        # for region in props:
        #     bd_length = region.area
        #     count = 0
        #     for coordinates in region.coords:
        #         if final_comparison[coordinates[0], coordinates[1]] == 255:
        #             count += 1
        #     if VISUAL_DEBUG:
        #         if count / bd_length < 0.3:
        #             print(region.label, bd_length, count, count / bd_length, count / bd_length < 0.3)
        #
        #     # if region.label == 137 or region.label == 138:
        #     #     print(region.label, bd_length, count, count / bd_length, count / bd_length < 0.3)
        #     if count / bd_length < 0.3:
        #         for coordinates in region.coords:
        #             output[coordinates[0], coordinates[1]] = 0
        #             # output[coordinates[0], coordinates[1]] = 0
        #     # if count / bd_length >= 0.5:
        #     #     for coordinates in region.coords:
        #     #         output[coordinates[0], coordinates[1]] = 255
        #
        # if VISUAL_DEBUG:
        #     plt.imshow(output, cmap='gray')
        #     plt.show()
        #
        # # do a copy of the image at the very beginning ... then will be done
        # # tt a l'air mega top ok --> keep it like that and do several tests
        #
        # # nb there is a bug in the detection of vertices
        # # bug in detection of vertices --> creates some artificial seg of cells in some cases
        #
        # if DEBUG:
        #     Img(output, dimensions='hw').save(os.path.join(path, 'fixed_bonds_final.tif'))
        #
        # # pas mal --> faire une dilation de ça une fois et puis fini mais faire ça en recursif avec differents nb de dilation --> TODO
        # output = ndimage.grey_dilation(output, footprint=s)
        #
        # return output

    def estimate_coef(self, x, y):
        # number of observations/points
        n = np.size(x)

        # mean of x and y vector
        m_x, m_y = np.mean(x), np.mean(y)

        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y * x) - n * m_y * m_x
        SS_xx = np.sum(x * x) - n * m_x * m_x

        # calculating regression coefficients
        a = SS_xy / SS_xx
        b = m_y - a * m_x

        return (a, b)

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
    path = '/D/Sample_images/sample_images_epiguy_pyta/egg_chamber_olivier_ArpI005_3 concat st4-TASrBcEcPNG/predict'  # this is the path to get
    # path = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729'  # this is the path to get
    # path = '/home/aigouy/Bureau/test_dye/predict_linknet-vgg16-sigmoid-ep0191-l0.144317_default_params'  # this is the path to get
    # path = '/home/aigouy/Bureau/test_dye/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729_default_refine_seg'  # this is the path to get
    # path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317'  # this is the path to get

    # img_with_holes = Img(os.path.join(path, '20190924_ecadGFP_400nM20E_000.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX
    img_with_holes = Img(os.path.join(path, '31.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX
    # img_with_holes = Img(os.path.join(path, 'StackFocused_Endocad-GFP(6-12-13)#19_016.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX
    # img_with_holes = Img(os.path.join(path, '5.tif'))[..., 0]  # small bug due to cells with just 1 px --> to FIX

    img_with_holes[img_with_holes > 0.3] = 255
    img_with_holes[img_with_holes <= 0.3] = 0

    # parfait --> it all seems to work perfectly actually now and better than CP

    # TODO virer les micro erreurs...
    # processed = FixBonds(img_with_holes, nb_dilations=1).process()

    fixer = FixBonds(img_with_holes, nb_dilations=1)

    fixed_bonds = fixer.process()
    # fixed_bonds = fixer.serial(min=1, max=17, increment=3) # ok
    plt.imshow(fixed_bonds, cmap='gray')
    plt.show()

    Img(fixed_bonds, dimensions='hw').save(os.path.join(path, 'fixed_bonds.tif'))
    print(os.path.join(path, 'fixed_bonds.tif'))

    # final_mask = fixer.finalize(fixed_bonds)
    # plt.imshow(final_mask, cmap='gray')
    # plt.show()
    # pas tjrs mieux --> le mettre comme une option pr certains tissus

    # Img(final_mask, dimensions='hw').save(os.path.join(path, 'final_fix.tif'))
    # print(os.path.join(path, 'final_fix.tif'))

    # TODO maybe also detect vertices on fixed bonds and delete if associated to  black ---> last ultimate control

    # voir le reultat sur une aile --> à tester
    # apporte pas tjrs grand chose faudrait faire un max en fait et aussi plusieurs dilats
    # TODO tester sur vraies images
