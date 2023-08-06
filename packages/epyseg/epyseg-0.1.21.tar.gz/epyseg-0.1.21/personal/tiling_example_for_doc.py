from matplotlib import patches

from epyseg.img import Img
import matplotlib.pyplot as plt


def print_as_bas64():
    import numpy as np
    import matplotlib as mpl
    import base64
    from PIL import Image
    import matplotlib.pyplot as plt
    import io

    # marche pas non plus --> bug
    # plt.savefig('/D/Sample_images/sample_images_PA/egg_chambers/test_raw.png')

    # plt.gcf()
    buf = io.BytesIO()
    # figdata_png = base64.b64encode(buf.getvalue())
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # marche pas --> empty --> why ????
    # im = Image.open(buf)
    # im.show()
    #
    # buf.seek(0)

    # my_base64_jpgData = base64.b64encode(buf.read())
    figdata_png = base64.b64encode(buf.getvalue())

    print(figdata_png)  # ça marche --> top cool je peux l'avoir en svg ou en png --> exactement ce que je veux...

    buf.close()

    print('\n'*5)
    print('####################################################################################################')
    print('\n' * 5)


raw = Img('/D/Sample_images/sample_images_PA/egg_chambers/Series016.png')
# make it draw over images
_, tiles_without_overlap = Img.get_2D_tiles_with_overlap(raw, width=512, height=512, overlap=0)
# plot as a 2x2 stuff
# maybe create images with


fig, ax = plt.subplots(1)

plt.title('single 1024 x 1024 image')
# Display the image
ax.imshow(raw)

# Create a Rectangle patch
rect = patches.Rectangle((0, 0), 512, 512, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)
rect = patches.Rectangle((512, 0), 512, 512, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)
rect = patches.Rectangle((0, 512), 512, 512, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)
rect = patches.Rectangle((512, 512), 512, 512, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

# Add the patch to the Axes
# need be called before plt.show otherwise white image
print_as_bas64()

plt.show()
plt.close()

# plt.title('four 256 x 256 non overlapping tiles')
f, axarr = plt.subplots(2, 2)

f.suptitle('four 512 x 512 non overlapping tiles')

axarr[0, 0].imshow(tiles_without_overlap[0][0])
axarr[0, 1].imshow(tiles_without_overlap[1][0])
axarr[1, 0].imshow(tiles_without_overlap[0][1])
axarr[1, 1].imshow(tiles_without_overlap[1][1])
# fig_tiles = plt.figure(figsize = (2, 2))
# plt.subplot(1,1,1)
# plt.imshow(tiles_without_overlap[0][0])
# plt.subplot(1,2,1)
# plt.imshow(tiles_without_overlap[1][0])

# fig_tiles.

# need be called before plt.show otherwise white image
print_as_bas64()

if True:
    import sys
    sys.exit(0)

# plt.imshow(tiles_without_overlap[0][0])
plt.show()
plt.close()

# do the same with overlap and I'm done...


_, tiles_without_overlap = Img.get_2D_tiles_with_overlap(raw, width=512, height=512, overlap=64)
fig, ax = plt.subplots(1)

plt.title('single 1024 x 1024 image')
# Display the image
ax.imshow(raw)

# Create a Rectangle patch
rect = patches.Rectangle((0, 0), 512 + 32, 512 + 32, linewidth=1, edgecolor='r', facecolor='none')
# rect.set_alpha(0.25)
ax.add_patch(rect)
rect = patches.Rectangle((512 - 32, 0), 512 + 64, 512 + 32, linewidth=1, edgecolor='g', facecolor='none')
# rect.set_alpha(0.25)
ax.add_patch(rect)
rect = patches.Rectangle((0, 512 - 32), 512 + 32, 512 + 64, linewidth=1, edgecolor='b', facecolor='none')
# rect.set_alpha(0.25)
ax.add_patch(rect)
rect = patches.Rectangle((512 - 32, 512 - 32), 512 + 64, 512 + 64, linewidth=1, edgecolor='y', facecolor='none')
# rect.set_alpha(0.25)
ax.add_patch(rect)

# Add the patch to the Axes


plt.show()
plt.close()

f, axarr = plt.subplots(2, 2)
f.suptitle('four 512 x 512 overlapping tiles')
axarr[0, 0].imshow(tiles_without_overlap[0][0])
# rect = patches.Rectangle((0,0),512-32,512-32,linewidth=1,edgecolor='r',facecolor='none')
# axarr[0,0].add_patch(rect)
# rect.set_alpha(0.25)
axarr[0, 1].imshow(tiles_without_overlap[1][0])
# rect = patches.Rectangle((64,0),512-32,512,linewidth=1,edgecolor='r',facecolor='none')
# axarr[0,1].add_patch(rect)
axarr[1, 0].imshow(tiles_without_overlap[0][1])

# axarr[1,0].add_patch(rect)
axarr[1, 1].imshow(tiles_without_overlap[1][1])

# axarr[1,1].add_patch(rect)
# fig_tiles = plt.figure(figsize = (2, 2))
# plt.subplot(1,1,1)
# plt.imshow(tiles_without_overlap[0][0])
# plt.subplot(1,2,1)
# plt.imshow(tiles_without_overlap[1][0])

# fig_tiles.


# plt.imshow(tiles_without_overlap[0][0])
# plt.show()
# plt.close()


# save as png or encode them 64 to embed them
# try encode 64 them


# print("![Hello World](data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAEYAAAAUCAAAAAAVAxSkAAABrUlEQVQ4y+3TPUvDQBgH8OdDOGa+oUMgk2MpdHIIgpSUiqC0OKirgxYX8QVFRQRpBRF8KShqLbgIYkUEteCgFVuqUEVxEIkvJFhae3m8S2KbSkcFBw9yHP88+eXucgH8kQZ/jSm4VDaIy9RKCpKac9NKgU4uEJNwhHhK3qvPBVO8rxRWmFXPF+NSM1KVMbwriAMwhDgVcrxeMZm85GR0PhvGJAAmyozJsbsxgNEir4iEjIK0SYqGd8sOR3rJAGN2BCEkOxhxMhpd8Mk0CXtZacxi1hr20mI/rzgnxayoidevcGuHXTC/q6QuYSMt1jC+gBIiMg12v2vb5NlklChiWnhmFZpwvxDGzuUzV8kOg+N8UUvNBp64vy9q3UN7gDXhwWLY2nMC3zRDibfsY7wjEkY79CdMZhrxSqqzxf4ZRPXwzWJirMicDa5KwiPeARygHXKNMQHEy3rMopDR20XNZGbJzUtrwDC/KshlLDWyqdmhxZzCsdYmf2fWZPoxCEDyfIvdtNQH0PRkH6Q51g8rFO3Qzxh2LbItcDCOpmuOsV7ntNaERe3v/lP/zO8yn4N+yNPrekmPAAAAAElFTkSuQmCC)")
