import numpy as np

from image_data_handling.exporters.dicom_exporter import export_dicom_series
from image_data_handling.exporters.nifti_exporter import export_nifti
from image_data_handling.exporters.video_exporter import export_as_mp4
from image_data_handling.exporters.image_exporter import export_slice_image
from ui.toast_api import toast


class VolumeDataManager:

    def __init__(self):
        self._volume_data = None
        self.original_dicom_headers = None
        self.nifti_affine_matrix = None
        self.current_data_type = None
        self._mask_data = None # Holds binary masks per slice (same shape as volume)
        self.slice_measurements = {} # {slice_index: [(p1, p2), ...]}
        self.pixel_spacing = None # to calculate distance in real space

    @property
    def volume_data(self):
        return self._volume_data

    @volume_data.setter
    def volume_data(self, data: np.ndarray):
        """Sets the raw 3d volume data"""
        self._volume_data = data

    @property
    def mask_data(self):
        return self._mask_data

    @mask_data.setter
    def mask_data(self, masks: np.ndarray):
        """
        Set the 3D mask volume.
        Shape must match volume_data (e.g. [N, H, W])
        """
        if masks.shape != self._volume_data.shape:
            raise ValueError("Mask shape does not match volumew data shape")
        self._mask_data = masks


    def set_original_dicom_headers(self, headers: list):
        self.current_data_type = "dicom"
        self.original_dicom_headers = headers
        self.nifti_affine_matrix = None #clear NIfTI specific data

        if headers:
            spacing = getattr(headers[0], "PixelSpacing", [1.0, 1.0]) # [row_spacing, col_spacing]#
            self.pixel_spacing = [float(spacing[0]), float(spacing[1])]
            #print(f"Pixel spacing set to: {self.pixel_spacing}")

    def set_nifti_affine_matrix(self, affine: np.ndarray):
        self.current_data_type = "nifti"
        self.nifti_affine_matrix = affine#
        self.original_dicom_headers = None

    def apply_windowing_internal(self, img: np.ndarray, width, level) -> np.ndarray:
        lower_bound = level - (width / 2)
        upper_bound = level + (width /2)

        windowed_img = np.clip(img, lower_bound, upper_bound)

        denom = upper_bound - lower_bound
        if denom == 0:
            windowed_img_normalized = np.zeros_like(windowed_img, dtype=np.float32)
        else:
            windowed_img_normalized = (windowed_img - lower_bound) / denom

        return np.nan_to_num(windowed_img_normalized * 255).astype(np.uint8)

    def apply_rescale_internal(self, slice_index):

        raw_slice_data = self.volume_data[slice_index]
        current_header = self.original_dicom_headers[slice_index]
        slope = float(getattr(current_header, 'RescaleSlope', 1.0))
        intercept = float(getattr(current_header, 'RescaleIntercept', 0.0))

        return raw_slice_data * slope + intercept

    def add_measurement(self, slice_index: int, p1, p2):
        if slice_index not in self.slice_measurements:
            self.slice_measurements[slice_index] = []
        self.slice_measurements[slice_index].append((p1, p2))

    def get_measurements(self, slice_index: int):
        return self.slice_measurements.get(slice_index, [])

    #################### Saving functions

    def save_current_slice(self, file_path, slice_index, ww, wl):
        try:
            if self.current_data_type == "dicom":
                raw_slice = self.apply_rescale_internal(slice_index)
            else:
                raw_slice = self.volume_data[slice_index]

            success = export_slice_image(raw_slice, ww, wl, self.apply_windowing_internal, file_path)

            if success:
                toast(f"Slice saved to {file_path}")
            else:
                toast(f"Failed to save slice to {file_path}")

        except Exception as e:
            toast(f"Error saving current slice: {e}")


    def save_as_dicom(self, directory_path):
        try:
            export_dicom_series(self.volume_data, self.original_dicom_headers, directory_path)
            toast(f"DICOM series saved to {directory_path}")
        except Exception as e:
            toast(f"Error saving DICOM series: {e}")

    def save_as_nifti(self, file_path):
        try:
            export_nifti(self.volume_data, self.nifti_affine_matrix, file_path)
            toast(f"NIfTI saved to {file_path}")
        except Exception as e:
            toast(f"Error saving NIfTI: {e}")

    def save_as_mp4(self, file_path, cine_interval, window_width, window_level):
        """Exports the current volume as MP4 video"""

        if not file_path.lower().endswith(".mp4"):
            file_path += ".mp4"

        fps = 1000 // cine_interval if cine_interval > 0 else 10

        try:
            def frame_callback(index_or_img):
                if self.current_data_type == "dicom":
                    return self.apply_windowing_internal(
                        self.apply_rescale_internal(index_or_img), window_width, window_level
                    )
                else:
                    return self.apply_windowing_internal(index_or_img, window_width, window_level)

            export_as_mp4(self.volume_data, file_path, fps, self.current_data_type, frame_callback)
            toast(f"MP4 saved to {file_path}")
        except Exception as e:
            toast(f"Error saving MP4: {e}")


