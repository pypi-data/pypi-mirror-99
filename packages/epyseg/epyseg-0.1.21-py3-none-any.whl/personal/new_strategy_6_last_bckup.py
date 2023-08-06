# all is ok now --> just finalize all and basta
# then try develop new models
# TODO put superfuse as an option and also put those size thingies as options
# TODO try that maybe on all images to see if it can improve things
# seems fucking good
# TODO maybe do a local blaster based on relative area compared to neighbors

# otherwise that is quite ok --> try on the funny image I wanna use for the paper and compare

# really need to score because model is not always the best
# runtime 12.5 to 16 min pr 65 images not so bad...

# see how to parmaterize that
# offer this as a post process...


# launch the quantifications and compare to cellpose to see the overseg and the underseg

# TODO can also save raw data in the PREDICT folder --> a good deal and no need to specify a new folder (save raw data) and can be used both for TA mode and normal mode

# try https://scikit-image.org/docs/dev/auto_examples/edges/plot_active_contours.html
# how to remove false bonds --> really a pb with the model

# try augmentation with normal model old one

# TODO just try to score the interface locally in a cell vs the other and if twice less then blast it ... --> maybe that'll work
# blaster les bonds par les vertex faire une dilation du blast mais reblaster alors les vertex quantifier les bonds cell per cell and if bond > size and much weaker then balst it --> thanks to the dilat I can score it better for intensity
# just remove max one bond per cell --> assume anyway very little overseg
# should I try this ???
# maybe compare to reduced seed watersheding because may be very different result
# should I multiply the image by smthg to get it to work

# can I find a correction that finds and blasts outliers locally --> center on the cells of interest then look around for the avg area of the seeds and if much smaller then blast it but will remove dying cells unfortunately maybe not with a good cutoff


# could offer an option of filtering cells by area --> easy in post process
# how can I do that ???

# final alternative compare two similar models

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

import glob
import traceback
# from skimage.morphology import flood
# skimage.morphology.flood_fill(image, …[, …])
from scipy import ndimage
from scipy.signal import convolve2d
from skimage import morphology, img_as_uint, img_as_ubyte
from skimage.feature import peak_local_max, corner_harris, corner_peaks
# from skimage.util import invert
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
from natsort import natsorted  # sort strings as humans would do

# TODO add the function where I revive the tiny cells when too many are removed -->

# TODO make this more modular so that things can be done easily...

# TODO ask if in TA mode or if should be saved in another folder

# add parameters

# maybe need check that the extra pixels do touch the seeds otherwise skip ???? --> how can I do that

# binary closing is really crap so I really need to implement my own connector for stuff really close enough and if area is also big enough in order not to fill small elongated cells
# TODO add binary closing as first step to connect really close by points # scipy.ndimage.binary_closing https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.binary_closing.html
# nb for Bro43_avproj0000.tif --> the wshed mask does not work --> that is maybe why cellpose does not work

# try cellpose with 120 cell size parameter for the Bro43_avproj0000.png image cause is more in line with real cell size --> pb is that it detects 7.5 px diameter (the diam is shown below the image and for this image it should be 120...)


# TODO make it loop over lists and find scores and compare to


# TODO do this as a class to allow for testing
# TODO tester le truc et les differents parametres


# make a class out of this
class EPySegPostProcess():

   def __init__(self):

    # pb si fusion de
    DEBUG = False
    VISUAL_DEBUG = False
    TA_name = None  # 'handCorrection.tif'
    # default_output_folder = '/home/aigouy/Bureau/final_folder_scoring/epyseg_masks'  # will be used if TA name is None
    default_output_folder = '/home/aigouy/Bureau/final_folder_scoring/epyseg_tests'  # will be used if TA name is None
    # else provide output folder --> easier to do some scoring

    # seems not bad --> try it and see if improves further the seg
    # TODO --> do filtering outside --> a tester --> keep size low first
    # all seems to work now need define the post process parameters and to make a class out of it


    extra_filter_by_size = 'auto'  # None # 'auto' # any user defined size or auto... or None --> ignore
    # extra_filter_by_size = 7000  # pr aile mais differents parametres pr autres
    # extra_filter_by_size = 100 # pr images embryons
    # extra_filter_by_size = 4000 # pr xenopes zoom
    # pb --> si plusieurs seeds adjacentes sont perdues et qu'elles font 200 alors il faudrait les merger et donc mettre une seed au lieu de 3 par example --> le plus simple serit de merger les seeds adjacentes tant qu'elles sont inferieur à la taille minimale
    # peut etre stocker les seeds effacees et voir si il faut les merger ou pas
    # dans ce cas la taille moyenne des cellules serait en effet le parametre

    # extra_filter_by_size = 12
    # extra_filter_by_size = 'auto'
    factor_below_average_for_extra_filter_by_size = 2  # 1 for bro... # 2 for max... stretched cells
    # TODO maybe still remove very tiny ones
    cutoff_cell_fusion = 2  # None # 2 # if None or 0 --> ignore
    # if TA mode save as expected

    # maybe still remove super tiny cells --> just do not fuse them

    start = timer()


    # get the image invert what needs to be inverted

    # based on https://math.stackexchange.com/questions/2724537/finding-the-clear-spacing-distance-between-two-rectangles
    # if <= 0 --> rectangles are touching/overlapping
    def rect_distance(bbox1, bbox2):
        width1 = abs(bbox1[3] - bbox1[1])
        width2 = abs(bbox2[3] - bbox2[1])
        height1 = abs(bbox1[2] - bbox1[0])
        height2 = abs(bbox2[2] - bbox2[0])
        # print(abs((bbox1[1]+width1/2)-(bbox2[1]+width2/2))-(width1+width2)/2,abs((bbox1[0]+height1/2)-(bbox2[0]+height2/2))-(height1+height2)/2)
        return max(abs((bbox1[1] + width1 / 2) - (bbox2[1] + width2 / 2)) - (width1 + width2) / 2,
                   abs((bbox1[0] + height1 / 2) - (bbox2[0] + height2 / 2)) - (height1 + height2) / 2)


    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/'
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_shells/'
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict/'
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_light_divided_by_2/'
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_paper/'
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/' #1
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729_rot_HQ_only/' #2
    root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/'  # 3
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/' #3
    # root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317_rot_HQ_only/' #4


    # loop over all images of that
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
    # path = root_path + '11.tif'
    # path = root_path + '100708_png06.tif'
    # path = root_path + '122.tif'
    # path = root_path + 'Optimized_projection_018.tif'
    # path = root_path + 'Bro43_avproj0000.tif'
    # path = root_path + 'Bro43_avproj0001.tif'
    # path = root_path + '100708_png06.tif'
    # path = root_path + '5.tif'
    # path = root_path + 'MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_2c.tif'
    # path = root_path + 'MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_ok_2.tif'

    list_of_files = glob.glob(root_path + "*.png") + glob.glob(root_path + "*.jpg") + glob.glob(
        root_path + "*.jpeg") + glob.glob(
        root_path + "*.tif") + glob.glob(root_path + "*.tiff")+ glob.glob(root_path + "*.lsm")+ glob.glob(root_path + "*.czi") + glob.glob(root_path + "*.lif")
    list_of_files = natsorted(list_of_files)

    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/Bro43_avproj0000.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/122.tif'] # en effet par defaut ça perd plein de cellules --> faudrait implementer un mecanisme pr gerer ça mieux --> ce que j'ai propose de compter les cellules perdues et si perd trop --> remettre les cellules dans la region et repasser ne blaster que les autres
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/100708_png06.tif'] # en effet par defaut ça perd plein de cellules --> faudrait implementer un mecanisme pr gerer ça mieux --> ce que j'ai propose de compter les cellules perdues et si perd trop --> remettre les cellules dans la region et repasser ne blaster que les autres
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/100708_png07.tif'] # en effet par defaut ça perd plein de cellules --> faudrait implementer un mecanisme pr gerer ça mieux --> ce que j'ai propose de compter les cellules perdues et si perd trop --> remettre les cellules dans la region et repasser ne blaster que les autres
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/StackFocused_Endocad-GFP(6-12-13)#19_000.tif'] # en effet par defaut ça perd plein de cellules --> faudrait implementer un mecanisme pr gerer ça mieux --> ce que j'ai propose de compter les cellules perdues et si perd trop --> remettre les cellules dans la region et repasser ne blaster que les autres
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png06.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png07.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/AVG_070219.lif - Series0020000.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/Bro43_avproj0000.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/Bro43_avproj0001.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_000.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_016.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_032.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_048.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_064.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_080.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_096.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_112.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_256.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_400.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/stitched_00000_RGB.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/disc_0003_DCAD.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png07.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png07.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png07.tif',
    #                  '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png07.tif'] # en effet par defaut ça perd plein de cellules --> faudrait implementer un mecanisme pr gerer ça mieux --> ce que j'ai propose de compter les cellules perdues et si perd trop --> remettre les cellules dans la region et repasser ne blaster que les autres
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/StackFocused_Endocad-GFP(6-12-13)#19_400.tif'] # en effet par defaut ça perd plein de cellules --> faudrait implementer un mecanisme pr gerer ça mieux --> ce que j'ai propose de compter les cellules perdues et si perd trop --> remettre les cellules dans la region et repasser ne blaster que les autres

    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/StackFocused_Endocad-GFP(6-12-13)#19_400.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/122.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/Bro43_avproj0000.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/100708_png06.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/100708_png06.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_2c.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/12.tif']
    list_of_files = [
        '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_ok_2.tif']
    # list_of_files = ['/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_ok_2.tif']

    # creer ces images et voir si je gagne et demain implementer le mode auto

    # this new filter is excellent

    for path in list_of_files:

        # path = root_path + 'disc_0002_DCAD.tif'
        img_orig = Img(path)

        # DO A DILATION OF SEEDS THEN AN EROSION TO JOIN CLOSE BY SEEDS

        img_has_seeds = True
        if img_orig.has_c():
            img_seg = img_orig[..., 0].copy()

            seeds_1 = img_orig[..., img_orig.shape[-1] - 1]
            seeds_1 = Img.invert(seeds_1)
            # seeds_1[seeds_1 >= 0.5] = 255
            # seeds_1[seeds_1 < 0.5] = 0
            seeds_1[seeds_1 >= 0.2] = 255
            seeds_1[seeds_1 < 0.2] = 0

            s = ndimage.generate_binary_structure(2, 1)
            seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
            seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
            seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
            seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
            seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
            # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)
            # seeds_1 = ndimage.grey_erosion(seeds_1, footprint=s)

            # for debug
            if DEBUG:
                Img(seeds_1, dimensions='hw').save(
                    os.path.join(default_output_folder, 'extras', 'wshed_seeds.tif'))  # not bad

            lab_seeds = label(seeds_1.astype(np.uint8), connectivity=2, background=0)
            #
            for region in regionprops(lab_seeds):
                if region.area < 10:
                    for coordinates in region.coords:
                        lab_seeds[coordinates[0], coordinates[1]] = 0

            if DEBUG:
                Img(seeds_1, dimensions='hw').save(
                    os.path.join(default_output_folder, 'extras', 'wshed_seeds_deblobed.tif'))
            #
            # plt.imshow(lab_seeds)
            # plt.show()

            # should I deblob seeds too ???

            img_orig[..., 3] = Img.invert(img_orig[..., 3])
            img_orig[..., 4] = Img.invert(img_orig[..., 4])

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
        if DEBUG:
            Img(img_orig, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'avg.tif'))

        img_saturated = img_orig.copy()
        if img_has_seeds:

            img_saturated[img_saturated >= 0.5] = 255
            img_saturated[img_saturated < 0.5] = 0
            # img_saturated[img_saturated >= 0.5] = 255
            # img_saturated[img_saturated < 0.5] = 0
        else:
            img_saturated[img_saturated >= 0.3] = 255
            img_saturated[img_saturated < 0.3] = 0

        # for debug
        if DEBUG:
            Img(img_saturated, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'handCorrection.tif'))

        deblob = True
        if deblob:
            image_thresh = label(img_saturated, connectivity=2, background=0)

            # plt.imshow(image_thresh)
            # plt.show()

            # for debug
            if DEBUG:
                Img(image_thresh, dimensions='hw').save(
                    os.path.join(default_output_folder, 'extras', 'before_deblobed.tif'))
            # deblob
            min_size = 200
            for region in regionprops(image_thresh):
                # take regions with large enough areas
                if region.area < min_size:
                    for coordinates in region.coords:
                        image_thresh[coordinates[0], coordinates[1]] = 0

            image_thresh[image_thresh > 0] = 255
            img_saturated = image_thresh
            # for debug
            if DEBUG:
                Img(img_saturated, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'deblobed.tif'))
            del image_thresh

        # for debug
        if DEBUG:
            Img(img_saturated, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'deblobed_out.tif'))

        extra_dilations = True
        if extra_dilations:
            # do a dilation of 2 to close bonds
            s = ndimage.generate_binary_structure(2, 1)
            dilated = ndimage.grey_dilation(img_saturated, footprint=s)
            dilated = ndimage.grey_dilation(dilated, footprint=s)
            # Img(dilated, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'filled_one_px_holes.tif'))

            # other_seeds = label(invert(np.grey_dilation(dilated, footprint=s).astype(np.uint8)), connectivity=1, background=0)

            labs = label(Img.invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)
            for region in regionprops(labs):
                seeds = []

                # exclude tiny cells form dilation because they may end up completely closed
                if region.area >= 10 and region.area < 350:
                    for coordinates in region.coords:
                        dilated[coordinates[0], coordinates[1]] = 0
                    continue
                else:
                    # pb when big cells around cause connections are not done
                    # preserve cells at edges because they have to e naturally smaller because they are cut
                    # put a size criterion too
                    if region.area < 100 and (
                            region.bbox[0] <= 1 or region.bbox[1] <= 1 or region.bbox[2] >= labs.shape[-2] - 2 or
                            region.bbox[
                                3] >= \
                            labs.shape[-1] - 2):
                        # edge cell detected --> removing dilation
                        for coordinates in region.coords:
                            dilated[coordinates[0], coordinates[1]] = 0
                        continue

            # I still lose some cells at the boundaries...
            # for region in regionprops(other_seeds):
            #     if region.area >10:

            # now do the opposite
            # if we detect a cell big enough copy it

            # pb if there is a very tiny cell need rebuild it # or just ignore
            img_saturated = dilated
            # for debug
            if DEBUG:
                Img(img_saturated, dimensions='hw').save(
                    os.path.join(default_output_folder, 'extras', 'dilated_further.tif'))
            del dilated

        list_of_cells_to_dilate = []
        labs = label(Img.invert(img_saturated.astype(np.uint8)), connectivity=1, background=0)

        # c'est cette correction qui fixe bcp de choses mais recree aussi des choses qui n'existent pas... --> voir à quoi sont dus ces lignes blobs
        # faudrait redeblober
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

                    threshold_values = [80 / 255, 60 / 255, 40 / 255, 30 / 255,
                                        20 / 255,
                                        10 / 255]  # 160 / 255, 140 / 255, 120 / 255, 100 / 255,  1 / 255 , 2 / 255, , 5 / 255

                    try:
                        for threshold in threshold_values:
                            mask = region.image.copy()
                            image = region.image.copy()
                            image[region.intensity_image > threshold] = True
                            image[region.intensity_image <= threshold] = False
                            final = np.zeros_like(image, dtype=np.uint8)
                            final = Img.invert(image.astype(np.uint8))
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
        if DEBUG:
            Img(img_saturated, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'saturated_mask4.tif'))

        # plt.imshow(img_saturated)
        # plt.show()

        final_seeds = label(Img.invert(img_saturated), connectivity=2,
                            background=0)  # keep like that otherwise creates tiny cells with erroneous wshed

        # TODO this extra size parameter is quite good --> can I automate it --> eg cells 3 times smaller than the average or more
        # eg could set it to auto then compute average and adapt thresold

        if extra_filter_by_size is not None and extra_filter_by_size != 'auto' and extra_filter_by_size != 0:
            filter_by_size = extra_filter_by_size
        # if extra_filter_by_size == 'auto':
        else:
            filter_by_size = None
        avg_area = 0
        count = 0
        for region in regionprops(final_seeds):
            # exclude border cells from average as they most likely are incorrect and can greatly falsify the avg area of cells if few cells are there and big black region around
            # en effet ça change tout
            # if region.label == 1:
            #     print('zoopa', (region.bbox[0] <= 2 or region.bbox[1] <= 2 or region.bbox[2] >= final_seeds.shape[-2] - 3 or region.bbox[
            #             3] >= \
            #                 final_seeds.shape[-1] - 3))
            if (region.bbox[0] <= 2 or region.bbox[1] <= 2 or region.bbox[2] >= final_seeds.shape[-2] - 3 or region.bbox[
                3] >= \
                    final_seeds.shape[-1] - 3):
                continue
            avg_area += region.area
            count += 1
        avg_area /= count
        if extra_filter_by_size == 'auto':
            filter_by_size = avg_area / factor_below_average_for_extra_filter_by_size
        print('filter cells below:', filter_by_size, 'avg cell area = ', avg_area)

        # for debug
        if DEBUG:
            Img(final_seeds, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'final_seeds_before.tif'))
        final_seeds = label(Img.invert(img_saturated), connectivity=2, background=0)  # is that needed ???
        # for debug
        if DEBUG:
            Img(final_seeds, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'final_seeds_before2.tif'))

        # store seeds
        # can I check localy seeds to see if can do better
        # should I rerun wshed
        # count seeds in same

        final_seeds[img_saturated == 255] = 0
        final_wshed = watershed(img_orig, markers=final_seeds,
                                watershed_line=True)  # , mask=img_saturated[img_saturated==255] #img_orig

        final_wshed[final_wshed != 0] = 1  # remove all seeds
        final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        final_wshed[final_wshed == 1] = 0  # set all other cell content to

        # plt.imshow(final_wshed)
        # plt.show()

        filename0 = os.path.basename(path)
        parent_path = os.path.dirname(os.path.dirname(path))
        # print(parent_path, os.path.join(parent_path, filename0))
        # for debug

        # TODO maybe offer the choice between saving wshed on predict or on orig
        if filter_by_size is None or filter_by_size == 0:
            Img(final_wshed, dimensions='hw').save(os.path.join(default_output_folder, os.path.splitext(filename0)[
                0]) + '.tif')  # need put original name here  TODO put image default name here

        # inutile leur wshed donne le meme resultat qq soit l'angle...
        #
        # img_orig=img_orig[::-1,...]
        # final_seeds = final_seeds[::-1,...]
        # final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)
        # final_wshed[final_wshed != 0] = 1  # remove all seeds
        # final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        # final_wshed[final_wshed == 1] = 0  # set all other cell content to
        # Img(final_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'optimized_wshed_inverted.tif'))

        # TODO offer this as an option but skip for now
        '''
        del final_wshed
    
        try:
            img_orig = Img(os.path.join(parent_path, filename0))
        except:
            img_orig = Img(os.path.join(parent_path, os.path.splitext(filename0)[0]) + '.png')
        if img_orig.has_c() and img_orig.shape[-1] != 1:
            img_orig = img_orig[..., 0]
    
        # could even AND optimized_wshed and other watersheds
        final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)  # , mask=img_saturated[img_saturated==255]
    
        # for debug
        # Img(img_orig, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'original.tif'))
    
        final_wshed[final_wshed != 0] = 1  # remove all seeds
        final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        final_wshed[final_wshed == 1] = 0  # set all other cell content to
    
        # plt.imshow(final_wshed)
        # plt.show()
        # for debug
        if DEBUG:
            Img(final_wshed, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'optimized_wshed_real_original.tif'))
    
        duration = timer() - start
        print('duration is sec', duration)
        '''

        if filter_by_size is not None and filter_by_size != 0:

            # TODO try that just to see if I win and how --> do this only for the images where I lose... # TODO find a way to fuse seeds to restore them if in contact for example

            final_seeds = label(Img.invert(final_wshed.astype(np.uint8)), connectivity=1, background=0)

            # plt.imshow(final_seeds)
            # plt.show()

            labels_n_bbox = {}
            labels_n_area = {}

            # MEGA TODO peut etre faire que si il remove trop de cellules dans certaines regions alors ces regions sont exclues du fuse --> permettrait d'avoir un cutoff bcp plus stringent et donc de blaster plus fort dans des regions ou c'est necessaire --> pour faire ça il faut enlever les cellules puis relancer un wshed et compter le nb d'anciennes cellules par nouvelles cellules et si c'est trop alors ces cellules sont restaurees et exclues du blast peut etre peut trouver les cellules par leur centroid pr gagner du temps par rapport à un scan  complet --> à tester
            # MEGA TODO try local blast and use the same strategy to find neighbors of the cell
            # TODO put this in post process too
            # TODO handle boundaries with removal of cells

            # c'est pas ici que je dois le faire mais bien apres
            # create sets
            if VISUAL_DEBUG:
                plt.imshow(final_seeds)
                plt.show()

            removed_seeds = []
            for region in regionprops(final_seeds):
                labels_n_bbox[region.label] = region.bbox
                labels_n_area[region.label] = region.area
                # remove cells below cutoff
                if region.area < filter_by_size:
                    # print('should I exclude cell', region.label)
                    # exclude border cells because they are naturally smaller anyway...
                    if (region.bbox[0] <= 2 or region.bbox[1] <= 2 or region.bbox[2] >= labs.shape[-2] - 3 or region.bbox[
                        3] >= \
                            labs.shape[
                                -1] - 3):  # best is to just exclude border cells even though there can be errors # and region.area > extra_filter_by_size/10
                        # print('no', region.label)
                        # print('in here', region.label)
                        continue
                    # if set to 0 these things do not exist anymore from regionprops --> cannot be used --> need copy them or add them to a list
                    # for coordinates in region.coords:
                    #     final_seeds[coordinates[0], coordinates[1]] = 0  # do remove the seed
                    # print('adding cell to removed cells', region.label)

                    # print(region.label, region.area, region.bbox, labs.shape[-1], labs.shape[-2], extra_filter_by_size/2, (region.bbox[0] <= 2 or region.bbox[1] <= 2 or region.bbox[2] >= labs.shape[-2] - 3 or region.bbox[3] >= \
                    #         labs.shape[-1] - 3))
                    # print(region.bbox[0] <= 2, region.bbox[1] <= 2 , region.bbox[2] >= labs.shape[-2] - 3 , region.bbox[3] >= labs.shape[-1] - 3, region.area < extra_filter_by_size/2)
                    # print((region.bbox[0] <= 2 or region.bbox[1] <= 2 or region.bbox[2] >= labs.shape[-2] - 3 or region.bbox[3] >= \
                    #         labs.shape[-1] - 3), region.area < extra_filter_by_size/2)
                    removed_seeds.append(region.label)

            # see if fused seeds overlap if I can fuse them
            # maybe fuse them by distance or check if they overlap and if so then fuse them
            #

            print('labels_n_area', labels_n_area)
            # print('removed_seeds', len(removed_seeds))
            # print('removed_seeds', removed_seeds)

            # loop over all
            # store it as a set of sets to avoid doublons
            cells_to_fuse = []

            for idx, removed_seed in enumerate(removed_seeds):

                # print('idx', idx, removed_seed)
                current_cells_to_fuse = set()
                closest_pair = None
                smallest_distance = None
                # print(labels_n_area[removed_seed] * 3 <  extra_filter_by_size, labels_n_area[removed_seed] * 3, extra_filter_by_size)
                # if labels_n_area[removed_seed] * 3 <  extra_filter_by_size:
                #     # filter out very tiny cells because they shoudl really be removed in any case
                #     continue
                # can I measure distance using bbox to find adjacency
                # compute 4 connections

                # should I only fuse by two --> maybe in fact...

                for idx2 in range(idx + 1, len(removed_seeds)):
                    removed_seed2 = removed_seeds[idx2]
                    # if removed_seed == removed_seed2:
                    #     continue
                    # else:
                    # print('distance between', removed_seed, 'and', removed_seed2)

                    if closest_pair is None:
                        if rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2]) <= 1:
                            closest_pair = removed_seed2
                            smallest_distance = rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2])
                    elif rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2]) <= smallest_distance:
                        closest_pair = removed_seed2
                        smallest_distance = rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2])

                    if rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2]) <= 1:
                        # found adjacent seeds --> fuse them if close enough
                        if removed_seed == 133 or removed_seed2 == 133:
                            print(removed_seed, 'and', removed_seed2, 'should be fused')
                            print('bbox', labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2])
                            print('area', labels_n_area[removed_seed], labels_n_area[removed_seed2])
                            # print('centroid', labels_n_area[removed_seed], labels_n_area[removed_seed2])
                            print('dist', rect_distance(labels_n_bbox[removed_seed], labels_n_bbox[removed_seed2]))
                        current_cells_to_fuse.add(removed_seed)
                        current_cells_to_fuse.add(removed_seed2)
                        # if one of the seeds is very tiny do not add it

                # current_cells_to_fuse = set()

                # if closest_pair is not None:
                #     print(removed_seed, closest_pair)
                #     current_cells_to_fuse.add(removed_seed)
                #     current_cells_to_fuse.add(closest_pair)
                # maybe just take one, the closest ???? otherwise --> very complex
                # or fuse all by proximity then decide
                # fuse them one by one as long as their area is below target area
                if current_cells_to_fuse:
                    cells_to_fuse.append(current_cells_to_fuse)

            cells_to_fuse = [frozenset(i) for i in cells_to_fuse]
            cells_to_fuse = list(dict.fromkeys(cells_to_fuse))

            # fused = set()

            # max_size = 0
            # for fuse in cells_to_fuse:
            #     max_size = max(len(fuse), max_size)
            # print('size', len(fuse), max_size)

            cells_to_keep = []
            if cutoff_cell_fusion is not None and cutoff_cell_fusion > 0:
                # faire un superfuse pr voir la taille et si trop grand --> ignorer ce truc
                superfuse = []
                # for idx, fuse in enumerate(cells_to_fuse):
                #     current_fusion=set(fuse.copy())
                #     # fused.update(current_fusion)
                #     for _id in fuse:
                #         if _id not in fused:
                #             for idx2 in range(idx + 1, len(cells_to_fuse)):
                #                 fuse2 = cells_to_fuse[idx2]
                #                 for _id2 in fuse2:
                #                     # if _id2 not in fused:
                #                         if _id == _id2:
                #                                 current_fusion.update(fuse2)
                #                                 # fused.add(_id)
                #                                 # fused.update(fuse2)
                #                         # continue
                #     # if _id not in fused:
                #     superfuse.append(current_fusion)
                #     fused.update(current_fusion)

                copy_of_cells_to_fuse = cells_to_fuse.copy()
                # should remove fused from list
                # fused_already = []
                # first try to fuse to any in the other list
                for idx, fuse in enumerate(copy_of_cells_to_fuse):
                    # if fuse in fused_already:
                    #     continue
                    # fused_already.append(fuse)
                    current_fusion = set(fuse.copy())
                    # fused_already.append(current_fusion)
                    # changed = False
                    # fused.update(current_fusion)
                    changed = True
                    while changed:
                        changed = False
                        for idx2 in range(len(copy_of_cells_to_fuse) - 1, idx, -1):
                            fuse2 = copy_of_cells_to_fuse[idx2]
                            # if fuse2 in fused_already:
                            #     continue
                            if idx2 == idx:
                                continue
                            if fuse2.intersection(current_fusion):
                                current_fusion.update(fuse2)
                                # fused_already.append(fuse2)
                                # fused_already.append(current_fusion)
                                del copy_of_cells_to_fuse[idx2]
                                changed = True
                            # changed=True
                    # for _id in fuse:
                    #     if _id not in fused:
                    #         for idx2 in range(idx + 1, len(cells_to_fuse)):
                    #             fuse2 = cells_to_fuse[idx2]
                    #             for _id2 in fuse2:
                    #                 # if _id2 not in fused:
                    #                 if _id == _id2:
                    #                     current_fusion.update(fuse2)
                    #                     # fused.add(_id)
                    #                     # fused.update(fuse2)
                    #                 # continue
                    # if _id not in fused:
                    # if changed:
                    #     inside =False
                    #     for f in superfuse:
                    #         if f.intersection(current_fusion):
                    #             f.update(current_fusion)
                    #             inside = True
                    #     if not inside:
                    superfuse.append(current_fusion)
                    #     fused_already.append(current_fusion)

                    # fused.update(current_fusion)

                    # or do recursive until nothing to fuse anymore --> no change

                print('superfuse', superfuse)

                for sf in superfuse:
                    # print('sf',len(sf))
                    if len(sf) > cutoff_cell_fusion:
                        for val in sf:
                            cells_to_keep.append(val)

                # if too many seeds ought to be removed --> cancel removal --> allow a cutoff of like two or 3 ???

                # now need determine cells to really remove --> all the others
                # for all the things that need be fused --> if they have the same area give them the id

                # sort from smallest number to biggest to avoid errors
                # if sum is superior or equal to seed size then set as seed

            seeds_to_fuse = []

            print(cells_to_fuse)
            print(len(cells_to_fuse))  # 8 sets of cells to fuse

            # seeds_that_really_need_be_removed = []
            # MEGA TODO fuse recursively all touch cells until it really fills something --> easy because they must share a neighbor

            # first try normal fuse then if not fused then try fuse more

            cells_to_fuse = sorted(cells_to_fuse, key=len)
            for fuse in cells_to_fuse:
                cumulative_area = 0
                for _id in fuse:
                    if _id in cells_to_keep:
                        if _id in removed_seeds:
                            removed_seeds.remove(_id)
                        continue
                    cumulative_area += labels_n_area[_id]
                # print('cumulative_area', cumulative_area, extra_filter_by_size)
                if cumulative_area >= filter_by_size:  #: #1200: #filter_by_size:
                    # print('create new unified seed')
                    # if should form a single seed need color all the seeds in the same way in the watershed --> add it to the
                    seeds_to_fuse.append(fuse)
                    for _id in fuse:
                        if _id in removed_seeds:
                            removed_seeds.remove(_id)
                # else:
                #     for _id in fuse:
                #         seeds_that_really_need_be_removed.append(_id)
                #     print('seeds too small --> remove them')

            # print('final seeds to fuse', seeds_to_fuse)

            # need recolor all the seeds in there with the new seed stuff
            for fuse in seeds_to_fuse:
                for _id in fuse:
                    break
                # print('id', _id)
                for region in regionprops(final_seeds):
                    # take id of the first
                    # print(region.label)
                    if region.label in fuse:
                        # print('seed found', region.label)
                        for coordinates in region.coords:
                            final_seeds[coordinates[0], coordinates[1]] = _id

                    # elif region.label in seeds_that_really_need_be_removed:
                    #     for coordinates in region.coords:
                    #             final_seeds[coordinates[0], coordinates[1]] = 0

            # for remove_seed in removed_seeds:
            for region in regionprops(final_seeds):
                if region.label in removed_seeds:
                    for coordinates in region.coords:
                        final_seeds[coordinates[0], coordinates[1]] = 0

            # print('seeds_that_really_need_be_removed', seeds_that_really_need_be_removed)
            # print('removed_seeds', removed_seeds)
            if VISUAL_DEBUG:
                plt.imshow(final_seeds)
                plt.show()

            final_wshed = watershed(img_orig, markers=final_seeds,
                                    watershed_line=True)  # , mask=img_saturated[img_saturated==255]

            # for debug
            # Img(img_orig, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'original.tif'))

            # ça marche --> maintenant activer ce code et le faire tourner sur bcp de mes trucs pr voir si mon score face à cellpose augmente

            final_wshed[final_wshed != 0] = 1  # remove all seeds
            final_wshed[final_wshed == 0] = 255  # set wshed values to 255
            final_wshed[final_wshed == 1] = 0  # set all other cell content to
            if VISUAL_DEBUG:
                plt.imshow(final_wshed)
                plt.show()
            # TODO remove 1200 !!!!!!!!!!!!!!!
            # c'est bon mon systeme de fusion de seeds fonctionne --> maintenant voir comment faire pr activer ça
            # maintenant juste finaliser le code et appliquer les seeds sur l'image originelle à nouveau --> et voir ce que ça donne

            # how can I compute this threshold automatically ???

            # plt.imshow(final_seeds)
            # plt.show()

            # print(len(removed_seeds))
            # print(removed_seeds)

            # when a seed is removed I should maybe check that sum of all seeds removed is not superior to threshold otherwise ignore

            # for debug
            # if DEBUG:
            # print(os.path.join(default_output_folder, 'extras', 'filtered_seeds.tif'))
            # Img(final_wshed, dimensions='hw').save(os.path.join(default_output_folder, 'extras', 'filtered_seeds.tif'))
            print('saving', os.path.join(default_output_folder, os.path.splitext(filename0)[0]) + '.tif')
            Img(final_wshed, dimensions='hw').save(os.path.join(default_output_folder, os.path.splitext(filename0)[
                0]) + '.tif')  # need put original name here  TODO put image default name here

        duration = timer() - start
        print('final duration wshed in secs', duration)

        # del final_seeds
        # del final_wshed
        # del img_orig

        # i think there is a bug but anyway it's unlikely to work...
        # try some seed blasting just to see how  it goes --> may very well work and will be parameterless

        #
        # final_seeds = final_wshed.copy()
        # s = ndimage.generate_binary_structure(2, 1)
        # final_seeds = ndimage.grey_dilation(final_seeds, footprint=s)
        # # final_seeds= ndimage.grey_dilation(final_seeds, footprint=s)
        #
        # plt.imshow(final_seeds)
        # plt.show()
        #
        # final_seeds = label(invert(final_seeds.astype(np.uint8)), connectivity=2, background=0)
        # ids_n_area = {}
        #
        # plt.imshow(final_seeds)
        # plt.show()
        #
        # for region in regionprops(final_seeds):
        #     # for each cell look around and if strongly different in area --> blast it
        #     # look just one or two rows on either side
        #     if region.bbox[0] <= 5 or region.bbox[1] <= 5 or region.bbox[2] >= final_seeds.shape[-2] - 6 or region.bbox[
        #         3] >= \
        #             final_seeds.shape[-1] - 6:
        #         continue
        #     else:
        #         if region.area >= 10:
        #             ids_n_area[region.label] = region.area
        #     # else:
        #     #     for coordinates in region.coords:
        #     #         final_seeds[coordinates[0], coordinates[1]] == 0
        #
        # # final_seeds = label(invert(final_seeds.astype(np.uint8)), connectivity=2, background=0)
        # cells_to_remove = []
        #
        # out = np.zeros_like(final_seeds, dtype=np.uint8)

        # TODO remove all border cells then restore them

        # I think that will not work...
        # I do need to remove border cells too cause they would cause errors
        # for region in regionprops(final_seeds):
        #     if region.area >= 10:
        #         if (region.bbox[0] <= 5 or region.bbox[1] <= 5 or region.bbox[2] >= final_seeds.shape[-2] - 6 or region.bbox[3] >= final_seeds.shape[-1] - 6):
        #             continue
        #         y1, x1, y2, x2 = region.bbox
        #         neighbors = set()
        #         for x in range(x1 - 20, x2 + 20):
        #             for y in range(y1 - 20, y2 + 20):
        #                 try:
        #                     cell_id = final_seeds[y, x]
        #                     if cell_id != region.label and cell_id != 0:
        #                         if cell_id in ids_n_area.keys():
        #                             neighbors.add(cell_id)
        #                 except:
        #                     pass
        #         # average_neighbor_size = 0
        #         smallest_neigbor_area = 0
        #         smallest_neigbor_id = 0
        #         for neigh_id in neighbors:
        #             if neigh_id in ids_n_area.keys():
        #                 if smallest_neigbor_area == 0:
        #                     smallest_neigbor_area = ids_n_area[neigh_id]
        #                     smallest_neigbor_id = neigh_id
        #                 if ids_n_area[neigh_id] < smallest_neigbor_area:
        #                     smallest_neigbor_area = ids_n_area[neigh_id]
        #                     smallest_neigbor_id = neigh_id
        #         if smallest_neigbor_id != 0 and smallest_neigbor_area != 0:
        #             # if region.label in ids_n_area:
        #             if 2 * region.area <  smallest_neigbor_area:
        #                 print('removing', region.label, region.area, smallest_neigbor_area, smallest_neigbor_id, region.centroid, region.bbox)
        #                 cells_to_remove.append(region.label)
        #                 for coordinates in region.coords:
        #                     out[coordinates[0], coordinates[1]] = 255
        #         #     if neigh_id in ids_n_area:
        #         #         average_neighbor_size += ids_n_area[neigh_id]
        #         # if average_neighbor_size != 0:
        #         #     average_neighbor_size /= len(neighbors)
        #         #     if ids_n_area[region.label] * 6 < average_neighbor_size:
        #         #         print('removing', region.label, region.area, average_neighbor_size)
        #         #         cells_to_remove.append(region.label)
        #         #         for coordinates in region.coords:
        #         #             out[coordinates[0], coordinates[1]] = 255
        #     else:
        #         cells_to_remove.append(region.label)
        #         for coordinates in region.coords:
        #             out[coordinates[0], coordinates[1]] = 255
        #
        # plt.imshow(out)
        # plt.show()
        #
        # # final_seeds = label(invert(final_seeds.astype(np.uint8)), connectivity=2, background=0)
        #
        # for region in regionprops(final_seeds):
        #     if region.label in cells_to_remove:
        #         print('removing')
        #         if region.bbox[0] <= 1 or region.bbox[1] <= 1 or region.bbox[2] >= labs.shape[-2] - 2 or region.bbox[
        #             3] >= \
        #                 labs.shape[-1] - 2:
        #             continue
        #         for coordinates in region.coords:
        #             final_seeds[coordinates[0], coordinates[1]] = 0
        #             out[coordinates[0], coordinates[1]] = 255
        #
        # plt.imshow(final_seeds)
        # plt.show()
        #
        # plt.imshow(out)
        # plt.show()
        #
        # final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)  # , mask=img_saturated[img_saturated==255]
        #
        # # for debug
        # # Img(img_orig, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'original.tif'))
        #
        # final_wshed[final_wshed != 0] = 1  # remove all seeds
        # final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        # final_wshed[final_wshed == 1] = 0  # set all other cell content to
        #
        # # plt.imshow(final_wshed)
        # # plt.show()
        # Img(final_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'optimized_wshed_reduced_seeds.tif'))
        #
        # duration = timer() - start
        # print('duration is sec', duration)
        #
        # del final_seeds
        #
        # #
        # # # try rewatersheding to find weak bonds --> does not seem to work
        # # s = ndimage.generate_binary_structure(2, 1)
        # # # seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
        # # # seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
        # # # seeds_1 = ndimage.grey_dilation(seeds_1, footprint=s)
        # # final_seeds = ndimage.grey_erosion(final_seeds, footprint=s)
        # # final_seeds = ndimage.grey_erosion(final_seeds, footprint=s)
        # # final_seeds = ndimage.grey_erosion(final_seeds, footprint=s)
        # # # si des seeds ont diparues faudrait les remettre
        # #
        # # final_wshed = watershed(img_orig, markers=final_seeds, watershed_line=True)  # , mask=img_saturated[img_saturated==255]
        # #
        # # # for debug
        # # # Img(img_orig, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'original.tif'))
        # #
        # # final_wshed[final_wshed != 0] = 1  # remove all seeds
        # # final_wshed[final_wshed == 0] = 255  # set wshed values to 255
        # # final_wshed[final_wshed == 1] = 0  # set all other cell content to
        # #
        # # Img(final_wshed, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'optimized_wshed_reduced_seeds.tif'))
        # #
        #
        #
        # # bond scoring does not work well yet --> deactivate for now
        # # if img_has_seeds:
        # #     kernel = np.ones((3, 3))
        # #     mask = convolve2d(final_wshed, kernel, mode='same', fillvalue=1)
        # #
        # #     # mask[mask<1020] = 0
        # #     # mask[mask>=1020] = 255
        # #
        # #     plt.imshow(mask)
        # #     plt.show()
        # #
        # #     result = np.zeros_like(mask)
        # #     result[np.logical_and(mask >= 1020, final_wshed == 255)] = 255
        # #
        # #     plt.imshow(result)
        # #     plt.show()
        # #
        # #     Img(result, dimensions='hw').save(os.path.join(os.path.splitext(path)[0], 'vertices_test.tif'))
        # #
        # #     # dirty vertex detection but maybe there is hope
        # #
        # #     final_wshed = final_wshed.astype(np.uint8) - result.astype(np.uint8)
        # #
        # #     # get regions and count nb of white pixels in this region and if too low --> blast it...
        # #     bonds = label(final_wshed, connectivity=2, background=0)
        # #
        # #     plt.imshow(bonds)
        # #     plt.show()
        # #
        # #     final = final_wshed.copy()
        # #
        # #     img_seg[img_seg >= 0.9] = 255
        # #     img_seg[img_seg < 0.9] = 0
        # #
        # #     for region in regionprops(bonds):
        # #         # if region.area>100:
        # #         count = 0
        # #         for coordinates in region.coords:
        # #             # final[coordinates[0], coordinates[1]]=255
        # #             if img_seg[coordinates[0], coordinates[1]] == 255:
        # #                 count += 1
        # #
        # #         print(count / region.area)
        # #
        # #         if count / region.area <= 0.3:
        # #
        # #             for coordinates in region.coords:
        # #                 # final[coordinates[0], coordinates[1]]=255
        # #                 final[coordinates[0], coordinates[1]] = 0
        # #
        # #     plt.imshow(final)
        # #     plt.show()

if __name__ == '__main__':
    pass