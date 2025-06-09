from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
import numpy as np

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # set focus so key events get detected
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

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

        self._mouse_pressed = False
        self._last_mouse_pos = None
        self._start_window_center = 0
        self._start_window_width = 0

        self.slice_slider = None
        self.center_slider = None
        self.width_slider = None

#        self.window_presets = {
 #           Qt.Key.Key_1: {"name": "Brain", "center": 40, "width": 80},
  #          Qt.Key.Key_2: {"name": "Lung", "center": -600, "width": 1500},
   #         Qt.Key.Key_3: {"name": "Bone", "center": 300, "width": 1500},
#
 #       }

        self.window_presets = {
            #head and neck
            "brain": {"width": 80, "level": 40},
            "subdural": {"width": 130, "level": 50},
            "stroke": {"width": 8, "level": 32},
            "temporal bones": {"width": 2800, "level": 600},
            #"soft tissues": {"width": 350, "level": 20},

            #chest
            "lungs": {"width": 1500, "level": -600},
            "mediastinum": {"width": 350, "level": 50},
            "vascular/heart": {"width": 600, "level": 200},

            #abdomen
            "soft tissues": {"width": 400, "level": 50},
            "liver": {"width": 150, "level": 30},

            #spine
            #"soft tissues": {"width": 250, "level": 50},
            "bone": {"width": 1800, "level": 400},

        }

        self.window_keys = {
            Qt.Key.Key_1: "brain",
            Qt.Key.Key_2: "lungs",
            Qt.Key.Key_3: "soft tissues",
            Qt.Key.Key_4: "bone"
        }

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
        #self.update_image(self.current_slice_index)

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

        if hasattr(self, 'slice_slider') and self.slice_slider: #syncs the slider with the current slice if it was changed with the mouse wheel
            if self.slice_slider.value() != slice_index:
                self.slice_slider.blockSignals(True)
                self.slice_slider.setValue(slice_index)
                self.slice_slider.blockSignals(False)

    def update_windowing(self, center: int, width: int):
        """Update the windowing"""
        self.window_center = center
        self.window_width = width
        self.update_image(self.current_slice_index)

        # Sync sliders
        if hasattr(self, 'center_slider') and self.center_slider is not None:
            self.center_slider.blockSignals(True)
            self.center_slider.setValue(center)
            self.center_slider.blockSignals(False)

        if hasattr(self, 'width_slider') and self.width_slider is not None:
            self.width_slider.blockSignals(True)
            self.width_slider.setValue(width)
            self.width_slider.blockSignals(False)

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

    def apply_window_preset(self, name: str):
        preset = self.window_presets.get(name)
        print(f"presets: {preset}")
        if preset:
            self.update_windowing(preset["level"], preset["width"])

    def get_current_window(self):
        print(f"width: {self.window_width}, level: {self.window_center}")

    def wheelEvent(self, event):
        if self.dicom_slices is None:
            return

        number_of_slices = self.dicom_slices.shape[0]
        delta = event.angleDelta().y() # Positive = scroll up, negative = scroll down

        # Default step = 1, with Ctrl = 5 slices
        # Qt6 modifiers: use Qt.KeyboardModifier.ControlModifier
        modifiers = event.modifiers()
        step = 5 if modifiers == Qt.KeyboardModifier.ControlModifier or \
                    modifiers & Qt.KeyboardModifier.ControlModifier else 1

        if delta > 0:
            self.current_slice_index = min(self.current_slice_index + step, number_of_slices - 1)
        elif delta < 0:
            self.current_slice_index = max(self.current_slice_index - step, 0)

        self.update_image(self.current_slice_index)

    def set_slider(self, slider, center_slider = None, width_slider = None):
        self.slice_slider = slider
        self.center_slider = center_slider
        self.width_slider  = width_slider

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._mouse_pressed = True
            self._last_mouse_pos = event.position()
            self._start_window_center = self.window_center
            self._start_window_width = self.window_width

    def mouseMoveEvent(self, event):
        if self._mouse_pressed:
            delta = event.position() - self._last_mouse_pos
            dx = delta.x()
            dy = delta.y()

            new_center = self._start_window_center + int(dy)
            new_width = self._start_window_width + int(dx)

            new_width = max(1, new_width) #to avoid division by zero

            self.update_windowing(new_center, new_width)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._mouse_pressed = False
            self._last_mouse_pos = None

    def keyPressEvent(self, event):
        key = event.key()
        #print(f"key pressed: {key}")
        name = self.window_keys.get(key)
        #print(f"name {name}")
        if name:
            self.apply_window_preset(name)

