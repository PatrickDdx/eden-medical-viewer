class SaveController:
    def __init__(self, viewer_widget, data_manager):
        self.viewer_widget = viewer_widget
        self.data_manager = data_manager

    def save_image(self, file_path):
        if file_path:
            self.data_manager.save_current_slice(file_path, self.viewer_widget.current_slice_index, self.viewer_widget.window_width, self.viewer_widget.window_center)
        else:
            print("Save cancelled")

    def save_dicom(self, directory):
        if self.data_manager.volume_data is None:
            print("No Data")
            return
        if self.data_manager.original_dicom_headers is None or not self.data_manager.original_dicom_headers:
            print("Missing Data: header")
            return

        if directory:
            self.data_manager.save_as_dicom(directory)
        else:
            print("Dicom saving cancelled")


    def save_nifti(self, file_path):
        if file_path:
            self.data_manager.save_as_nifti(file_path)
        else:
            print("Save cancelled")

    def save_mp4(self, file_path):
        if file_path:
            try:
                self.data_manager.save_as_mp4(file_path, self.viewer_widget.cine_interval, self.viewer_widget.window_width, self.viewer_widget.window_center)
                print("MP4 export completed successfully.")
            except Exception as e:
                print(f"MP4 export failed: {e}")
        else:
            print("Save cancelled")
