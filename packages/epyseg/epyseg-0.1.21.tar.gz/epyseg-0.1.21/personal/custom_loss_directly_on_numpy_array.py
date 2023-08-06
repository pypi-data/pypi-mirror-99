# TODO tester https://github.com/google/ffn # --> des floodfilling neural networks --> cool
from epyseg.img import Img
import numpy as np
import tensorflow.keras.backend as K


# def custom_loss_numpy (encodings, user_id):
# # user_id: a pandas series of users
# # encodings: a pandas dataframe of encodings
#
#     batch_dist = 0
#
#     for i in range(len(user_id)):
#          first_row = encodings.iloc[i,:].values
#          first_user = user_id[i]
#
#          for j in range(i+1, len(user_id)):
#               second_user = user_id[j]
#               second_row = encodings.iloc[j,:].values
#
#         # compute distance: if the users are same then Euclidean distance is positive otherwise negative.
#             if first_user == second_user:
#                 tmp_dist = np.linalg.norm(first_row - second_row)
#             else:
#                 tmp_dist = -np.linalg.norm(first_row - second_row)
#
#             batch_dist += tmp_dist
#
#     return batch_dist

# def custom_loss_keras(user_id, encodings):
#     pairwise_diff = K.expand_dims(encodings, 0) - K.expand_dims(encodings, 1)
#     pairwise_squared_distance = K.sum(K.square(pairwise_diff), axis=-1)
#     pairwise_distance = K.sqrt(pairwise_squared_distance + K.epsilon())
#
#     user_id = K.squeeze(user_id, axis=1)  # remove the axis added by Keras
#     pairwise_equal = K.equal(K.expand_dims(user_id, 0), K.expand_dims(user_id, 1))
#
#     pos_neg = K.cast(pairwise_equal, K.floatx()) * 2 - 1
#     return K.sum(pairwise_distance * pos_neg, axis=-1) / 2


def custom_loss_keras(user_id, encodings):
    # calculate pairwise Euclidean distance matrix
    pairwise_diff = K.expand_dims(encodings, 0) - K.expand_dims(encodings, 1)
    pairwise_squared_distance = K.sum(K.square(pairwise_diff), axis=-1)

    # add a small number before taking K.sqrt for numerical safety
    # (K.sqrt(0) sometimes becomes nan)
    pairwise_distance = K.sqrt(pairwise_squared_distance + K.epsilon())

    # this will be a pairwise matrix of True and False, with shape (batch_size, batch_size)
    pairwise_equal = K.equal(K.expand_dims(user_id, 0), K.expand_dims(user_id, 1))

    # convert True and False to 1 and -1
    pos_neg = K.cast(pairwise_equal, K.floatx()) * 2 - 1

    # divide by 2 to match the output of `custom_loss_numpy`, but it's not really necessary
    return K.sum(pairwise_distance * pos_neg, axis=-1) / 2

    # # score calculation
    # intersection = backend.sum(gt * pr, axis=axes)
    # union = backend.sum(gt + pr, axis=axes) - intersection
    #
    # score = (intersection + smooth) / (union + smooth)


encodings = np.random.rand(32, 10)
user_id = np.random.randint(10, size=32)

print(K.eval(custom_loss_keras(K.variable(user_id), K.variable(encodings))).sum())

# print(custom_loss_numpy(pd.DataFrame(encodings), pd.Series(user_id)))

# encodings = np.random.rand(32, 10)
# encodings2 = np.random.rand(32, 10)

# np.random.rand(3, 2) --> a 3 x 2 image
target = np.random.rand(10, 4, 5)  # np.arange(20).reshape(4,5)
prediction = np.random.rand(10, 4, 5)  # np.arange(20).reshape(4,5)

print(target, prediction)
# prediction[0,5] = 1
# prediction[0,0] = 12


# def __init__(self, class_weights=None, class_indexes=None, per_image=False, smooth=SMOOTH):
#     super().__init__(name='jaccard_loss')
#     self.class_weights = class_weights if class_weights is not None else 1
#     self.class_indexes = class_indexes
#     self.per_image = per_image
#     self.smooth = smooth
#
#
# def __call__(self, gt, pr):
#     return 1 - F.iou_score(
#         gt,
#         pr,
#         class_weights=self.class_weights,
#         class_indexes=self.class_indexes,
#         smooth=self.smooth,
#         per_image=self.per_image,
#         threshold=None,
#         **self.submodules
#     )

# def iou_score(gt, pr, class_weights=1., class_indexes=None, smooth=SMOOTH, per_image=False, threshold=None, **kwargs):
#     r""" The `Jaccard index`_, also known as Intersection over Union and the Jaccard similarity coefficient
#     (originally coined coefficient de communauté by Paul Jaccard), is a statistic used for comparing the
#     similarity and diversity of sample sets. The Jaccard coefficient measures similarity between finite sample sets,
#     and is defined as the size of the intersection divided by the size of the union of the sample sets:
#
#     .. math:: J(A, B) = \frac{A \cap B}{A \cup B}
#
#     Args:
#         gt: ground truth 4D keras tensor (B, H, W, C) or (B, C, H, W)
#         pr: prediction 4D keras tensor (B, H, W, C) or (B, C, H, W)
#         class_weights: 1. or list of class weights, len(weights) = C
#         class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.
#         smooth: value to avoid division by zero
#         per_image: if ``True``, metric is calculated as mean over images in batch (B),
#             else over whole batch
#         threshold: value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round
#
#     Returns:
#         IoU/Jaccard score in range [0, 1]
#
#     .. _`Jaccard index`: https://en.wikipedia.org/wiki/Jaccard_index

#
#     """
#
#     backend = kwargs['backend']
#
#     gt, pr = gather_channels(gt, pr, indexes=class_indexes, **kwargs)
#     pr = round_if_needed(pr, threshold, **kwargs)
#     axes = get_reduce_axes(per_image, **kwargs)
#
#     # score calculation
#     intersection = backend.sum(gt * pr, axis=axes)
#     union = backend.sum(gt + pr, axis=axes) - intersection
#
#     score = (intersection + smooth) / (union + smooth)
#     score = average(score, per_image, class_weights, **kwargs)
#
#     return score


# c'est bon j'ai mon iou --> facile de comparer entre mon soft et cellpose sur des images de tests
# TODO aussi faire ma propre loss qui compte le nb d'erreurs

import tensorflow.keras.backend as kb


def custom_loss(y_actual, y_pred):
    custom_loss = kb.square(y_actual - y_pred)
    return custom_loss


target = target > 0.5
prediction = prediction > 0.5

print(target, prediction)

intersection = np.logical_and(target, prediction)
union = np.logical_or(target, prediction)
iou_score = np.sum(intersection) / np.sum(union)

print(iou_score)

# do I need to round things up...

jaccard = 1 - iou_score
print(jaccard)

# ça marche et ça marche pas mal


# voir comment implementer une loss qui mesure comment avoir les cellules proprement segmentees en comparant EZF vs mon truc
# binariser les images
# binariser le ground truth
# count per cell the number of oversegmentation and of undersegmentation --> how can I do that
# loop over all cells of the ground truth and count how many colors = ids are found in it --> it is a count of oversegmentation
# for undersegmentation use the cells of the prediction image and count how many cells within the prediction cell id are found in the real image that should tell me undersegmentation
# sur le papier ça devrait marcher mais essayer de dessiner le truc...


# print(K.eval(jaccard_loss(array, array2)))
# parameters = {'backend':K}
# print(iou_score(array,array2),parameters)

'''

        Eccentricity of the ellipse that has the same second-moments as the
        region. The eccentricity is the ratio of the focal distance
        (distance between focal points) over the major axis length.
        The value is in the interval [0, 1).
        When it is 0, the ellipse becomes a circle.
    **equivalent_diameter** : float
        The diameter of a circle with the same area as the region.
    **euler_number** : int
        Euler characteristic of region. Computed as number of objects (= 1)
        subtracted by number of holes (8-connectivity).
    **extent** : float
        Ratio of pixels in the region to pixels in the total bounding box.
        Computed as ``area / (rows * cols)``
    **filled_area** : int
        Number of pixels of the region will all the holes filled in. Describes
        the area of the filled_image.
    **filled_image** : (H, J) ndarray
        Binary region image with filled holes which has the same size as
        bounding box.
    **image** : (H, J) ndarray
        Sliced binary region image which has the same size as bounding box.
    **inertia_tensor** : ndarray
        Inertia tensor of the region for the rotation around its mass.
    **inertia_tensor_eigvals** : tuple
        The eigenvalues of the inertia tensor in decreasing order.
    **intensity_image** : ndarray
        Image inside region bounding box.
    **label** : int
        The label in the labeled input image.
    **local_centroid** : array
        Centroid coordinate tuple ``(row, col)``, relative to region bounding
        box.
    **major_axis_length** : float
        The length of the major axis of the ellipse that has the same
        normalized second central moments as the region.
    **max_intensity** : float
        Value with the greatest intensity in the region.
    **mean_intensity** : float
        Value with the mean intensity in the region.
    **min_intensity** : float
        Value with the least intensity in the region.
    **minor_axis_length** : float
        The length of the minor axis of the ellipse that has the same
        normalized second central moments as the region.
    **moments** : (3, 3) ndarray
        Spatial moments up to 3rd order::

            m_ij = sum{ array(row, col) * row^i * col^j }

        where the sum is over the `row`, `col` coordinates of the region.
    **moments_central** : (3, 3) ndarray
        Central moments (translation invariant) up to 3rd order::

            mu_ij = sum{ array(row, col) * (row - row_c)^i * (col - col_c)^j }

        where the sum is over the `row`, `col` coordinates of the region,
        and `row_c` and `col_c` are the coordinates of the region's centroid.
    **moments_hu** : tuple
        Hu moments (translation, scale and rotation invariant).
    **moments_normalized** : (3, 3) ndarray
        Normalized moments (translation and scale invariant) up to 3rd order::

            nu_ij = mu_ij / m_00^[(i+j)/2 + 1]

        where `m_00` is the zeroth spatial moment.
    **orientation** : float
        Angle between the 0th axis (rows) and the major
        axis of the ellipse that has the same second moments as the region,
        ranging from `-pi/2` to `pi/2` counter-clockwise.
    **perimeter** : float
        Perimeter of object which approximates the contour as a line
        through the centers of border pixels using a 4-connectivity.
    **slice** : tuple of slices
        A slice to extract the object from the source image.
    **solidity** : float
        Ratio of pixels in the region to pixels of the convex hull image.
    **weighted_centroid** : array
        Centroid coordinate tuple ``(row, col)`` weighted with intensity
        image.
    **weighted_local_centroid** : array
        Centroid coordinate tuple ``(row, col)``, relative to region bounding
        box, weighted with intensity image.
    **weighted_moments** : (3, 3) ndarray
        Spatial moments of intensity image up to 3rd order::

            wm_ij = sum{ array(row, col) * row^i * col^j }

        where the sum is over the `row`, `col` coordinates of the region.
    **weighted_moments_central** : (3, 3) ndarray
        Central moments (translation invariant) of intensity image up to
        3rd order::

            wmu_ij = sum{ array(row, col) * (row - row_c)^i * (col - col_c)^j }

        where the sum is over the `row`, `col` coordinates of the region,
        and `row_c` and `col_c` are the coordinates of the region's weighted
        centroid.
    **weighted_moments_hu** : tuple
        Hu moments (translation, scale and rotation invariant) of intensity
        image.
    **weighted_moments_normalized** : (3, 3) ndarray
        Normalized moments (translation and scale invariant) of intensity
        image up to 3rd order::

            wnu_ij = wmu_ij / wm_00^[(i+j)/2 + 1]

        where ``wm_00`` is the zeroth spatial moment (intensity-weighted area).

'''


# TODO --> do a test with simple masks for a test


# TODO check image has just one channel otherwise it'll crash
# TODO could also apply additional dilation in case segment is good but edges aren't precise

# NB need KEEP min_area low otherwise will crash --> need a control based on self area --> if self area < min_area --> can cause values to be less than 1 ideally should keep it to 0 but then small cells would cause errors
# see if and how I can fix this bug --> maybe by comparing to its own area and converting min area to a fraction of its own area --> still might be a pb for
# another quick fix is force its length to be 1 at minimum



    # the closer to 1 is underseg and overseg --> the better --> do a test with two images
    # the higher the worse can also add a cutoff to consider stuff
from personal.cellpose.measures_comparison_cellpose_epyseg import measure_overseg_underseg

# super slow but ok...
print('#' * 20)
gt = Img('/D/Sample_images/sample_images_PA/trash_test_mem/mini/focused_Series012/handCorrection.png')[..., 0]
pred = Img('/D/Sample_images/sample_images_PA/trash_test_mem/mini/focused_Series012/handCorrection.tif')[..., 0]
# pred = Img('/D/Sample_images/sample_images_PA/trash_test_mem/mini/focused_Series012/handCorrection.png')[..., 0]
# measure_overseg_underseg(gt, pred)

# TO measure overseg and underseg

underesg_percent, overseg_percent = measure_overseg_underseg(gt, pred, extra_dilation=3, min_area_not_recommended_to_use=30) # , min_area=0
print('underseg percentage:', underesg_percent*100, 'overseg percentage:', overseg_percent*100) # keep NB values must be positive otherwise there is an error somewhere --> the __min_area_do_not_use param was used and set to value superior to some cell size
print('#' * 20)
# pas mal ça a l'air de marcher --> 16 percent
# seems to work --> use this to compare to