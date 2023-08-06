# TODO test the python viewer napari maybe...


# check 3D and co...
# try use the napari viewer as much as possible and TA is largely compatible conceptually with napari and its layer concept --> good


# URGENT TODO whenever I do anything to the image --> save in the db that I did something so that I know everything need be updated --> will prevent a lot of bugs I had in TA

# TODO connect the watershed and do a preview --> add a preview in the main window
#

# need keep zoom across images --> test it

# TODO le plus simple pr faire des crops serait un range fait par deux spinner
# peut etre besoin de ce truc de crop que pr la 3D ??? --> faire un GUI que pour ça
# sinon faire un simple browser
# faire un code dynamic pr ça avec les dimensions names et ou indices... --> pas trop bete je pense
# ou alors faire çe en texte --> passer ça entant que parametre --> # super puissant mais necessite de connaitre le code --> seulement pr les pros mais ok peut etre

# TODO read this https://blog.miguelgrinberg.com/post/how-to-make-python-wait to better handle wait especially for 3D stacks
# TODO use the same shortcuts for 2D and 3D to avoid issues
# find a way to pass shortcuts from main GUI to 3D without using its own stuff ???
# next try real machine learning...

# TODO handle dimensions better

# TODO use slider to display images and browse anything easily
# think where to put them

# added support for 3D cropping

# https://doc.qt.io/qt-5/macos-issues.html --> again a lot of mac specific crap...  but good thing is right click is supported
# set taskbar icon https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
# think how I can handle numpy images with possibility of Z and or t or both and all this on the fly and also the channels --> also allow infinite nb of masks --> masks need always match the image # all this not so easy --> thke time
# TODO --> also allow support for 3D in the same interface --> replace the widget by the 3D one
# maybe if image is stack add button to the list by creating custom item that has a button for next z or next t or prev z or t and also has projection ticker --> would be ok but a bit slow maybe but I really like the idea
# from PyQt5.QtCore import QSettings, QPoint
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

# should I try 3D segmentation and should I  do it in 2D --> maybe --> could at least give it a try

# add open or save do all as single
# all
# sel
# for processing
# try centralize everything can pass function and parameters anyway so should not be too hard
# TODO try Qthread from pyqt when loading image to avid freeze

# TODO --> rather handle my own image format to avoid pbs and make it compatible to QImage to allow compatibility
# doit aussi etre facile de changer le contraste de l'image
# verif que le wshed se comporte comme dans TA et verif si ça marche mieux en uint8 qu'en float au cas où il y ait un bug dans l'algo

# allow high dpi scaling only on systems that support it it's really cool and I should have this in all main classes of PyQT stuff
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

__MAJOR__ = 0
__MINOR__ = 1
__MICRO__ = 0
__RELEASE__='b' #https://www.python.org/dev/peps/pep-0440/#public-version-identifiers --> alpha beta, ...
__VERSION__ = ''.join([str(__MAJOR__), '.', str(__MINOR__), '.'.join([str(__MICRO__)]) if __MICRO__ != 0 else '', __RELEASE__])
__AUTHOR__ = 'Benoit Aigouy'
__NAME__ = 'Deep Tissue Analyzer'
__EMAIL__ = 'baigouy@gmail.com'

# shall I start and recode the wshed ???? --> should I also do it in C ??? with a float array to be sure it will always work ?
# just try default watershed then try segmentation of the stuff
# try code the watershed again --> first use the python one then mine
# try also see the gaussian blurs and the fast gaussian maybe also compare to the random walker data as it seems relatively efficient --> a tester


class TissueAnalyzer(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()

        # should fit in 1024x768 (old computer screens)
        window_width = 900
        window_height = 700
        self.setGeometry(
            # QtCore.QRect(centerPoint.x() - window_width / 2, centerPoint.y() - window_height / 2, window_width,
            #              window_height))  # should I rather center on the screen
            QtCore.QRect(centerPoint.x() - int(window_width / 2), centerPoint.y() - int(window_height / 2),
                         window_width,
                         window_height))

        # set the window icon
        self.setWindowIcon(QtGui.QIcon('./../../IconsPA/src/main/resources/Icons/ico_packingAnalyzer2.gif'))

        # zoom parameters
        self.scale = 1.0
        self.min_scaling_factor = 0.1
        self.max_scaling_factor = 20
        self.zoom_increment = 0.05

        self.setWindowTitle(__NAME__ + ' v' + str(__VERSION__))

        self.paint = Createpaintwidget()

        # initiate 2D image for 2D display
        self.img = None
        # initiate 3D volume for 3D display
        self.vol = None
        # initialize cropping properties
        self.cropValues = None

        # add a dockable area with the channels --> could be a good idea maybe --> but think about it

        # this contains all the dimension sliders
        self.dimensionSliders = []

        self.dockedDimensionWidget = QDockWidget("Dimensions", self)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           self.dockedDimensionWidget)  # BottomDockWidgetArea # LeftDockWidgetArea # c'est ici qu'on ajoute le dockable element et sa position
        self.dockedWidgetInDimension = QWidget(self)
        self.dockedDimensionWidget.setWidget(self.dockedWidgetInDimension)
        self.dockedWidgetInDimension.setLayout(QVBoxLayout())

        # self.dockedWidget.hide()
        self.dockedDimensionWidget.hide()

        # ui.tabWidget.setStyleSheet("QTabWidget::pane { border: 0; }");
        # self.setStyleSheet("QMainWindow::separator {width: 1px; border: none;}");

        # self.dockedWidgetInDimension.layout().setSpacing(0)


        # for i in range(5):
        #     self.dockedWidget.layout().addWidget(QPushButton("{}".format(i)))
        # end dockable area

        self.list = QListWidget(self)  # a list that contains files to read or play with
        # self.list.setFixedWidth(200)  # peut pas etre retaille
        # self.list.setMaximumWidth(300)
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list.selectionModel().selectionChanged.connect(self.selectionChanged)  # connect it to sel change

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.paint)
        self.paint.scrollArea = self.scrollArea

        self.table_widget = QWidget()
        table_widget_layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # self.tabs.resize(300, 200)
        # self.tabs.setFixedHeight(150)

        # Add tabs
        self.tabs.addTab(self.tab1, "Segmentation")
        self.tabs.addTab(self.tab2, "Analysis")
        self.tabs.addTab(self.tab3, "Image browsing")

        # Create first tab
        self.tab1.layout = QVBoxLayout()
        self.pushButton1 = QPushButton("Watershed segmentation")
        self.pushButton1.clicked.connect(self.run_watershed)
        self.tab1.layout.addWidget(self.pushButton1)

        # self.pushButton2 = QPushButton("Deep learning segmentation")
        # self.pushButton2.clicked.connect(self.deep_learning)
        # self.tab1.layout.addWidget(self.pushButton2)


        self.tab3.layout = QVBoxLayout()
        # self.tab3.layout.addWidget(QPushButton("test button"))
        self.tab3.setLayout(self.tab3.layout)

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
        table_widget_layout.addWidget(self.tabs)
        self.table_widget.setLayout(table_widget_layout)








        # voilà le stackwidget --> et comment on ajoute des trucs dedans --> permet de ne montrer que certains widgets
        self.Stack = QStackedWidget(self)
        self.volumeViewer = QWidget()
        # ça c'est juste la layout du stack --> on s'en fout

        # TODO replace that with napari
        # self.volumeViewerUI()
        self.Stack.addWidget(self.scrollArea)
        # self.Stack.addWidget(self.volumeViewer)

        # create a grid that will contain all the GUI interface
        self.grid = QGridLayout()
        # grid.setSpacing(10)

        # grid.addWidget(self.scrollArea, 0, 0)  # first height then width --> same as in numpy...
        self.grid.addWidget(self.Stack, 0, 0)  # first height then width --> same as in numpy...
        self.grid.addWidget(self.list, 0, 1)
        # The first parameter of the rowStretch method is the row number, the second is the stretch factor. So you need two calls to rowStretch, like this: --> below the first row is occupying 80% and the second 20%
        self.grid.setRowStretch(0, 75)
        self.grid.setRowStretch(2, 25)

        # first col 75% second col 25% of total width
        self.grid.setColumnStretch(0, 75)
        self.grid.setColumnStretch(1, 25)

        # void QGridLayout::addLayout(QLayout * layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = 0)
        self.grid.addWidget(self.table_widget, 2, 0, 1, 2)  # spans over one row and 2 columns

        # BEGIN TOOLBAR
        # here is how I can add a toolbar below the GUI

        # pen spin box and connect
        self.penSize = QSpinBox(objectName='penSize')
        self.penSize.setSingleStep(1)
        self.penSize.setRange(1, 256)
        self.penSize.setValue(3)
        self.penSize.valueChanged.connect(self.penSizechange)

        self.channels = QComboBox(objectName='channels')
        self.channels.addItem("merge")
        # self.channels.addItem("0")
        # self.channels.addItems(["1", "2", "3"])
        self.channels.currentIndexChanged.connect(self.channelChange)

        tb = QToolBar()

        # tb.setFloatable(True)
        # tb.setStyle(QStyle.PE_IndicatorToolBarHandle)
        # tb.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        # tb.setHidden(True)
        # tb.setFloatable(True) # marche pas... tant pis
        toolButton = QToolButton()
        toolButton.setText("Draw")
        tb.addWidget(self.channels)
        tb.addWidget(toolButton)
        tb.addAction("Save")

        tb.addAction("sq...")
        tb.addWidget(self.penSize)

        pushButton1 = QPushButton("pbar")
        pushButton1.clicked.connect(
            self.simulate_progress_in_progressbar)  # someFunctionCalledFromAnotherThread # load_long_process
        tb.addWidget(pushButton1)

        cropVolumeButton = QPushButton("crop vol")
        cropVolumeButton.clicked.connect(
            self.cropVolume)  # someFunctionCalledFromAnotherThread # load_long_process
        tb.addWidget(cropVolumeButton)

        createVideoButton = QPushButton('--> video from 3D')
        createVideoButton.clicked.connect(
            self.create_a_movie_from_3D_stack_video)  # someFunctionCalledFromAnotherThread # load_long_process
        tb.addWidget(createVideoButton)

        createVideoFramesButton = QPushButton('--> series of imgs for video from 3D')
        createVideoFramesButton.clicked.connect(
            self.create_a_movie_from_3D_stack_individual_frames)  # someFunctionCalledFromAnotherThread # load_long_process
        tb.addWidget(createVideoFramesButton)

        snap3DVolumeButton = QPushButton('--> snap from 3D')
        snap3DVolumeButton.clicked.connect(
            self.snap_3D_volume)  # someFunctionCalledFromAnotherThread # load_long_process
        tb.addWidget(snap3DVolumeButton)

        # the 4 lines below are just for a test
        self.textEditor = TATextEditor()
        textEditor = QPushButton("text editor")
        textEditor.clicked.connect(self.openTextEditor)  # someFunctionCalledFromAnotherThread # load_long_process
        tb.addWidget(textEditor)

        self.grid.addWidget(tb, 1, 0, 1, 2)
        # END toolbar

        # self.setCentralWidget(self.scrollArea)
        self.setCentralWidget(QFrame())
        self.centralWidget().setLayout(self.grid)

        # self.statusBar().showMessage('Ready')
        statusBar = self.statusBar()  # sets an empty status bar --> then can add messages in it
        self.paint.statusBar = statusBar

        # add progress bar to status bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        statusBar.addWidget(self.progress)

        # rather put a grid in there and add it to the grid

        # maybe put this back
        # self.myQMenuBar = QtWidgets.QMenuBar(self)
        # exitMenu = self.myQMenuBar.addMenu('File')
        # exitAction = QtGui.QAction('Exit', self)
        # exitAction.triggered.connect(QtGui.qApp.quit)
        # exitMenu.addAction(exitAction)

        # Set up menu bar
        self.mainMenu = self.menuBar()

        self.zoomInAct = QAction("Zoom &In (25%)", self,  # shortcut="Ctrl++",
                                 enabled=True, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self,  # shortcut="Ctrl+-",
                                  enabled=True, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self,  # shortcut="Ctrl+S",
                                     enabled=True, triggered=self.defaultSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=True,
                                      checkable=True,  # shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.testMenu = QMenu("&Mode", self)
        self.changeModeAct = QAction("Vectorial Mode", self, enabled=True,
                                     checkable=True, triggered=self.changeMode)
        self.testMenu.addAction(self.changeModeAct)
        self.replaceWidgetAct = QAction("3D viewer", self, enabled=True,
                                        triggered=self.replaceWidget)
        self.testMenu.addAction(self.replaceWidgetAct)

        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.testMenu)

        self.setMenuBar(self.mainMenu)

        # Setup hotkeys for whole system
        # Delete selected vectorial objects
        deleteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.down)
        deleteShortcut.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        # set drawing window fullscreen
        fullScreenShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        fullScreenShortcut.activated.connect(self.fullScreen)
        fullScreenShortcut.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        # exit from full screen TODO add quit the app too ??
        escapeShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        escapeShortcut.activated.connect(self.escape)
        escapeShortcut.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        # Show/Hide the mask
        escapeShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_H), self)
        escapeShortcut.activated.connect(self.showHideMask)
        escapeShortcut.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        zoomPlus = QtWidgets.QShortcut("Ctrl+Shift+=", self)
        zoomPlus.activated.connect(self.zoomIn)
        zoomPlus.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        zoomPlus2 = QtWidgets.QShortcut("Ctrl++", self)
        zoomPlus2.activated.connect(self.zoomIn)
        zoomPlus2.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        zoomMinus = QtWidgets.QShortcut("Ctrl+Shift+-", self)
        zoomMinus.activated.connect(self.zoomOut)
        zoomMinus.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        zoomMinus2 = QtWidgets.QShortcut("Ctrl+-", self)
        zoomMinus2.activated.connect(self.zoomOut)
        zoomMinus2.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        # all of this is now quite good just need specify output folder and/or output name

        save3DVolumeframe = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S), self)
        save3DVolumeframe.activated.connect(self.snap_3D_volume)
        save3DVolumeframe.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        save3DVolumeframes = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_T), self)
        save3DVolumeframes.activated.connect(self.create_a_movie_from_3D_stack_individual_frames)
        save3DVolumeframes.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        createMovieFromVol = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_V), self)
        createMovieFromVol.activated.connect(self.create_a_movie_from_3D_stack_video)
        createMovieFromVol.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        spaceShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), self)
        spaceShortcut.activated.connect(self.nextFrame)
        spaceShortcut.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        backspaceShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Backspace), self)
        backspaceShortcut.activated.connect(self.prevFrame)
        backspaceShortcut.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        # if press enter --> run wshed
        # enterShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self)
        enterShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self)  # voila
        enterShortcut.activated.connect(self.runWshed)
        enterShortcut.setContext(QtCore.Qt.ApplicationShortcut)  # make sure the shorctut always remain active

        # center window on screen --> can be done earlier
        # self.center()

        # self.lay.addWidget(self.mainMenu)

        # KEEP IMPORTANT absolutely required to allow DND on window
        self.setAcceptDrops(True)  # KEEP IMPORTANT

    # def volumeViewerUI(self):
    #     # layout = QFormLayout()
    #     # layout.addRow("Name", QLineEdit())
    #     # layout.addRow("Address", QLineEdit())
    #     # # self.setTabText(0,"Contact Details")
    #     # self.stack1.setLayout(layout)
    #     # instead get the napari view there
    #     self.v3d = MainWindow()
    #     self.v3d.finalize_load()
    #     self.v3d.finalize_load2()
    #
    #     # self.frame = Qt.QFrame()
    #     # self.vl = Qt.QVBoxLayout()
    #     # self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
    #     # self.vl.addWidget(self.vtkWidget)
    #     #
    #     # self.ren = vtk.vtkRenderer()
    #     # self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
    #     # self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
    #     #
    #     # # Create source
    #     # source = vtk.vtkSphereSource()
    #     # source.SetCenter(0, 0, 0)
    #     # source.SetRadius(5.0)
    #     #
    #     # # Create a mapper
    #     # mapper = vtk.vtkPolyDataMapper()
    #     # mapper.SetInputConnection(source.GetOutputPort())
    #     #
    #     # # Create an actor
    #     # actor = vtk.vtkActor()
    #     # actor.SetMapper(mapper)
    #     #
    #     # self.ren.AddActor(actor)
    #     #
    #     # self.ren.ResetCamera()
    #     #
    #     # self.frame.setLayout(self.vl)
    #     # self.setCentralWidget(self.frame)
    #     #
    #     # self.show()
    #     # self.iren.Initialize()
    #     # self.iren.Start()
    #     self.volumeViewer.setLayout(
    #         self.v3d.vl)  # TROP cool ça marche mais maintenant faudra tt bien connecter et demander si 2D ou 3D en fonction des datas
    #
    # # def load_long_process(self):
    # #     print('begin')
    # #     self.img = Img(self.list.item(0).toolTip())
    # #     print('done')

    def channelChange(self, i):
        # update displayed image depending on channel
        # dqqsdqsdqsd
        # pass
        # try change channel if
        if self.img is not None:
            # print('in', self.img.metadata)
            if self.Stack.currentIndex() == 0:
                # need copy the image --> implement that
                # print(self.img[..., i].copy())
                # print(self.img[..., i])
                if i == 0:
                    self.paint.setImage(self.img)
                    # print('original', self.img.metadata)
                else:
                    # print('modified0', self.img.metadata)
                    channel_img = self.img.imCopy(c=i - 1)  # it's here that it is affected
                    # print('modified1', self.img.metadata)
                    # print('modified2', channel_img.metadata)
                    self.paint.setImage(channel_img)
                self.paint.update()
            else:
                # logger.error("Not implemented yet TODO add support for channels in 3D viewer")
                # sdqdqsdsqdqsd
                self.loadVolume()

    def penSizechange(self):
        self.paint.brushSize = self.penSize.value()
        # self.update() # too slow if I update --> avoid
        # self.l1.setFont(QFont("Arial", size))

    def selectionChanged(self):
        # print(self.list.selectedIndexes())
        # just set current image to sel view
        # pass return
        # restore mask if it was deactivated
        self.paint.maskVisible = True
        # self.img = None

        # mon truc threade ne marche pas --> do that another day need understand signal and connect to get it to work
        # if True:
        #     self.someFunctionCalledFromAnotherThread()
        #     return

        selected_items = self.list.selectedItems()
        if selected_items:
            start = timer()
            if self.img is not None:
                # make sure we don't load the image twice
                if selected_items[0].toolTip() != self.img.metadata['path']:
                    self.img = Img(selected_items[0].toolTip())
                    logger.debug("took " + str(timer() - start) + " secs to load image")
                else:
                    logger.debug("image already loaded --> ignoring")
            else:
                self.img = Img(selected_items[0].toolTip())
                logger.debug("took " + str(timer() - start) + " secs to load image")

        if self.img is not None:
            # update channels
            # selection = self.channels.itemData(self.channels.currentIndex())
            # selection = self.channels.currentData()
            selection = self.channels.currentIndex()
            self.channels.disconnect()
            # print('sel', selection)
            self.channels.clear()
            comboData = ['merge']
            if self.img.has_c():
                for i in range(self.img.get_dimension('c')):
                    comboData.append(str(i))
            logger.debug('channels found ' + str(comboData))
            self.channels.addItems(comboData)
            # index = self.channels.findData(selection)

            # print("data", index)
            if selection != -1 and selection < self.channels.count():
                self.channels.setCurrentIndex(selection)
                # self.channelChange(selection)
            else:
                self.channels.setCurrentIndex(0)
                # self.channelChange(0)
            self.channels.currentIndexChanged.connect(self.channelChange)
            # if selection != 0:

        if self.Stack.currentIndex() == 0:
            if selected_items:
                # print(selected_items[0])
                # logger.debug('Loading ' + selected_items[0].toolTip())
                self.statusBar().showMessage('Loading ' + selected_items[0].toolTip())
                # store image in fact
                selection = self.channels.currentIndex()
                if selection == 0:
                    self.paint.setImage(self.img)
                else:
                    self.paint.setImage(self.img.imCopy(c=selection - 1))
                self.scaleImage(0)
                self.update()
                self.paint.update()
                # we update the image icon if none
                # print(self.list.currentItem().icon().isNull())
                if self.list.currentItem() and self.list.currentItem().icon().isNull():
                    logger.debug('Updating icon')
                    icon = QIcon(QPixmap.fromImage(self.paint.image))
                    pixmap = icon.pixmap(24, 24)
                    icon = QIcon(pixmap)
                    self.list.currentItem().setIcon(icon)
            else:
                logger.debug("Empty selection")
                self.paint.image = None
                self.scaleImage(0)
                self.update()
                self.paint.update()
                self.img = None
        else:
            if selected_items:
                #     # need update the list of files of the 3D viewer --> a bit dirty need do it better
                #     # pas si mal sinon envoyer tte la liste --> plus simple --> refelechir en fait --> doit aussi mettre a jour l'image selectionnee dans la liste --> son numero sinon va faire des trucs bizarres
                #     list = [file.toolTip() for file in selected_items]
                #     # print(list)
                #     self.v3d.image_list = list
                #     # loading 3D image
                #     if self.vol is not None:
                #         self.v3d.ren.RemoveViewProp(self.vol)
                #     logger.debug('Loading 3D volume ' + self.list.currentItem().toolTip())
                #     # self.vol = self.v3d.load_volume(self.list.currentItem().toolTip())
                #
                #     #if a channel is selected then only allow loading of the channel
                #     if self.channels.currentIndex() == 0:
                #         self.vol = self.v3d.load_volume2(self.img) # so that we do not have to reread image
                #     else:
                #         self.vol = self.v3d.load_volume2(self.img.copy(c=self.channels.currentIndex()-1))  # so that we do not have to reread image
                #     self.v3d.ren.AddViewProp(self.vol)
                #     self.v3d.ren.ResetCamera()  # par contre si images du meme style faut pas resetter la camera
                #     self.v3d.renWin.Render()
                self.loadVolume(selected_items)
        # force update the sliders
        self.update_sliders()

    # if t is specified --> keep parameters
    # seems quite good now
    def loadVolume(self, selected_items=None, t=None, force_no_reset_for_camera=False):
        # if selected_items:
        t_is_specified = t is not None

        # TODO split image 2D and 3D --> à tester

        # no image --> nothing to do
        if self.img is None:
            logger.debug("No image loaded: volume can't be created")
            self.vol = None
            vols = self.v3d.ren.GetVolumes()
            for v in vols:
                self.v3d.ren.RemoveVolume(v)
            # self.v3d.ren.RemoveViewProp --> TODO remove all
            return

        start = timer()
        logger.debug('Loading 3D volume to vtk')
        # need update the list of files of the 3D viewer --> a bit dirty need do it better
        # pas si mal sinon envoyer tte la liste --> plus simple --> refelechir en fait --> doit aussi mettre a jour l'image selectionnee dans la liste --> son numero sinon va faire des trucs bizarres
        # if selected_items is not None:
        #     list = [file.toolTip() for file in selected_items]
        # else:
        #     list = []
        # print(list)
        # self.v3d.image_list = list
        # loading 3D image
        if self.vol is not None:
            self.v3d.ren.RemoveViewProp(self.vol)

        # maybe set it once for good to avoid pbs --> self.img3D or not
        # change the code to make it load only the appropriate stuff
        img3D = None
        if self.cropValues is not None:
            img3D = self.img.crop(**self.cropValues)
        else:
            img3D = self.img
        # self.vol = self.v3d.load_volume(self.list.currentItem().toolTip())
        # if a channel is selected then only allow loading of the channel

        # test crop
        # self.img = self.img.crop(**{'w': [256, 1512-512], 'h': [512, 1512-256], 'd': [3, 10]}) # parfait ça marche nickel mais faut faire un GUI et recup ces parametres

        # if a channel is selected then also need to update it
        # do crop and this the same way
        if self.channels.currentIndex() == 0:
            if t is None:
                self.vol = self.v3d.load_volume2(img3D)  # so that we do not have to reread image
            else:
                self.vol = self.v3d.load_volume2(img3D.imCopy(t=t))  # so that we do not have to reread image
        else:
            self.vol = self.v3d.load_volume2(
                img3D.imCopy(t=t, c=self.channels.currentIndex() - 1))  # so that we do not have to reread image

        if self.img.has_t():
            self.v3d.nb_t = img3D.get_dimension('t') - 1
        else:
            self.v3d.nb_t = 0
        # print("oubi ", self.img.has_t())
        self.v3d.ren.AddViewProp(self.vol)
        # prevent update camera if it is the same image that we browse --> we only reset between different images to avoid pbs

        if not force_no_reset_for_camera and not t_is_specified:
            logger.debug('force reset camera')
            self.v3d.ren.ResetCamera()  # par contre si images du meme style faut pas resetter la camera
        self.v3d.print_coords_on_screen()
        self.v3d.renWin.Render()
        logger.debug("took " + str(timer() - start) + " secs to load vol in vtk")

    # gros bug --> need hide or show slider rather than delete them
    def clearlayout(self, layout):

        # if self.sliders:
        #     for slider in self.sliders:
        #         slider.setParent(None)
        # pass
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    # def clearLayout2(self, layout):
    #     while layout.count() > 0:
    #         item = layout.takeAt(0)
    #
    #         if not item:
    #             pass
    #
    #         w = item.widget()
    #         if w:
    #             w.deleteLater()

    # if widget has childs --> need remove them too... this is not optimal --> best is to hide them according to name ????
    # if all invisible --> ignore

    '''
            >    def unfill(self):
        >        def deleteItems(layout):
        >            if layout is not None:
        >                while layout.count():
        >                    item = layout.takeAt(0)
        >                    widget = item.widget()
        >                    if widget is not None:
        >                        widget.deleteLater()
        >                    else:
        >                        deleteItems(item.layout())
        >        deleteItems(self.ui.verticalLayout)

    '''

    # TODO --> create an object that contains both and set it properly
    def update_sliders(self):
        # need remove all
        # self.dockedWidget.layout().

        logger.debug('updating sliders')
        # TODO only put for known dimensions otherwise use range slider to crop maybe --> give it a try ???? --> how hard is it
        # self.clearLayout(self.dockedWidget.layout()) # URGENT DOES NOT WORK
        # self.sliders.clear()

        # del self.dockedWidget.layout()
        # self.dockedWidget.setLayout(QVBoxLayout())

        for slider in self.dimensionSliders:
            slider.hide()

        if self.img is None:
            logger.debug('empty image cannot update sliders')
        else:
            logger.debug('image dimensions ' + self.img.metadata['dimensions'])
        if self.img is not None:
            # print('empty ', self.dockedWidget.layout().isEmpty())
            for d in self.img.metadata['dimensions']:
                if d not in ['w', 'h', 'c']:

                    logger.debug('updating dimension ' + d)
                    # labeled = QHBoxLayout(self.dockedWidget)
                    # labeled.addWidget(QLabel(d))

                    labelledSlider = None
                    for slider in self.dimensionSliders:
                        if slider.getDim() == d:
                            labelledSlider = slider
                            labelledSlider.setValue(0)
                            labelledSlider.show()
                            break

                    # print(labelledSlider)

                    if labelledSlider is None:
                        labelledSlider = LabelledSlider(None, d, self.display)

                    # print(labelledSlider)
                    # labeled_slider.setLayout(QHBoxLayout())
                    # labeled_slider.layout().addWidget(QLabel(d))
                    # startSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
                    # startSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
                    # startSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
                    # startSlider.setTickInterval(1)
                    # startSlider.setSingleStep(1)
                    # startSlider.valueChanged.connect(self.display)
                    # startSlider.setToolTip(d)

                    labelledSlider.setMinimum(0)
                    labelledSlider.setMaximum(self.img.get_dimension(d) - 1) # it's ok that works really well
                    # startSlider.ma

                    # startSlider.toolTip()

                    # startSlider.setMinimumSize(QtCore.QSize(200, 10))
                    # labeled.addWidget(startSlider)
                    # startSlider.setMaximumSize(QtCore.QSize(16777215, 10))
                    # startSlider.setAttribute('dimension', d)
                    # print(startSlider.__getattribute__('dimension'))

                    # need connect the slider to the dimension
                    # self.table_widget.add_sliders(startSlider)
                    # labeled_slider.layout().addWidget(startSlider)
                    self.dockedWidgetInDimension.layout().addWidget(labelledSlider)  # startSlider
                    # pb les trucs sont pas addes
                    # print('not empty 1 ? ', self.dockedWidget.layout().isEmpty())
                    self.dimensionSliders.append(labelledSlider)

                    # self.dockedWidget.layout().addLayout(labeled)

        # print('not empty ? ', self.dockedWidget.layout().isEmpty())

        needShow = True
        for slider in self.dimensionSliders:
            if slider.isVisible():
                needShow = True
                break

        # print(needShow)

        if needShow:
            self.dockedDimensionWidget.update()
            self.dockedWidgetInDimension.update()
            self.dockedDimensionWidget.show()
            logger.debug('showing sliders')
        else:
            self.dockedDimensionWidget.hide()
            logger.debug('hiding sliders')

    # ça marche les sliders mais faire ça proprement et uniquement pr les trucs qui font sens et peut etre utiliser aussi ça pr cropper ou trucs comme ça
    def display(self):
        # print('there there')
        # print(self.sender()) # the source of the signal sent
        # slider = self.sender() # KEEP THIS IS HOW TO GET THE SENDER --> REALLY COOL I LOVE IT
        # print(slider.maximum())
        # print(slider.toolTip())
        # create a parameter to pass
        # in fact I need to update all the sliders at the same time or to find a trick --> best is update all the sliders
        # loop over all the sliders to get the parameters

        # need loop over all the sliders in the layout
        # if

        params = {}
        # for i in range(self.dockedWidget.layout().count()):
        #     print(self.dockedWidget.layout().itemAt(i))
        #     for j in range(self.dockedWidget.layout().itemAt(i).layout().count()):
        #         el = self.dockedWidget.layout().itemAt(i).layout().itemAt(j)
        #         if isinstance(el, QSlider):
        #             params[el.toolTip()] = el.value()

        # we create the slicing parameters from user image
        for slider in self.dimensionSliders:
            if slider.isVisible():
                params[slider.toolTip()] = slider.value()
        # for i in reversed(range(layout.count())):
        #     layout.itemAt(i).widget().setParent(None)

        if params:
            # create a slice that corresponds to user entry
            # print('params of image', params)
            neo = self.img.imCopy(**params)  # now need update the image
            # print('neo', neo.shape, self.img.shape, neo.metadata['dimensions'])
            self.paint.setImage(neo)

        # permet de changer d'image avec ce slider
        if self.Stack.currentIndex() == 1:
            if 't' in params.keys():
                self.loadVolume(t=params['t'])

        # sqdsqsqdqs
        # neo.pop()
        # ça marche

    def changeMode(self):
        self.paint.vdp.active = self.changeModeAct.isChecked()

    def replaceWidget(self):
        if self.Stack.currentIndex() == 0:
            self.Stack.setCurrentIndex(1)
            self.selectionChanged()
        else:
            self.Stack.setCurrentIndex(0)
            self.selectionChanged()

    def showHideMask(self):
        self.paint.maskVisible = not self.paint.maskVisible
        self.paint.update()

    def escape(self):
        if self.Stack.isFullScreen():
            self.fullScreen()

    # brings stuff full screen then restore it back after
    def fullScreen(self):
        # TODO --> do a list of shortcuts to ease the work
        # print("fullscreen")

        if not self.Stack.isFullScreen():
            # settings = QSettings()
            # settings.setValue('geometry', self.Stack.saveGeometry())
            # settings.setValue('windowState', self.Stack.saveState())
            # super(Window, self).closeEvent(event)
            # self.flags = QtCore.Qt.WindowFlags()
            # print(self.flags)
            # flags = self.Stack.
            self.Stack.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                # QtCore.Qt.WindowTitleHint |
                # QtCore.Qt.WindowCloseButtonHint |
                QtCore.Qt.WindowStaysOnTopHint
            )
            '''
                  self.setWindowFlags(
                    QtCore.Qt.Window |
                    QtCore.Qt.CustomizeWindowHint |
                    QtCore.Qt.WindowTitleHint |
                    QtCore.Qt.WindowCloseButtonHint |
                    QtCore.Qt.WindowStaysOnTopHint
                  )
            '''
            self.Stack.showFullScreen()
        else:
            # settings = QSettings()
            # self.Stack.restoreGeometry(settings.value("geometry")) #.toByteArray()
            self.Stack.setWindowFlags(QtCore.Qt.Widget)
            # self.Stack.setWindowFlags(self.flags)
            self.grid.addWidget(self.Stack, 0, 0)  # pas trop mal mais j'arrive pas à le remettre dans le truc principal
            # dirty hack to make it repaint properly --> obviously not all lines below are required but some are --> need test, the last line is key though
            self.grid.update()
            self.Stack.update()
            self.Stack.show()
            self.centralWidget().setLayout(self.grid)
            self.centralWidget().update()
            self.update()
            self.show()
            self.repaint()
            self.Stack.update()
            self.Stack.repaint()
            self.centralWidget().repaint()
            # self.adjustSize()
            # self.resize(QSize(self.size().width()+1, self.size().height()))
            # qApp.processEvents()
            # does not redraw properly --> need to have it done differently
            # pas top mais pas si mal en fait
            # self.restoreState(settings.value("windowState").toByteArray())
            # self.Stack.restoreGeometry()

    def down(self):
        # print('down')
        if self.paint.vdp.active:
            # print('in')
            self.paint.vdp.remove_selection()
            self.paint.update()
        # Or put code to implement from code 1

    def has_more_t(self, img):
        return self.has_more_dim(img, img.metadata['cur_t'], 't')

    def has_more_dim(self, img, curpos, dim):
        dim_t_size = img.get_dimension(dim)
        if dim_t_size is None:
            return False
        return curpos + 1 < dim_t_size

    def nextFrame(self):
        # print("zest", self.img.metadata['cur_t'], self.img.get_dimension('t'))
        if self.img is not None and self.img.has_t() and self.has_more_t(self.img):
            # print("zab")
            # self.v3d.nb_t = self.img.get_dimension('t')
            self.img.metadata['cur_t'] += 1
            # print(self.img.metadata['cur_t'])
            self.loadVolume(t=self.img.metadata['cur_t'])
        else:
            # select next image in list
            # qsdsqdsqd
            # selectedItems
            # print(self.list.currentRow())
            # self.last = 'next'
            # self.list.setCurrentRow(self.list.currentRow()+1)
            # self.list.selectionModel().select(self.list.currentRow()+1, QItemSelectionModel.ClearAndSelect)
            idx = self.list.model().index(self.list.currentRow() + 1, 0)
            if idx.isValid():
                self.list.selectionModel().setCurrentIndex(idx, QItemSelectionModel.ClearAndSelect)  # SelectCurrent

        # otherwise move to next img in the list...

        # print('full moving next')
        # self.cur_frame += 1
        # if self.cur_frame < len(self.image_list):
        #     self.current_volume = None


    # almost there but was a pain
    def runWshed(self):
        if self.paint.imageDraw:
            handCorrection = Img.qimageToNumpy(self.paint.imageDraw, mode='bnw8') # bug here --> ce truc ne marche pas en fait qd fait deux fois --> pkoi
            # print(handCorrection.max(), handCorrection.min())

            # plt.imshow(handCorrection, cmap='gray')
            # plt.show()

            # set 0 to 1 to avoid bugs
            # print(handCorrection.shape, handCorrection.dtype) # TODO BE CAREFUL it's really key for wshed to have it as ubyte otherwise it does not seem to work apparently --> check it
            # handCorrection[handCorrection == 0] = 1 --> value is 255 everywhere --> why
            # see how to run watershed on a binary image

            # image is ok till here then ???

            # from matplotlib import pyplot as plt
            # plt.imshow(handCorrection, cmap='gray')
            # plt.show()

            # now run wshed on it
            handCorrection = Wshed.run(handCorrection, seeds='mask') #TODO urgent add min size

            # marche pas car single channel and need ARGB ici ... --> à fixer en fait
            # and I need to make it compat to the current color mode --> but shouldn't be too hard I guess
            # print(handCorrection.shape, handCorrection.dtype) # ideally should be int 8 not int 32
            # #
            # from matplotlib import pyplot as plt
            # plt.imshow(handCorrection, cmap='gray')
            # plt.show()


            # need an RGBA here
            # print(self.paint.imageDraw)
            self.paint.imageDraw = Img(self.createRGBA(handCorrection), dimensions='hwc').getQimage() # marche pas car besoin d'une ARGB
            # print(self.paint.imageDraw)
            self.paint.update()

    def createRGBA(self, handCorrection):
        # use pen color to display the mask
        # in fact I need to put the real color
        RGBA = np.zeros((handCorrection.shape[0], handCorrection.shape[1], 4), dtype=np.uint8)

        red = self.paint.drawColor.red()
        green = self.paint.drawColor.green()
        blue = self.paint.drawColor.blue()

        #(handCorrection.shape[0], handCorrection.shape[1], 4))
        # mask = handCorrection[handCorrection==255]




        # ce truc est bleu --> pkoi
        # RGBA[..., 0] = 255#handCorrection --> totalement transp --> transparence color --> GREEN --> BLUE
        # RGBA[..., 1] = 0  # this is the red channel --> RED --> GREEN
        # RGBA[..., 2] = 0 # rien ici --> tt transparent --> alpha ??? --> ALPHA -->RED
        # RGBA[..., 3] = 255 # --> BLUE --> ALPHA --> ok

        # pkoi je swappe les channels avant

        # 255 partout --> blanc
        # 0 255 255 0 --> rouge --> 1 = red channel and 2 = alpha --> weird



        #
        # RGBA[RGBA[..., 0] > 0, 0] = blue
        # RGBA[RGBA[..., 1] > 0, 1] = green
        # RGBA[RGBA[..., 2] > 0, 2] = red
        # RGBA[..., 3] = 255 # ne s'affiche pas et je comprend pas pkoi

        #BGR in fact --> need fix here or the other --> the one in


        # bug somewhere in qimage --> fix it some day --> due to bgra instead of RGBA
        RGBA[handCorrection != 0, 0] = blue # b
        # RGBA[..., 1] = handCorrection
        RGBA[handCorrection != 0, 1] = green # g
        RGBA[handCorrection != 0, 2] = red # r
        RGBA[..., 3] = 255 # alpha --> indeed alpha
        RGBA[handCorrection == 0, 3] = 0 # ça marche maintenant --> super complexe qd meme je trouve


        # ok mais plus transparent

        #
        # print(red, green, blue)

        # RGBA[RGBA[..., 0] == 255] = red
        # RGBA[RGBA[..., 1] == 255] = green
        # RGBA[RGBA[..., 2] == 255] = blue

        return RGBA

    def prevFrame(self):
        # print("zest", self.img.metadata['cur_t'], self.img.get_dimension('t'))
        if self.img is not None and self.img.has_t() and self.img.metadata['cur_t'] > 0:
            # print("zab")
            # self.v3d.nb_t = self.img.get_dimension('t')
            self.img.metadata['cur_t'] -= 1
            # print(self.img.metadata['cur_t'])
            self.loadVolume(t=self.img.metadata['cur_t'])
        else:
            # select next image in list
            # qsdsqdsqd
            # selectedItems
            # print(self.list.currentRow())
            # self.last = 'prev'

            idx = self.list.model().index(self.list.currentRow() - 1, 0)
            if idx.isValid():
                self.list.selectionModel().setCurrentIndex(idx, QItemSelectionModel.ClearAndSelect)  # SelectCurrent

            # self.list.setCurrentRow(self.list.currentRow()-1)

            # row = self.selectionModel.selectedRows()[0]
            # self.list.selectionModel().select(self.list., QItemSelectionModel.ClearAndSelect)
        # otherwise move to next img in the list...

        # print('full moving next')
        # self.cur_frame += 1
        # if self.cur_frame < len(self.image_list):
        #     self.current_volume = None

    # last = 'next'
    # not really a smart way --> find a better way to do that
    def zoomIn(self):
        self.statusBar().showMessage('Zooming in',
                                     msecs=200)  # shows message for only a few secs and removes it --> very useful
        if self.Stack.currentIndex() == 0:
            self.scaleImage(self.zoom_increment)

        if self.Stack.currentIndex() == 1:
            # dispatch zoom in to it
            self.v3d.Keypress(None, None, key='plus')
        # else:
        #     self.v3d.Keypress(key='plus') # simaulate zoom in

    def zoomOut(self):
        self.statusBar().showMessage('Zooming out', msecs=200)
        if self.Stack.currentIndex() == 0:
            self.scaleImage(-self.zoom_increment)

        # dirty hack to send stuff
        if self.Stack.currentIndex() == 1:
            # dispatch zoom in to it
            self.v3d.Keypress(None, None, key='minus')
        # else:
        #     self.v3d.Keypress(key='minus') # simaulate zoom in

    def defaultSize(self):
        self.paint.adjustSize()
        self.scale = 1.0

    # null car respecte pas le w/h ratio --> à fixer --> alterner between w and h
    def fitToWindow(self):
        # TODO most likely a bug there because calls self.defaultSize that resets the scale --> MAKE NO SENSE
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

        # self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        # self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scale < self.max_scaling_factor)
        self.zoomOutAct.setEnabled(self.scale > self.min_scaling_factor)

    # def adjustScrollBar(self, scrollBar, factor):
    #     scrollBar.setValue(int(factor * scrollBar.value()
    #                            + ((factor - 1) * scrollBar.pageStep() / 2)))



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
                urls.append(url.toLocalFile())
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

    def openTextEditor(self):
        print(self.textEditor.getDoc().toPlainText())  # ça marche pas trop mal
        print(self.textEditor.getDoc().toHtml())
        print(self.textEditor.getSize())
        if self.textEditor.isVisible():
            self.textEditor.hide()
        else:
            self.textEditor.show()

    # need store the values somewhere to reuse them
    def cropVolume(self):
        values, ok = VolumeCropperDialog.getValues(self.img, parent=self)
        if ok:
            # print(values)
            # could create an independent volume if needed --> but will add a lot more pbs
            # self.img = self.img.crop(**values)
            self.paint.setImage(self.img.crop(**values))
            self.cropValues = values
            # force a reload
        else:
            self.cropValues = None

        # reset 3D view if smthg changed
        if self.Stack.currentIndex() == 1:
            self.loadVolume()


            # simulate slow process making progressbar advance

    def simulate_progress_in_progressbar(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)

        self.progress.setValue(0)

    outputFolderForSnaps = None

    def snap_3D_volume(self):
        # need define name
        if self.outputFolderForSnaps is None:
            # ask the user for output folder
            # TODO ask for output dir --> same on every reset
            self.outputFolderForSnaps = './../trash/'
        self.v3d.save_frame()

    # could be ok # maybe just implement a function stuff to make it generic for the stuff

    def create_a_movie_from_3D_stack_individual_frames(self):
        self._create_a_movie_from_3D_stack(self.v3d.save_frame)

    def create_a_movie_from_3D_stack_video(self):
        self._create_a_movie_from_3D_stack(self.v3d.init_video, self.v3d.save_video_frame, self.v3d.close_video)

    # TODO add name of output --> do it here and do that accordingly
    # TODO add a shortcut to allow creation of video in fullscreen --> v for video and f for frames or
    def _create_a_movie_from_3D_stack(self, *func):
        # if len(func) == 3:
        #     get output file name
        # else:
        #     get output dir

        # fabriquer un film en offline rendering ou pas ???
        # self.v3d.init_video()
        if len(func) == 3:
            func[0]()
        # need to loop over the images and ask for output file name
        # loop over all images in the list, for keep camera then restore current image or not
        self.progress.setValue(0)
        total_nb_of_images = self.list.count()
        # 100 % = total_nb_of_images
        # so

        for i in range(total_nb_of_images):
            item = self.list.item(i)
            # would be great to prevent reloading a volume that is already loaded cause it's super slow can I parallelize the rendering --> maybe but think how and check the system available memory with some security

            self.loadVolume(selected_items=[item], force_no_reset_for_camera=True)
            logger.debug('creating video frame for frame 0 of img ' + str(item.toolTip()))
            if self.img.is_time_series():
                self.img.set_t(0)  # reset time if not 0
            #     self.progress.setValue(self.img.get_dimension('t'))
            # self.v3d.save_video_frame()
            if (len(func) == 3):
                func[1]()
            else:
                func[0]()
            if self.img.is_time_series():
                for j in range(1, self.img.get_dimension('t')):
                    logger.debug('creating video frame for frame ' + str(j) + ' of img ' + str(item.toolTip()))
                    self.loadVolume(t=j, force_no_reset_for_camera=True)
                    # self.v3d.save_video_frame()
                    if (len(func) == 3):
                        func[1]()
                    else:
                        func[0]()
                    self.progress.setValue((j / self.img.get_dimension('t')) * 100)

            # lui faire loader l'image et resetter le truc
            # if multi frame --> reset then loop or just reload it
        # close video
        self.progress.setValue(100)
        # self.v3d.close_video()
        if (len(func) == 3):
            func[2]()
        self.progress.setValue(0)

        # TODO faire aussi une touche pour grabber le volume et garder ça pr tt le film

    def add_sliders(self, *args):
        for arg in args:
            print('adding ', arg)
            self.tab3.layout.addWidget(arg)
        self.tab3.layout.update()
        self.tab3.update()
        self.tabs.update()
        self.layout.update()

    # just need zoom
    # due to zoom if cells are a little bit too small then that doesn't work...
    # indeed if I artificially make cells bigger it works better --> maybe due to the size of the training images --> but it's probably ok still I have a shift with the images from raphael --> wing.png and wing_double_sized.png --> is it an artifact of the slicing ????
    # should i retrain the model 1 px wide ???? or ok like that ???
    # in one image everything appears shifted by 1 px --> why is that ????
    # TODO think about it and see why shifted by one pixel
    # or rerun whsed based on seeds from this --> yet another possibility
    # think and do tests over the WE
    # TODO handle several channels
    # or maybe dissolve by watershed then check bonds that disappeared and try to revive them if they are long enough --> try to cut them then connect them
    # check my java code to increase bond length of ROIs if I made it
    # pas mal --> voir si je peux pas faire mieux encore et trouver un algo de connection
    # check how long it would take on another machine that has no GPU nvidia such as my laptop ... --> would it be fast enough just based on a CPU ???




    deepTA = None


    # nb on the image of andreas the model does not work well probably because cells are too small 'wing_disc_epi_only.png' --> if I scale it 4 times it works --> it is becauuse cells are small that it does not work --> need scale down the cells and mask quite a lot
    def deep_learning(self):
        # pretrained = "/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/retrained_model_512x512_4_different_organisms_data_augmentation_test_100_epochs/vgg_unet_1"  # "/D/datasets_deep_learning/keras_segmentation_dataset/TA_test_set/output_models/vgg_unet_1"
        # if 'indow' in platform.system():
        #     # pretrained = 'C:\\Users\\baigo\\Desktop\\dataset1\\output_models\\retrained_model_512x512_3_different_organisms\\vgg_unet_1'
        #     pretrained = 'C:\\Users\\baigo\\Desktop\\dataset1\\output_models\\retrained_model_512x512_4_different_organisms_big_images_input\\vgg_unet_1'
        #
        # # load the model only once and only if necessary --> I however need to know how to free gpu memory and close session or model properly --> for example in order to reload a model
        # if self.deepTA is None:
        #     self.deepTA = DeepTA(pretrained=pretrained) # prevent retraining the model

        if True:
            if self.img is not None:

                inp = self.img
                # only works with RGB images so far --> need fix that
                # inp[..., 0] = inp[..., 1]
                # inp[..., 2] = inp[..., 1]

                print('now', self.img.shape, self.img.dtype)

                # erroneous segmentation may be fixed by having a better control over input and output size --> improve all of that and try to do better than what I have now


                # do that directly in the other code
                # import numpy as np

                # print(inp.shape)
                # make input twice bigger --> does that solve anything

                overlap = 64
                # this new method for making overlapping chunks is just really what I needed and that totally removes black holes that I had at borders in the mask --> that's really perfect
                desired_w = 512 - overlap
                desired_h = 512 - overlap
                if inp.shape[0] == 512 and inp.shape[1] == 512:
                    # no need to slice if image is already the same size --> could
                    overlap = 0
                # if width or height < 10% difference from 512x512 --> useless to split in fact --> directly pass the image by setting overlap to 0 and changing width and height
                if inp.shape[0] - 512 < 10 * inp.shape[0] / 100:
                    desired_h = inp.shape[0]
                if inp.shape[1] - 512 < 10 * inp.shape[1] / 100:
                    desired_w = inp.shape[1]
                if desired_h == inp.shape[0] and desired_w == inp.shape[1]:
                    overlap = 0
                crops, splits = Img.get_2D_tiles_with_overlap(inp, width=desired_w, height=desired_h, overlap=overlap)
                # print('1', len(splits))
                # print('2', len(splits[0]))

                # tmp = deepTA.blockshaped(inp, 3, 3)
                # inp = inp[585:585+512, 1407:1407+512]
                # inp = inp[585:585+512, 900:900+512]
                # tmp = np.hsplit(inp, 2)
                # tmp = np.array_split(inp, 3)
                # for chunk in tmp:
                #     print(chunk.shape)

                # need split then reconstitute the image

                # inp = inp[1000:1000+412, 900:900+512]
                # very good

                # print(inp.shape)# TODO need force it to be three channel
                # img = np.array([[1, 2], [3, 4]])
                # for r in splits:
                #     for chk in r:
                #         print(chk.shape)
                #         chk = np.stack((chk,) * 3, axis=-1)
                # inp = np.stack((inp,) * 3, axis=-1)
                # print(inp.shape)

                # nb there is a bug at borders so need to get a bigger region and then further crop to avoid bounds issues --> should not be too hard

                # need remove blob


                # nb this is the wrong predict file need the corrected one
                row = 0
                for r in splits:
                    col = 0
                    for chk in r:
                        if len(chk.shape) != 3:
                            chk = np.stack((chk,) * 3, axis=-1)

                        # probably need to force each chunk to be the same as the original
                        out = self.deepTA.predict_from_current_model(
                            inp=chk,
                            out_fname=None
                        )
                        print(
                            out.shape)  # image half the size --> why is that --> returned image is not the same as saved one  --> why --> need check
                        # now resizes back to normal shape
                        out = cv2.resize(out, dsize=(chk.shape[1], chk.shape[0]),
                                         interpolation=cv2.INTER_NEAREST)  # cv2.INTER_CUBIC

                        print(
                            out.shape)  # image half the size --> why is that --> returned image is not the same as saved one  --> why --> need check
                        splits[row][col] = out
                        col += 1
                    row += 1

                final_mask = Img.reassemble_tiles(splits, crops)

                # print(final_mask.shape)
                #
                # print(final_mask.shape)

                # import matplotlib.pyplot as plt
                #
                # plt.imshow(final_mask)
                # plt.show()

                # why all white ???

                # print('shp', final_mask.shape, final_mask.dtype)

                final_mask[final_mask == 1] = 255


                # final_copy = final_mask.copy()
                # skel, final_copy = Wshed.run_fix_mask(final_copy)
                # cv2.imwrite(out_fname + '_empty_ends.png', final_copy)


                # marche pas mal du tout maintenant mais bcp de sursegmentation --> need a better algo
                # final_mask = Wshed.run_dist_transform_watershed(final_mask) # vraiment pas mal mais besoin de scorer les nouveaux bonds --> si 0 overlap with mask from AI --> remove them otherwise keep them --> TODO implement that
                # here again the blur and the watershed fuck everything for things touching the edges --> see how to fix that
                # really try to connect by smallest distance to any pixel on the other side ????

                # or get the closest wshed line to the unconnected bond --> might work --> some sort of hybrid algo --> try to do that and see


                # TODO sur le skeletonize detecter les vertices et les bonds et les etendre droit jusqu'au prochain pixel peut etre aussi faire un score ???
                # reflechir à comment faire ça ...


                self.paint.imageDraw = Img(self.createRGBA(final_mask), dimensions='hwc').getQimage()
                self.paint.update()

        # ça ne free pas la memoire mais par contre ça a l'air de marcher et de pas bugger --> à tester
        # subprocess.run("nvidia-smi")
        # self.deepTA.reset_keras()
        # del self.deepTA
        # subprocess.run("nvidia-smi")

        # self.deepTA.reset_keras()
                # cv2.imwrite(out_fname + '_corrected.png', final_mask)
        #



    def run_watershed(self):
        # faudrait faire un dispatcher qui verifie si il y a qq chose dans la liste ey traiter les choses differement en fonction de ce qu'il y a

        dialog = WshedDialog()



        # ça marche mais besoin d'overrider les boutons et les trucs de l'autre
        values, ok = TAGenericDialog.getValues(parent=self, UI=dialog, preview_enabled=True)
        if ok:
            print(values)
            print(dialog) #it still exists --> could do the run in it --> easier to maintain
            # should I save each mask as a separate channel with .ch1.npy .... maybe the most robust stuff but think
            # get current image and process it or maybe even get current channel
            # if has time --> could use it
            # pb is don't have access to the image
            # print(self.paint.image) # ça marche maintenant même si c'est vide --> voir comment je peux faire en fait
            # print(self.img)
            # print('zeb')
            if self.img is not None: # bug here
                # print('here')
                # print(self.img.shape, self.img.dtype)

                # NB run is faster for small images than the run_fast --> use this wisely according to size

                print(self.img.shape)

                mask = Wshed.run_fast(self.img, first_blur=values[0], second_blur=values[1])
                # print('here 2')
                # self.paint.imageDraw = Img(mask, dimensions='hw').getQimage()
                # see the bug here
                # print(mask.shape, mask.dtype)
                # print(mask)

                # ca marche mais need ask for stuff
                # need add border for wshed --> see how I can do that and why that does not work
                self.paint.imageDraw = Img(self.createRGBA(mask), dimensions='hwc').getQimage()
                self.paint.update()

                # ça marche mais est ce que l'ordre est bon ???
                # import matplotlib.pyplot as plt
                # plt.imshow(Img(self.createRGBA(mask), dimensions='hw'), cmap='gray')
                # plt.show()

            #todo




    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


# TODO --> FAIRE UN LOAD IMAGE LA DEDANS et faire un retaillage de la fenetre



# http://euanfreeman.co.uk/pyqt-qpixmap-and-threads/
#     def someFunctionCalledFromAnotherThread(self):
#         # run long thread
#
#         thread = LoadImageThread(self.load_long_process)
#         # self.connectNotify(thread, QtCore.pyqtSignal(self.showImage(QString)"), self.showImage)
#
#         thread.start()
#
#
#     # def showImage(self, filename):
#     #
#     #     # pixmap = QtGui.QPixmap(filename).scaled(w, h)
#     #     # self.image.setPixmap(pixmap)
#     #     # self.image.repaint()
#     #     self.load_long_process()

#
# class LoadImageThread(QtCore.QThread):
#
#     def __init__(self, function):
#         QtCore.QThread.__init__(self)
#         self.function = function
#
#
#     def __del__(self):
#         self.wait()
#
#
#     def run(self):
#         # self.emit(QtCore.SIGNAL('showImage(QString)'), self.file)
#         # self.load_long_process()
#         self.function()


# class YourThreadName(QtCore.QThread):
#
#     def __init__(self):
#         QtCore.QThread.__init__(self)
#
#     def __del__(self):
#         self.wait()
#
#     def run(self):
#         # your logic here
#         self.load_long_process()


class LabelledSlider(QWidget):

    def __init__(self, parent, d, func):
        super(QWidget, self).__init__(parent)
        layout = QHBoxLayout()
        # labeled_slider = QWidget()
        # labeled_slider.setLayout(QHBoxLayout())
        self.label = QLabel(d)
        layout.addWidget(self.label)
        self.startSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.startSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
        # startSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.startSlider.setTickInterval(1)
        self.startSlider.setSingleStep(1)
        self.startSlider.valueChanged.connect(func)
        self.startSlider.setToolTip(d)
        self.func = func

        # self.startSlider.setMinimum(0)
        # self.startSlider.setMaximum(self.img.get_dimension(d) - 1)
        # startSlider.ma

        # startSlider.toolTip()

        self.startSlider.setMinimumSize(QtCore.QSize(200, 10))
        layout.addWidget(self.startSlider)
        # labeled.addWidget(startSlider)
        # startSlider.setMaximumSize(QtCore.QSize(16777215, 10))
        # startSlider.setAttribute('dimension', d)
        # print(startSlider.__getattribute__('dimension'))

        # need connect the slider to the dimension
        # self.table_widget.add_sliders(startSlider)
        # labeled_slider.layout().addWidget(startSlider)
        # self.dockedWidget.layout().addWidget(labeled_slider)  # startSlider
        self.setLayout(layout)

    def setMaximum(self, max):
        self.startSlider.setMaximum(max)

    def setMinimum(self, min):
        self.startSlider.setMinimum(min)

    def setDim(self, d):
        self.startSlider.setToolTip(d)
        self.label.setText(d)

    def value(self):
        return self.startSlider.value()

    def getDim(self):
        return self.startSlider.toolTip()

    def toolTip(self):
        return self.getDim()

    def setValue(self, value):
        self.startSlider.disconnect()
        self.startSlider.setValue(value)
        self.startSlider.valueChanged.connect(self.func)



# class TA_tabs(QWidget):



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # set app icon
    app_icon = QtGui.QIcon('./../../IconsPA/src/main/resources/Icons/ico_packingAnalyzer2.gif')  # add taskbar icon
    # app_icon.addFile('gui/icons/16x16.png', QtCore.QSize(16, 16))
    # app_icon.addFile('gui/icons/24x24.png', QtCore.QSize(24, 24))
    # app_icon.addFile('gui/icons/32x32.png', QtCore.QSize(32, 32))
    # app_icon.addFile('gui/icons/48x48.png', QtCore.QSize(48, 48))
    # app_icon.addFile('gui/icons/256x256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    w = TissueAnalyzer()
    w.show()
    sys.exit(app.exec_())
