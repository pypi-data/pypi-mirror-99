# code to filter seeds based on their area, maybe also find a way to fuse close by seeds


import glob
import traceback
# from skimage.morphology import flood
# skimage.morphology.flood_fill(image, …[, …])
from scipy import ndimage
from scipy.signal import convolve2d
from skimage import morphology, img_as_uint, img_as_ubyte
from skimage.feature import peak_local_max, corner_harris, corner_peaks
from skimage.util import invert
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


# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_centroid_n_inverted/'
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_shells/'
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict/'
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_vgg16_light_divided_by_2/'
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_paper/'
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729/' #1
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_Linknet-seresnext101-smloss-256x256-ep0099-l0.158729_rot_HQ_only/' #2
root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317/' #3
# root_path = '/home/aigouy/Bureau/final_folder_scoring/predict_linknet-vgg16-sigmoid-ep0191-l0.144317_rot_HQ_only/' #4

list_of_files = glob.glob(root_path + "*.png") + glob.glob(root_path + "*.jpg") + glob.glob(
    root_path + "*.jpeg") + glob.glob(
    root_path + "*.tif") + glob.glob(root_path + "*.tiff")+ glob.glob(root_path + "*.lsm")+ glob.glob(root_path + "*.czi") + glob.glob(root_path + "*.lif")
list_of_files = natsorted(list_of_files)


