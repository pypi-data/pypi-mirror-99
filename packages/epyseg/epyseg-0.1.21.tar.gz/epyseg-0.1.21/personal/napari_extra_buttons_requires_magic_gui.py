import numpy as np
import napari
from magicgui import magicgui

with napari.gui_qt():
    viewer = napari.Viewer()
    layer = viewer.add_image(np.random.normal(10, 1, (256, 256)))


    @magicgui(
        auto_call=True,  # call function whenever a param is changed
        width={'maximum': 512},
        height={'maximum': 512},
        noise_type={'choices': ['normal', 'gumbel', 'laplace', 'logistic']},
    )
    def new_image(
            width=256, height=256, loc=10, scale=1.0, noise_type='normal'
    ):
        """generate new random image with some type of noise"""
        function = getattr(np.random, noise_type)
        return function(loc, scale, (width, height))


    def update_layer(result):
        layer.data = result
        # layer.reset_contrast_limits()


    # create the widget
    new_image_widget = new_image.Gui(show=True)
    # connect its "called" signal to your callback function
    new_image.called.connect(update_layer)
    # optionally, add it as a docked widget (and inherit styles) on viewer
    viewer.window.add_dock_widget(new_image_widget)