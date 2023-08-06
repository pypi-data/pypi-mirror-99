# ça marche pr la go deep inside selection --> maintenant faire le snap en cas de failure à faire qq chose surtout si inner component
# voir comment ke fais ça dans l'autre --> probablement faire un set_p1 et un get_p1 ???

# is it possible then to store and serialize all the images as a xml stuff --> most likely yes with all its parameters --> guess yes and that may be what i want to do --> esay to store image content as a tree and browse it and do stuff with it
# see pyqt_treeview_dom_example.py for an example of treeview with dom and see if I can and want to really use that
# TODO bug in svg when resized --> most likely a scaling bug of the crop --> see how I can handle that --> probably a bug of scaling of the crop values...

# voir comment faire en fait --> si nothing to --> snap position

# maybe the bond scoring for the comparison between scaled and non scaled image will solve everything --> could be the bond score may do the job and prevent me from removing cells that should not


# tester comment combiner les 2 dois aussi faire le hd si je dezoome ???




# should I allow letters outside too
# allow browse inside
# MEGA TODO maybe show hierarchy or object as a TREE so that one can browse inside and if that is so only allow selection of parent obejct --> maybe it's a way to do that would be the simplest and most efficient
# --> à tester
# also offer a bg or not --> TODO
# best way to browse an object --> using a TREE --> how about that in fact
# do I need to implement a draw sel with a color


# http://zetcode.com/pyqt/qtooltip/ examples --> TODO


# not bad but just fix it at some point --> TODO
# even when rows are exactly same height or width there are pbs
# gérer les différentes fusions d'images possibles et browser à l'intérieur pour éditer les images
# voir comment faire ça car pas si facile en fait mais peut etre ok
# allow swaps etc...
# faire des boutons qui permettent de gerer ça ou bien des popups
# browser jusqu'aux images pr editer les parametres du truc
# TODO implement the loop inside selection
# faire un free draw ou un autopack --> tt est à faire
# handle selections





# still a bit slow but probably ok --> just check it at some point and see if one can speed up compytation of size using fake stuff
# TODO do a test --> can size be computed that would be the optimal
# TODO
# pas mal en fait car si tous meme taille à la base --> alors facile de les mettre à la bonne taille, je pense ???--> y reflechir --> est ce que ça varie en x ou en y ??,

# nb there seems to be a bug in bounding rect and size is also not correct

#  bug in settowidth

# nb should + always be add to a row as a column of a row and / add as a row of a column and the double // be the new line (row/col) maybe simpler to compose image
# + --> adds to row as a new col / adds to col as a new row __floordiv__ // adds a new row or a new col depending on object
# maybe all of this would be simpler this way or could use the or to add horizontally intsead of the + as it is visually what should be done
# __or__ use or for horizontal and / for vertical and __floordiv or double || vertical for new row/col for both
# __ifloordiv__ and floordiv should do the same
# list of operators https://docs.python.org/3/library/operator.html || existe pas fonc prendre floordiv car top
# --> TODO
# can I use a, b = b, a for a swap in python or find dome other things maybe modulo could be a good synonym for swap too A % B --> swaps
# peut etre permettre des tranches et des get items et set items voir comment faire qd meme
# que dois je faire si or sur col ou sur row et si truediv sur row ou col
# almost there but small bug in height in some new_row / new_col floordiv probably due to spaces/incompressible height/width
# stuff is ok for one but not the other --> just check quickly to see errors
# bug is in row --> see why that is
# probably not big deal though
# row//col is ok
# col//row is ok but bug in settowidth --> see why that is
# merging of row over row is incorrect --> needs better fix I guess by removing some of the complexity


# TODO implement missing operators for rows and cols


# TODO implement crop based on image ROIs --> use my minimal_demo_cropping_rect.py that works great!!!!


# voir quoi faire en cas de DND --> se baser sur EZF en fait --> pas trop dur meme si moins de shapes...
# pb text does not work
# TODO improve selection to draw it transparent
# TODO permettre d'editer une shape si on double click dessus --> good idea, maybe even images see how I should do that ??? --> maybe reset first point and if people drags redraw the shape or use magic bounds as in TA -> maybe more what the user wants

# TODO add set a bg image and maybe allow draw on it --> this way can be used always in TA and also there --> simpler as it is just one tool --> need set different modes though
# make that it can have an infinite nb of layers --> drawn transparently on top of one another
# not easy to do crops --> need rotate it so that it is there
# crop image


# https://github.com/leimao/Rotated_Rectangle_Crop_OpenCV --> this is how to crop a rect and that is what I want roughly
# try implement that ...


# maybe not so hard indeed --> crop around then rotate then crop

# crop


# alternatively could put move to to set p1 but pb of override

import sys
import os
import traceback
from functools import partial
from PyQt5.QtGui import QPalette, QPainter, QColor, QIcon, QPen
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtWidgets import QMenu, QApplication, QMainWindow, QPushButton, QWidget, QLabel, QScrollArea, \
    QAction, QProgressBar, QDockWidget, QSpinBox, QComboBox, QGridLayout, QDialog, QGroupBox, QDoubleSpinBox
from epyseg.draw.shapes.polygon2d import Polygon2D
from epyseg.draw.shapes.line2d import Line2D
from epyseg.draw.shapes.rect2d import Rect2D
from epyseg.draw.shapes.scalebar import ScaleBar
from epyseg.draw.shapes.square2d import Square2D
from epyseg.draw.shapes.ellipse2d import Ellipse2D
from epyseg.draw.shapes.circle2d import Circle2D
from epyseg.draw.shapes.freehand2d import Freehand2D
from epyseg.draw.shapes.point2d import Point2D
from epyseg.draw.shapes.polyline2d import PolyLine2D
from epyseg.draw.shapes.image2d import Image2D
from PyQt5.QtCore import QPointF, QRectF, Qt, QRect, QSize
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import qApp
from epyseg.draw.shapes.txt2d import TAText2D
from epyseg.draw.shapes.vectorgraphics2d import VectorGraphics2D
from epyseg.figure.alignment import updateBoudingRect, setToWidth, setToHeight, setToHeight2, setToWidth2
from epyseg.figure.column import Column
from epyseg.figure.row import Row
from personal.no_color_pyqt_color_picker import NoColorDialog
from epyseg.figure.alignment import alignRight, alignLeft, alignTop, alignBottom, alignCenterH, alignCenterV, packY, \
    packX, packYreverse

# logging
from epyseg.tools.logger import TA_logger

logger = TA_logger()


# do a json script for positioning ???
# how can I save images without serialization --> maybe implement serialization...
# see how to fake compute width just to go fast without a real resize

class VectorialDrawPane2(QWidget):
    FIT_TO_WIDTH = 0
    FIT_TO_HEIGHT = 1
    line_styles = [Qt.SolidLine, Qt.DashLine, Qt.DashDotLine, Qt.DotLine, Qt.DashDotDotLine, Qt.CustomDashLine]

    # TODO change parameters
    def __init__(self, parent=None, active=False, demo=False, scale=1.0, drawing_mode=False):
        super(QWidget, self).__init__(parent)

        self.default_page_width = 512  # TODO change this at some point
        self.default_page_height = 768  # TODO change this at some point

        # color parameters for shape drawing
        self.contour_color = QColor(255, 255, 0)
        self.fill_color = None
        self.opacity = 1
        self.theta = 0

        self.positions = None

        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self)
        # self.paint.scrollArea = self.scrollArea

        # self.paint = QWidget()
        #
        # self.image = None
        # self.imageDraw = None
        # self.cursor = None
        #
        # self.scrollArea.setWidget(self.paint)
        #
        # dockLayout = QVBoxLayout()
        # dockLayout.addWidget(self.scrollArea)
        # layout.setMenuBar(tb)
        #
        # self.setLayout(dockLayout)
        # self.layout().addWidget(self.scrollArea)

        self.shapes = []
        self.currently_drawn_shape = None
        self.shape_to_draw = None
        self.selected_shape = []
        self.active = active
        self.active = True

        # default scaling parameters # maybe allow users to set them
        self.scale = scale
        self.min_scaling_factor = 0.1
        self.max_scaling_factor = 20
        self.zoom_increment = 0.05

        # line style parameters
        self.line_style = None

        # self.scale = 3
        drawing_mode = True
        self.drawing_mode = drawing_mode

        # self.setWidgetResizable(True)

        # KEEP IMPORTANT required to track mouse even when not clicked
        self.setMouseTracking(True)  # KEEP IMPORTANT
        # self.setBaseSize(512,512)
        # self.resize(512,512)
        # self.resizeEvent = self.onResize

        demo = True
        if demo:
            # self.shapes.append(Rect2D(0, 0, 512, 512, color=0xFF00FF, stroke=6)) # bounds
            # self.shapes.append(Polygon2D(0, 0, 10, 0, 10, 20, 0, 20, 0, 0, color=0x00FF00))
            # self.shapes.append(
            #     Polygon2D(100, 100, 110, 100, 110, 120, 10, 120, 100, 100, color=0x0000FF, fill_color=0x00FFFF,
            #               stroke=2))
            # self.shapes.append(Line2D(0, 0, 110, 100, color=0xFF0000, stroke=3))
            # self.shapes.append(Rect2D(200, 150, 250, 100, stroke=10))
            # self.shapes.append(Square2D(300, 260, 250, stroke=3))
            # self.shapes.append(Ellipse2D(0, 50, 600, 200, stroke=3))
            # self.shapes.append(Circle2D(150, 300, 30, color=0xFF0000))
            # self.shapes.append(PolyLine2D(10, 10, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
            # self.shapes.append(PolyLine2D(10, 10, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
            # self.shapes.append(Point2D(128, 128, color=0xFF0000, stroke=6))
            # self.shapes.append(Point2D(128, 128, color=0x00FF00, stroke=1))
            # self.shapes.append(Point2D(10, 10, color=0x000000, stroke=6))
            # img0 = Image2D('/D/Sample_images/sample_images_EZF/counter/00.png')
            # img1 = Image2D('/D/Sample_images/sample_images_EZF/counter/01.png')
            # img2 = Image2D('/D/Sample_images/sample_images_EZF/counter/02.png')
            # img3 = Image2D('/D/Sample_images/sample_images_EZF/counter/03.png')
            # img4 = Image2D('/D/Sample_images/sample_images_EZF/counter/04.png')
            # img5 = Image2D('/D/Sample_images/sample_images_EZF/counter/05.png')
            # img6 = Image2D('/D/Sample_images/sample_images_EZF/counter/06.png')
            # img7 = Image2D('/D/Sample_images/sample_images_EZF/counter/07.png')
            # img8 = Image2D('/D/Sample_images/sample_images_EZF/counter/08.png')
            # img9 = Image2D('/D/Sample_images/sample_images_EZF/counter/09.png')
            # img10 = Image2D('/D/Sample_images/sample_images_EZF/counter/10.png')
            #
            # row = img1 + img2 + img10
            #
            # row.setToWidth(512)
            # self.shapes.append(row)
            #
            # row2 = img4 + img5
            # row2.setToWidth(512)
            # self.shapes.append(row2)

            self.shapes.append(Polygon2D(0, 0, 10, 0, 10, 20, 0, 20, 0, 0, color=0x00FF00))
            self.shapes.append(
                Polygon2D(100, 100, 110, 100, 110, 120, 10, 120, 100, 100, color=0x0000FF, fill_color=0x00FFFF,
                          stroke=2))
            self.shapes.append(Line2D(0, 0, 110, 100, color=0xFF0000, stroke=3))
            self.shapes.append(Rect2D(200, 150, 250, 100, stroke=10, fill_color=0xFF0000))
            self.shapes.append(Ellipse2D(0, 50, 600, 200, stroke=3))
            self.shapes.append(Circle2D(150, 300, 30, color=0xFF0000, fill_color=0x00FFFF))
            self.shapes.append(PolyLine2D(10, 10, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
            self.shapes.append(PolyLine2D(10, 10, 20, 10, 20, 30, 40, 30, color=0xFF0000, stroke=2))
            self.shapes.append(Point2D(128, 128, color=0xFF0000, fill_color=0x00FFFF, stroke=0.65))
            self.shapes.append(Point2D(128, 128, color=0x00FF00, stroke=0.65))
            self.shapes.append(Point2D(10, 10, color=0x000000, fill_color=0x00FFFF, stroke=3))

            self.shapes.append(
                Rect2D(0, 0, self.default_page_width, self.default_page_height, color=0xFF00FF, stroke=6))

            path_to_counter = '/D/Sample_images/sample_images_PA/trash_test_mem/counter/'  # path_to_counter + '/'
            img0 = Image2D(path_to_counter + '/00.png')

            inset = Image2D(path_to_counter + '/01.png')
            inset2 = Image2D(path_to_counter + '/01.png')
            inset3 = Image2D(path_to_counter + '/01.png')
            # inset.setToHeight(32)
            # check inset

            scale_bar = ScaleBar(30, '<font color="#FF00FF">10µm</font>')
            scale_bar.set_P1(0, 0)
            # scale_bar.set_scale(self.get_scale())
            # # scale_bar.set_P1(self.get_P1().x()+extra_space, self.get_P1().y()+extra_space)
            img0.add_object(scale_bar, Image2D.TOP_LEFT)
            # scale_bar0 = ScaleBar(30, '<font color="#FF00FF">10µm</font>')
            # scale_bar0.set_P1(0, 0)
            # img0.add_object(scale_bar0, Image2D.TOP_LEFT)
            img0.add_object(inset3, Image2D.TOP_LEFT)

            # all seems fine and could even add insets to it --> not so hard I guess
            # check

            # see how to handle insets --> in a way they can be classical images and one should just determine what proportion of the parent image width they should occupy -->
            # need a boolean or need set fraction of orig --> jut one variable
            # maybe also need draw a square around it of a given size --> see how to do that ???

            # img0.add_object(TAText2D(text='<font color="#FF0000">top right</font>'), Image2D.TOP_RIGHT)
            # img0.add_object(TAText2D(text='<font color="#FF0000">top right2</font>'), Image2D.TOP_RIGHT)
            # img0.add_object(TAText2D(text='<font color="#FF0000">top right3</font>'), Image2D.TOP_RIGHT)

            img0.add_object(inset,
                            Image2D.BOTTOM_RIGHT)  # ça marche meme avec des insets mais faudrait controler la taille des trucs... --> TODO
            # img0.add_object(inset2, Image2D.BOTTOM_RIGHT)  # ça marche meme avec des insets mais faudrait controler la taille des trucs... --> TODO
            # img0.add_object(TAText2D(text='<font color="#FF0000">bottom right</font>'), Image2D.BOTTOM_RIGHT)
            # img0.add_object(TAText2D(text='<font color="#FF0000">bottom right2</font>'), Image2D.BOTTOM_RIGHT)
            img0.add_object(TAText2D(text='<font color="#FF0000">bottom right3</font>'), Image2D.BOTTOM_RIGHT)

            # ask whether a border should be drawn for the inset or not ??? and ask for its width...

            # ça a l'air de marcher mais voir comment faire pour gérer

            # img0.add_object(TAText2D(text='<font color="#FF0000">bottom left1</font>'), Image2D.BOTTOM_LEFT)
            # img0.add_object(TAText2D(text='<font color="#FF0000">bottom left2</font>'), Image2D.BOTTOM_LEFT)
            # img0.add_object(TAText2D(text='<font color="#FF0000">bottom left3</font>'), Image2D.BOTTOM_LEFT)

            # seems to work --> just finalize things up...

            # img0 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # size is not always respected and that is gonna be a pb but probably size would be ok for journals as they would not want more than 14 pt size ????

            # ci dessous la font size marche mais je comprend rien ... pkoi ça marche et l'autre marche pas les " et ' ou \' ont l'air clef...
            # in fact does not work font is super small
            # img0.setLetter(TAText2D(text='<font face="Comic Sans Ms" size=\'12\' color=yellow ><font size=`\'12\'>this is a <br>test</font></font>'))
            # img0.setLetter(TAText2D(text='<font face="Comic Sans Ms" color=yellow ><font size=12 >this is a <br>test</font></font>'))
            # img0.setLetter(TAText2D("<p style='font-size: large font-color: yellow'><b>Serial Number:</b></p> "))
            # a l'air de marcher mais à tester
            # img0.setLetter(TAText2D('<html><body><p><font face="verdana" color="yellow" size="2000">font_face = "verdana"font_color = "green"font_size = 3</font></html>'))

            # try that https://www.learnpyqt.com/examples/megasolid-idiom-rich-text-editor/
            # img0.setLetter(TAText2D(text='<html><font face="times" size=3 color=yellow>test</font></html>'))
            # img0.setLetter(TAText2D(text="<p style='font-size: 12pt font-style: italic font-weight: bold color: yellow text-align: center'> <u>Don't miss it</u></p><p style='font-size: 12pt font-style: italic font-weight: bold color: yellow text-align: center'> <u>Don't miss it</u></p>"))

            # this is really a one liner but a bit complex to do I find
            # chaque format different doit etre dans un span different --> facile
            # ça marche mais voir comment faire ça
            # img0.setLettering(TAText2D(
            #     text='<p style="text-align:leftcolor: yellow">This text is left aligned <span style="float:rightfont-style: italicfont-size: 8pt"> This text is right aligned </span><span style="float:rightfont-size: 4ptcolor:red"> This text is another text </span></p>'))
            img0.setLettering('<font color="red">A</font>')
            # letter
            img0.annotation.append(Rect2D(88, 88, 200, 200, stroke=3, color=0xFF00FF))
            img0.annotation.append(Ellipse2D(88, 88, 200, 200, stroke=3, color=0x00FF00))
            img0.annotation.append(Circle2D(33, 33, 200, stroke=3, color=0x0000FF))
            img0.annotation.append(Line2D(33, 33, 88, 88, stroke=3, color=0x0000FF))
            img0.annotation.append(Freehand2D(10, 10, 20, 10, 20, 30, 288, 30, color=0xFFFF00, stroke=3))
            # img0.annotation.append(PolyLine2D(10, 10, 20, 10, 20, 30, 288, 30, color=0xFFFF00, stroke=3))
            img0.annotation.append(Point2D(128, 128, color=0xFFFF00, stroke=6))
            # everything seems to work but do check

            img1 = Image2D(path_to_counter + '/01.png')
            # img1 = Image2D('D:/dataset1/unseen/focused_Series012.png')
            # img1.setLetter(TAText2D(text="<font face='Comic Sans Ms' size=16 color='blue' >this is a <br>test</font>"))
            # ça ça marche vraiment en fait --> use css to write my text instead of that

            # ça ça a l'air de marcher --> pas trop mal en fait du coup
            # ça a l'air de marcher maintenant --> could use that and do a converter for ezfig ???
            # img1.setLetter(TAText2D(text="<span style='font-size: 12pt font-style: italic font-weight: bold color: yellow paddind: 20px text-align: center'> <u>Don't miss it</u></span><span style='font-size: 4pt font-style: italic font-weight: bold color: #00FF00 paddind: 3px text-align: right'> <u>test2</u></span>"))

            # TODO need remove <meta name="qrichtext" content="1" /> from the stuff otherwise alignment is not ok... TODO --> should I offer a change to that ??? maybe not
            test_text = '''
                </style></head><body style=" font-family:'Comic Sans MS' font-size:22pt font-weight:400 font-style:normal">
                <p style="color:#00ff00"><span style=" color:#ff0000">toto</span><br />tu<span style=" vertical-align:super">tu</span></p>
                '''
            img1.setLettering(TAText2D(text=test_text))

            # background-color: orange
            # span div et p donnent la meme chose par contre c'est sur deux lignes
            # display:inline float:left # to display as the same line .... --> does that work html to svg
            # https://stackoverflow.com/questions/10451445/two-div-blocks-on-same-line --> same line for two divs

            img2 = Image2D(path_to_counter + '/02.png')
            # crop is functional again but again a packing error
            img2.crop(left=60)
            img2.crop(right=30)
            img2.crop(bottom=90)
            img2.crop(top=60)
            # img2.crop(all=0) # reset crop
            # img2.crop(top=0) # reset crop --> seems ok
            # now seems ok --> see how to do that with figures/vector graphics ...
            # img2.crop(right=60)
            # img2.crop(bottom=60)
            img3 = Image2D(path_to_counter + '/03.png')
            img4 = Image2D(path_to_counter + '/04.png')
            img5 = Image2D(path_to_counter + '/05.png')
            img6 = Image2D(path_to_counter + '/06.png')
            img7 = Image2D(path_to_counter + '/07.png')
            img8 = Image2D(path_to_counter + '/08.png')

            # reference point is the original image and stroke should be constant irrespective of zoom --> most likely need the scaling factor too there
            # reference size is also the underlying original image --> TODO
            # img8.annotation.append(Line2D(0, 0, 110, 100, color=0xFF0000, stroke=3))
            img8.annotation.append(Rect2D(60, 60, 100, 100, stroke=20, color=0xFF00FF))
            # need make the scale rese
            # img8.annotation.append(Ellipse2D(0, 50, 600, 200, stroke=3))

            img9 = Image2D(path_to_counter + '/09.png')
            img10 = Image2D(path_to_counter + '/10.png')
            # Data for plotting
            import numpy as np
            import matplotlib.pyplot as plt

            t = np.arange(0.0, 2.0, 0.01)
            s = 1 + np.sin(2 * np.pi * t)

            fig, ax = plt.subplots()
            ax.plot(t, s)

            ax.set(xlabel='time (s)', ylabel='voltage (mV)',
                   title='About as simple as it gets, folks')
            ax.grid()

            # plt.show()
            # fig.savefig("test.png")
            # plt.show()
            # ça marche --> voici deux examples de shapes

            # first graph test --> TODO improve that
            graph2d = VectorGraphics2D(fig)
            graph2d.crop(all=20)  # not great neither

            # D:/sample_images_svg/
            # /D/Sample_images/sample_images_svg/
            path_to_svg = '/D/Sample_images/sample_images_svg/'
            vectorGraphics = VectorGraphics2D(path_to_svg + 'cartman.svg')

            # nb cropping marche en raster mais pas en svg output --> besoin de faire un masque d'ecretage --> pourrait aussi dessiner un rectangle de la meme taille de facon à le faire

            # TODO KEEP unfortunately cropping does not work when saved as svg but works when saved as raster...
            vectorGraphics.crop(left=10, right=30, top=10, bottom=10)
            animatedVectorGraphics = VectorGraphics2D(
                path_to_svg + 'animated.svg')  # car n'existe pas --> bloquer addition si existe pas
            # print(animatedVectorGraphics.isSet)

            # bug cause shears the stuff --> would need crop the other dimension too to maintain AR
            animatedVectorGraphics.crop(left=30)  # , top=20, bottom=20

            # self.shapes.append(graph2d)

            # img10 = Image2D(path_to_counter + '/10.png')
            # img2 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # img3 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # img4 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # img5 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # img6 = Image2D('D:/dataset1/unseen/focused_Series012.png')
            # img7 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # img8 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # img9 = Image2D('D:/dataset1/unseen/100708_png06.png')
            # img10 = Image2D('D:/dataset1/unseen/focused_Series012.png')

            # is row really different from a panel ??? probably not that different
            # row = img1 + img2

            # self.shapes.append(row)
            # self.shapes.append(row)

            # pkoi ça creerait pas plutot un panel
            # au lieu de creer une row faut creer des trucs
            # row2 = img4 + img5
            # fig = row / row2
            # fig = col(row, row2, width=512)# ça c'est ok
            # self.shapes.append(fig)

            # TODO add image swapping and other changes and also implement sticky pos --> just need store initial pos

            # print(len(row))
            # for img in row:
            #     print(img.boundingRect())

            # fig.setToWidth(512) # bug is really here I do miss something but what and why

            # print('rows', len(fig))
            # for r in fig:
            #     print('bounding rect', r.boundingRect())
            #     print('cols in row', len(r))

            # self.shapes.append(fig)

            # bug in row is due to the vectorial object
            # peut etre si rien n'est mis juste faire une row avec un panel
            # c'est animated vector graphics qui me met dedans
            row1 = Row(img0, img1, graph2d, animatedVectorGraphics, img2) #  , graph2d, animatedVectorGraphics  # , img6, #, nCols=3, nRows=2 #le animated marche mais faut dragger le bord de l'image mais pas mal qd meme
            # see how I should handle size of graphs but I'm almost there

            # marche pas en fait car un truc ne prend pas en charge les figs
            # ça marche donc en fait tt peut etre un panel en fait

            col1 = Column(img4, img5, vectorGraphics, img6)  # ,  , img6, img6, nCols=3, nRows=2,# ,
            col2 = Column(img3, img7, img10)
            #
            # col1.setLettering('<font color="#FFFFFF">A</font>')

            # col1+=col2
            # col1 //= col2
            # hack test1
            # from epyseg.figure.alignment import alignRight, alignLeft, alignTop, alignBottom, alignCenterH, \
            #     alignCenterV, packY, \
            #     packX, packYreverse

            # TODO replace code by the following to avoid errors
            # hack this and set this as the row packer
            if False:
                alignTop(Point2D(col1.topLeft()), *[col1, col2, row1])
                packX(3, Point2D(col1.topLeft()), *[col1, col2, row1])  # ça marche
                # par contre controler la width de tout n'est pas facile --> voir comment faire
                # une fois que tt est bon
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds', bounds)
                setToWidth(512, *[col1, col2,
                                  row1])  # ça marche mais ne respecte absolument pas les proportions en hauteur qui sont differentes --> comment corriger
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds2', bounds)
                # if worked ok otherwise refine size
                # TODO
                # if col1.boundingRect().height()!=col2.boundingRect().height():
                #     print()
                print(col1.boundingRect().height(), col2.boundingRect().height(), row1.boundingRect().height())
                # prendre la taille min des trois et augmenter jusqu'à obtenir la desired width
                # take min height then increase to get desired
                min_width = min(col1.boundingRect().height(), col2.boundingRect().height(),
                                row1.boundingRect().height())

                print('min height', min_width)
                # en math la solution doit etre l'intersection de n droites --> pas sur reflechir en fait c'est pas en 2D en fait non ? reflechir
                while True:
                    setToHeight(min_width, *[col1, col2, row1])
                    bounds = updateBoudingRect(*[col1, col2, row1])
                    if bounds.width() >= 512:
                        print('finally', bounds.width(), min_width)
                        break
                    min_width += 1

                # marche mais un peu slow --> ameliorer ça qd meme et faire du fake pr gagner du temps
                # d'ailleurs ne pas reellement packer en fait juste calculer la somme des width avec le spacing pr voir si tt est bon ou pas
                min_width -= 1
                #  then once execeeded --> refine it
                while True:
                    min_width += 0.05
                    setToHeight(min_width, *[col1, col2, row1])
                    bounds = updateBoudingRect(*[col1, col2, row1])
                    if bounds.width() >= 512:
                        print('finally', bounds.width(), min_width)
                        break

            # setwidth for cols
            if False:
                alignLeft(Point2D(col1.topLeft()), *[col1, col2, row1])

                # par contre controler la width de tout n'est pas facile --> voir comment faire
                # une fois que tt est bon
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds', bounds)
                # for
                # col1.setToWidth(512)
                # col2.setToWidth(512)
                # row1.setToWidth(512)
                # packY(3, Point2D(col1.topLeft()), *[col1, col2, row1])  # ça marche
                setToWidth2(512, *[col1, col2,
                                   row1])
                # setToWidth(512, *[col1, col2,
                #                   row1])  # ça marche mais ne respecte absolument pas les proportions en hauteur qui sont differentes --> comment corriger
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds2', bounds)
                # if worked ok otherwise refine size
                # TODO
                # if col1.boundingRect().height()!=col2.boundingRect().height():
                #     print()
                print(col1.boundingRect().height(), col2.boundingRect().height(), row1.boundingRect().height())

            # everything seems to work now
            # setheight for rows
            if False:
                alignTop(Point2D(col1.topLeft()), *[col1, col2, row1])

                # par contre controler la width de tout n'est pas facile --> voir comment faire
                # une fois que tt est bon
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds', bounds)
                # for
                # col1.setToHeight(512)
                # col2.setToHeight(512)
                # row1.setToHeight(512)
                # packX(3, Point2D(col1.topLeft()), *[col1, col2, row1])  # ça marche
                setToHeight(512, *[col1, col2,
                                   row1])
                # setToWidth(512, *[col1, col2,
                #                   row1])  # ça marche mais ne respecte absolument pas les proportions en hauteur qui sont differentes --> comment corriger
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds2', bounds)
                # if worked ok otherwise refine size
                # TODO
                # if col1.boundingRect().height()!=col2.boundingRect().height():
                #     print()
                print(col1.boundingRect().height(), col2.boundingRect().height(), row1.boundingRect().height())

            # fits in height col --> works ok but figure out math there too
            if False:
                alignLeft(Point2D(col1.topLeft()), *[col1, col2, row1])
                packY(3, Point2D(col1.topLeft()), *[col1, col2, row1])  # ça marche
                # par contre controler la width de tout n'est pas facile --> voir comment faire
                # une fois que tt est bon
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds', bounds)
                setToHeight2(512, *[col1, col2,
                                    row1])  # ça marche mais ne respecte absolument pas les proportions en hauteur qui sont differentes --> comment corriger
                bounds = updateBoudingRect(*[col1, col2, row1])
                print('bounds2', bounds)
                # if worked ok otherwise refine size
                # TODO
                # if col1.boundingRect().height()!=col2.boundingRect().height():
                #     print()
                print(col1.boundingRect().width(), col2.boundingRect().width(), row1.boundingRect().width())
                # prendre la taille min des trois et augmenter jusqu'à obtenir la desired width
                # take min height then increase to get desired
                min_width = min(col1.boundingRect().width(), col2.boundingRect().width(),
                                row1.boundingRect().width())

                print('min height', min_width)
                # en math la solution doit etre l'intersection de n droites --> pas sur reflechir en fait c'est pas en 2D en fait non ? reflechir
                while True:
                    setToWidth2(min_width, *[col1, col2, row1])
                    bounds = updateBoudingRect(*[col1, col2, row1])
                    if bounds.height() >= 512:
                        print('finally', bounds.height(), min_width)
                        break
                    min_width += 1

                # marche mais un peu slow --> ameliorer ça qd meme et faire du fake pr gagner du temps
                # d'ailleurs ne pas reellement packer en fait juste calculer la somme des width avec le spacing pr voir si tt est bon ou pas
                min_width -= 1
                #  then once execeeded --> refine it
                while True:
                    min_width += 0.05
                    setToWidth2(min_width, *[col1, col2, row1])
                    bounds = updateBoudingRect(*[col1, col2, row1])
                    if bounds.height() >= 512:
                        print('finally', bounds.height(), min_width)
                        break

                # alignLeft(Point2D(col1.topLeft()), *[col1, col2, row1])
                # packY(3, Point2D(col1.topLeft()), *[col1, col2, row1])  # ça marche

                # c'est parfait --> le probleme vient juste si je veux setter en height le truc --> a ce moment la faut refaire tt le truc

                # prendre la taille min des trois et augmenter jusqu'à obtenir la desired width
                # take min height then increase to get desired
                # min_height = min(col1.boundingRect().height(), col2.boundingRect().height(),
                #                  row1.boundingRect().height())
                #
                # print('min height', min_height)
                # en math la solution doit etre l'intersection de n droites --> pas sur reflechir en fait c'est pas en 2D en fait non ? reflechir
                # while True:
                #     setToHeight(min_height, *[col1, col2, row1])
                #     bounds = updateBoudingRect(*[col1, col2, row1])
                #     if bounds.width() >= 512:
                #         print('finally', bounds.width(), min_height)
                #         break
                #     min_height += 1

                # marche mais un peu slow --> ameliorer ça qd meme et faire du fake pr gagner du temps
                # d'ailleurs ne pas reellement packer en fait juste calculer la somme des width avec le spacing pr voir si tt est bon ou pas
                # min_height -= 1
                #  then once execeeded --> refine it
                # while True:
                #     min_height += 0.05
                #     setToHeight(min_height, *[col1, col2, row1])
                #     bounds = updateBoudingRect(*[col1, col2, row1])
                #     if bounds.width() >= 512:
                #         print('finally', bounds.width(), min_height)
                #         break

            # brute force --> replace by maths
            # marche enfin mais slow --> faut faire un emulate du retaillage mais pas vraiment retailler le truc sinon marche pas...

            # faudrait calculer une height qui soit la meme pour tous et qui respecte la deisred width --> comment faire en fait???
            # doit calculer ça de part l'incompressible height
            # en fait doit pouvoir calculer la width globale depuis la height actuelle et aussi je connais la fraction de la width occupee par le truc actuel moins l'incompressible width et ça doit rester constant ??? --> est ce correct ? peut etre en fait
            # if size if above then decrease all heights until a value fits --> then refine if smaller --> decrease stuff

            # en fait c'est la taille en y qui doit etre fixe et faut gérer le tout dedans...

            # bug c quoi ???
            # tres dur de mettre à la bonne taille car forme tres complexe due à l'imbrication
            # tester

            # je pense que c'est ça en fait

            # col1+=img3

            # print('mega begin', panel2.nCols, panel2.nRows, panel2.orientation, len(panel2.images), type(panel2), panel2.boundingRect())
            # print('mega begin', len(col1.images), type(col1), col1.boundingRect())

            # ok need increment and need see how to change the font of the stuff and bg color and fg color --> TODO but ok for now
            row2 = Row(img8, img9)
            row2.setLettering('<font color="#FFFFFF">a</font>')

            # row1+=row2
            # row1 //= row2
            # hack test 2
            # from epyseg.figure.alignment import alignRight, alignLeft, alignTop, alignBottom, alignCenterH, \
            #     alignCenterV, packY, \
            #     packX, packYreverse

            # row1 = row1 | row2
            # row1 |= row2

            # essayer entre types pr voir si ça marche
            # row1//=col1
            # hack test 3

            # row1 % row2 #TODO IMPLEMENT THAT PROPERLY

            # row1+= img7

            # all seems fine now

            # BUG IN ROW SET TO WIDTH AND ALSO IN ROW / --> fix all of this some day

            # panel = Panel(img0)# , img1, img2, img3)  # , img6, #, nCols=3, nRows=2

            # # marche pas en fait car un truc ne prend pas en charge les figs
            #
            # # ça marche donc en fait tt peut etre un panel en fait
            #
            # panel2 = Panel(img4, img5)  # ,

            # panel2.setToWidth(256)
            # panel3.setToWidth(256)
            # panel.setToWidth(256)

            # print(type(col1))

            # tt marche
            # should I put align top left or right...
            # should I put align top left or right...

            # col1.setToHeight(512)  # creates big bugs now
            # panel3.setToWidth(512)
            # row1.setToWidth(512) # TODO FIX THIS SOON

            # print(type(row1))# should be a col
            # print(row1.boundingRect())
            # for panel in row1:
            #     print('size', panel.boundingRect())#bug in boundingrect here is it due to the hack of bounding rtect of rect2D

            # row1.setLettering('<font color="#FF00FF">B</font>')
            # row1.setLettering(' ') # remove letters
            # row1.setToWidth(1024)
            # ça a l'air de marcher...

            # it now seems ok
            # from epyseg.figure.alignment import alignRight, alignLeft, alignTop, alignBottom, alignCenterH, alignCenterV

            # alignLeft(row1, col1)
            # alignRight(row1, col1)
            # alignTop(row1, col1)
            # alignBottom(row1, col1)
            # alignCenterH(row1, col1)
            # alignCenterV(row1, col1)

            # can I add self to any of the stuff --> check --> if plus --> adds if divide --> stack it --> good idea and quite simple

            # fig = col(panel,panel2,panel3)

            # panel2+=panel
            # print(type(panel2))

            # panel2.setToHeight(512)
            # panel2.setToWidth(512)

            # all seems fine now --> see how I can fix things

            # panel2+=panel3 # bug here cause does not resize the panel properly
            # print('mega final', panel2.nCols, panel2.nRows, panel2.orientation, len(panel2.images), type(panel2), panel2.boundingRect(), panel.boundingRect())
            # print('mega final', len(col1.images), type(col1), col1.boundingRect(), row1.boundingRect())

            # on dirait que tt marche

            # maintenant ça marche mais reessayer qd meme
            # panel2.setToWidth(256) # seems still a very modest bug somewhere incompressible height and therefore ratio is complex to calculate for width with current stuff --> see how I can do --> should I ignore incompressible within stuff --> most likely yes... and should set its width and height irrespective of that
            # panel2.setToWidth(512) # seems still a very modest bug somewhere incompressible height and therefore ratio is complex to calculate for width with current stuff --> see how I can do --> should I ignore incompressible within stuff --> most likely yes... and should set its width and height irrespective of that

            # panel2.setToHeight(1024) #marche pas --> à fixer
            # panel2.setToHeight(128) # marche pas --> faut craiment le coder en fait --> voir comment je peux faire ça

            # marche pas non plus en fait --> bug qq part
            # panel2.setToHeight(82.65128578548527) # marche pas --> faut craiment le coder en fait --> voir comment je peux faire ça

            # panel += img7
            # panel -= img0
            # panel -= img1
            # panel -= img10
            # self.shapes.append(panel)
            # panel2.set_P1(256, 300)

            # panel2.set_P1(512,0)
            # panel3.set_P1(1024, 0)
            # self.shapes.append(panel2)

            img14 = Image2D(path_to_counter + '/04.png')
            img15 = Image2D(path_to_counter + '/05.png')
            img16 = Image2D(path_to_counter + '/06.png')
            panel_hor = img14 | img15 | img16
            panel_hor.set_P1(256, 256)

            img14b = Image2D(path_to_counter + '/04.png')
            img15b = Image2D(path_to_counter + '/05.png')
            img16b = Image2D(path_to_counter + '/06.png')
            panel_vertb = img14b / img15b / img16b
            panel_vertb.set_P1(128, 128)

            # nb need compute size without extra space --> that is the desired size in fact!!!
            col1.setToHeight(512)
            # col2.setToHeight(512)
            print('col1', col1.boundingRect())  # not ok --> bigger
            print('row1-0', row1.boundingRect())  # not ok --> bigger
            row1.setToWidth(512)
            print('row1-1', row1.boundingRect())  # not ok --> bigger

            print('test', updateBoudingRect(row1))

            panel_hor.setToWidth(256)
            print(panel_hor.boundingRect())
            panel_vertb.setToHeight(256)
            print('panel_vertb', panel_vertb.boundingRect())

            self.shapes.append(panel_hor)
            self.shapes.append(panel_vertb)
            self.shapes.append(col1)
            # self.shapes.append(col2)
            self.shapes.append(row1)
            # self.shapes.append(row2)

            # self.shapes.append(Rect2D(0, 0, 512, 512, stroke=10, scale=0.5, fill_color=0xFF0000))

            # big bug marche pas
            # packX(3, None, *[img0, img1, img2])  # ça marche presque de nouveau

            # print(img0.boundingRect(), img1.boundingRect(), img2.boundingRect())
            #
            # self.shapes.append(img0)
            # self.shapes.append(img1)
            # self.shapes.append(img2)

            img4.setLettering('<font color="#0000FF">Z</font>')  # ça marche mais voir comment faire en fait
            # self.shapes.append(fig)

            # panel2 | panel
            # panel2 | panel # for swapping panels
            # panel | panel2

            # panel << img3

            # ça ne marche pas pkoi

            # img3 >> panel # does not work --> need implement it in my image2D

            # panel >> img3

            # cannot be dragged --> is it because self.is_set
            # row.packX()
            # row.packY() # ça marche mais finaliser le truc pr que ça soit encore plus simple à gerer
            # img.setP1(10,10) #translate it --> cool
            # self.shapes.append(img1)
            # self.shapes.append(img2)
            # self.shapes.append(img3)

            # fig = row / row2
            # fig = Column(row, row2)
            # self.shapes.append(fig)
            self.drawing_mode = True
            # self.shape_to_draw = Line2D
            # self.shape_to_draw = Rect2D
            # self.shape_to_draw = Square2D
            # self.shape_to_draw = Ellipse2D
            # self.shape_to_draw = Circle2D
            # self.shape_to_draw = Point2D  # ok maybe small centering issue
            # self.shape_to_draw = Freehand2D
            # self.shape_to_draw = PolyLine2D
            # self.shape_to_draw = Polygon2D
            self.shape_to_draw = Rect2D

            # TODO freehand drawing
            # TODO broken line --> need double click for end
            self.update_size()

    def set_scale(self, scale):
        # same scale nothing to do
        if scale == self.scale:
            return
        if scale >= self.max_scaling_factor:
            self.scale = self.max_scaling_factor
            logger.warning('Zoom exceeds max_scaling_factor --> ignoring')
        elif scale <= self.min_scaling_factor:
            self.scale = self.min_scaling_factor
            logger.warning('Zoom is below min_scaling_factor --> ignoring')
        else:
            self.scale = scale
        self.update_size()
        self.update()

    # pas trop dur en fait
    def scale_to_window(self, window_size, mode=FIT_TO_WIDTH, scroll_size=20):
        if window_size is not None:
            bounds = updateBoudingRect(*self.shapes)
            if mode == self.FIT_TO_WIDTH:
                scaling_to_fit = (window_size.width() - scroll_size) / bounds.width()
            else:
                scaling_to_fit = (window_size.height() - scroll_size) / bounds.height()
            self.set_scale(scaling_to_fit)

    def reset_scale(self):
        self.set_scale(1)

    def zoom_in(self):
        self.set_scale(self.scale + self.zoom_increment)


    def zoom_out(self):
        self.set_scale(self.scale - self.zoom_increment)

        # def resizeEvent(self, event):

    #     pixmap1 = QtGui.QPixmap("image.png")
    # self.pixmap = pixmap1.scaled(self.width(), self.height())
    # self.label.setPixmap(self.pixmap)
    # self.label.resize(self.width(), self.height())

    # def onResize(self, event):
    #     self.resize(event.size())

    # def mousePressEvent(self, event):
    #
    #     self.clickCount = 1
    #     if self.vdp.active:
    #         self.vdp.mousePressEvent(event)
    #         self.update()
    #         return
    #
    #     if event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.RightButton:
    #         self.drawing = True
    #         zoom_corrected_pos = event.pos() / self.scale
    #         self.lastPoint = zoom_corrected_pos
    #         self.drawOnImage(event)

    # def mouseMoveEvent(self, event):
    #
    #     if self.statusBar:
    #         # print(event.pos)
    #         zoom_corrected_pos = event.pos() / self.scale
    #         self.statusBar.showMessage('x=' + str(zoom_corrected_pos.x()) + ' y=' + str(
    #             zoom_corrected_pos.y()))  # show color and rgb value of it
    #         # QMainWindow.statusBar().showMessage('x=' + str(zoom_corrected_pos.x()) + ' y=' + str(zoom_corrected_pos.y()))
    #
    #     if self.vdp.active:
    #         self.vdp.mouseMoveEvent(event)
    #         # print("in here 323232")
    #         # maybe should not update
    #         # maybe should only update the region of interest --> get field of view of scrollpane
    #
    #         # viewPortSizeHint
    #         # self.s
    #
    #         # print(self.scrollArea.sizeHint())
    #         # print(self.scrollArea.viewportSizeHint())
    #
    #         # ça marche pas du tout ça donne pas la taille de la zone vue --> null
    #         # painter = QtGui.QPainter(self.cursor)
    #         # print("test ", painter.viewport()) # ça donne la taille de toute l'image
    #         # painter.end()
    #
    #         # QWidget::visibleRegion
    #         # QAbstractScrollArea::viewport
    #         # print(self.scrollArea.widget().visibleRegion())
    #         # view region = self.scrollArea.widget().visibleRegion()
    #         # Only update the visible rect
    #         region = self.scrollArea.widget().visibleRegion()
    #         # print(region.boundingRect()) # parfait voilà ce que je veux
    #
    #         self.update(region)
    #         return
    #
    #     self.drawOnImage(event)

    def color_picker(self, method_to_set_color):
        # how to create a canceled color
        # could even store alpha channel

        # dialog = QColorDialog()
        # dialog.setOption(QColorDialog.ShowAlphaChannel, on=True)
        # # dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Run")
        # dialog.setOption(QColorDialog.DontUseNativeDialog, on=True)
        #
        # buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, dialog)
        # buttons.accepted.connect(dialog.accept)
        # buttons.rejected.connect(dialog.reject)
        # buttons.button(QDialogButtonBox.Ok).setDefault(True)  # force Ok as default
        # buttons.button(QDialogButtonBox.Cancel).setAutoDefault(False)  # prevent Cancel to be the default button
        #
        # preview_button = QPushButton('No Color/transparent')
        #
        # def no_color():
        #     dialog.done(3)
        #
        # preview_button.clicked.connect(no_color)
        # buttons.addButton(preview_button, QDialogButtonBox.ApplyRole)
        #
        # if dialog.exec_() == QDialog.Accepted:
        #     c = dialog.selectedColor()
        # #     if color.isValid():
        # # c = QColorDialog.getColor()
        #     if c.isValid(): # make sure the user did not cancel otherwise ignore
        #         self.sender().setStyleSheet("background-color: "+str(c.name()))
        #         return c
        # return None

        dialog = NoColorDialog()
        dialog.show()

        result = dialog.exec_()

        # print(result)

        if result == QDialog.Accepted:
            c = dialog.selectedColor()
            if c.isValid():  # make sure the user did not cancel otherwise ignore # useless with current code
                # print(c.name())
                self.sender().setStyleSheet("background-color: " + str(c.name()))
                self.sender().setText(c.name())
                method_to_set_color(c)
                # return c
        elif result == QDialog.Rejected:
            # return None
            pass
        else:
            self.sender().setStyleSheet('')
            self.sender().setText('None')
            method_to_set_color(None)
            # return None

    # def fill_color_picker(self):
    #     c = QColorDialog.getColor()
    #     self.sender().setStyleSheet("background-color: " + str(c.name()))
    #     return c

    def change_shape(self):

        # this is how one gets the sender text --> this way I can centralize things
        # very good
        # print(self.sender().text(), "pressed")
        sender = self.sender().toolTip().lower()

        # drawing_methods = [Line2D, Rect2D, Square2D, Ellipse2D, Circle2D, Point2D, Freehand2D, PolyLine2D, Polygon2D]
        # print(sender)
        if 'square' in sender:
            self.shape_to_draw = Square2D
        elif 'rect' in sender:
            self.shape_to_draw = Rect2D
        elif 'elli' in sender:
            self.shape_to_draw = Ellipse2D
        elif 'circle' in sender:
            self.shape_to_draw = Circle2D
        elif 'point' in sender:
            self.shape_to_draw = Point2D
        elif 'free' in sender or 'hand' in sender:
            self.shape_to_draw = Freehand2D
        elif 'poly' in sender and 'line' in sender:
            self.shape_to_draw = PolyLine2D
        elif 'poly' in sender and 'gon' in sender:
            self.shape_to_draw = Polygon2D
        elif 'line' in sender:
            self.shape_to_draw = Line2D
        else:
            print(sender, 'Shape not supported yet!!!')
            self.shape_to_draw = None

        # print('current shape type', self.shape_to_draw)

        # if btn is not None:
        #     # change shape to draw
        #     print(btn.text(), "pressed")
        # if btn == self.button1:
        # Button 1 was clicked
        # pass
        # elif btn == self.button2:
        #     pass
        # Button 2 was clicked

    #
    # def mouseReleaseEvent(self, event):
    #
    #     if self.vdp.active:
    #         self.vdp.mouseReleaseEvent(event)
    #         self.update()  # required to update drawing
    #         return
    #
    #     if event.button == QtCore.Qt.LeftButton:
    #         self.drawing = False
    #
    #     if self.clickCount == 1:
    #         QTimer.singleShot(QApplication.instance().doubleClickInterval(),
    #                           self.updateButtonCount)
    #     # else:
    #     #     # Perform double click action.
    #     #     self.message = "Double Click"
    #     #     print("Double click")
    #     # self.update()
    #
    #     # REMOVE THIS THIS IS JUST TO SHOW AND SAVE THE IMAGE DRAWN
    #     # self.imageDraw.save('./../trash/mask.png')
    #     # ça marche --> ça ne sauve en effet que le mask ---> TROP COOL --> TRES FACILE DE RECUPERER CE QUI A ETE DESSINE


    def __save_selection_position(self):
        self.positions = None
        if self.selected_shape is None or not self.selected_shape:
            return self.positions
        self.positions = [img.get_P1() for img in self.selected_shape]

    def __restore_selection_position(self):
        if self.selected_shape is None  or not self.selected_shape:
            return
        if self.positions is None:
            return
        for pos in range(len(self.positions)):
            self.selected_shape[pos].set_P1(self.positions[pos])

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(1)
        visibleRect = None
        # if len(args) >= 2:
        #       visibleRect = args[1]

        painter.save()
        if self.scale != 1.0:
            painter.scale(self.scale, self.scale)

        for shape in self.shapes:
            # only draw shapes if they are visible --> requires a visiblerect to be passed
            if visibleRect is not None:
                # only draws if in visible rect
                if shape.boundingRect().intersects(QRectF(visibleRect)):
                    shape.draw(painter)
            else:
                shape.draw(painter)

        if self.currently_drawn_shape is not None:
            if self.currently_drawn_shape.isSet:
                self.currently_drawn_shape.draw(painter)

        sel = self.create_master_rect()

        # draw a selection on top of everything else
        if sel is not None:
            pen = QPen(QColor(0xFF0000))
            pen.setStyle(Qt.DashDotLine)
            painter.setPen(pen)  # draw red transparent selection
            painter.setOpacity(0.5)
            painter.drawRect(sel)
        painter.restore()
        del painter

    # def paintEvent(self, event):
    #     canvasPainter = QtGui.QPainter(self)
    #     # the scrollpane visible region
    #     visibleRegion = self.scrollArea.widget().visibleRegion()
    #     # the corresponding rect
    #     visibleRect = visibleRegion.boundingRect()
    #     # the visibleRect taking zoom into account
    #     scaledVisibleRect = QRect(visibleRect.x() / self.scale, visibleRect.y() / self.scale,
    #                               visibleRect.width() / self.scale, visibleRect.height() / self.scale)
    #     if self.image is None:
    #         canvasPainter.eraseRect(visibleRect)
    #         canvasPainter.end()
    #         return
    #     canvasPainter.drawImage(visibleRect, self.image, scaledVisibleRect)
    #     # canvasPainter.drawImage(self.rect(), self.image, self.image.rect())  # KEEP ORIGINAL
    #     if not self.vdp.active:
    #         # canvasPainter.drawImage(self.rect(), self.imageDraw, self.imageDraw.rect()) # KEEP ORIGINAL
    #         canvasPainter.drawImage(visibleRect, self.imageDraw, scaledVisibleRect)
    #         # should draw the cursor
    #     canvasPainter.drawImage(visibleRect, self.cursor, scaledVisibleRect)
    #     # canvasPainter.drawImage(self.rect(), self.cursor, self.cursor.rect())# KEEP ORIGINAL
    #     if self.vdp.active:
    #         self.vdp.paintEvent(canvasPainter, scaledVisibleRect)  # to draw shape # here too would be cool
    #     canvasPainter.end()

    def group_contains(self, x, y):
        # checks if master rect for group contains click
        # get bounds and create union and compare
        master_rect = self.create_master_rect()
        if master_rect is None:
            return False
        return master_rect.contains(QPointF(x, y))

    def create_master_rect(self):
        master_rect = None
        if self.selected_shape:
            for shape in self.selected_shape:
                if master_rect is None:
                    master_rect = shape.boundingRect()
                else:
                    master_rect = master_rect.united(shape.boundingRect())
        return master_rect

    def set_rotation(self, theta):
        if theta is not None:
            # if opacity >= 2:
            #     opacity /= 100
            if theta < 0:
                logger.error('Rotation angle must be in degrees between 0 and 360')
                return
            self.theta = theta
        if self.selected_shape:
            for shape in self.selected_shape:
                if not isinstance(shape, Column) and not isinstance(shape, Row) and not isinstance(shape,
                                                                                                   Point2D) and not isinstance(
                        shape, Circle2D):
                    shape.theta = self.theta
            self.update()

    def set_opacity(self, opacity):
        if opacity is not None:
            if opacity >= 2:
                opacity /= 100
            if opacity < 0:
                logger.error('opacity must be between 0 and 1 or 0 and 100')
                return
            self.opacity = opacity
        if self.selected_shape:
            for shape in self.selected_shape:
                if not isinstance(shape, Column) and not isinstance(shape, Row):
                    shape.set_opacity(self.opacity)
            self.update()

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color
        if self.selected_shape:
            for shape in self.selected_shape:
                if not isinstance(shape, Column) and not isinstance(shape, Row):
                    shape.fill_color = fill_color
            self.update()

    def set_contour_color(self, contour_color):
        self.contour_color = contour_color
        if self.selected_shape:
            for shape in self.selected_shape:
                if not isinstance(shape, Column) and not isinstance(shape, Row):
                    shape.color = contour_color
            self.update()

    def set_line_style(self, style):
        '''allows lines to be dashed or dotted or have custom pattern

        :param style: a list of numbers or any of the following Qt.SolidLine, Qt.DashLine, Qt.DashDotLine, Qt.DotLine, Qt.DashDotDotLine but not Qt.CustomDashLine, Qt.CustomDashLine is assumed by default if a list is passed in. None is also a valid value that resets the line --> assume plain line
        :return:
        '''

        # TODO add more controls or do it in a more comprehensive way
        if isinstance(style, list):
            if len(style) % 2 != 0:
                logger.error('Dash pattern not of even length --> ignoring, try 1,4 or 1,4,5,4 or alike')
                return
        else:
            if style not in self.line_styles[:-1]:
                logger.error('Unknonw Dash pattern --> ignoring')
                return

        self.line_style = style
        # if style is a list then assume custom pattern otherwise apply solidline
        if self.selected_shape:
            for shape in self.selected_shape:
                shape.set_line_style(self.line_style)
            self.update()

    def bring_to_front(self):
        # print('bring sel to front')
        if self.selected_shape:
            self.shapes = [e for e in self.shapes if e not in self.selected_shape]
            self.shapes.extend(self.selected_shape)
        self.update()

    def send_to_back(self):
        # print('send to back')
        if self.selected_shape:
            self.shapes = [e for e in self.shapes if e not in self.selected_shape]
            # TODO maybe I should keep the original order in the list, but ok for now and no big deal
            for shape in self.selected_shape:
                self.shapes.insert(0, shape)
        self.update()

    def move_to_origin(self):
        if self.selected_shape:
            for shape in self.selected_shape:
                shape.set_P1(QPointF(0,
                                     0))  # TODO fix set_P1 that it always works the same for every shapes and takes point or values here 0,0 does not work for some shapes dunno which
        self.update()

    def erode(self):
        # print('bring sel to front')
        if self.selected_shape:
            for shape in self.selected_shape:
                shape.erode()
        self.update()

    def dilate(self):
        # print('bring sel to front')
        if self.selected_shape:
            for shape in self.selected_shape:
                shape.dilate()
        self.update()

    def remove_selection(self):
        # print('called remove sel')
        if self.selected_shape:
            self.shapes = [e for e in self.shapes if e not in self.selected_shape]
            del self.selected_shape
            self.selected_shape = []
        del self.currently_drawn_shape
        self.currently_drawn_shape = None
        self.update()

# clicked vs dragged

# voir comment bloquer
# faire une distinction entre mouse pressed et clicked
# or do double click to go inside... maybe simpler
# if no drag --> mouse clicked in fact sinon mouse pressed

    # maybe should block dragging if inside a sel or just restore initial position upon failure todo stuff if inside another shape
    # only do stuff if no drag --> otherwise ignore --> put new sel on mouse release ???? for going deeper inside
    def mousePressEvent(self, event):
        self.dragged = False
        self.can_go_deeper = False
        if event.button() == QtCore.Qt.LeftButton:
            # print("drawing")
            self.drawing = True
            self.lastPoint = event.pos() / self.scale
            self.firstPoint = event.pos() / self.scale

            shapeFound = False
            if self.currently_drawn_shape is None:
                for shape in reversed(self.shapes):
                    if shape.contains(self.lastPoint) and not shape in self.selected_shape:
                        logger.debug('you clicked shape:' + str(shape))
                        if event.modifiers() == QtCore.Qt.ControlModifier:
                            if shape not in self.selected_shape:  # avoid doublons
                                self.selected_shape.append(shape)  # add shape to group
                                logger.debug('adding shape to group')
                                # shapeFound = True
                        else:
                            # if selected shape was already this one then browse inside further --> go deeper
                            print('testing')
                            if not self.group_contains(self.lastPoint.x(), self.lastPoint.y()):
                                print('going not deeper')
                                self.selected_shape = [shape]
                                logger.debug('only one element is selected')
                                # shapeFound = True
                            else:
                                self.can_go_deeper = True

                        self.__save_selection_position()

                        # update drawing of selection
                        self.update_size()
                        self.update()
                        return
                    else:
                        print('shape was already selected ...')
                        if self.selected_shape is not None and len(self.selected_shape)==1 and shape in self.selected_shape:
                            self.can_go_deeper = True


                if not shapeFound and event.modifiers() == QtCore.Qt.ControlModifier:
                    for shape in reversed(self.shapes):
                        if shape.contains(self.lastPoint):
                            if shape in self.selected_shape:  # avoid doublons
                                logger.debug('you clicked again shape:' + str(shape))
                                self.selected_shape.remove(shape)  # add shape to group
                                logger.debug('removing a shape from group')
                                shapeFound = True
                # no shape found --> reset sel
                if not shapeFound and not self.group_contains(self.lastPoint.x(), self.lastPoint.y()):
                    logger.debug('resetting sel')
                    self.selected_shape = []

            # check if a shape is selected and only move that
            if self.drawing_mode and not self.selected_shape and self.currently_drawn_shape is None:
                # do not reset shape if not done drawing...
                if self.shape_to_draw is not None:
                    # here I need to pass in the parameters for color and stroke, etc...
                    parameters = {}
                    # pass fill color to new object
                    if self.fill_color is not None:
                        parameters['fill_color'] = int(self.fill_color.name().replace('#', ''), 16)
                    # pass contour color to new object
                    if self.contour_color is not None:
                        parameters['color'] = int(self.contour_color.name().replace('#', ''), 16)
                    else:
                        # allow None color for contour if fill color is set
                        if self.fill_color is not None:
                            parameters['color'] = None
                    # pass line style parameters to new object
                    if self.line_style is not None:
                        parameters['line_style'] = self.line_style
                    if self.opacity is not None:
                        parameters['opacity'] = self.opacity
                    # not a good idea to set angle here...
                    # if self.theta is not None and self.theta != 0:
                    #     parameters['theta'] = self.theta

                    # if no color for contour and filling --> prevent drawing shape and raise a warning
                    if self.fill_color is None and self.contour_color is None:
                        self.currently_drawn_shape = None
                        # show a warning
                        print('no color set for line contour --> nothing to draw...')
                        return
                    # handle shapes that need a contour color to be drawn
                    elif self.contour_color is None and self.shape_to_draw in [Line2D, PolyLine2D,
                                                                               Freehand2D]:  # TODO check if freehand is filled or not --> maybe change that the future # , Freehand2D
                        self.currently_drawn_shape = None
                        # show a warning
                        print('no color set for line contour --> nothing to draw...')
                        return

                    self.currently_drawn_shape = self.shape_to_draw(**parameters)
                else:
                    self.currently_drawn_shape = None

            if self.drawing_mode and not self.selected_shape:
                if self.currently_drawn_shape is not None:
                    # print("here", self.currently_drawn_shape)
                    # print(self.currently_drawn_shape.listVertices())
                    # TODO fix that cause not really nice in fact set_P1 should only be used to set the origin of the stuff and nothing else here it may be set origin (first point)
                    if not isinstance(self.currently_drawn_shape, Polygon2D):
                        self.currently_drawn_shape.set_P1(QPointF(self.lastPoint.x(), self.lastPoint.y()))
                    else:
                        self.currently_drawn_shape.append(QPointF(self.lastPoint.x(), self.lastPoint.y()))

            self.update_size()
            self.update()

    def mouseMoveEvent(self, event):
        self.dragged = True
        if event.buttons() and QtCore.Qt.LeftButton:
            if self.selected_shape and self.currently_drawn_shape is None:
                logger.debug('moving' + str(self.selected_shape))
                for shape in self.selected_shape:
                    shape.translate(event.pos() / self.scale - self.lastPoint)
                self.update_size()
                self.update()

        if self.currently_drawn_shape is not None:
            self.currently_drawn_shape.add(self.firstPoint, self.lastPoint)
            self.update_size()
            self.update()

        self.lastPoint = event.pos() / self.scale

    def mouseReleaseEvent(self, event):
        # if just clicked then allow to go deeper inside otherwise skip
        # allow go deeper inside or not and do so only if no drag
        if not self.dragged:
            print('just clicked')
            # allow can go deeper
        else:
            print('just dragged')
            # block can go deeper
            self.can_go_deeper = False
        self.dragged=False

        if event.button() == QtCore.Qt.LeftButton:

            if self.can_go_deeper:
                print('go deeper inside shape 2')
                if self.selected_shape:
                    if isinstance(self.selected_shape[0], Row) or isinstance(self.selected_shape[0], Column):
                        sel = self.selected_shape[0].get_shape_at_coord(self.lastPoint.x(), self.lastPoint.y())
                        if sel is not None:
                            self.selected_shape = [sel]
                        else:
                            self.selected_shape = []
                        # sel changed --> need update it
                        self.update()

            if self.firstPoint != self.lastPoint:
                if self.selected_shape:
                    # check on what the stuff is dragged onto
                    # --> loop over objects below and allow all the stuff
                    # something is selected --> check if dragged onto some stuff
                    # print(self.selected_shape.boundingRect())

                    found_something = False
                    for shape in self.shapes:
                        if not shape in self.selected_shape and shape.contains(self.lastPoint):
                            print('dragged over', type(shape))
                            found_something = True
                            # if all same type --> will do different things
                            # check if unique or many
                            if len(self.selected_shape) == 1:
                                # unique selection
                                # if isinstance(self.selected_shape, Row) and is
                                # if type(self.selected_shape[0]) is type(shape): # pb not always good in fact --> rather ask the user what to do depending on type
                                if (isinstance(self.selected_shape[0], Row) and isinstance(shape, Row)) or (
                                        isinstance(self.selected_shape[0], Row) and isinstance(shape, Column)) or (
                                        isinstance(self.selected_shape[0], Column) and isinstance(shape, Row)) or (
                                        isinstance(self.selected_shape[0], Column) and isinstance(shape, Column)):
                                    print(len(self.shapes))
                                    # there are some merging bugs but it's there
                                    print('merging', type(shape), type(self.selected_shape[0]))
                                    self.shapes.remove(shape)
                                    print('size before merging', shape.boundingRect())

                                    width_before = shape.boundingRect().width()
                                    height_before = shape.boundingRect().height()

                                    # set to width or height of initial element...
                                    # if

                                    original_pos = shape.get_P1()#self.selected_shape[0].get_P1()
                                    # ça marche pas mal en fait comme ça --> prend la bonne position une fois mis

                                    shape //= self.selected_shape[0]

                                    # restore position

                                    # shape.setToWidth(width_in_px=width_before)
                                    # bug somewhere in setting width or height --> try find a way to fix it --> maybe best is to set to default page width

                                    # NB bounds are incorrect but size seems ok --> how is that possible --> check it

                                    shape.setToWidth(self.default_page_width)

                                    shape.set_P1(original_pos)

                                    # pas trop mal --> juste des pbs de taille qd not set properly initially --> find a fix for that
                                    if self.selected_shape[0] in self.shapes:
                                        self.shapes.remove(self.selected_shape[0])
                                    else:
                                        # TODO if part of an object then need remove it from that object
                                        pass

                                    self.shapes.append(shape)
                                    print('size after merging', shape.boundingRect())
                                    self.selected_shape.remove(self.selected_shape[0])

                                    # should I force draw it ???
                                    self.update_size()
                                    self.update()

                                    # print(len(self.shapes))
                                    return
                                else:
                                    # ça marche mais faudra améliorer ça
                                    # restore position upon drag failure
                                    if self.selected_shape is not None and self.selected_shape and self.selected_shape[0] not in self.shapes:
                                        self.__restore_selection_position()
                                        self.update()
                                        self.update_size()

                    if not found_something:
                        # TODO avoid code duplication with the above but anyways it's far from being done
                        if self.selected_shape is not None and self.selected_shape and self.selected_shape[0] not in self.shapes:
                            #en fait permettre le deplacement de certains objets
                            print('dragged over empty space')
                            # restore position upon drag failure
                            self.__restore_selection_position()
                            self.update()
                            self.update_size()
                            # most likely nothing to do --> just drag

            self.drawing = False
            if self.drawing_mode and self.currently_drawn_shape is not None:
                self.currently_drawn_shape.add(self.firstPoint, self.lastPoint)
                if isinstance(self.currently_drawn_shape, Freehand2D):
                    #     # this closes the freehand shape
                    self.currently_drawn_shape.add(self.lastPoint,
                                                   self.firstPoint)  # should I keep it closed or opened maybe do two buttons and ask for the option by a button
                #     # print('freehand add pt')
                #     self.shapes.append(self.currently_drawn_shape)
                #     self.currently_drawn_shape = None
                #     # self.selected_shape = [self.currently_drawn_shape]  # do select drawn shape
                # # should not erase the shape if it's a polyline or a polygon by the way
                # #     print(isinstance(self.currently_drawn_shape, PolyLine2D))
                # el
                if isinstance(self.currently_drawn_shape, Freehand2D) or (
                        not isinstance(self.currently_drawn_shape, PolyLine2D) and not isinstance(
                    self.currently_drawn_shape,
                    Polygon2D)):
                    self.shapes.append(self.currently_drawn_shape)
                    # self.selected_shape = self.currently_drawn_shape
                    self.selected_shape = [self.currently_drawn_shape]  # do select drawn shape
                    self.currently_drawn_shape = None

                self.update_size()
                self.update()

    def update_size(self):
        # seems to work but do this properly and handle scale ???
        bounds = updateBoudingRect(*self.shapes)
        # print('bds3', bounds)
        self.setMinimumSize((bounds.width() + bounds.x()) * self.scale,
                            (bounds.height() + bounds.y()) * self.scale)  # marche

    def mouseDoubleClickEvent(self, event):
        if isinstance(self.currently_drawn_shape, PolyLine2D) or isinstance(self.currently_drawn_shape, Polygon2D):
            self.shapes.append(self.currently_drawn_shape)
            self.selected_shape = [self.currently_drawn_shape]  # do select drawn shape
            self.currently_drawn_shape = None

    # this contains the right click event
    # adds context/right click menu but only in vectorial mode
    def contextMenuEvent(self, event):
        # if not self.vdp.active:
        #     return
        cmenu = QMenu(self)
        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()

    def cm_to_inch(self, size_in_cm):
        return size_in_cm / 2.54

    def scaling_factor_to_achieve_DPI(self, desired_dpi):
        return desired_dpi / 72

    # TODO maybe get bounding box size in px by measuring the real bounding box this is especially important for raster images so that everything is really saved...
    SVG_INKSCAPE = 96
    SVG_ILLUSTRATOR = 72

    def save(self, path, filetype=None, title=None, description=None, svg_dpi=SVG_INKSCAPE):
        if path is None or not isinstance(path, str):
            logger.error('please provide a valide path to save the image "' + str(path) + '"')
            return
        if filetype is None:
            if path.lower().endswith('.svg'):
                filetype = 'svg'
            else:
                filetype = os.path.splitext(path)[1]
        dpi = 72  # 300 # inkscape 96 ? check for illustrator --> check

        if filetype == 'svg':
            generator = QSvgGenerator()
            generator.setFileName(path)
            if svg_dpi == self.SVG_ILLUSTRATOR:
                generator.setSize(QSize(595, 842))
                generator.setViewBox(QRect(0, 0, 595, 842))
            else:
                generator.setSize(QSize(794, 1123))
                generator.setViewBox(QRect(0, 0, 794, 1123))

            if title is not None and isinstance(title, str):
                generator.setTitle(title)
            if description is not None and isinstance(description, str):
                generator.setDescription(description)
            generator.setResolution(
                svg_dpi)  # fixes issues in inkscape of pt size --> 72 pr illustrator and 96 pr inkscape but need change size

            painter = QPainter(generator)

            # print(generator.title(), generator.heightMM(), generator.height(), generator.widthMM(),
            #       generator.resolution(), generator.description(), generator.logicalDpiX())
        else:
            scaling_factor_dpi = 1
            scaling_factor_dpi = self.scaling_factor_to_achieve_DPI(300)

            # in fact take actual page size ??? multiplied by factor
            # just take real image size instead

            # image = QtGui.QImage(QSize(self.cm_to_inch(21) * dpi * scaling_factor_dpi, self.cm_to_inch(29.7) * dpi * scaling_factor_dpi), QtGui.QImage.Format_RGBA8888) # minor change to support alpha # QtGui.QImage.Format_RGB32)

            # NB THE FOLLOWING LINES CREATE A WEIRD ERROR WITH WEIRD PIXELS DRAWN some sort of lines NO CLUE WHY
            img_bounds = self.getBounds()
            image = QtGui.QImage(
                QSize(img_bounds.width() * scaling_factor_dpi, img_bounds.height() * scaling_factor_dpi),
                QtGui.QImage.Format_RGBA8888)  # minor change to support alpha # QtGui.QImage.Format_RGB32)
            # print('size at dpi',QSize(img_bounds.width() * scaling_factor_dpi, img_bounds.height()* scaling_factor_dpi))
            # QSize(self.cm_to_inch(0.02646 * img_bounds.width())
            # self.cm_to_inch(0.02646 * img_bounds.height())
            # need convert pixels to inches
            # is there a rounding error

            # force white bg for non jpg
            try:
                # print(filetype.lower())
                # the tif and png file formats support alpha
                if not filetype.lower() == '.png' and not filetype.lower() == '.tif' and not filetype.lower() == '.tiff':
                    image.fill(QColor.fromRgbF(1, 1, 1))
                else:
                    # image.fill(QColor.fromRgbF(1, 1, 1, alpha=1))
                    # image.fill(QColor.fromRgbF(1, 1, 1, alpha=1))
                    # TODO KEEP in fact image need BE FILLED WITH TRANSPARENT OTHERWISE GETS WEIRD DRAWING ERRORS
                    # TODO KEEP SEE https://stackoverflow.com/questions/13464627/qt-empty-transparent-qimage-has-noise
                    # image.fill(qRgba(0, 0, 0, 0))
                    image.fill(QColor.fromRgbF(0, 0, 0, 0))
            except:
                pass
            painter = QPainter(image)  # see what happens in case of rounding of pixels
            # painter.begin()
            painter.scale(scaling_factor_dpi, scaling_factor_dpi)

        painter.setRenderHint(QPainter.HighQualityAntialiasing)  # to improve rendering quality
        self.paint(painter)
        painter.end()
        if filetype != 'svg':
            image.save(path)

    def paint(self, painter):
        painter.save()
        for shape in self.shapes:
            shape.draw(painter)
        painter.restore()

    def getBounds(self):
        # loop over shape to get bounds to be able to draw an image
        bounds = QRectF()
        max_width = 0
        max_height = 0
        for shape in self.shapes:
            rect = shape.boundingRect()
            max_width = max(max_width, rect.x() + rect.width())
            max_height = max(max_height, rect.y() + rect.height())
        bounds.setWidth(max_width)
        bounds.setHeight(max_height)
        return bounds

    # def change_shape(self):
    #     import random
    #     drawing_methods = [Line2D, Rect2D, Square2D, Ellipse2D, Circle2D, Point2D, Freehand2D, PolyLine2D, Polygon2D]
    #     self.shape_to_draw = random.choice(drawing_methods)


class MainWindow(QMainWindow):
    def __init__(self, qt_viewer=None):
        QMainWindow.__init__(self, parent=None)

        # should it be part of the viewer or should it be here
        # zoom parameters

        # self.scale = 1.0

        self.CURRENT_MODE = True
        self.qt_viewer = qt_viewer

        self._qt_window = self
        self._qt_window.setAttribute(Qt.WA_DeleteOnClose)
        self._qt_window.setUnifiedTitleAndToolBarOnMac(True)
        self._qt_center = QWidget(self._qt_window)
        # self._qt_window.setCentralWidget(self._qt_center)

        # self._qt_center.setLayout(QVBoxLayout())
        # label =
        # self._qt_center.layout().addWidget(QLabel('MainWindow2'))

        self.scrollArea = QScrollArea()
        # self.scrollArea.resizeEvent = self.on_resize
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(qt_viewer)
        # qt_viewer.setWidgetResizable(True)
        self.setCentralWidget(self.scrollArea)

        #
        #         self.set
        # qsdqsqdsqdqs

        self.setMinimumSize(800, 800)

        # add menu
        if True:
            # Set up menu bar
            self.mainMenu = self.menuBar()
            # changeColour = self.mainMenu.addMenu("changeColour")
            # changeColourAction = QtWidgets.QAction("change", self)
            # changeColour.addAction(changeColourAction)
            # changeColourAction.triggered.connect(self.changeColour)

            save = self.mainMenu.addMenu("Save")
            saveAction = QtWidgets.QAction("Save as...", self)
            save.addAction(saveAction)
            saveAction.triggered.connect(self.save_as)

            self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++",
                                     enabled=True, triggered=self.qt_viewer.zoom_in)
            self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-",
                                      enabled=True, triggered=self.qt_viewer.zoom_out)
            self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+N",
                                         enabled=True, triggered=self.qt_viewer.reset_scale)
            # self.fitToWindowAct = QAction("&Fit to Window", self, enabled=True,
            #                               checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
            self.fitToWindowAct = QAction("&Fit to Window", self, enabled=True,
                                          shortcut="Ctrl+F", triggered=self.fitToWindow)

            self.showDrawWidgetAct = QAction("Draw widget", self, enabled=True,  # checkable=True,
                                             shortcut="", triggered=self.show_draw_widget)

            self.viewMenu = QMenu("&View", self)
            self.viewMenu.addAction(self.zoomInAct)
            self.viewMenu.addAction(self.zoomOutAct)
            self.viewMenu.addAction(self.normalSizeAct)
            self.viewMenu.addAction(self.fitToWindowAct)
            self.viewMenu.addSeparator()
            # allow drawing of panels to be shown
            # self.dockedWidgetShapes
            self.viewMenu.addAction(self.showDrawWidgetAct)

            # self.testMenu = QMenu("&MetaGenerator", self)
            # self.changeModeAct = QAction("Vectorial Mode", self, enabled=True,
            #                              checkable=True, triggered=self.changeMode)
            # self.testMenu.addAction(self.changeModeAct)

            self.menuBar().addMenu(self.viewMenu)
            # self.menuBar().addMenu(self.testMenu)

            self.setMenuBar(self.mainMenu)

            # Setup hotkeys
            deleteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
            deleteShortcut.activated.connect(self.down)

            # center window on screen --> can be done earlier
            # self.center()

            # self.lay.addWidget(self.mainMenu)

        # add status bar
        if True:
            statusBar = self.statusBar()  # sets an empty status bar --> then can add messages in it
            self.progress = QProgressBar(self)
            self.progress.setGeometry(200, 80, 250, 20)
            statusBar.addWidget(self.progress)

        # allow DND
        if True:
            # KEEP IMPORTANT absolutely required to allow DND on window
            self.setAcceptDrops(True)  # KEEP IMPORTANT

        # add a dock
        if True:
            # TODO change position to have it on the right and add all shapes and all options...
            self.dockedWidgetShapes = QDockWidget("", self)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                               self.dockedWidgetShapes)  # BottomDockWidgetArea # LeftDockWidgetArea # c'est ici qu'on ajoute le dockable element et sa position
            self.dockedWidgetInShapes = QWidget(self)
            self.dockedWidgetShapes.setWidget(self.dockedWidgetInShapes)
            self.dockedWidgetInShapes.setLayout(QGridLayout())

            # TODO nb I can have as many docked widget as I want --> really cool
            # self.dockedDimensionWidget2 = QDockWidget("Shapes2", self)
            # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
            #                    self.dockedDimensionWidget2)  # BottomDockWidgetArea # LeftDockWidgetArea # c'est ici qu'on ajoute le dockable element et sa position
            # self.dockedWidgetInDimension2 = QWidget(self)
            # self.dockedDimensionWidget2.setWidget(self.dockedWidgetInDimension2)
            # self.dockedWidgetInDimension2.setLayout(QVBoxLayout())

            # self.pushButton2 = QPushButton('Go')
            # self.pushButton2.clicked.connect(qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(self.pushButton2)

            # buttons for all shapes and their colors
            # self.pushButton2 = QPushButton('Go')
            # self.pushButton2.clicked.connect(qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(self.pushButton2)

            # list of icons availbale here
            # http://standards.freedesktop.org/icon-theme-spec/icon-theme-spec-latest.html
            # http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html

            # default icons pyqt5
            # https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html

            # Just a test button for trying stuff
            # test_button = QPushButton("test")
            # test_button.clicked.connect(partial(self.qt_viewer.set_line_style, Qt.DashLine))
            # self.dockedWidgetInShapes.layout().addWidget(test_button)

            # group them
            self.general_toolbox = QGroupBox('View',objectName='general_toolbox')
            self.general_toolbox.setEnabled(True)

            general_toolbox_layout = QGridLayout()
            # general_toolbox_layout.setAlignment(Qt.AlignTop)
            # general_toolbox_layout.setColumnStretch(0, 12.5)
            # general_toolbox_layout.setColumnStretch(1, 37.5)
            # general_toolbox_layout.setColumnStretch(2, 12.5)
            # general_toolbox_layout.setColumnStretch(3, 37.5)
            # general_toolbox_layout.setHorizontalSpacing(3)
            # general_toolbox_layout.setVerticalSpacing(3)

            # ces icones sont vraiment laides et incomprehensibles --> mieux vaut prendre les miennes
            zoomplus = QPushButton()
            zoomplus.setToolTip("Zoom +")
            zoomplusicon = QIcon.fromTheme("crap", QIcon("../icons/Icons/zoom in.png"))  # "zoom-in"
            zoomplus.setIcon(zoomplusicon)
            zoomplus.clicked.connect(self.qt_viewer.zoom_in)
            general_toolbox_layout.addWidget(zoomplus, 0, 0)
            # self.dockedWidgetInShapes.layout().addWidget(zoomplus)

            # "/Icons/zoom out.png"
            zoomminus = QPushButton()
            zoomminus.setToolTip("Zoom -")
            zoomminusicon = QIcon("../icons/Icons/zoom out.png")
            zoomminus.setIcon(zoomminusicon)
            zoomminus.clicked.connect(self.qt_viewer.zoom_out)
            general_toolbox_layout.addWidget(zoomminus, 0, 1)
            # self.dockedWidgetInShapes.layout().addWidget(zoomminus)
            # "/Icons/1in1.png"
            one2one = QPushButton()
            one2one.setToolTip("1:1 original/default size")
            one2oneicon = QIcon("../icons/Icons/1in1.png")
            one2one.setIcon(one2oneicon)
            one2one.clicked.connect(self.qt_viewer.reset_scale)
            # self.dockedWidgetInShapes.layout().addWidget(one2one)
            general_toolbox_layout.addWidget(one2one, 0, 2)
            # "/Icons/fit_2_screen.gif"
            auto = QPushButton()
            auto.setToolTip("Fit To window (alternate between fit with and fit height)")
            autoicon = QIcon("../icons/Icons/fit_2_screen.gif")
            auto.setIcon(autoicon)
            auto.clicked.connect(self.fitToWindow)
            # self.dockedWidgetInShapes.layout().addWidget(auto)
            general_toolbox_layout.addWidget(auto, 1, 0)
            # "/Icons/send_to_back.png"
            send2back = QPushButton()
            send2back.setIcon(QIcon("../icons/Icons/send_to_back.png"))
            send2back.setToolTip("Send to back")
            send2back.clicked.connect(self.qt_viewer.send_to_back)
            # self.dockedWidgetInShapes.layout().addWidget(send2back)
            general_toolbox_layout.addWidget(send2back, 1, 1)
            # "/Icons/bring_to_front.png"
            bring2front = QPushButton()
            bring2front.setIcon(QIcon("../icons/Icons/bring_to_front.png"))
            bring2front.setToolTip("Bring to front")
            bring2front.clicked.connect(self.qt_viewer.bring_to_front)
            # self.dockedWidgetInShapes.layout().addWidget(bring2front)
            general_toolbox_layout.addWidget(bring2front, 1, 2)

            self.general_toolbox.setLayout(general_toolbox_layout)
            self.dockedWidgetInShapes.layout().addWidget(self.general_toolbox)

            self.shapes_toolbox = QGroupBox('Shapes',objectName='shapes_toolbox')
            self.shapes_toolbox.setEnabled(True)

            shapes_toolbox_layout = QGridLayout()

            # "/Icons/rectangle.png"
            rectangle = QPushButton()
            rectangle.setIcon(QIcon("../icons/Icons/rectangle.png"))
            rectangle.setToolTip("Rectangle")
            rectangle.clicked.connect(
                self.qt_viewer.change_shape)  # this is how one can pass the button to the function to
            # self.dockedWidgetInShapes.layout().addWidget(rectangle)
            shapes_toolbox_layout.addWidget(rectangle, 0, 0)
            # "/Icons/circle.png"
            circle = QPushButton()
            circle.setIcon(QIcon("../icons/Icons/circle.png"))
            circle.setToolTip("Circle")
            circle.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(circle)
            shapes_toolbox_layout.addWidget(circle, 0, 1)

            # "/Icons/arrow.png"
            arrow = QPushButton()
            arrow.setEnabled(False)
            arrow.setIcon(QIcon("../icons/Icons/arrow.png"))
            arrow.setToolTip("Arrow")
            arrow.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(arrow)
            shapes_toolbox_layout.addWidget(arrow, 0, 2)
            # "/Icons/accolade.png"
            accolade = QPushButton()
            accolade.setEnabled(False)
            accolade.setIcon(QIcon("../icons/Icons/accolade.png"))
            accolade.setToolTip("Accolade")
            accolade.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(accolade)
            shapes_toolbox_layout.addWidget(accolade, 1, 0)
            # "add text"
            text = QPushButton("txt")
            text.setEnabled(False)
            # zuppa.setIcon(QIcon("../icons/Icons/bring_to_front.png"))
            text.setToolTip("Floating txt")
            text.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(text)
            shapes_toolbox_layout.addWidget(text, 1, 1)

            # new line

            # "/Icons/line.png"
            line = QPushButton()
            line.setIcon(QIcon("../icons/Icons/line.png"))
            line.setToolTip("Line")
            line.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(line)
            shapes_toolbox_layout.addWidget(line, 1, 2)
            # "/Icons/freehand.png"
            freehand = QPushButton()
            freehand.setIcon(QIcon("../icons/Icons/freehand.png"))
            freehand.setToolTip("hand drawing")
            freehand.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(freehand)
            shapes_toolbox_layout.addWidget(freehand, 2, 0)
            # "/Icons/square.png"
            square = QPushButton()
            square.setIcon(QIcon("../icons/Icons/square.png"))
            square.setToolTip("square")
            square.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(square)
            shapes_toolbox_layout.addWidget(square, 2, 1)
            # "/Icons/line_brisee.png"
            polyline = QPushButton()
            polyline.setIcon(QIcon("../icons/Icons/line_brisee.png"))
            polyline.setToolTip("polyline")
            polyline.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(polyline)
            shapes_toolbox_layout.addWidget(polyline, 2, 2)
            # "/Icons/ellipse.png"
            Ellipse = QPushButton()
            Ellipse.setIcon(QIcon("../icons/Icons/ellipse.png"))
            Ellipse.setToolTip("Ellipse")
            Ellipse.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(Ellipse)
            shapes_toolbox_layout.addWidget(Ellipse, 3, 0)
            # "/Icons/polygon.png"
            polygon = QPushButton()
            polygon.setIcon(QIcon("../icons/Icons/polygon.png"))
            polygon.setToolTip("Polygon")
            polygon.clicked.connect(self.qt_viewer.change_shape)
            # self.dockedWidgetInShapes.layout().addWidget(polygon)
            shapes_toolbox_layout.addWidget(polygon, 3, 1)
            # "/Icons/Trash Empty.png"
            delete = QPushButton()
            delete.setIcon(QIcon("../icons/Icons/Trash Empty.png"))
            delete.setToolTip("Delete ROI")
            delete.clicked.connect(self.qt_viewer.remove_selection)
            # self.dockedWidgetInShapes.layout().addWidget(delete)
            shapes_toolbox_layout.addWidget(delete, 3, 2)

            Edit = QPushButton('Edit/Finalise selected ROI')
            Edit.setEnabled(False)
            Edit.setToolTip("Edit/Finalise selected ROI")
            # self.dockedWidgetInShapes.layout().addWidget(Edit)
            shapes_toolbox_layout.addWidget(Edit, 4, 0, 1, 3)
            jLabel2 = QLabel('Contour:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel2)
            shapes_toolbox_layout.addWidget(jLabel2, 6, 0)
            changeWidthHeight = QPushButton('width/height')
            changeWidthHeight.setEnabled(False)
            # self.dockedWidgetInShapes.layout().addWidget(changeWidthHeight)
            shapes_toolbox_layout.addWidget(changeWidthHeight, 5, 0, 1, 3)
            contourColor = QPushButton()  # new Commons.PaintedButton()
            # if self.qt_viewer.contour_color is not None:
            #     contourColor.setStyleSheet("background-color: "+self.qt_viewer.contour_color.name())
            #     contourColor.setText(self.qt_viewer.contour_color.name())
            # else:
            #     contourColor.setText(str(self.qt_viewer.contour_color))
            self.set_button_color(contourColor, self.qt_viewer.contour_color)
            contourColor.clicked.connect(partial(self.qt_viewer.color_picker, self.qt_viewer.set_contour_color))
            # self.dockedWidgetInShapes.layout().addWidget(contourColor)
            shapes_toolbox_layout.addWidget(contourColor, 6, 1, 1, 2)
            jLabel12 = QLabel('Fill:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel12)
            shapes_toolbox_layout.addWidget(jLabel12, 7, 0)
            fillColor = QPushButton()  # new Commons.PaintedButton()

            # if self.qt_viewer.fill_color is not None:
            #     fillColor.setStyleSheet("background-color: "+self.qt_viewer.fill_color.name())
            #     fillColor.setText(self.qt_viewer.fill_color.name())
            # else:
            #     fillColor.setText(str(self.qt_viewer.fill_color))
            self.set_button_color(fillColor, self.qt_viewer.fill_color)
            # fillColor.setStyleSheet("background-color: red")
            fillColor.clicked.connect(partial(self.qt_viewer.color_picker, self.qt_viewer.set_fill_color))
            # self.dockedWidgetInShapes.layout().addWidget(fillColor)
            shapes_toolbox_layout.addWidget(fillColor, 7, 1, 1, 2)
            # jLabel14 = QLabel('color')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel14)
            # shapes_toolbox_layout.addWidget(jLabel14,3,4)
            # jLabel15 = QLabel('Contour:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel15)
            # shapes_toolbox_layout.addWidget(jLabel15,3,5)
            # jLabel16 = QLabel('Fill:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel16)
            # shapes_toolbox_layout.addWidget(jLabel16,3,4)
            jLabel17 = QLabel('Opacity')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel17)
            shapes_toolbox_layout.addWidget(jLabel17, 8, 0)
            self.opacity_spinner = QDoubleSpinBox()
            self.opacity_spinner.setSingleStep(0.05)
            self.opacity_spinner.setRange(0, 1)
            self.opacity_spinner.setValue(1)
            self.opacity_spinner.valueChanged.connect(self.opacity_changed)

            # self.dockedWidgetInShapes.layout().addWidget(drawOpacitySpinner)
            shapes_toolbox_layout.addWidget(self.opacity_spinner, 8, 1, 1, 2)
            # fillOpacitySpinner = QSpinBox()
            # # self.dockedWidgetInShapes.layout().addWidget(fillOpacitySpinner)
            # shapes_toolbox_layout.addWidget(fillOpacitySpinner)
            # "COnvert a rectangular ROI to an image inset"

            jLabel9 = QLabel('Rotation :')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel9)
            shapes_toolbox_layout.addWidget(jLabel9, 9, 0)
            self.rotation_spinner = QSpinBox(objectName='rotation_spinner')
            self.rotation_spinner.setSingleStep(1)
            self.rotation_spinner.setRange(0, 360)
            self.rotation_spinner.setValue(0)
            self.rotation_spinner.valueChanged.connect(self.rotation_changed)
            # self.dockedWidgetInShapes.layout().addWidget(jSpinner7)
            shapes_toolbox_layout.addWidget(self.rotation_spinner, 9, 1, 1, 2)
            # "COnvert a rectangular ROI to an image inset"
            toInset = QPushButton('ROI --> Inset')
            toInset.setEnabled(False)
            # self.dockedWidgetInShapes.layout().addWidget(toInset)
            shapes_toolbox_layout.addWidget(toInset, 10, 0)
            toCrop = QPushButton('ROI(s) --> Crop(s)')
            toCrop.setEnabled(False)
            # self.dockedWidgetInShapes.layout().addWidget(toCrop)
            shapes_toolbox_layout.addWidget(toCrop, 10, 1, 1, 2)

            self.shapes_toolbox.setLayout(shapes_toolbox_layout)
            self.dockedWidgetInShapes.layout().addWidget(self.shapes_toolbox)

            # line style toolbox
            self.line_toolbox = QGroupBox('Line style',objectName='line_toolbox')
            self.line_toolbox.setEnabled(True)

            line_toolbox_layout = QGridLayout()
            jLabel1 = QLabel('Size:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel1)
            line_toolbox_layout.addWidget(jLabel1, 0, 0)
            jSpinner1 = QSpinBox(objectName='jSpinner1')
            line_toolbox_layout.addWidget(jSpinner1, 0, 1)

            jLabel5 = QLabel('Type:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel5)
            line_toolbox_layout.addWidget(jLabel5, 1, 0)
            # "Plain", "Dashed", "Dotted", "DashDot"
            jComboBox1 = QComboBox(objectName='jComboBox1')
            jComboBox1.addItems(["SolidLine", "DashLine", "DashDotLine", "DotLine", "DashDotDotLine", "CustomDashLine"])
            jComboBox1.currentTextChanged.connect(self.line_style_changed)
            #
            #
            # make it there

            # self.dockedWidgetInShapes.layout().addWidget(jComboBox1)
            line_toolbox_layout.addWidget(jComboBox1, 1, 1)
            jLabel6 = QLabel('Custom dash pattern:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel6)
            line_toolbox_layout.addWidget(jLabel6, 2, 0)
            self.lineEdit = QtWidgets.QLineEdit()
            self.lineEdit.setText('1, 4, 5, 4')
            self.lineEdit.setEnabled(False)
            self.lineEdit.textChanged.connect(self.line_style_changed)
            line_toolbox_layout.addWidget(self.lineEdit, 2, 1)
            # add a text change to adapt the pattern after some delay maybe

            # jLabel7 = QLabel('Gap:')
            # # self.dockedWidgetInShapes.layout().addWidget(jLabel7)
            # line_toolbox_layout.addWidget(jLabel7)
            # jLabel8 = QLabel('Dot:')
            # # self.dockedWidgetInShapes.layout().addWidget(jLabel8)
            # line_toolbox_layout.addWidget(jLabel8)
            # jSpinner4 = QSpinBox()
            # # self.dockedWidgetInShapes.layout().addWidget(jSpinner4)
            # line_toolbox_layout.addWidget(jSpinner4)
            # jSpinner5 = QSpinBox()
            # line_toolbox_layout.addWidget(jSpinner5)
            # # self.dockedWidgetInShapes.layout().addWidget(jSpinner5)
            # jSpinner6 = QSpinBox()
            # # self.dockedWidgetInShapes.layout().addWidget(jSpinner6)
            # line_toolbox_layout.addWidget(jSpinner6)

            self.line_toolbox.setLayout(line_toolbox_layout)
            self.dockedWidgetInShapes.layout().addWidget(self.line_toolbox)

            # new group
            self.arrow_toolbox = QGroupBox('Arrow style',objectName='arrow_toolbox')
            self.arrow_toolbox.setEnabled(False)

            arrow_toolbox_layout = QGridLayout()

            jLabel3 = QLabel('Width:')
            arrow_toolbox_layout.addWidget(jLabel3, 0, 0)
            # self.dockedWidgetInShapes.layout().addWidget(jLabel3)
            jSpinner2 = QSpinBox(objectName='jSpinner2')
            arrow_toolbox_layout.addWidget(jSpinner2, 0, 1)
            # self.dockedWidgetInShapes.layout().addWidget(jSpinner2)
            jLabel10 = QLabel('Height:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel10)
            arrow_toolbox_layout.addWidget(jLabel10, 0, 2)
            jSpinner8 = QSpinBox(objectName='jSpinner8')
            # self.dockedWidgetInShapes.layout().addWidget(jSpinner8)
            arrow_toolbox_layout.addWidget(jSpinner8, 0, 3)
            jLabel11 = QLabel('Type:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel11)
            arrow_toolbox_layout.addWidget(jLabel11, 1, 0)
            jComboBox2 = QComboBox(objectName='jComboBox2')
            # self.dockedWidgetInShapes.layout().addWidget(jComboBox2)
            arrow_toolbox_layout.addWidget(jComboBox2, 1, 1)
            jLabel13 = QLabel('Filling:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel13)
            arrow_toolbox_layout.addWidget(jLabel13, 1, 2)
            # "Filled", "Outline", "Fancy"
            jComboBox4 = QComboBox(objectName='jComboBox4')
            # self.dockedWidgetInShapes.layout().addWidget(jComboBox4)
            arrow_toolbox_layout.addWidget(jComboBox4, 1, 3)

            self.arrow_toolbox.setLayout(arrow_toolbox_layout)
            self.dockedWidgetInShapes.layout().addWidget(self.arrow_toolbox)

            self.bracket_toolbox = QGroupBox('Bracket',objectName='bracket_toolbox')
            self.bracket_toolbox.setEnabled(False)

            bracket_toolbox_layout = QGridLayout()

            jLabel4 = QLabel('Bracket Width:')
            # self.dockedWidgetInShapes.layout().addWidget(jLabel4)
            bracket_toolbox_layout.addWidget(jLabel4, 0, 0)
            jSpinner3 = QSpinBox(objectName='jSpinner3')
            # self.dockedWidgetInShapes.layout().addWidget(jSpinner3)
            bracket_toolbox_layout.addWidget(jSpinner3, 0, 1)

            self.bracket_toolbox.setLayout(bracket_toolbox_layout)
            self.dockedWidgetInShapes.layout().addWidget(self.bracket_toolbox)

            # new toolbox
            self.misc_toolbox = QGroupBox('Misc',objectName='misc_toolbox')
            self.misc_toolbox.setEnabled(True)

            misc_toolbox_layout = QGridLayout()

            # other tools
            # jList1 = new javax.swing.JList()
            # self.dockedWidgetInShapes.layout().addWidget(jList1)
            erode = QPushButton('Erode')
            erode.setEnabled(False)
            erode.clicked.connect(self.qt_viewer.erode)
            # self.dockedWidgetInShapes.layout().addWidget(erode)
            misc_toolbox_layout.addWidget(erode, 0, 0)
            dilate = QPushButton('Dilate')
            dilate.setEnabled(False)
            dilate.clicked.connect(self.qt_viewer.dilate)
            # self.dockedWidgetInShapes.layout().addWidget(dilate)
            misc_toolbox_layout.addWidget(dilate, 0, 1)
            reCenter = QPushButton('Move to ori (0,0)')
            reCenter.clicked.connect(self.qt_viewer.move_to_origin)
            misc_toolbox_layout.addWidget(reCenter, 0, 2)

            self.misc_toolbox.setLayout(misc_toolbox_layout)
            self.dockedWidgetInShapes.layout().addWidget(self.misc_toolbox)

            # self.dockedWidgetInShapes.layout().addWidget(reCenter)
            # delete2 = QPushButton('del')
            # # why not working
            # delete2.clicked.connect(self.qt_viewer.remove_selection)
            # self.dockedWidgetInShapes.layout().addWidget(delete2)

            # self.dockedWidget.hide()
            # self.dockedDimensionWidget.hide()

        # self.paint.scrollArea = self.scrollArea

        # self.paint = QWidget()
        #
        # self.image = None
        # self.imageDraw = None
        # self.cursor = None
        #
        # self.scrollArea.setWidget(self.paint)

        # self.scrollArea.setWidget(self.widget)

        # self._qt_center.layout().addWidget(self.scrollArea)
        # self._qt_center.layout().addWidget(qt_viewer)
        # self.button = QPushButton("Click me !", self)
        # self.button.clicked.connect(self.click)
        # self.wd = window

    def rotation_changed(self):
        self.qt_viewer.set_rotation(self.rotation_spinner.value())

    def opacity_changed(self):
        self.qt_viewer.set_opacity(self.opacity_spinner.value())

    def line_style_changed(self):
        if isinstance(self.sender(), QComboBox):
            sel = self.sender().currentText()
            idx = self.sender().currentIndex()
            # print(sel)
            self.lineEdit.setEnabled('ustom' in sel.lower())
        else:
            sel = 'custom'
        if not 'ustom' in sel.lower():
            self.qt_viewer.set_line_style(VectorialDrawPane2.line_styles[idx])
            # print(VectorialDrawPane2.line_styles[idx])
        else:
            try:
                txt = self.lineEdit.text()
                if ',' in txt or ";" in txt:
                    txt = txt.replace(";", ",")
                    my_list = txt.split(",")
                    # print('there')
                else:
                    my_list = txt.split()
                    # print('here', my_list)
                my_list = [int(e) for e in my_list]

                # print(my_list)
                self.qt_viewer.set_line_style(my_list)
            except:
                traceback.print_exc()
                logger.warning('invalid custom dash pattern')

    # def on_resize(self, event):
    #     self.scrollArea.resize(self.qt_viewer.size())
    def save_as(self):
        # ask where to save and the format
        path_to_svg= '/D/Sample_images/sample_images_svg/'
        if True:
            self.qt_viewer.save(path_to_svg + 'out2.svg')
            # TODO make it also paint to a raster just to see what it gives

        # TO SAVE AS RASTER --> quite good
        if True:
            # Tif, jpg and png are supported --> this is more than enouch for now
            # self.paintToFile(path_to_svg + 'out2.png')
            # self.paintToFile(path_to_svg + 'out2.tif')
            # widget.save(path_to_svg + 'out2.jpg')
            # widget.save(path_to_svg + 'out2.png')
            self.qt_viewer.save(path_to_svg + 'out2.jpg')
            self.qt_viewer.save(path_to_svg + 'out2.png')
            self.qt_viewer.save(path_to_svg + 'out2.tif')  # now has noise
            # first save is ok then gets weird lines

    def set_button_color(self, btn, color):
        if color is not None:
            btn.setStyleSheet("background-color: " + color.name())
            btn.setText(color.name())
        else:
            btn.setStyleSheet('')  # reset style sheet
            btn.setText(str(color))

    # not really a smart way --> find a better way to do that
    # def zoomIn(self):
    #     self.qt_viewer.zoom_in()
    #
    # def zoomOut(self):
    #     self.qt_viewer.zoom_out()
    #
    # def defaultSize(self):
    #     self.qt_viewer.reset_scale()
    def show_draw_widget(self):
        # bool
        # oldState = self.showDrawWidgetAct.blockSignals(True)

        # self.showDrawWidgetAct.setEnabled(False)
        # if not self.showDrawWidgetAct.isChecked():
        self.dockedWidgetShapes.show()
        # self.showDrawWidgetAct.setChecked(True)

    # else:
    #     self.dockedWidgetShapes.hide()
    #     self.showDrawWidgetAct.setChecked(False)

    # self.showDrawWidgetAct.blockSignals(False)
    # self.showDrawWidgetAct.setEnabled(True)

    # null car respecte pas le w/h ratio --> à fixer --> alterner between w and h
    def fitToWindow(self):
        # print('setting CURRENT_MODE ', self.CURRENT_MODE)
        # self.CURRENT_MODE = self.FIT_TO_HEIGHT
        # print('CURRENT_MODE', self.CURRENT_MODE)
        #
        # else:
        # print('setting CURRENT_MODE HEIGHT', self.CURRENT_MODE)
        # self.CURRENT_MODE = self.FIT_TO_WIDTH
        # print('CURRENT_MODE', self.CURRENT_MODE)

        # print(self.scrollArea.size())
        self.qt_viewer.scale_to_window(self.scrollArea.size(), mode=0 if self.CURRENT_MODE else 1)

        if self.CURRENT_MODE:
            self.CURRENT_MODE = False
        else:
            self.CURRENT_MODE = True

        # fitToWindow = self.fitToWindowAct.isChecked()
        # self.scrollArea.setWidgetResizable(fitToWindow)
        # if not fitToWindow:
        #     self.defaultSize()

    # will not work
    def scaleImage(self, factor):
        self.scale += factor
        # if self.qt_viewer.image is not None:
        self.qt_viewer.resize(self.scale * self.qt_viewer.size())
        # else:
        # no image set size to 0, 0 --> scroll pane will auto adjust
        # self.paint.resize(QSize(0, 0))
        # self.scale -= factor  # reset zoom

        self.qt_viewer.scale = self.scale
        # self.paint.vdp.scale = self.scale

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

            # create a row out of the images ???
            # then add them

            imgs = []
            # add all dropped items to the list
            for url in urls:
                # url = '/home/aigouy/mon_prog/Icons/src/main/resources/Icons/1in1.png'
                # icon = QIcon(url)
                # pixmap = icon.pixmap(24, 24)
                # icon = QIcon(pixmap)
                import os
                # item = QListWidgetItem(os.path.basename(url), self.list)
                # item.setIcon(icon)
                # item.setText(os.path.basename(url))
                # item.setToolTip(url)

                # print("data", item.toolTip()) # can store in tooltip

                # so by status tip things can be grabbed

                # item.setData(10, url)
                # print("data", item.data(10), os.path.basename(url))  # so cool can really  store any data in it I love it and so simple
                # self.list.addItem(item)
                # ask if row or col
                # then also check images are valid

                # print('DND of files ', os.path.basename(url), url)
                # allow stack or pack and allow align and have a default mode that stacks automatically things that people can switch between

                img = Image2D(url)
                if img.img is not None:
                    imgs.append(img)

                # check all the possible drag and see which operations can be made
                # --> on release --> check dragged stuff

                # add it as a row and take action depending on stuff
                # add them as a row for example
            # self.list.addItems(urls)
            if imgs:
                row = Row(*imgs)
                row.setToWidth(self.default_page_width)  # TODO rather fit to page size
                self.qt_viewer.shapes.append(row)
                self.qt_viewer.update()

            # check according to DND
            # self.scaleImage(0)  # no rescale just take original size
            # self.update()
            # CODE ABOVE IS MY OWN CODE AND NEED BE MODIFIED OR BE REMOVED
        else:
            event.ignore()

    def down(self):
        # make it delete the current selected shape and remove it from the list
        self.qt_viewer.remove_selection()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vdp = VectorialDrawPane2(active=True)

    main = MainWindow(qt_viewer=vdp)
    main.show()

    # pos = QtGui.QCursor.pos()
    # widget = QApplication.widgetAt(pos)
    # print(widget)
    # vdp.show()



    sys.exit(app.exec_())
