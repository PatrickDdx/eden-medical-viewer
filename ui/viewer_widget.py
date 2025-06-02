from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
import numpy as np

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_label = QLabel()

        self.image_label.setScaledContents(False)  # Let you control the scaling manually
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.image_label.setText("No file selected")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.current_pixmap = None
        self.dicom_slices = None #3D array (z, y,x)
        self.current_slice_index = 0
        self.window_center = 0
        self.window_width = 0

    def resizeEvent(self, event):
        if hasattr(self, "current_pixmap") and self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

    def load_dicom_series(self, volume_data: np.ndarray):
        """Takes a 3D NumPy array and sets up the viewer."""
        self.dicom_slices = volume_data
        self.current_slice_index = 0
        self.update_image(self.current_slice_index)

    def display_image(self, image_data_2d):
        """receives 2D array of type np.uint8 and displays it"""

        height, width = image_data_2d.shape
        bytes_per_line = width

        q_image = QImage(image_data_2d.tobytes(), width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        self.current_pixmap = QPixmap.fromImage(q_image)
        #self.image_label.setPixmap(self.current_pixmap)
        scaled_pixmap = self.current_pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        self.image_label.setText("") #clear Text

    def update_image(self, slice_index: int):
        """Update the displayed slice"""
        if self.dicom_slices is None:
            return

        self.current_slice_index = slice_index
        slice_data = self.dicom_slices[slice_index]
        processed = self.apply_windowing(slice_data)
        self.display_image(processed)

    def update_windowing(self, center: int, width: int):
        """Update the windowing"""
        self.window_center = center
        self.window_width = width
        self.update_image(self.current_slice_index)

    def apply_windowing(self, img: np.ndarray) -> np.ndarray:
        lower_bound = self.window_center - (self.window_width / 2)
        upper_bound = self.window_center + (self.window_width /2)

        windowed_img = np.clip(img, lower_bound, upper_bound)

        denom = upper_bound - lower_bound
        if denom == 0:
            windowed_img_normalized = np.zeros_like(windowed_img, dtype=np.float32)
        else:
            windowed_img_normalized = (windowed_img - lower_bound) / denom

        img_8bit = np.nan_to_num(windowed_img_normalized * 255).astype(np.uint8)

        return img_8bit

