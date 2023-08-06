import numpy as np
import matplotlib.pyplot as plt

from skimage import measure


# Construct some test data
from epyseg.img import Img

x, y = np.ogrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
r = np.sin(np.exp((np.sin(x)**3 + np.cos(y)**2)))


img = Img('/home/aigouy/Bureau/trash/test_new_seeds_seg_stuff/focused_Series194.tif')

# also that https://stackoverflow.com/questions/40615515/how-to-ignore-remove-contours-that-touch-the-image-boundaries !!!
# can I implement find contour by dilation of the shape then score ???
#

# Find contours at a constant value of 0.8
# takes forever
contours = measure.find_contours(img, 0.8) # marche mais super long et en plus splitte les bonds

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(img, cmap=plt.cm.gray)

for contour in contours:
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()