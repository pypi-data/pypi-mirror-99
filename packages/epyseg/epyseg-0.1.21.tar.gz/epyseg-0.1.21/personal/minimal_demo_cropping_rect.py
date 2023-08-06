# ça marche -->  c'est parfait et plutot facile à faire en fait
# nb there may be bugs if drawn rect is bigger than the image --> best is not to allow that

# test of a minimal demo of a cropping rect based on the idea https://github.com/leimao/Rotated_Rectangle_Crop_OpenCV
from epyseg.draw.shapes.image2d import Image2D
from epyseg.draw.shapes.rect2d import Rect2D
from epyseg.img import Img
import matplotlib.pyplot as plt

img = Img('/D/Sample_images/sample_images_PA/trash_test_mem/mini/focused_Series012.png')
# rect = Rect2D(128,128,256,128)
# rect = Rect2D(128,128,256,128)
rect = Rect2D(128,256,128,256)
print(rect)
rect.set_rotation(45)
#

# si rect depasse alors il faut cropper stuff

plt.imshow(img)
plt.show()

bounds = rect.boundingRect()
print(bounds)
# crop image # just the current view only
crop_params = {'w': [int(bounds.x()), int(bounds.x()+bounds.width())], 'h': [int(bounds.y()), int(bounds.y()+bounds.height())]} # in fact would need to increase image size if crop goes beyond but that does no make sense --> just do not allow this
cropped = img.crop(**crop_params)#x1=bounds.x(), y1=bounds.y(), x2=bounds.x()+bounds.width(), y2=bounds.y()+bounds.height()
# then rotate the image and crop it

plt.imshow(cropped)
plt.show()

tmp = Image2D('/D/Sample_images/sample_images_PA/trash_test_mem/mini/focused_Series012.png')
tmp.annotation.append(rect)

# draw and show this ???
# tmp.show()


# good but if there is a rotation then need an additional step
rotation = rect.theta
if rotation is not None and rotation != 0:
    # need rotate the image and the square the same way
    # rotate image and its associated rect then recrop it to the rect size --> is that hard or not ???
    # test = Image2D(cropped)
    # rect has to be centered always --> easy --> take image rotate it and center rect and that's it

    # TODO could be -rotation in fact

    from scipy import ndimage, misc
    full_img_rotated = ndimage.rotate(cropped, -rotation, reshape=True)

    plt.imshow(full_img_rotated)
    plt.show()

    # center rect onto it and crop it
    # take the original with and height and center it onto the image

    original_rect = rect.boundingRect(scaled=False)
    width = original_rect.width()
    height = original_rect.height()

    # center this rect on cropped rotated image and I'm done...
    #

    trans_x = full_img_rotated.shape[1] - width
    trans_x/=2
    trans_y = full_img_rotated.shape[0] - height
    trans_y/=2

    print(trans_x, trans_y)


    final_cropped = full_img_rotated[int(trans_x if trans_x>0 else 0):int(trans_x+width),int(trans_y if trans_y>0 else 0):int(trans_y+height)]#
    plt.imshow(final_cropped)
    plt.show()








