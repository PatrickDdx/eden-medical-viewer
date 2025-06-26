from src.ui.toast_api import toast

class LoadController:
    def __init__(self, main_window, data_manager, viewer_widget, metadata_viewer):
        self.main_window = main_window
        self.data_manager = data_manager
        self.viewer_widget = viewer_widget
        self.metadata_viewer = metadata_viewer
        self.original_dicom_headers = None
        self.nifti_affine_matrix = None

    def open_image_file(self):
        from PyQt6.QtWidgets import QFileDialog
        import cv2
        import numpy as np

        image_filename, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (*.bmp);;All Files (*)") # "sample_medical_image.png"

        if image_filename:

            # Read the image
            image_grayscale = cv2.imread(image_filename)
            if image_grayscale is None:
                raise FileNotFoundError(f"Image not found at {image_filename}. Please check path and upload.")

            # Convert to RGB (SAM expects RGB)
            image_rgb = cv2.cvtColor(image_grayscale, cv2.COLOR_BGR2GRAY) #shape (x,y)

            image_volume = np.expand_dims(image_rgb, axis=0)

            self.viewer_widget.load_volume_series(image_volume)

            # Set the control sliders
            slice_maximum = image_volume.shape[0] - 1
            self.main_window.floating_controls_window.controls.slider.setMaximum(slice_maximum)
            self.main_window.floating_controls_window.controls.slice_value_label.setText(f"1/{slice_maximum+1}")

            min_val = np.min(image_grayscale)
            max_val = np.max(image_grayscale)

            default_center = (max_val + min_val) // 2
            default_width = max_val - min_val

            self.viewer_widget.update_windowing(default_center, default_width)




    def open_dicom_file(self):
        from PyQt6.QtWidgets import QFileDialog
        import os
        from src.image_data_handling.dicom_loader_thread import start_dicom_loader
        from src.image_data_handling.dicom_reader import DicomReader

        file_path, _ = QFileDialog.getOpenFileName(None, "Open DICOM File", "", "DICOM Files (*.dcm);;All Files (*)")
        if file_path:
            folder = os.path.dirname(file_path)
            self.viewer_widget.show_loading_animation()

            self.reader_dicom = DicomReader()

            self.dicom_thread, self.dicom_loader = start_dicom_loader(
                folder,
                self.reader_dicom,
                self._on_dicom_loading_finished,
                self._on_volume_loading_error
            )

    def open_nifti_file(self):
        from PyQt6.QtWidgets import QFileDialog
        from src.image_data_handling.NIfTI_loader_thread import start_nifti_loader
        from src.image_data_handling.NIfTI_reader import NIfTIReader

        file_path, _ = QFileDialog.getOpenFileName(None, "Open NIfTI File", "", "NIfTI Files (*.nii);;All Files (*)")
        if file_path:
            self.viewer_widget.show_loading_animation()

            self.reader_nifti = NIfTIReader()
            self.nifti_thread, self.nifti_loader = start_nifti_loader(
                file_path,
                self.reader_nifti,
                self._on_nifti_loading_finished,
                self._on_volume_loading_error
            )

    def _on_dicom_loading_finished(self, volume, center, width, metadata, original_dicom_headers):
        self.original_dicom_headers = original_dicom_headers
        self.data_manager.set_original_dicom_headers(self.original_dicom_headers)
        self._on_volume_loaded(volume, center, width, metadata)

    def _on_nifti_loading_finished(self, volume, center, width, affine_matrix = None):
        self.nifti_affine_matrix = affine_matrix
        self.data_manager.set_nifti_affine_matrix(self.nifti_affine_matrix)
        self._on_volume_loaded(volume, center, width)

    def _on_volume_loaded(self, volume, default_center, default_width, metadata_dict=None):
        self.viewer_widget.hide_loading_animation()

        # Update your UI with the loaded data
        self.viewer_widget.load_volume_series(volume)
        self.viewer_widget.update_windowing(default_center, default_width)

        if metadata_dict is None:
            metadata_dict = {}
        self.metadata_viewer.display_metadata(metadata_dict)

        #Set the control sliders
        slice_maximum = volume.shape[0] - 1
        self.main_window.floating_controls_window.controls.slider.setMaximum(slice_maximum)
        self.main_window.floating_controls_window.controls.slice_value_label.setText(f"1/{slice_maximum}")
        self.main_window.floating_controls_window.controls.center_slider.setValue(default_center)
        self.main_window.floating_controls_window.controls.width_slider.setValue(default_width)

    def _on_volume_loading_error(self, error_message):
        # Hide and clean up the loading animation
        self.viewer_widget.hide_loading_animation()

        # Show an error message to the user
        toast(f"Loading Error. Failed to load:\n{error_message}")
