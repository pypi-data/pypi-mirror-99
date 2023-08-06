import napari
import numpy as np
from PyQt5 import QtCore, QtGui, QtSvg
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath, QLinearGradient, QPolygon, QPixmap, QImage, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView, qApp, QActionGroup, QMessageBox, QFileDialog, QMenu, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QSizePolicy, QPushButton,  QComboBox, QSpacerItem, QRadioButton, QToolButton, QCheckBox

from PyQt5.QtCore import pyqtSignal, Qt
with napari.gui_qt():
    viewer = napari.Viewer()
    main_window = viewer.window._qt_window
    qt_viewer = viewer.window.qt_viewer
    assert isinstance(qt_viewer, QWidget)  # True
    assert isinstance(main_window, QWidget)  # True

