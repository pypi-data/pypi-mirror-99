from epyseg.img import Img

# img = Img('/D/mini_tuto_epyseg/retrain_model_use_pretrained_cropped.tif')
# img = Img('/D/mini_tuto_epyseg/retrain_model_train_window_crop_optimizer.tif')
# img = Img('/D/mini_tuto_epyseg/retrain_model_train_window_train_data_crop.tif')
# img = Img('/D/mini_tuto_epyseg/retrain_model_input_data.png')
# img = Img('/D/mini_tuto_epyseg/retrain_model_output.png')
# img = Img('/D/mini_tuto_epyseg/retrain_model_train_window_data_aug_main_crop.tif')
# img = Img('/D/mini_tuto_epyseg/retrain_data_aug.png')
img = Img('/D/mini_tuto_epyseg/retrained_model_ready_to_run_crop.tif')
# img = Img('/D/mini_tuto_epyseg/train_tab_raw_training_parameters.png')
# img = Img('/D/mini_tuto_epyseg/train_tab_raw_crop_image_normalization.png')
# img = Img('/D/mini_tuto_epyseg/train_tab_raw_crop_tiling.png')
# img = Img('/D/mini_tuto_epyseg/crop_data_aug_final.png')
# img = Img('/D/mini_tuto_epyseg/set_parameters_n_channels_training_crop.png')
# img = Img('/D/mini_tuto_epyseg/set_parameters_n_channels_crop.png')
# img = Img('/D/mini_tuto_epyseg/popup_dataset.png')
# img = Img('/D/mini_tuto_epyseg/train_tab_raw_crop_input_dataset.png')
# img = Img('/D/mini_tuto_epyseg/train_tab_raw_compile_crop.png')
# img = Img('/D/mini_tuto_epyseg/build_a_new_model_parameters_crop.png')
# img = Img('/D/mini_tuto_epyseg/build_a_new_model_crop.png')
# img = Img('/D/mini_tuto_epyseg/predict_tab_raw_tune_score_param_crop.png')
# img = Img('/D/mini_tuto_epyseg/predict_selected_input_channel_crop.png')
# img = Img('/D/mini_tuto_epyseg/predict_selected_input_folder_cropped.png')
# img = Img('/D/mini_tuto_epyseg/Model tab_press_go.png')
# img = Img('/D/mini_tuto_epyseg/crop_model_selection.png')


# 'No layer with name {} in  model {}.'.format(layer_name, model.name)
html_img = '<img src="data:image/png;base64, {}" alt="{}">'.format(Img.img2Base64(img),"select model")

print(html_img)

