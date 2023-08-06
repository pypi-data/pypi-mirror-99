# I think I like dask --> can I use it for my images

# https://blog.dask.org/2019/06/20/load-image-data --> really cool!!!
# https://github.com/dask/dask-tutorial/ --> à tester

# import dask_image
# the two below are required for to_zarr # KEEP TODO PLEASE KEEP
import zarr # the two below are required for to_zarr # KEEP TODO PLEASE KEEP
import fsspec # the two below are required for to_zarr # KEEP TODO PLEASE KEEP

# import dask_image.imread
# import dask_image.ndfilters

# rest of imports
import imageio
import glob
import sys
from natsort import natsorted
from epyseg.img import Img

filenames = glob.glob("/D/Sample_images/sample_images_PA/trash_test_mem/complete/*.png")
filenames = natsorted(filenames)
print(len(filenames))
# sample = imageio.imread(filenames[0])
# print(sample.shape)

import dask
import dask.array as da
import numpy as np

# lazy_arrays = [dask.delayed(imageio.imread)(fn) for fn in filenames]
lazy_arrays = [dask.delayed(Img)(fn) for fn in filenames] # can do a lazy array of anything
sample = lazy_arrays[0].compute()
# nb this assumes all images have the same size otherwise stuff like concatenate and stack will crash
lazy_arrays = [da.from_delayed(x, shape=sample.shape, dtype=sample.dtype)
               for x in lazy_arrays]

print(lazy_arrays)


from matplotlib import pyplot as plt

# it seems to work --> see how I can really make use of that
print(sys.getsizeof(lazy_arrays[0]))
print(sys.getsizeof(lazy_arrays[1]))
print(sys.getsizeof(lazy_arrays[1].compute()))
print(sys.getsizeof(lazy_arrays[1]))

plt.imshow(lazy_arrays[0].compute(), cmap='gray') # now image is really read before it's not
plt.show()

# tmp = da.concatenate(lazy_arrays[:10], axis=0)
# tmp = da.stack(lazy_arrays[:10])


# from skimage.filters import gaussian
# def dask_gauss(x, sigma_tuple):
#     # chunksize = tuple(c[0] for c in v.chunks)
#     chunksize = x.compute().shape
#     out_sigma = tuple(max(1, int(2 * sigma)) for sigma in sigma_tuple)
#     if any([a < b for a, b in zip(chunksize, out_sigma)]):
#         new_chunksize = [max(a, b) for a, b in zip(chunksize, out_sigma)]
#         print('Rechunking:', new_chunksize)
#         x = x.rechunk(new_chunksize)
#
#     return x.map_overlap(lambda y: gaussian(y, sigma_tuple).astype(np.float32), depth=out_sigma, boundary='reflect')


# lazy_arrays = dask_gauss(lazy_arrays,3)

tmp = da.stack(lazy_arrays) # concat all in a single array
print('last', sys.getsizeof(tmp))

# https://examples.dask.org/applications/image-processing.html --> pas mal aussi
# smoothed_image = dask_image.ndfilters.gaussian_filter(tmp, sigma=[1, 1])
# print(smoothed_image) # only really done when consumes is done --> may gain a lot of time and space in memory if using dask with deep learning ??? no in fact no

# plt.ion()
print(tmp.shape)

print(tmp.sum()) #just creates a dask sum but does not really compute it
print(tmp.sum().compute()) #does really compute sum of all arrays

# this is how one blurs a dask stuff
# tmp = dask_gauss(tmp,3)
# for img in tmp:
#     plt.imshow(img) #shows frame #100 of a stack # ça marche
#     plt.draw()
#     plt.pause(0.1)

plt.imshow(tmp[128])
plt.show()

# ça marche --> vraiment essayer d'utiliser ça...

def grayscale(rgb):
    result = ((rgb[..., 0] * 0.2989) +
              (rgb[..., 1] * 0.5870) +
                  (rgb[..., 2] * 0.1140))
    return result

single_image_result = grayscale(lazy_arrays[180])
print(single_image_result) # a dask array
# single_image_result.visualize() # super slow ??? or blocked


# ça marche --> ça va etre assez puissant je pense en fait --> assez cool
plt.imshow(single_image_result.compute(), cmap='gray') # a numpy array again... --> finally ok
plt.show()

if False:
    # marche pas... en fait si si ça mais faut pip install zarr et pip install fsspec
    single_image_result.to_zarr("/home/aigouy/Bureau/trash/mydata.zarr") # store the dask stuff

    # now we reload it --> quite cool in fact it's really the result of all and not the complete path to get there...
    test = zarr.load('/home/aigouy/Bureau/trash/mydata.zarr')

    plt.imshow(test)  # a numpy array again... --> finally ok
    plt.show()

# plot 3D images with napari

# or
# from numcodecs import Blosc
# single_image_result.to_zarr("mydata.zarr", compressor=Blosc(cname='zstd', clevel=3, shuffle=Blosc.BITSHUFFLE))


# import dask_image
# x = dask_image.imread.imread('raw/*.tif')