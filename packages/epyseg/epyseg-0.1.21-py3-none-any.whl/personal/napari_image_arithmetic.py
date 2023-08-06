import enum
import numpy
import napari
from napari.layers import Image
# from magicgui import magicgui # marche pas


# Enums are a convenient way to get a dropdown menu
class Operation(enum.Enum):
    """A set of valid arithmetic operations for image_arithmetic."""
    add = numpy.add
    subtract = numpy.subtract
    multiply = numpy.multiply
    divide = numpy.divide


with napari.gui_qt():
    # create a new viewer with a couple image layers
    viewer = napari.Viewer()
    viewer.add_image(numpy.random.rand(20, 20), name=f"Layer 1")
    viewer.add_image(numpy.random.rand(20, 20), name=f"Layer 2")

    # here's the magicgui!  We also use the additional `call_button` option
    # @magicgui(call_button="execute")
    def image_arithmetic(layerA: Image, operation: Operation, layerB: Image) -> Image:
        """Adds, subtracts, multiplies, or divides two image layers of similar shape."""
        return operation.value(layerA.data, layerB.data)

    # instantiate the widget
    gui = image_arithmetic.Gui()
    # add our new widget to the napari viewer
    viewer.window.add_dock_widget(gui)
    # keep the dropdown menus in the gui in sync with the layer model
    viewer.layers.events.changed.connect(lambda x: gui.refresh_choices())


# instantiate the widget
gui = image_arithmetic.Gui()