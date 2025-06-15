from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QApplication, QStackedLayout, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QMovie, QPainter
import numpy as np
import cv2

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        #self.graphics_view.setSceneRect(self.graphics_view.viewport().rect())
        #self.graphics_view.setSceneRect(self.graphics_view.scene().itemsBoundingRect())

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)


        self.graphics_view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.graphics_view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.graphics_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.graphics_view.setBackgroundBrush(Qt.GlobalColor.black)
        self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        #disable scrollbars so the image doesn't shift on wheel events
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # set focus so key events get detected
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        #Main image label
        """
        self.image_label = QLabel()
        self.image_label.setScaledContents(False)  # Let you control the scaling manually
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image_label.setText("No file selected")
        """

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
        self.window_center = 0
        self.window_width = 0

        self.zoom_factor = 1.0
        self.pan_offset = (0,0)
        self.is_panning = False
        self.pan_start_pos = None

        self._mouse_pressed = False
        self._last_mouse_pos = None
        self._start_window_center = 0
        self._start_window_width = 0

        self.slice_slider = None
        self.center_slider = None
        self.width_slider = None

        self.cine_timer = QTimer()
        self.cine_timer.timeout.connect(self.next_frame)
        self.is_cine_playing = False
        self.cine_interval = 100

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

    def resizeEvent(self, event):
        """
        if hasattr(self, "current_pixmap") and self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            """
        self.update_scaled_pixmap()
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
        self.pixmap_item.setPixmap(self.current_pixmap)
        self.graphics_view.resetTransform()
        self.graphics_view.scale(self.zoom_factor, self.zoom_factor)
        self.graphics_view.centerOn(self.pixmap_item)

        #self.update_scaled_pixmap()

        """
        scaled_pixmap = self.current_pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        self.image_label.setText("") #clear Text
        
        """

    def update_scaled_pixmap(self):
        if not self.current_pixmap or self.current_pixmap.isNull():
            return

        self.graphics_view.resetTransform()
        self.graphics_view.scale(self.zoom_factor, self.zoom_factor)
        self.graphics_view.centerOn(self.pixmap_item)

    def update_image(self, slice_index: int):
        """Update the displayed slice"""
        if self.dicom_slices is None:
            return

        self.pan_offset = (0, 0)
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
            self.update_scaled_pixmap()
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

    def mousePressEvent(self, event):
        #right button for windowing
        if event.button() == Qt.MouseButton.RightButton:
            self._mouse_pressed = True
            self._last_mouse_pos = event.position()
            self._start_window_center = self.window_center
            self._start_window_width = self.window_width

         #left button for panning
        elif event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = True
            self.pan_start_pos = event.position()


    def mouseMoveEvent(self, event):
        if self._mouse_pressed:
            delta = event.position() - self._last_mouse_pos
            dx = delta.x()
            dy = delta.y()

            new_center = self._start_window_center + int(dy)
            new_width = self._start_window_width + int(dx)

            new_width = max(1, new_width) #to avoid division by zero

            self.update_windowing(new_center, new_width)

        elif self.is_panning and self.pan_start_pos:
            delta = event.position() - self.pan_start_pos
            self.pan_start_pos = event.position()
            self.translate(delta.x(), delta.y())


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._mouse_pressed = False
            self._last_mouse_pos = None
        elif event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = False

    def keyPressEvent(self, event):
        key = event.key()
        #print(f"key pressed: {key}")
        name = self.window_keys.get(key)
        #print(f"name {name}")
        if name:
            self.apply_window_preset(name)

        if key == Qt.Key.Key_P:
            self.toggle_cine_loop()


    def save_current_slice(self, filepath: str):
        """Saves the current pixmap (from image_display) to a file
         :param filepath: Full file path including extension (e.g., 'output.png' or 'output.jpg')
         """
        if self.current_pixmap is not None:
            success = self.current_pixmap.save(filepath)
            if not success:
                print(f"Failed to save image to {filepath}")
            else:
                print(f"Image saved to {filepath}")

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

    def normalize_to_uint8(self, image):
        img = np.clip(image, np.min(image), np.max(image))
        img = (img-img.min()) / (img.max() - img.min()) * 255
        return  img.astype(np.uint8)

    def export_as_mp4(self, file_path):
        print("Starting export_as_mp4")

        if self.dicom_slices is None:
            print("No dicom_slices loaded")
            return

        if not file_path.lower().endswith(".mp4"):
            file_path += ".mp4"

        print(f"Saving to: {file_path}")
        print(f"cine_interval: {self.cine_interval}")

        height, width = self.dicom_slices[0].shape
        fps = 1000 // self.cine_interval if self.cine_interval > 0 else 10
        print(f"Video dimensions: {width}x{height}, FPS: {fps}")

        import cv2  # <- make sure OpenCV is imported at the top

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(file_path, fourcc, fps, (width, height))

        for i in range(self.dicom_slices.shape[0]):
            img = self.apply_windowing(self.dicom_slices[i])
            frame = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            writer.write(frame)

        writer.release()
        print(f"Export complete: {file_path}")





