import napari

from epyseg.img import Img

# not working!!!!!!!!!!!!!
with napari.gui_qt():
    view = napari.View()
    #add images here
    viewer = napari.Viewer(ndisplay=3)  # 3D viewer
    viewer.dims.ndisplay = 3  # alternative way to go 3D
    image = Img("/home/aigouy/Bureau/Image1.tif")
    viewer.add_image(image, scale=(10, 1, 1))  #


    # make movie
    movie = napari.Movie(view)
    #do what's necessary for making the movie here
    movie.finish()
