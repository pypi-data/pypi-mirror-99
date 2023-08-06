# https://doc.qt.io/qt-5/macos-issues.html --> again a lot of mac specific crap...  but good thing is right click is supported
# set taskbar icon https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
# think how I can handle numpy images with possibility of Z and or t or both and all this on the fly and also the channels --> also allow infinite nb of masks --> masks need always match the image # all this not so easy --> thke time
# TODO --> also allow support for 3D in the same interface --> replace the widget by the 3D one
# maybe if image is stack add button to the list by creating custom item that has a button for next z or next t or prev z or t and also has projection ticker --> would be ok but a bit slow maybe but I really like the idea

from PyQt5.QtWidgets import QToolBar, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import QRect, QSize, QTimer
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QAction, QScrollArea
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QToolButton, QListWidget, QFrame, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QMenu, QApplication
from PyQt5.QtWidgets import QToolBar, QListWidgetItem, QAbstractItemView, QSpinBox, QComboBox, QProgressBar, QVBoxLayout, QDockWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QSize, QItemSelectionModel
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import QAction, QScrollArea, QStackedWidget
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QToolButton, QListWidget, QFrame, QTabWidget
from PyQt5.QtGui import QIcon

# from deprecated_demos.deep_learning_old.Keras_segmentation.test_seg_from_git_site import DeepTA
from PyQt5.QtWidgets import QMenu, QApplication
# do remove this...
from epyseg.draw.widgets.paint import Createpaintwidget
from deprecated_demos.pyqt.eztexteditor import TATextEditor
# 3D VTK viewer or alike
from deprecated_demos.pyqtdlg.ez_generic_dlg import TAGenericDialog
from deprecated_demos.pyqtdlg.volume_crop_dlg import VolumeCropperDialog
from deprecated_demos.pyqtdlg.wshed_dlg import WshedDialog
from deprecated_demos.ta.wshed import Wshed
# from deprecated_demos.ta3d.viewer_solo_3D import MainWindow # TODO replace that with napari --> easy I think
from timeit import default_timer as timer
from PyQt5 import QtWidgets, QtCore, QtGui
from epyseg.img import Img
import numpy as np
import platform
import cv2
# logging
from epyseg.tools.logger import TA_logger

logger = TA_logger()
# doit aussi etre facile de changer le contraste de l'image
# faire des conversion en Qimage d'images qui sont en numpy
# handle 3D images

__VERSION__ = 0.1
__AUTHOR__ = 'Benoit Aigouy'
__NAME__ = 'Deep Tissue Analyzer'
__EMAIL__ = 'baigouy@gmail.com'

from epyseg.draw.widgets.vectorial import VectorialDrawPane


class TissueAnalyzer(QtWidgets.QMainWindow):
    # zoom parameters
    min_scaling_factor = 0.1
    max_scaling_factor = 20
    zoom_increment = 0.05

    def __init__(self, parent=None):
        super().__init__(parent)

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()

        # should fit in 1024x768 (old computer screens)
        window_width = 900
        window_height = 700
        self.setGeometry(
            # QtCore.QRect(centerPoint.x() - window_width / 2, centerPoint.y() - window_height / 2, window_width,
            #              window_height))  # should I rather center on the screen
            QtCore.QRect(centerPoint.x() - int(window_width / 2), centerPoint.y() - int(window_height / 2), window_width,
                     window_height))

        self.scale = 1.0
        self.setWindowTitle(__NAME__ + ' v' + str(__VERSION__))

        self.paint = Createpaintwidget()

        self.list = QListWidget(self)  # a list that contains files to read or play with
        self.list.setFixedWidth(200)  # peut pas etre retaille
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list.selectionModel().selectionChanged.connect(self.selectionChanged)  # connect it to sel change

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.paint)
        self.paint.scrollArea = self.scrollArea

        self.table_widget = TA_tabs(self)  # j'y suis presque

        # create a grid that will contain all the GUI interface
        grid = QGridLayout()
        # grid.setSpacing(10)
        grid.addWidget(self.scrollArea, 0, 0)  # first height then width --> same as in numpy...
        grid.addWidget(self.list, 0, 1)
        # The first parameter of the rowStretch method is the row number, the second is the stretch factor. So you need two calls to rowStretch, like this: --> below the first row is occupying 80% and the second 20%
        grid.setRowStretch(0, 80)
        grid.setRowStretch(2, 20)

        # void QGridLayout::addLayout(QLayout * layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = 0)
        grid.addWidget(self.table_widget, 2, 0, 1, 2)  # spans one row and 2 columns --> aligns perfectly with the above

        # BEGIN TOOLBAR
        # here is how I can add a toolbar below the GUI
        tb = QToolBar()
        toolButton = QToolButton()
        toolButton.setText("Draw")
        tb.addWidget(toolButton)
        tb.addAction("Save")
        tb.addAction("sq...")
        grid.addWidget(tb, 1, 0, 1, 2)
        # END toolbar

        # self.setCentralWidget(self.scrollArea)
        self.setCentralWidget(QFrame())
        self.centralWidget().setLayout(grid)

        # self.statusBar().showMessage('Ready')
        statusBar = self.statusBar()  # sets an empty status bar --> then can add messages in it
        self.paint.statusBar = statusBar

        # rather put a grid in there and add it to the grid

        # maybe put this back
        # self.myQMenuBar = QtWidgets.QMenuBar(self)
        # exitMenu = self.myQMenuBar.addMenu('File')
        # exitAction = QtGui.QAction('Exit', self)
        # exitAction.triggered.connect(QtGui.qApp.quit)
        # exitMenu.addAction(exitAction)

        # Set up menu bar
        self.mainMenu = self.menuBar()
        changeColour = self.mainMenu.addMenu("changeColour")
        changeColourAction = QtWidgets.QAction("change", self)
        changeColour.addAction(changeColourAction)
        changeColourAction.triggered.connect(self.changeColour)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++",
                                 enabled=True, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-",
                                  enabled=True, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S",
                                     enabled=True, triggered=self.defaultSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=True,
                                      checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.testMenu = QMenu("&MetaGenerator", self)
        self.changeModeAct = QAction("Vectorial Mode", self, enabled=True,
                                     checkable=True, triggered=self.changeMode)
        self.testMenu.addAction(self.changeModeAct)

        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.testMenu)

        self.setMenuBar(self.mainMenu)

        # Setup hotkeys
        deleteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.down)

        # center window on screen --> can be done earlier
        # self.center()

        # self.lay.addWidget(self.mainMenu)

        # KEEP IMPORTANT absolutely required to allow DND on window
        self.setAcceptDrops(True)  # KEEP IMPORTANT

    def selectionChanged(self):
        # print(self.list.selectedIndexes())
        # just set current image to sel view
        # pass
        selected_items = self.list.selectedItems()
        if selected_items:
            # print(selected_items[0])
            logger.debug('Loading ' + selected_items[0].toolTip())
            self.statusBar().showMessage('Loading ' + selected_items[0].toolTip())
            self.paint.load(selected_items[0].toolTip())
            self.scaleImage(0)
            self.update()
            self.paint.update()
            # peut etre mettre ça on the fly
            icon = QIcon(QPixmap.fromImage(self.paint.image))
            pixmap = icon.pixmap(24, 24)  # pas mal et vraiment rapide
            icon = QIcon(pixmap)
            # selected_items.setIcon(icon)

            # quite cool --> add icon on the fly when file is loaded --> so cool...
            self.list.currentItem().setIcon(icon)

            # icon = QIcon(url)
            # pixmap = icon.pixmap(24, 24)
            # icon = QIcon(pixmap)
            # import os
            # item = QListWidgetItem(os.path.basename(url), self.list)
            # item.setIcon(icon)

            # faire un load image avec cette image et juste traiter ça
            # get selection
        else:
            logger.debug("Empty selection")
            self.paint.image = None
            self.scaleImage(0)
            self.update()
            self.paint.update()

    def changeMode(self):
        self.paint.vdp.active = self.changeModeAct.isChecked()

    def down(self):
        # print('down')
        if self.paint.vdp.active:
            # print('in')
            self.paint.vdp.removeCurShape()
            self.paint.update()
        # Or put code to implement from code 1

    def changeColour(self):
        # ça dessine un carré effaceur --> pas très utile mais le changement d'icone est cool
        self.paint.change = not self.paint.change
        if self.paint.change:
            pixmap = QtGui.QPixmap(QtCore.QSize(1,
                                                1) * self.paint._clear_size)  # qt a l'air de vraiment bien supporter des curseurs de taille infinie --> bon à savoir mais est-ce portable sur mac et windows ?
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.drawRect(pixmap.rect())
            painter.end()
            cursor = QtGui.QCursor(pixmap)
            QtWidgets.QApplication.setOverrideCursor(cursor)
        else:
            QtWidgets.QApplication.restoreOverrideCursor()

    # not really a smart way --> find a better way to do that
    def zoomIn(self):
        self.statusBar().showMessage('Zooming in',
                                     msecs=200)  # shows message for only a few secs and removes it --> very useful
        self.scaleImage(self.zoom_increment)

    def zoomOut(self):
        self.statusBar().showMessage('Zooming out', msecs=200)
        self.scaleImage(-self.zoom_increment)

    def defaultSize(self):
        self.paint.adjustSize()
        self.scale = 1.0

    # null car respecte pas le w/h ratio --> à fixer --> alterner between w and h
    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.defaultSize()

    def scaleImage(self, factor):
        self.scale += factor
        if self.paint.image is not None:
            self.paint.resize(self.scale * self.paint.image.size())
        else:
            # no image set size to 0, 0 --> scroll pane will auto adjust
            self.paint.resize(QSize(0, 0))
            self.scale -= factor  # reset zoom

        self.paint.scale = self.scale
        self.paint.vdp.scale = self.scale

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scale < self.max_scaling_factor)
        self.zoomOutAct.setEnabled(self.scale > self.min_scaling_factor)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    # allow DND
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    # handle DND on drop
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            urls = []
            for url in event.mimeData().urls():
                urls.append(str(url.toLocalFile()))
            # print(urls)
            # ça marche --> juste à handler le truc

            # update image and rescale
            # CODE BELOW IS MY OWN CODE AND NEED BE MODIFIED OR BE REMOVED

            # self.paint.image = QtGui.QImage(urls[0])  # voilà comment je peux loader l'image
            # TODO faire un set image dans ce truc qui retaille tout pour avoir la meme taille que l'image et eviter des pbs
            # l'ideal serait de tt sauver ds une liste en dur en fait --> serait vraiment un clone de TA
            # self.paint.update()
            # self.paint.setBaseSize(self.paint.image.width(), self.paint.image.height())

            # add all dropped items to the list
            for url in urls:
                # url = '/home/aigouy/mon_prog/Icons/src/main/resources/Icons/1in1.png'
                # icon = QIcon(url)
                # pixmap = icon.pixmap(24, 24)
                # icon = QIcon(pixmap)
                import os
                item = QListWidgetItem(os.path.basename(url), self.list)
                # item.setIcon(icon)
                # item.setText(os.path.basename(url))
                item.setToolTip(url)

                # print("data", item.toolTip()) # can store in tooltip

                # so by status tip things can be grabbed

                # item.setData(10, url)
                # print("data", item.data(10), os.path.basename(url))  # so cool can really  store any data in it I love it and so simple
                self.list.addItem(item)
            # self.list.addItems(urls)

            # self.scaleImage(0)  # no rescale just take original size
            # self.update()
            # CODE ABOVE IS MY OWN CODE AND NEED BE MODIFIED OR BE REMOVED
        else:
            event.ignore()


class TA_tabs(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        # self.tabs.resize(300, 200)
        self.tabs.setFixedHeight(150)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)

        # # I can add a tool bar to the stuff
        # tb = QToolBar()
        # self.tab1.layout.addWidget(tb)
        # toolButton = QToolButton()
        # toolButton.setText("Apple")
        # tb.addWidget(toolButton)
        # tb.addAction("hi")
        # tb.addAction("hello")

        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


# TODO --> FAIRE UN LOAD IMAGE LA DEDANS et faire un retaillage de la fenetre

class Createpaintwidget(QWidget):
    vdp = VectorialDrawPane(active=False, demo=True)
    scrollArea = None
    statusBar = None

    def __init__(self):
        super().__init__()
        # layout = QVBoxLayout()
        # self.setLayout(layout)

        # could be replaced by a real image
        # self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_ARGB32)
        # self.image.fill(QtCore.Qt.red)

        self.image = None
        self.imageDraw = None
        self.cursor = None

        self.drawing = False
        self.brushSize = 30
        self._clear_size = 20
        # self.draw
        self.drawColor = QtGui.QColor(QtCore.Qt.red)
        self.eraseColor = QtGui.QColor(QtCore.Qt.black)
        self.cursorColor = QtGui.QColor(QtCore.Qt.green)
        self.lastPoint = QtCore.QPoint()

        self.change = False
        # KEEP IMPORTANT required to track mouse even when not clicked
        self.setMouseTracking(True)  # KEEP IMPORTANT

        # self.scrollArea = QtGui.QScrollArea()
        # self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)

        # add toolbar
        # exitAct = QAction(QIcon('./../../Icons/src/main/resources/Icons/1in1.png'), 'Exit', self)
        # exitAct.setShortcut('Ctrl+Q')
        # exitAct.triggered.connect(qApp.quit)
        #
        # # just one tool bar --> really cool really love it
        # self.toolbar = self.addToolBar('Exit')
        # self.toolbar.addAction(exitAct)
        #
        # tb = QToolBar()
        # layout.addWidget(tb)
        # toolButton = QToolButton()
        # toolButton.setText("Apple")
        # tb.addWidget(toolButton)
        # tb.addAction("hi")
        # tb.addAction("hello")
        # tbox = QPlainTextEdit()
        # layout.addWidget(tbox)

        #
        #
        # dockLayout = QVBoxLayout()
        # layout.setMenuBar(tb)
        #
        # self.setLayout(dockLayout)

    def load(self, path):
        self.image = QtGui.QImage(path)
        # print(self.image.size())
        width = self.image.size().width()
        height = self.image.size().height()
        top = left = 0

        self.scale = 1.0

        # marche pas avec des grandes images car besoin de connaitre le facteur de zoom si peut pas depasser l'ecran
        self.setGeometry(top, left, width, height)

        # print(top, left, width, height, self.geometry()) # ça ça colle mais
        # somehow size is changed after compared to original size --> so it needs a fix

        self.imageDraw = QtGui.QImage(self.image.size(), QtGui.QImage.Format_ARGB32)
        self.imageDraw.fill(QtCore.Qt.transparent)

        # my crap
        # maybe I can have as many images as I want ????on top
        self.cursor = QtGui.QImage(self.image.size(), QtGui.QImage.Format_ARGB32)
        self.cursor.fill(QtCore.Qt.transparent)
        # end my crap

    def mousePressEvent(self, event):
        self.clickCount = 1
        if self.vdp.active:
            self.vdp.mousePressEvent(event)
            self.update()
            return

        if event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.RightButton:
            self.drawing = True
            zoom_corrected_pos = event.pos() / self.scale
            self.lastPoint = zoom_corrected_pos
            self.drawOnImage(event)

    def mouseMoveEvent(self, event):

        if self.statusBar:
            # print(event.pos)
            zoom_corrected_pos = event.pos() / self.scale
            self.statusBar.showMessage('x=' + str(zoom_corrected_pos.x()) + ' y=' + str(
                zoom_corrected_pos.y()))  # show color and rgb value of it
            # QMainWindow.statusBar().showMessage('x=' + str(zoom_corrected_pos.x()) + ' y=' + str(zoom_corrected_pos.y()))

        if self.vdp.active:
            self.vdp.mouseMoveEvent(event)
            # print("in here 323232")
            # maybe should not update
            # maybe should only update the region of interest --> get field of view of scrollpane

            # viewPortSizeHint
            # self.s

            # print(self.scrollArea.sizeHint())
            # print(self.scrollArea.viewportSizeHint())

            # ça marche pas du tout ça donne pas la taille de la zone vue --> null
            # painter = QtGui.QPainter(self.cursor)
            # print("test ", painter.viewport()) # ça donne la taille de toute l'image
            # painter.end()

            # QWidget::visibleRegion
            # QAbstractScrollArea::viewport
            # print(self.scrollArea.widget().visibleRegion())
            # view region = self.scrollArea.widget().visibleRegion()
            # Only update the visible rect
            region = self.scrollArea.widget().visibleRegion()
            # print(region.boundingRect()) # parfait voilà ce que je veux

            self.update(region)
            return

        self.drawOnImage(event)

    def drawOnImage(self, event):

        zoom_corrected_pos = event.pos() / self.scale

        # ça marche pas mal c'est presque comme dans TA deja --> c'est rapide
        # my crap
        # draw a circle around the mouse --> could be my mouse pointer fake

        if self.drawing and (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.RightButton):  #
            # now drawing or erasing over the image
            painter = QtGui.QPainter(self.imageDraw)
            if event.buttons() == QtCore.Qt.LeftButton:
                painter.setPen(QtGui.QPen(self.drawColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                          QtCore.Qt.RoundJoin))
            else:
                painter.setPen(QtGui.QPen(self.eraseColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                          QtCore.Qt.RoundJoin))

            # print("here")
            # we erase the cursor irrespective of draw or erase

            # if self.change:
            #     r = QtCore.QRect(QtCore.QPoint(), self._clear_size * QtCore.QSize())
            #     r.moveCenter(zoom_corrected_pos)
            #     painter.save()
            #     painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
            #     painter.eraseRect(r)
            #     painter.restore()
            # else:
            # print(self.lastPoint, zoom_corrected_pos)
            if self.lastPoint != zoom_corrected_pos:
                painter.drawLine(self.lastPoint, zoom_corrected_pos)
            else:
                # if zero length line then draw point instead
                painter.drawPoint(zoom_corrected_pos)
            painter.end()

            # painter = QtGui.QPainter(self.imageDraw)
            # on efface le precedent pointeur
            # r = QtCore.QRect(self.lastPoint, self._clear_size * QtCore.QSize()) # ça marche à peu près mais faut tester
            # r.moveCenter(zoom_corrected_pos)
            # painter.save()
            # painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
            # painter.eraseRect(r)
            # painter.restore()
            # painter.end()
            # self.lastPoint = zoom_corrected_pos

            self.lastPoint = zoom_corrected_pos
            # self.update()
            # we update later so no need to update now
            # region = self.scrollArea.widget().visibleRegion()
            # self.update(region)

        # Drawing the cursor TODO add boolean to ask if drawing cursor should be shown
        painter = QtGui.QPainter(self.cursor)
        # on efface le precedent pointeur #je pourrais meme effacer le visible rect complet ? Est-ce plus long
        r = QtCore.QRect(QtCore.QPoint(), self._clear_size * QtCore.QSize() * self.brushSize)
        r.moveCenter(zoom_corrected_pos)
        painter.save()
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        painter.eraseRect(r)
        painter.restore()
        # on dessine le nouveau
        painter.setPen(QtGui.QPen(self.cursorColor, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.drawEllipse(zoom_corrected_pos, self.brushSize / 2.,
                            self.brushSize / 2.)  # ça marche presque ma correction de position*(self.imageDraw.width()/self.geometry().width()) # peut etre faut il corriger mieux que ça
        painter.end()
        # logger.debug('drawing cursor')
        region = self.scrollArea.widget().visibleRegion()
        self.update(region)
        # self.update()
        # end my crap

        # if event.buttons() == QtCore.Qt.NoButton:
        #     print("Simple mouse motion")
        # elif event.buttons() == QtCore.Qt.LeftButton:
        #     print("Left click drag")
        # elif event.buttons() == QtCore.Qt.RightButton:
        #     print("Right click drag")
        #
        # if event.button() == QtCore.Qt.LeftButton:
        #     print("Left Button Clicked")
        # elif event.button() == QtCore.Qt.RightButton:
        #     # do what you want here
        #     print("Right Button Clicked")

        # if self.drawing and event.buttons() == QtCore.Qt.LeftButton:
        # print("here draw ", event.buttons())

        # if self.drawing and event.buttons() == QtCore.Qt.RightButton:
        #     # print("here draw ", event.buttons())
        #     painter = QtGui.QPainter(self.imageDraw)
        #     painter.setPen(QtGui.QPen(self.drawColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
        #                               QtCore.Qt.RoundJoin))
        #     if self.change:
        #         r = QtCore.QRect(QtCore.QPoint(), self._clear_size * QtCore.QSize())
        #         r.moveCenter(zoom_corrected_pos)
        #         painter.save()
        #         painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        #         painter.eraseRect(r)
        #         painter.restore()
        #     else:
        #         painter.drawLine(self.lastPoint, zoom_corrected_pos)
        #     painter.end()
        #     self.lastPoint = zoom_corrected_pos
        #     self.update()

        # c'est super slow vaut peut etre mieux le black drawing instead
        # erase rect is TOO SLOW --> KEEPING BLACK DRAWING INSTEAD
        # if self.drawing and event.buttons() == QtCore.Qt.RightButton:
        #     # Erase stuff
        #     # print("here erase")
        #     painter = QtGui.QPainter(self.imageDraw)
        #     # on efface le precedent pointeur
        #     r = QtCore.QRect(QtCore.QPoint(), self._clear_size * QtCore.QSize()) # ça marche à peu près mais faut tester
        #     r.moveCenter(zoom_corrected_pos)
        #     painter.save()
        #     painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        #
        #     # need to draw a line of erase between points self.lastPoint, zoom_corrected_pos
        #     # --> that is super complicated --> forget --> need to do non overlapping squares along a line
        #
        #     painter.eraseRect(r)
        #     painter.restore()
        #     painter.end()
        #     self.lastPoint = zoom_corrected_pos
        #     # self.lastPoint = zoom_corrected_pos
        #
        #     # region = self.scrollArea.widget().visibleRegion()
        #     #
        #     # self.update(region)
        #     self.update()

    def mouseReleaseEvent(self, event):

        if self.vdp.active:
            self.vdp.mouseReleaseEvent(event)
            self.update()  # required to update drawing
            return

        if event.button == QtCore.Qt.LeftButton:
            self.drawing = False

        if self.clickCount == 1:
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.updateButtonCount)
        # else:
        #     # Perform double click action.
        #     self.message = "Double Click"
        #     print("Double click")
        # self.update()

        # REMOVE THIS THIS IS JUST TO SHOW AND SAVE THE IMAGE DRAWN
        # self.imageDraw.save('./../trash/mask.png')
        # ça marche --> ça ne sauve en effet que le mask ---> TROP COOL --> TRES FACILE DE RECUPERER CE QUI A ETE DESSINE

    # SOOO SIMPLE I LOVE IT....
    # adds context/right click menu but only in vectorial mode
    def contextMenuEvent(self, event):
        # adds context/right click menu but only in vectorial mode
        if not self.vdp.active:
            return

        cmenu = QMenu(self)
        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()

    def updateButtonCount(self):
        self.clickCount = 1

    def mouseDoubleClickEvent(self, event):
        self.clickCount = 2
        self.vdp.mouseDoubleClickEvent(event)

    def paintEvent(self, event):
        canvasPainter = QtGui.QPainter(self)
        # the scrollpane visible region
        visibleRegion = self.scrollArea.widget().visibleRegion()
        # the corresponding rect
        visibleRect = visibleRegion.boundingRect()
        # the visibleRect taking zoom into account
        scaledVisibleRect = QRect(visibleRect.x() / self.scale, visibleRect.y() / self.scale,
                                  visibleRect.width() / self.scale, visibleRect.height() / self.scale)
        if self.image is None:
            canvasPainter.eraseRect(visibleRect)
            canvasPainter.end()
            return
        canvasPainter.drawImage(visibleRect, self.image, scaledVisibleRect)
        # canvasPainter.drawImage(self.rect(), self.image, self.image.rect())  # KEEP ORIGINAL
        if not self.vdp.active:
            # canvasPainter.drawImage(self.rect(), self.imageDraw, self.imageDraw.rect()) # KEEP ORIGINAL
            canvasPainter.drawImage(visibleRect, self.imageDraw, scaledVisibleRect)
            # should draw the cursor
        canvasPainter.drawImage(visibleRect, self.cursor, scaledVisibleRect)
        # canvasPainter.drawImage(self.rect(), self.cursor, self.cursor.rect())# KEEP ORIGINAL
        if self.vdp.active:
            self.vdp.paintEvent(canvasPainter, scaledVisibleRect)  # to draw shape # here too would be cool
        canvasPainter.end()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = TissueAnalyzer()
    w.show()
    sys.exit(app.exec_())
