from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QApplication, QStackedLayout, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QMovie, QPainter
import numpy as np
import cv2

from dicom.data_manager import DataSaver
from ui.graphics_view import CustomGraphicsView
from dicom.data_manager import DataSaver

def calculate_distance(width, level, x_predefined, y_predefined):
  distance = np.sqrt((width-x_predefined)**2+(level-y_predefined)**2)

  return distance

class ViewerWidget(QWidget):
    def __init__(self, data_manager: DataSaver = None):
        super().__init__()

        self.data_manager = data_manager

        self.graphics_view = CustomGraphicsView(self)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        #disable scrollbars so the image doesn't shift on wheel events

        # set focus so key events get detected
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.setup_loading_animation() #loading animation setup

        # --- Main Layout using QStackedLayout ---
        self.main_stacked_layout = QStackedLayout()
        self.main_stacked_layout.addWidget(self.graphics_view)  # use the QGraphicsView itself
        self.main_stacked_layout.addWidget(self.loading_container)  # Index 1: Loading animation

        # Set the main layout of the ViewerWidget
        self.setLayout(self.main_stacked_layout)

        # Set initial visible widget (image_label)
        self.main_stacked_layout.setCurrentWidget(self.graphics_view)

        self.current_pixmap = None
        self.dicom_slices = None #3D array (z, y,x)
        self.current_slice_index = 0
        self.window_center = 40
        self.window_width = 80

        self.zoom_factor = 1.0

        self.slice_slider = None
        self.center_slider = None
        self.width_slider = None

        self.cine_timer = QTimer()
        self.cine_timer.timeout.connect(self.next_frame)
        self.is_cine_playing = False
        self.cine_interval = 100

        self.window_presets = {
            #head and neck
            "Brain": {"width": 80, "level": 40},
            "Subdural": {"width": 130, "level": 50},
            "Stroke": {"width": 8, "level": 32},
            "Temporal bones": {"width": 2800, "level": 600},
            #"soft tissues": {"width": 350, "level": 20},

            #chest
            "Lungs": {"width": 1500, "level": -600},
            "Mediastinum": {"width": 350, "level": 50},
            "Vascular/heart": {"width": 600, "level": 200},

            #abdomen
            "Soft tissues": {"width": 400, "level": 50},
            "Liver": {"width": 150, "level": 30},

            #spine
            #"soft tissues": {"width": 250, "level": 50},
            "Bone": {"width": 1800, "level": 400},

        }

        self.window_keys = {
            Qt.Key.Key_1: "Brain",
            Qt.Key.Key_2: "Lungs",
            Qt.Key.Key_3: "Soft tissues",
            Qt.Key.Key_4: "Bone"
        }


    def resizeEvent(self, event):
        # When the viewer resizes, ensure the image fits properly
        if self.current_pixmap and not self.current_pixmap.isNull():
            self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)

    def load_dicom_series(self, volume_data: np.ndarray):
        """Takes a 3D NumPy array and sets up the viewer."""
        self.dicom_slices = volume_data
        if self.data_manager:
            self.data_manager.volume_data = volume_data
        self.current_slice_index = 0
        #self.update_image(self.current_slice_index) #-> the image gets updated (and therefore windowed) when loading initially from the main Window

    def display_image(self, image_data_2d):
        """receives 2D array of type np.uint8 and displays it"""

        height, width = image_data_2d.shape
        bytes_per_line = width

        q_image = QImage(image_data_2d.tobytes(), width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        self.current_pixmap = QPixmap.fromImage(q_image)
        self.pixmap_item.setPixmap(self.current_pixmap)

        self.graphics_view.resetTransform()
        self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.graphics_view.scale(self.zoom_factor, self.zoom_factor)

    def update_image(self, slice_index: int):
        """Update the displayed slice"""
        if self.dicom_slices is None:
            return

        self.current_slice_index = slice_index
        slice_data = self.dicom_slices[slice_index]
        processed = self.apply_windowing(slice_data)
        self.display_image(processed)

        # IMPORTANT: When the image is updated by non-slider means (e.g., cine loop, key press, wheel event),
        # we update the slider's value directly. The slider's valueChanged signal will then trigger
        # the DicomControls label update.
        if self.slice_slider and self.slice_slider.value() != slice_index:
            # NO blockSignals(True) here. We want the slider's signal to propagate to DicomControls.
            self.slice_slider.setValue(slice_index)

    def update_windowing(self, center: int, width: int):
        """Update the windowing"""
        self.window_center = center
        self.window_width = width
        self.update_image(self.current_slice_index)

        # Sync sliders
        # Update sliders if values were set externally (e.g., by default windowing, preset)
        # NO blockSignals(True) here. We want the slider's signal to propagate to DicomControls.
        if self.center_slider and self.center_slider.value() != center:
            self.center_slider.setValue(center)
        if self.width_slider and self.width_slider.value() != width:
            self.width_slider.setValue(width)

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
        #print(f"presets: {preset}")
        if preset:
            self.update_windowing(preset["level"], preset["width"])

    def get_current_window(self):
        print(f"width: {self.window_width}, level: {self.window_center}")

    def wheelEvent(self, event):
        if self.dicom_slices is None:
            return

        modifiers = event.modifiers()
        delta = event.angleDelta().y()  # Positive = scroll up, negative = scroll down

        if modifiers & Qt.KeyboardModifier.ControlModifier:
            zoom_step = 0.1
            if delta > 0:
                self.zoom_factor = min(5.0, self.zoom_factor + zoom_step)
            else:
                self.zoom_factor = max(0.1, self.zoom_factor - zoom_step)

            self.graphics_view.resetTransform()
            self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
            self.graphics_view.scale(self.zoom_factor, self.zoom_factor)

            return #skip slice scrolling while zooming

        #Regular slice scrolling
        number_of_slices = self.dicom_slices.shape[0]

        step_amount = int(number_of_slices * 0.10) #10% of the slices when fast scrolling

        # Default step = 1, with Shift = 5 slices
        # Qt6 modifiers: use Qt.KeyboardModifier.#shiftModifier
        step = step_amount if modifiers == Qt.KeyboardModifier.ShiftModifier or \
                    modifiers & Qt.KeyboardModifier.ShiftModifier else 1

        if delta > 0:
            self.current_slice_index = min(self.current_slice_index + step, number_of_slices - 1)
        elif delta < 0:
            self.current_slice_index = max(self.current_slice_index - step, 0)

        self.update_image(self.current_slice_index)

        event.accept()

    def set_slider(self, slider, center_slider = None, width_slider = None):
        self.slice_slider = slider
        self.center_slider = center_slider
        self.width_slider  = width_slider

    def keyPressEvent(self, event):
        key = event.key()
        #print(f"key pressed: {key}")
        name = self.window_keys.get(key)
        #print(f"name {name}")
        if name:
            self.apply_window_preset(name)

        if key == Qt.Key.Key_P:
            self.toggle_cine_loop()

        super().keyPressEvent(event)


####################################################### Loading animation

    def setup_loading_animation(self):
        # --- Loading Animation Setup ---
        self.loading_animation_label = QLabel(self)
        self.loading_animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.loading_animation_label.hide()  # Hide initially

        self.loading_movie = QMovie(
            "C:/Users/patri/GIT/dicomViewer/assets/animations/Ripple@1x-1.0s-200px-200px.gif")  # Adjust path as needed
        if self.loading_movie.isValid():
            self.loading_animation_label.setMovie(self.loading_movie)
        else:
            print("Warning: Loading GIF not found or invalid. Using text placeholder.")
            self.loading_animation_label.setText("Loading...")
            self.loading_animation_label.setStyleSheet("color: white;")  # Example style

        # Add a placeholder label for loading text
        self.loading_text_label = QLabel("Loading DICOM files, please wait...", self)
        self.loading_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_text_label.setStyleSheet("color: white;")
        #self.loading_text_label.hide()

        self.loading_container = QWidget()
        loading_layout = QVBoxLayout()
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(self.loading_animation_label)
        loading_layout.addWidget(self.loading_text_label)
        self.loading_container.setLayout(loading_layout)
        self.loading_container.hide()

    def show_loading_animation(self):
        """Shows the loading animation and hides the image label."""
        self.main_stacked_layout.setCurrentWidget(self.loading_container)
        if self.loading_movie.isValid():
            self.loading_movie.start()
        QApplication.processEvents()

    def hide_loading_animation(self):
        """Hides the loading animation and shows the image label."""
        if self.loading_movie.isValid():
            self.loading_movie.stop()
        self.main_stacked_layout.setCurrentWidget(self.graphics_view)


##################################################### Cine loop functions

    def start_cine_loop(self):
        if self.dicom_slices is None:
            return
        self.cine_timer.start(self.cine_interval)
        self.is_cine_playing = True

    def stop_cine_loop(self):
        self.cine_timer.stop()
        self.is_cine_playing = False

    def toggle_cine_loop(self):
        if self.is_cine_playing:
            self.stop_cine_loop()
        else:
            self.start_cine_loop()

    def next_frame(self):
        if self.dicom_slices is None:
            return
        self.current_slice_index = (self.current_slice_index + 1) % self.dicom_slices.shape[0]
        self.update_image(self.current_slice_index)

    def increase_cine_speed(self):
        self.cine_interval = max(10, self.cine_interval - 30)
        if self.is_cine_playing:
            self.cine_timer.start(self.cine_interval)

    def decrease_cine_speed(self):
        self.cine_interval = min(250, self.cine_interval + 30)
        if self.is_cine_playing:
            self.cine_timer.start(self.cine_interval)

###################################################################################

    def normalize_to_uint8(self, image):
        img = np.clip(image, np.min(image), np.max(image))
        img = (img-img.min()) / (img.max() - img.min()) * 255
        return  img.astype(np.uint8)


    def find_nearest_neighbor(self, current_width, current_level):
        """Finds the nearest predefined window preset to a given (width, level) point"""

        if self.current_pixmap is None:
            return "N/A"

        closest_window_name = None

        names = []
        distances_to_preset = []

        for key in self.window_presets:
            dist = calculate_distance(current_width, current_level, self.window_presets[key]["width"], self.window_presets[key]["level"])
            names.append(key)
            distances_to_preset.append(dist)

        min_idx = np.argmin(distances_to_preset)
        closest_window_name = names[min_idx]
        #print(f"nearest predefined window is: {names[min_idx]} ; distance: {distances_to_preset[min_idx]}")

        return closest_window_name

######################################## Saving functions
    def save_current_slice_ui(self, filepath: str):
        """UI-level method to trigger saving of the currently displayed image."""
        self.data_manager.save_current_slice(self.current_pixmap, filepath)

    def save_as_dicom_ui(self, directory_path: str, original_dicom_headers: list = None):
        self.data_manager.save_as_dicom(
            self.data_manager.volume_data,
            original_dicom_headers,
            directory_path
        )

    def save_as_nifti_ui(self):
        pass

    def export_as_mp4_ui(self, file_path):
        self.data_manager.save_as_mp4(file_path, self.cine_interval, self.window_width, self.window_center)
        print(f"width: {self.window_width}, level: {self.window_center}")

