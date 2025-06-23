from PyQt6.QtWidgets import (
    QWidget, QApplication, QStackedLayout,
    QGraphicsScene, QGraphicsPixmapItem
)
from PyQt6.QtCore import Qt, QPointF, QThread
from PyQt6.QtGui import QPixmap, QImage, QPen, QColor, QFont

import numpy as np
import os
from AI.SAM.sam_worker import SAMWorker, SAMWorkerRunner
from image_data_handling.logic.mask_utils import overlay_mask, ensure_rgb
from AI.SAM.sam_controller import SAMController
from AI.SAM.sam_segmenter import SAMSegmenter
from controllers.cine_loop_controller import CineController
from ui.graphics_view import CustomGraphicsView, InteractionMode
from image_data_handling.data_manager import VolumeDataManager
from ui.loading_widget import LoadingWidget
from ui.toast_api import toast

class ViewerWidget(QWidget):
    def __init__(self, data_manager: VolumeDataManager = None, windowing_manager = None):
        super().__init__()

        self.sam = SAMSegmenter()
        self.show_mask_overlay = False

        self.data_manager = data_manager
        self.windowing_manager = windowing_manager
        self.sam_runner = None

        self.sam_controller = SAMController(self.sam, self.data_manager)

        self.graphics_view = CustomGraphicsView(self)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.mask_overlay_item = QGraphicsPixmapItem()
        self.scene.addItem(self.mask_overlay_item)
        self.mask_overlay_item.setZValue(1) # Draw on top of base image

        self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        #disable scrollbars so the image doesn't shift on wheel events

        # set focus so key events get detected
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        # Calculate the base directory relative to where this script (loading_widget.py) is
        # Go up one directory (from 'ui' to 'dicomViewer')
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        # Construct the full path to the GIF using os.path.join
        gif_path = os.path.join(base_dir, "assets", "animations", "Ripple@1x-1.0s-200px-200px.gif")

        self.loading_widget = LoadingWidget(gif_path)

        # --- Main Layout using QStackedLayout ---
        self.main_stacked_layout = QStackedLayout()
        self.main_stacked_layout.addWidget(self.graphics_view)  # use the QGraphicsView itself
        self.main_stacked_layout.addWidget(self.loading_widget)  # Index 1: Loading animation

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

        self.cine_controller = CineController(self.next_frame)

        self.window_keys = {
            Qt.Key.Key_1: "Brain",
            Qt.Key.Key_2: "Lungs",
            Qt.Key.Key_3: "Soft tissues",
            Qt.Key.Key_4: "Bone"
        }

        self.graphics_view.clicked_in_sam_mode.connect(self.on_sam_click)
        self.overlay = None

        #Measure
        self.line_item = None
        self.text_item = None

        self.graphics_view.send_measurement_points.connect(self.on_measure)

        self.measurement_items = []

        self.show_mask_overlay_mode = False

    def resizeEvent(self, event):
        # When the viewer resizes, ensure the image fits properly
        if self.current_pixmap and not self.current_pixmap.isNull():
            self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)

    def load_volume_series(self, volume_data: np.ndarray):
        """Takes a 3D NumPy array and sets up the viewer."""
        self.dicom_slices = volume_data
        if self.data_manager:
            self.data_manager.volume_data = volume_data
            self.data_manager.slice_measurements = {} #clerar measurements form series before
        self.current_slice_index = 0
        #self.update_image(self.current_slice_index) #-> the image gets updated (and therefore windowed) when loading initially from the main Window
        self.delete_all_measurements()

    def display_image(self, image_data):
        """
           Display a grayscale or RGB image using QImage/QPixmap.
           Accepts:
               - Grayscale: shape (H, W)
               - RGB: shape (H, W, 3), dtype=uint8
           """

        if image_data.ndim ==2: #Grayscale

            height, width = image_data.shape
            bytes_per_line = width
            q_image = QImage(image_data.tobytes(), width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        elif image_data.ndim == 3 and image_data.shape[2] == 3: #RGB
            height, width, _ = image_data.shape
            bytes_per_line = 3 * width
            q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        else:
            raise ValueError("Unsupported image shape for display")

        self.current_pixmap = QPixmap.fromImage(q_image)
        self.pixmap_item.setPixmap(self.current_pixmap)

        self.mask_overlay_item.setPixmap(QPixmap())  # Clear any existing mask
        self.mask_overlay_item.setOffset(self.pixmap_item.offset())
        self.mask_overlay_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)

        self.graphics_view.resetTransform()
        self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.graphics_view.scale(self.zoom_factor, self.zoom_factor)

    def update_image(self, slice_index: int):
        """Update the displayed slice"""
        if self.dicom_slices is None:
            return

        self.current_slice_index = slice_index
        raw_slice_data = self.dicom_slices[slice_index]

        if self.data_manager and self.data_manager.current_data_type == "dicom":
            if self.data_manager and self.data_manager.original_dicom_headers:
                modality_slice_data = self.data_manager.apply_rescale_internal(slice_index)
            else:
                # Fallback if no headers or data_manager is set
                modality_slice_data = raw_slice_data
                toast("Warning: No DICOM headers available for display rescale. Displaying raw data.")
        elif self.data_manager and self.data_manager.current_data_type == "nifti":
            modality_slice_data = raw_slice_data #as get_fdata() already scales the data
        else:
            modality_slice_data = raw_slice_data #for Images (png/jpg) or as fallback if not dcm and not nifti

        processed = self.windowing_manager.apply(modality_slice_data, self.window_width, self.window_center)

        if self.show_mask_overlay and self.data_manager.mask_data is not None:
            mask = self.data_manager.mask_data[self.current_slice_index]
            if np.any(mask):  # mask exists for this slice
                self.display_mask_overlay()
            else:
                self.display_image(processed)
        else:
            self.display_image(processed)

        self.update_measurements_on_scene()

        # IMPORTANT: When the image is updated by non-slider means (e.g., cine loop, key press, wheel event),
        # we update the slider's value directly. The slider's valueChanged signal will then trigger
        # the DicomControls label update.
        if self.slice_slider and self.slice_slider.value() != slice_index:
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

    def apply_window_preset(self, preset_name):
        preset = self.windowing_manager.get_preset(preset_name)
        if preset:
            ww, wl = preset
            self.window_width = ww
            self.window_center = wl
            self.width_slider.setValue(ww)
            self.center_slider.setValue(wl)
            self.update_image(self.current_slice_index)

    def get_current_window(self):
        toast(f"width: {self.window_width}, level: {self.window_center}")

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

        if key == Qt.Key.Key_O:
            # Toggle mask mode
            self.show_mask_overlay = not self.show_mask_overlay
            self.update_image(self.current_slice_index)  # Refresh current view
            toast(f"Mask overlay {'enabled' if self.show_mask_overlay else 'disabled'}")

        if key == Qt.Key.Key_M:
            self.enable_measure(not self.graphics_view._mode == InteractionMode.MEASURE)

        super().keyPressEvent(event)

####################################################### Loading animation
    def hide_loading_animation(self):
        self.loading_widget.stop()
        self.main_stacked_layout.setCurrentWidget(self.graphics_view)

    def show_loading_animation(self):
        self.loading_widget.start()
        self.main_stacked_layout.setCurrentWidget(self.loading_widget)


##################################################### Cine loop functions
    def toggle_cine_loop(self):
        self.cine_controller.toggle()

    def next_frame(self):
        if self.dicom_slices is None:
            return
        self.current_slice_index = (self.current_slice_index + 1) % self.dicom_slices.shape[0]
        self.update_image(self.current_slice_index)

    def increase_cine_speed(self):
        self.cine_controller.increase_speed()

    def decrease_cine_speed(self):
        self.cine_controller.decrease_speed()

####################### SAM


    def on_sam_click(self, scene_pos:QPointF):
        #print(f"Handling SAM click at: {scene_pos.x()}, {scene_pos.y()}")
        x = int(scene_pos.x())
        y = int(scene_pos.y())

        #self.graphics_view.setCursor(Qt.CursorShape.BusyCursor)
        QApplication.processEvents()

        # Get the current image
        image_np = self.dicom_slices[self.current_slice_index]

        self.sam_runner = SAMWorkerRunner(
            sam_controller=self.sam_controller,
            image_np=image_np, click_point=(x,y),
            slice_index=self.current_slice_index,
            on_sam_finished=self.on_sam_finished,
            on_sam_error=self.on_sam_error)
        self.sam_runner.start()

    def enable_sam(self, enabled:bool):
        if enabled:
            toast("SAM enabled. Choose a something to segment.")
            #print("sam enabled!")
            self.graphics_view.set_interaction_mode(InteractionMode.SAM)

    def toggle_mask_overlay(self):

        if self.data_manager.mask_data is None or np.max(self.data_manager.mask_data[self.current_slice_index]) == 0:
            toast("No mask for current slice")
            self.update_image(self.current_slice_index)
            return

        self.show_mask_overlay = not self.show_mask_overlay
        if self.show_mask_overlay:
            self.display_mask_overlay()
        else:
            #print("not showing overlay/ showing normal image")
            self.update_image(self.current_slice_index)

    def display_mask_overlay(self):
        # print("showing overlay")
        raw_image = self.data_manager.volume_data[self.current_slice_index]
        windowed_image = self.windowing_manager.apply(raw_image, self.window_width, self.window_center)

        mask = self.data_manager.mask_data[self.current_slice_index]
        image_rgb = ensure_rgb(windowed_image)  # Or however you convert grayscale to RGB
        overlay = overlay_mask(image_rgb, mask)
        self.display_image(overlay)

    def on_sam_finished(self):
            self.toggle_mask_overlay()
            #self.graphics_view.setCursor(Qt.CursorShape.ArrowCursor)

    def on_sam_error(self, error_message: str):
        toast(f"Error during SAM processing: {error_message}")
        #self.graphics_view.setCursor(Qt.CursorShape.ArrowCursor)

####################### Measure

    def enable_measure(self, checked:bool = False):
        if not checked:
            self.graphics_view.set_interaction_mode(InteractionMode.NONE)
        else:
            self.graphics_view.set_interaction_mode(InteractionMode.MEASURE)

    def on_measure(self, p1:QPointF, p2:QPointF):
        #print(f"point 1: {p1}, point 2: {p2}")
        self.data_manager.add_measurement(self.current_slice_index, p1, p2)
        self.update_measurements_on_scene()

    def update_measurements_on_scene(self):
        # Remove old items
        for item in getattr(self, 'measurement_items', []):
            self.scene.removeItem(item)
        self.measurement_items = []

        measurements = self.data_manager.get_measurements(self.current_slice_index)
        if not measurements:
            return

        pixel_spacing = self.data_manager.pixel_spacing or [1.0, 1.0]
        font = QFont("Helvetica Neue")
        font.setPointSize(10)
        font.setWeight(QFont.Weight.Medium)
        pen = QPen(QColor(0, 122, 255, 200))
        pen.setWidthF(1.5)
        pen.setCosmetic(True)

        for p1, p2 in measurements:
            dy = (p2.y() - p1.y()) * pixel_spacing[0]
            dx = (p2.x() - p1.x()) * pixel_spacing[1]
            distance = np.sqrt(dx ** 2 + dy ** 2)

            line = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
            mid_x = (p1.x() + p2.x()) / 2
            mid_y = (p1.y() + p2.y()) / 2
            text = self.scene.addText(f"{distance:.2f} mm", font)
            text.setDefaultTextColor(QColor(255, 255, 255))
            text.setPos(mid_x + 5, mid_y + 5)

            self.measurement_items.extend([line, text])

    def delete_all_measurements(self):
        # Clear existing measurement visuals
        for item in getattr(self, 'measurement_items', []):
            self.scene.removeItem(item)
        self.measurement_items = []

        self.data_manager.slice_measurements = {}


