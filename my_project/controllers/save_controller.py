from my_project.ui.toast_api import toast

class SaveController:
    def __init__(self, viewer_widget, data_manager):
        self.viewer_widget = viewer_widget
        self.data_manager = data_manager

    def save_image(self, file_path):
        if file_path:
            self.data_manager.save_current_slice(file_path, self.viewer_widget.current_slice_index, self.viewer_widget.window_width, self.viewer_widget.window_center)
        else:
            toast("Save cancelled")

    def save_overlay(self, file_path):
        if file_path:
            self.data_manager.save_current_scene_with_overlays(self.viewer_widget, file_path)
        else:
            toast("Save cancelled")

    def save_dicom(self, directory):
        if self.data_manager.volume_data is None:
            toast("No Data")
            return

        if directory:
            self.data_manager.save_as_dicom(directory)
        else:
            toast("Dicom saving cancelled")


    def save_nifti(self, file_path):
        if file_path:
            self.data_manager.save_as_nifti(file_path)
        else:
            toast("Save cancelled")

    def save_mp4(self, file_path):
        if file_path:
            try:
                interval_ms = self.viewer_widget.cine_controller.get_speed()
                self.data_manager.save_as_mp4(file_path, interval_ms, self.viewer_widget.window_width, self.viewer_widget.window_center)
                toast("MP4 export completed successfully.")
            except Exception as e:
                toast(f"MP4 export failed: {e}")
        else:
            toast("Save cancelled")
