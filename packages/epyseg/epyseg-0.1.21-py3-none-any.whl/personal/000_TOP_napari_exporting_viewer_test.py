
# https://matplotlib.org/3.2.1/gallery/user_interfaces/embedding_in_qt_sgskip.html
from epyseg.img import Img
from skimage import data
import napari
import numpy as np
from PyQt5 import QtCore, QtGui, QtSvg
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath, QLinearGradient, QPolygon, QPixmap, QImage, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView, qApp, QActionGroup, QMessageBox, QFileDialog, QMenu, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QSizePolicy, QPushButton,  QComboBox, QSpacerItem, QRadioButton, QToolButton, QCheckBox

from PyQt5.QtCore import pyqtSignal, Qt


class MainWindow2(QMainWindow):

    # QMainWindow doesn't have a closed signal, so we'll make one.
    closed = pyqtSignal()

    def __init__(self, parent=None, qt_viewer=None):
        print(parent)
        QMainWindow.__init__(self, parent)
        # QMainWindow.__init__(self, None)
        self.parent = parent

        self._qt_window = self
        self._qt_window.setAttribute(Qt.WA_DeleteOnClose)
        self._qt_window.setUnifiedTitleAndToolBarOnMac(True)
        self._qt_center = QWidget(self._qt_window)
        self._qt_window.setCentralWidget(self._qt_center)


        self._qt_center.setLayout(QVBoxLayout())
        # label =
        self._qt_center.layout().addWidget(QLabel('MainWindow2'))
        self._qt_center.layout().addWidget(qt_viewer)
        # self._qt_center.layout().addWidget(parent) # almost there it seems
        # self._qt_center.layout().addItem(parent.layout().children()[0])
        # je n'y arrive pas



        # parent.show()
        # self._qt_center = QWidget(parent)

        # self._qt_window = QMainWindow()
        # self._qt_window.setAttribute(Qt.WA_DeleteOnClose)
        # self._qt_window.setUnifiedTitleAndToolBarOnMac(True)
        # self._qt_center = QWidget(self._qt_window)
        # self._qt_center = parent._qt_center

        # self.setCentralWidget(parent)
        # self.addDockWidget(parent)
        self._qt_center.show()
        self.show()


    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

if __name__ == '__main__':
    # ça marche vraiment...
    with napari.gui_qt():
        # viewer = napari.Viewer()
        viewer = napari.Viewer(ndisplay = 3)# 3D viewer
        # viewer = napari.view_image(data.astronaut(), rgb=True)
        print(viewer.window._qt_window)
        # viewer.show()
        # viewer.window._qt_window.hide()

        main_window = viewer.window._qt_window
        main_window.hide()
        qt_viewer = viewer.window.qt_viewer
        assert isinstance(qt_viewer, QWidget)  # True
        assert isinstance(main_window, QWidget)  # True

        # viewer.add_image(data.astronaut(), rgb=True) # ça marche je peux ajouter une image --> vraiment pas mal en fait
        # viewer.grid_view() # opposite: viewer.stack_view() # marche pas
        #viewer.stack_view()

        # TOP KEEP BEST TODO REMOVE IMAGE FROM VIEWER
        # viewer.layers.pop(0) # this is how ones removes images --> quite cool in fact
        # viewer.add_image(data.cell())  # ça marche je peux ajouter une image --> vraiment pas mal en fait



        # MARCHE AUSSI EN 3D
        # viewer.theme = 'light' # to change theme (doesn't work for all --> a bug somewhere)
        image = Img("/home/aigouy/Bureau/Image1.tif")
        print(image.shape)
        viewer.add_image(image) #
        # TODO TOP GREAT WAY OF CHANGING THINGS here is how one can change scale dynamically
        viewer.layers[0].scale = [3, 1, 1]


        # ça marche je peux hider la window et sinon la montrer dans autre chose aussi
        test = MainWindow2(main_window, qt_viewer)
        test.show()


