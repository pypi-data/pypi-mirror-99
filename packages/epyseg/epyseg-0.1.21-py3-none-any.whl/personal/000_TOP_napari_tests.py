# TODO remove ITK from TA code --> really ok in fact
# finalize the figure creation tool
# can I elaborate a language to create figures from human language ??? --> would be fun


# TOP BEST TODO NB attenuated_mip works well but MIP too with proper scaling although it's a bit slow..., need change depth scaling --> use scale
#


# can you elaborate?
# TODO MEGA BEST TOP The main napari viewer is an instance of QMainWindow 1 and when you create a viewer instance with viewer = napari.Viewer(), the QtMainWindow object is available at viewer.window._qt_window. If you’re looking to add the whole napari window to some QLayout in some external program, that’s the object you need to add.

# TODO --> check this for movie https://github.com/guiwitz/naparimovie/blob/fb7b9853c28f283bfee6c93c5e0b3b729a60d686/naparimovie/naparimovie.py#L105
#
# import os
# import numpy as np
# import napari
#
# volume = np.random.random((5, 768, 1024))
#
#
# with napari.gui_qt():
#     viewer = napari.Viewer(ndisplay=3)
#     layer_norm = viewer.add_image(
#         volume,
#         visible=False,
#     )
#     # layer_norm.interpolation = 'linear'
from vispy.scene import PanZoomCamera, ArcballCamera
from vispy.util.quaternion import Quaternion
from epyseg.img import Img
from skimage import data
import napari
import numpy as np
import random
# import imgfileutils as imf


# maybe that is what I should


# with tifffile.Timer('Loading pyramid:'):
#     with tifffile.TiffFile('HandEcompressed_Scan1.qptiff') as tif:
#         pyramid = list(reversed(sorted(tif.series, key=lambda p:p.size)))
#         size = pyramid[0].size
#         pyramid = [p for p in pyramid if size % p.size == 0]
#         pyramid = [p.asarray() for p in pyramid]
#
# print('pyramid levels:', [p.shape for p in pyramid])
#
# with napari.gui_qt():
#     napari.view_image(pyramid, is_pyramid=True)

# ça marche bien
with napari.gui_qt():

    # napari.Viewer.sewindow._qt_window
    # viewer = napari.Viewer()# 2D viewer
    viewer = napari.Viewer(ndisplay = 3)# 3D viewer
    viewer.dims.ndisplay = 3 # alternative way to go 3D
    # viewer.theme = 'light' # to change theme (doesn't work for all --> a bug somewhere)
    # image = Img("/home/aigouy/Bureau/Image1.tif")
    image = Img("/home/aigouy/Bureau/test bon.czi")
    # image = Img("/home/aigouy/Bureau/mini_volume_t.tif") # tt marche y compris la 3D avec le temps --> le truc est fonctionnel et un peu lent mais franchement ça va... --> supprimer itk et remplacer par ça de partout!!!
    # ça marche --> donc très facile à integrer à mon code


    print(image.shape)

    #   name=None,        metadata=None,        scale=None,        translate=None,        opacity=1,        blending=None,
    viewer.add_image(image) # scale=(10, 1, 1)# this is how one can change scale # ndisplay =3 adds a 3D image

    # alternative way of changing scale TODO TOP BEST KEEP IN MIND
    viewer.layers[0].scale = [3, 1, 1]
    # viewer.ndisplay = 3 # sets as 3D viewer/ does that work ???

    center = (20, 10, 15)
    scale = 100
    angles = (90, 0, 0)
    # here is how one can change camera angle programmatically
    # viewer.window.qt_viewer.view.camera.update( angles=angles) #center=center, scale=scale,
    # viewer.camera.update( angles=angles)

    vispy_view = viewer.window.qt_viewer.view

    # Update camera model and check vispy camera changes in 3D
    center = (20, 10, 15)
    # scale = 10
    angles = (-20, 10, -45)
    # viewer.camera.update(center=center, scale=scale, angles=angles)
    # assert viewer.camera.ndisplay == 3
    # assert viewer.camera.center == center
    # assert viewer.camera.scale == scale
    # assert viewer.camera.angles == angles
    # assert isinstance(vispy_view.camera, ArcballCamera)
    # assert vispy_view.camera.center == center[::-1]
    # assert vispy_view.camera.scale_factor == 100


    # TODO keep below ça marche je peux changer zoom, pan et autres trucs programmatically meme si c'est qd mm un peu compliqué...
    # en fait si dessous c'est pr une camera 3D et choses differentes pr 2D mais facile
    # vispy_view.camera.center = vispy_view.camera.center #(12, -2, 8)
    # vispy_view.camera.scale_factor = 2
    # angles = (0, 0,90) # ça marche mais faut updater la view tou

    print(viewer.window.qt_viewer.view.camera.get_state())
    print('angles', vispy_view.camera._quaternion.get_axis_angle()) # not sure I get those angle values need read about quaternions
    from scipy.spatial.transform import Rotation as R

    r = R.from_quat(list(vispy_view.camera._quaternion.get_axis_angle()))
    # is it possible that my dim order is incorrect ???
    print('angles for humans',r.as_euler('zyx', degrees=True)) # not sure that works

    angles = (0, 0,180) # ça marche mais faut updater la view tou # --> parfait c'est ça que je veux, de la rotation a 180 !!!! --> en fait ça fait une section transversale --> comprend pas mais ok...
    q = Quaternion.create_from_euler_angles(*angles, degrees=True)
    # change 3D camera angle
    vispy_view.camera._quaternion = q
    state = viewer.window.qt_viewer.view.camera.get_state()
    # we must update camera otherwise nothing is shown...
    viewer.window.qt_viewer.view.camera.set_state(state) # ça marche enfin --> c'est comme ça qu'on update la camera


    # we must update camera otherwise nothing is shown...
    # viewer.window.qt_viewer._update_camera() # marche pas


    # viewer.window.qt_viewer.view.camera.set_state(state)

    # assert viewer.camera.center == (8, -2, 12)
    # assert viewer.camera.scale == 20


    # """Test camera."""
    # viewer = ViewerModel()
    # np.random.seed(0)
    # data = np.random.random((10, 15, 20))
    # viewer.add_image(data)

    # viewer.dims.ndisplay = 2 # back to 2D # programmatically --> really getting there

    # print(viewer.window.qt_viewer.view.camera.get_state()) # seems to indeed access the camera --> from now on will be easy
    # viewer.window.qt_viewer.view.camera.center = (512.0, 1024.0, 350.0) # to change center of camera
    # viewer.window.qt_viewer.view.camera.angles = (90, 90, 90) # to change camera angle programmatically
    # viewer.window.qt_viewer.view.camera
    # print(viewer.window.qt_viewer.view.camera.get_state())  # seems to indeed access the camera --> from now on will be easy

    # state = viewer.window.qt_viewer.view.camera.get_state()

    # viewer.window.qt_viewer.view.camera.set_state(state)

    # assert len(viewer.layers) == 1

    # assert np.all(viewer.layers[0].data == data)
    # assert viewer.dims.ndim == 3
    # assert viewer.dims.ndisplay == 2
    # assert viewer.camera.ndisplay == 2
    # assert viewer.camera.center == (7.5, 10)
    # assert viewer.camera.angles == (0, 0, 90)
    # viewer.dims.ndisplay = 3
    # assert viewer.dims.ndisplay == 3
    # assert viewer.camera.ndisplay == 3
    # assert viewer.camera.center == (5, 7.5, 10)
    # assert viewer.camera.angles == (0, 0, 90)
    # viewer.dims.ndisplay = 2
    # assert viewer.dims.ndisplay == 2
    # assert viewer.camera.ndisplay == 2
    # assert viewer.camera.center == (7.5, 10)
    # assert viewer.camera.angles == (0, 0, 90)
    # center = (20, 45)
    # scale = 300
    # angles = (-20, 10, -45)
    # viewer.camera.update(center=center, scale=scale, angles=angles)
    # assert viewer.camera.ndisplay == 2
    # assert viewer.camera.center == center
    # assert viewer.camera.scale == scale
    # assert viewer.camera.angles == angles



    points = np.array([[100, 100], [200, 200], [300, 100]])
    viewer.add_points(points, size=30)

    blobs = np.stack(
        [
            data.binary_blobs(
                length=512, blob_size_fraction=0.05, n_dim=2, volume_fraction=f
            )
            for f in np.linspace(0.05, 0.5, 10)
        ],
        axis=0,
    ).astype(float)
    viewer.add_image(blobs, name='blobs', opacity=0.5, colormap='red')




    # custom key binding --> really cool
    @viewer.bind_key('p')
    def print_names(viewer):
        print([layer.name for layer in viewer.layers])


    @viewer.bind_key('m')
    def print_message(viewer):
        print('hello')
        yield
        print('goodbye')


    # to take a screenshot of the napari view... --> ça marche et c pas mal en fait peut etre le linker
    @viewer.bind_key('s')
    def save_snape(viewer):
        viewer.screenshot(path='/home/aigouy/Bureau/trash/test_napari_snap.tif', canvas_only=True)
        yield
        print('done')

    @viewer.bind_key('k')
    def change_scale(viewer):
        # alternative way of changing scale TODO TOP BEST KEEP IN MIND
        viewer.layers[0].scale = [random.randint(1, 30), 1, 1]
        yield
        print('done', viewer.layers[0].scale[0])
        print('done')


    @viewer.bind_key('2')
    def view2D(viewer):
        # switch to 2D view
        viewer.dims.ndisplay = 2
        yield
        print('done', viewer.dims.ndisplay)
        print('done')


    @viewer.bind_key('3')
    def view3D(viewer):
        # switch to 3D view
        viewer.dims.ndisplay = 3
        yield
        print('done', viewer.dims.ndisplay)
        print('done')


    @viewer.bind_key('g')
    def getcamstate(viewer):
        print(viewer.window.qt_viewer.view.camera.get_state())
        # q = Quaternion.create_from_euler_angles(*angles, degrees=True)
        # change 3D camera angle
        q = viewer.window.qt_viewer.view.camera._quaternion
        print(q.get_axis_angle())
        print(q)
        r = R.from_quat(list(vispy_view.camera._quaternion.get_axis_angle()))
        print('angles for humans', r.as_euler('zyx', degrees=True))



    # import napari
    #
    # # use napari.gui_qt() if you don't already have a Qt loop
    # viewer = napari.Viewer()
    #
    # # the QtViewer is one of the most important classes to look at
    # viewer.window.qt_viewer

    # can I get and copy this to my own GUI --> if so I can use napari as my default viewer

    #
    # # among other things, it contains a "canvas" object that comes from vispy
    # viewer.window.qt_viewer.canvas
    #
    # # it has a "native" attribute that is a QWidget
    # from qtpy.QtWidgets import QWidget
    #
    # assert isinstance(viewer.window.qt_viewer.canvas.native, QWidget)

    # viewer.add_image(channel,
    #                  name=chname,
    #                  scale=(1, 1, 1, scalefactors['zx'], 1, 1),
    #                  contrast_limits=clim,
    #                  blending='additive',
    #                  gamma=0.85)

#
    # viewer = napari.view_image(data.astronaut(), rgb=True)
#
#
"""
Add named or unnamed vispy colormaps to existing layers.
"""
#
# import numpy as np
# import vispy.color
# from skimage import data
# import napari
#
#
# histo = data.astronaut() / 255
# rch, gch, bch = np.transpose(histo, (2, 0, 1))
# red = vispy.color.Colormap([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
# green = vispy.color.Colormap([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
# blue = vispy.color.Colormap([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
#
# with napari.gui_qt():
#     v = napari.Viewer()
#
#     rlayer = v.add_image(rch, name='red channel')
#     rlayer.blending = 'additive'
#     rlayer.colormap = 'red', red
#     glayer = v.add_image(gch, name='green channel')
#     glayer.blending = 'additive'
#     glayer.colormap = green  # this will appear as [unnamed colormap]
#     blayer = v.add_image(bch, name='blue channel')
#     blayer.blending = 'additive'
#     blayer.colormap = {'blue': blue}