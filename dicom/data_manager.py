import numpy as np
import cv2
import pydicom
import nibabel
from PyQt6.QtGui import QPixmap, QImage
from pathlib import Path

class DataSaver:

    def __init__(self):
        self._volume_data = None
        self.original_dicom_headers = None
        self.nifti_affine_matrix = None

    @property
    def volume_data(self):
        return self._volume_data

    @volume_data.setter
    def volume_data(self, data: np.ndarray):
        """Sets the raw 3d volume data"""
        self._volume_data = data

    def set_original_dicom_headers(self, headers: list):
        self.original_dicom_headers = headers

    def set_nifti_affine_matrix(self, affine: np.ndarray):
        self.nifti_affine_matrix = affine

    def apply_windowing_internal(self, img: np.ndarray, width, level) -> np.ndarray:
        lower_bound = level - (width / 2)
        upper_bound = level + (width /2)

        windowed_img = np.clip(img, lower_bound, upper_bound)

        denom = upper_bound - lower_bound
        if denom == 0:
            windowed_img_normalized = np.zeros_like(windowed_img, dtype=np.float32)
        else:
            windowed_img_normalized = (windowed_img - lower_bound) / denom

        img_8bit = np.nan_to_num(windowed_img_normalized * 255).astype(np.uint8)

        return img_8bit


#################### Saving functions

    def save_current_slice(self, pixmap: QPixmap, filepath: str):
        """Saves the current pixmap (from image_display) to a file
         :param filepath: Full file path including extension (e.g., 'output.png' or 'output.jpg')
         """
        if pixmap is not None and not pixmap.isNull():
            success = pixmap.save(filepath)
            if not success:
                print(f"Failed to save image to {filepath}")
            else:
                print(f"Image saved to {filepath}")
        else:
            print("No pixmap to save")

    def save_as_dicom(self, directory_path: str):
        if self.volume_data is None or self.original_dicom_headers is None or not self.original_dicom_headers:
            print("No data or original DICOM headers available to save")
            return

        print(f"Saving DICOM series to: {directory_path}")

        print("DICOM saved (or not because the method is blank...)")
        return

    def save_as_nifti(self, filepath: str):
        if self.volume_data is None or self.nifti_affine_matrix is None:
            print("Missing data or affine Matrix")
            print(f"volume_data is None? {self.volume_data is None}")
            print(f"affine_matrix is None? {self.nifti_affine_matrix is None}")

            return

        try:
            save_volume = np.transpose(self.volume_data, (2, 1, 0))

            nifti_img = nibabel.Nifti1Image(save_volume, self.nifti_affine_matrix)
            nibabel.save(nifti_img, filepath)

            print(f"NIfTI save to {filepath}")
        except Exception as e:
            print(f"Failed to save NIfTI: {e}")


    def save_as_mp4(self, file_path: str, cine_interval, window_width, window_level):
        """Exports the current volume as MP4 video"""
        print("Starting export_as_mp4")

        if self.volume_data is None:
            print("No dicom_slices loaded")
            return

        if not file_path.lower().endswith(".mp4"):
            file_path += ".mp4"

        print(f"Saving to: {file_path}")
        print(f"cine_interval: {cine_interval}")

        num_slices, height, width = self.volume_data.shape
        fps = 1000 // cine_interval if cine_interval > 0 else 10
        print(f"Video dimensions: {width}x{height}, FPS: {fps}")

        import cv2  # <- make sure OpenCV is imported at the top

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(file_path, fourcc, fps, (width, height))

        for i in range(self.volume_data.shape[0]):
            img = self.apply_windowing_internal(self.volume_data[i], window_width, window_level)
            frame = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            writer.write(frame)

        writer.release()
        print(f"Export complete: {file_path}")