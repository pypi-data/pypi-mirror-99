import os
import dask_image # pip install dask-image
import dask_image.imread
import dask_image.ndfilters
import dask_image.ndmeasure
import dask.array as da
import glob
from natsort import natsorted
from epyseg.img import Img


# filenames = glob.glob("/D/Sample_images/sample_images_PA/trash_test_mem/complete/*.png")
# filenames = natsorted(filenames)

# en fait ça fait just un concat et donc je m'en fous en plus c'est meme pas dans l'ordre alpahbetique
filename_pattern = os.path.join('/D/Sample_images/sample_images_PA/trash_test_mem/complete/', '*.png')
tiled_astronaut_images = dask_image.imread.imread(filename_pattern)
print(tiled_astronaut_images)

