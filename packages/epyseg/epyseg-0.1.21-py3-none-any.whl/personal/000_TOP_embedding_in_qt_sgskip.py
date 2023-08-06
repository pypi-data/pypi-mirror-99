# ce qui est vraiment cool c'est que la taille du graphe s'adapte et c'est vraiment ce que je veux
# voir comment monter des graphes mais du coup ça devrait pas etre trop dur en fait
# par defaut les graphes peuvent prendre tt l'espace qui reste de la row ou de la colonne
# finaliser mon code pour le soft de creation d'images
# pb ce truc sera pas portable en integration dans mon code car peut pas displayer du pyqt dans autre chose --> sauf peut etre en recuperant le
# I could contrain the image to a certain size and recover the display and that should really work...
# TODO --> just try that --> ça a l'air de marcher donc ça va etre du gateau ke pense de tout mettre maintenant
"""
===============
Embedding in Qt
===============

Simple Qt application embedding Matplotlib canvases.  This program will work
equally well using Qt4 and Qt5.  Either version of Qt can be selected (for
example) by setting the ``MPLBACKEND`` environment variable to "Qt4Agg" or
"Qt5Agg", or by first importing the desired version of PyQt.
"""

# really cool --> maybe use that to display my own graphs --> pretty cool

import sys
import time

import numpy as np
from PyQt5 import QtCore, QtGui, QtSvg
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath, QLinearGradient, QPolygon, QPixmap, QImage, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView, qApp, QActionGroup, QMessageBox, QFileDialog, QMenu, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QSizePolicy, QPushButton,  QComboBox, QSpacerItem, QRadioButton, QToolButton, QCheckBox

from PyQt5.QtCore import pyqtSignal, Qt
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5 # KEEP IT WORKS EVEN THOUGH IT DOES NOT LOOK LIKE IT

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(QLabel('this is a QT embedding test'))
        layout.addWidget(static_canvas)
        # self.addToolBar(NavigationToolbar(static_canvas, self)) # put this back to get the matplotlib navigation toolbar back
        # can I make it interactive such as drawing a square on it ...
        # so it's rather easy to get things to work then maybe even in my code for the ezfig --> can I even let python use the interface


        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            50, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Use fixed vertical limits to prevent autoscaling changing the scale
        # of the axis.
        self._dynamic_ax.set_ylim(-1.1, 1.1)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
