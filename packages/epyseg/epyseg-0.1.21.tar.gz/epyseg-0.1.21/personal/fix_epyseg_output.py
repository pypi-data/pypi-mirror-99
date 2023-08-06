# en fait le wshed n'aide pas a resegmenter contrairement à ce que je pensais
# peut etre en thresoldant ???

# load image do avg proj
# then binarise and try threshold it
# try run wshed on it with some size criterion
# test of all
#
from deprecated_demos.ta.wshed import Wshed
from epyseg.img import Img
from matplotlib import pyplot as plt
# from skimage.morphology import watershed
from skimage.segmentation import watershed
from skimage.measure import label, regionprops
import numpy as np
from skimage.util import invert

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd
from skimage import io
from skimage import measure
# from skimage.morphology import watershed
from skimage.segmentation import watershed
from skimage.segmentation import find_boundaries
from skimage.color import gray2rgb

# img = Img('/home/aigouy/Bureau/AVG_100708_png06.png')
img = Img('/home/aigouy/Bureau/AVG_5.png')
# final_mask = Wshed.run_dist_transform_watershed(img)


if True:
    image_thresh = img > 140
    image_thresh = image_thresh.astype(np.uint8)
    print(image_thresh.max(), image_thresh.min())

    plt.imshow(image_thresh)
    plt.show()

    image_thresh = label(image_thresh, connectivity=2, background=0)  # can I use - instead of invert --> faster ???

    plt.imshow(image_thresh)
    plt.show()

    # deblob
    min_size = 300
    for region in regionprops(image_thresh):
        # take regions with large enough areas
        if region.area < min_size:
            for coordinates in region.coords:
                image_thresh[coordinates[0], coordinates[1]] = 0

    image_thresh[image_thresh > 0] = 255

    # min_size = 300
    # for region in regionprops(image_thresh):
    #     # take regions with large enough areas
    #     if region.area < min_size:
    #         for coordinates in region.coords:
    #             image_thresh[coordinates[0], coordinates[1]] = 255
    #



    image_thresh = invert(image_thresh.astype(np.uint8))

    print(image_thresh.min(), image_thresh.max())

    plt.imshow(image_thresh)
    plt.show()

    labels = nd.label(image_thresh)[0]
    distance = nd.distance_transform_edt(image_thresh)
    markers = label(labels, connectivity=2, background=0)
    # coords = np.array([np.round(p['Centroid']) for p in props], dtype=int)

    plt.imshow(distance)
    plt.show()

    plt.imshow(markers)
    plt.show()

    # Create marker image where blob centroids are marked True
    # markers = np.zeros(img.shape, dtype=bool)
    # markers[tuple(np.transpose(coords))] = True
    labelled_image = watershed(-distance, markers, watershed_line=True) # mask=image_thresh,
    # find outline of objects for plotting
    # boundaries = find_boundaries(labelled_image)
    # img_rgb = gray2rgb(img)
    boundaries = labelled_image
    boundaries[boundaries != 0] = 1  # remove all seeds
    boundaries[boundaries == 0] = 255  # set wshed values to 255
    boundaries[boundaries == 1] = 0  # set all other cell content to 0

    # not bad too even though super noisy

    print('wshed edm')
    # overlay = visualize_boundaries(img_rgb, boundaries, color=(1, 0, 0))
    plt.imshow(boundaries)
    plt.show()

# markers = np.zeros_like(img)
# foreground, background = 1, 2
# markers[img < 30.0] = background
# markers[img > 150.0] = foreground
# # markers = img[img<64]
#
#
# final_mask = watershed(img, markers, watershed_line=True)
# # do the tip for
# final_mask[final_mask != 0] = 1  # remove all seeds
# final_mask[final_mask == 0] = 255  # set wshed values to 255
# final_mask[final_mask == 1] = 0  # s
#
# plt.imshow(final_mask)
# plt.show()
# plt.imshow(img)
# plt.show()
#
# final_mask = Wshed.run_fast(img, seeds='mask')
# final_mask[final_mask != 0] = 1  # remove all seeds
# final_mask[final_mask == 0] = 255  # set wshed values to 255
# final_mask[final_mask == 1] = 0  # s
# plt.imshow(final_mask)
# plt.show()

# markers = np.zeros_like(img)
# markers[img < 30.0] = background
# markers[img > 100.0] = foreground

# plt.imshow(markers)
# plt.show()

# is that what I want ??? think about it ???

img = Img('/home/aigouy/Bureau/AVG_5.png')
img_bckup = img.copy()
img_bckup[img_bckup<64]=0
print(img.dtype)
img[img > 160] = 255
img[img < 160] = 0

plt.imshow(img)
plt.show()
markers = label(img, connectivity=2, background=0)  # can I use - instead of invert --> faster ???

plt.imshow(markers)
plt.show()

# deblob
min_size = 300
for region in regionprops(markers):
    # take regions with large enough areas
    if region.area < min_size:
        for coordinates in region.coords:
            markers[coordinates[0], coordinates[1]] = 0

markers[markers > 0] = 255

plt.imshow(markers)
plt.show()

# markers = label(invert(markers), connectivity=2, background=0)



# markers = markers.astype(np.uint8)
# print(img.shape, img.dtype, markers.shape, markers.dtype, markers.max(), markers.min())


# there is a bug in markers --> can i fix that ???
# print('toto')
# plt.imshow(markers)
# plt.show()
labels_ws = watershed(markers,
                      watershed_line=True) # markers=markers, # connectivity=2, # is markers the seeds ??? , watershed_line=True # somehow line seems discontinuous --> why --> is that an artifact # en fait ça marche et c'est continu mais on le voit pas car il faut zoomer --> presque ok --> juste finaliser tt maintenant
# nb if I do the line below then I don't lose the edges otherwise using peak_local_I lose them
# labels_ws = watershed(strong, markers=None, watershed_line=True) # connectivity=2, # is markers the seeds ??? , watershed_line=True # somehow line seems discontinuous --> why --> is that an artifact # en fait ça marche et c'est continu mais on le voit pas car il faut zoomer --> presque ok --> juste finaliser tt maintenant
# labels_ws = random_walker(weak, markers, beta=10, mode='bf')


# print('now') # seems to do nothing --> why
# labels_ws[labels_ws == 0] = 255
plt.imshow(labels_ws)
plt.show()

plt.imshow(img)
plt.show()


labels_ws[labels_ws != 0] = 1  # remove all seeds
labels_ws[labels_ws == 0] = 255  # set wshed values to 255
labels_ws[labels_ws == 1] = 0  # set all other cell content to 0

plt.imshow(labels_ws)
plt.show()
