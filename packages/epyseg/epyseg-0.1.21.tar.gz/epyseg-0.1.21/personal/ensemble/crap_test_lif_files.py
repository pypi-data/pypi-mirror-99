# /D/Sample_images/sample_images_denoise_manue/200709_armGFP_suz_46hAPF_ON
from epyseg.img import Img

img = Img('/D/Sample_images/sample_images_denoise_manue/200709_armGFP_suz_46hAPF_ON/200709_armGFP_suz_46hAPF_ON.lif - Series029_t000.tif')
print(img) # ok indeed the full range is missing --> now check reading from the lif file directly and also try using 16bits on the leica in case they fucked their conversion to 8 bits...
# check lif file directly