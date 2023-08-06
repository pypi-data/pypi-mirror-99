from epyseg.img import Img

img = Img('/home/aigouy/Téléchargements/flywing.tif')
print(img.shape)
#(1, 35, 520, 692, 1) --> easy to try on my images --> TODO

img = Img('/home/aigouy/Dropbox/armGFP_1_manue_10percent_laser_speed6_line2_test_n2v_3d.tif')
print(img.shape)
# (25, 924, 1004)