from epyseg.img import Img
import matplotlib.pyplot as plt

img = Img('/D/VirtualBox/final_paper_deep_learning/new_figures/new_figure_model/MAX_160610_test_ocelli_ok_but_useless_cause_differs_a_lot_from_ommatidia.lif - test_visualization_head_ommatidia_32h_APF_ok_2.tifavg.tif')


plt.imshow(img)
plt.colorbar()
plt.show()



# segment with deep learning and return one output

# load model and segment

# useless --> do it from the GUI