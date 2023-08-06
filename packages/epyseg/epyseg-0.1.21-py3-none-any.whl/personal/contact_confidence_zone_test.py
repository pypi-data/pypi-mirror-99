#
# TODO try a model with up to four dilation model
# 0 dilation --> first layer
# 1 dilation --> second layer
# 2 dilation --> third layer
# 3 dilation --> 4th layer

# TODO --> add a layer that corresponds to the seeds --> ce qui reste apres une dilation de 3 ou 4 fois et tt reste en noir
# can be used for rewatersheding and for blasting
from scipy import ndimage

from epyseg.img import Img
import numpy as np

s = ndimage.generate_binary_structure(2, 1)
mask_dilations = 3


msk = Img('/home/aigouy/Bureau/final_folder_scoring/Bro43_avproj0000/handCorrection.png')
c = 0 # channel of interest
dilated_imgs = []

# need add a batch dimension

if mask_dilations:

    # Apply dilation to every channel then reinject
    # for c in range(output_shape[-1]):
        dilated = msk[..., c]
        dilated_imgs.append(dilated)
        for dilation in range(mask_dilations):
            dilated = ndimage.grey_dilation(dilated, footprint=s)
            dilated_imgs.append(dilated)


        seeds = np.zeros_like(dilated)
        # should I invert it basically or do another dilation ???
        # just take the negative
        seeds[dilated == 0] = 255
        seeds[dilated == 255] = 0
        dilated_imgs.append(seeds)

        # final = Img.tiles_to_batch(dilated_imgs)

        # add dimension if not there yet


        for idx,img in enumerate(dilated_imgs):
            dilated_imgs[idx]=np.reshape(dilated_imgs[idx], (1,*dilated_imgs[idx].shape,1))

        final = np.concatenate(tuple(dilated_imgs), axis=0)
        print(final.shape)



        # ça marche du coup faut que je le sauve pr verif
        Img(final, dimensions='dhwc').save('/home/aigouy/Bureau/trashme.tif')  # files[idx] + 'pred_cell_seg2.tif')

    # perfect now try to get the model to produce this shit
# then create a stack out of that and save it as IJ image so that I can check it

