import numpy as np
import napari

# we use qtpy as an abstraction layer on most of the Qt goodies
from qtpy.QtWidgets import QPushButton

with napari.gui_qt():
    viewer = napari.Viewer()
    layer = viewer.add_image(np.random.random((512, 512)))

    def add_layer():
        viewer.add_image(np.random.random((512, 512)))

    def randomize_last_layer():
        try:
            layer = viewer.layers[-1]
            layer.data = np.random.random((512, 512))
        except IndexError:
            pass

    # create buttons
    add_button = QPushButton("add layer")
    update_button = QPushButton("update layer")

    # hook up the "clicked" event to a callback:
    # https://doc.qt.io/qt-5/qabstractbutton.html#clicked
    add_button.clicked.connect(add_layer)
    update_button.clicked.connect(randomize_last_layer)

    # show the buttons
    add_button.show()
    update_button.show()