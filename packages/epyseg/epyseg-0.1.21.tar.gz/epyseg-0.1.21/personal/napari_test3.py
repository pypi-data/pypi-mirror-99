# napari does not seem to have a pen/free drawing layer --> can i hack one though ???
# maybe one can hack the multiline with autopoints and removing consecutive dupes ????

# can you elaborate?
# TODO MEGA BEST TOP The main napari viewer is an instance of QMainWindow 1 and when you create a viewer instance with viewer = napari.Viewer(), the QtMainWindow object is available at viewer.window._qt_window. If you’re looking to add the whole napari window to some QLayout in some external program, that’s the object you need to add.

import numpy as np
from skimage import data
import napari


# create the list of polygons
triangle = np.array([[11, 13], [111, 113], [22, 246]])
person = np.array([[505, 60], [402, 71], [383, 42], [251, 95], [212, 59],
                   [131, 137], [126, 187], [191, 204], [171, 248], [211, 260],
                   [273, 243], [264, 225], [430, 173], [512, 160]])
building = np.array([[310, 382], [229, 381], [209, 401], [221, 411],
                     [258, 411], [300, 412], [306, 435], [268, 434],
                     [265, 454], [298, 461], [307, 461], [307, 507],
                     [349, 510], [352, 369], [330, 366], [330, 366]])
polygons = [triangle, person, building]

with napari.gui_qt():
    # add the image
    viewer = napari.view_image(data.camera(), name='photographer')

    # add the polygons
    layer = viewer.add_shapes(polygons, shape_type='polygon', edge_width=5,
                              edge_color='coral', face_color='royalblue')