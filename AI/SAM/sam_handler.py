
from PyQt6.QtCore import QPointF
import numpy as np
from PyQt6.QtWidgets import QApplication

from image_data_handling.logic.mask_utils import overlay_mask, ensure_rgb
from ui.graphics_view import InteractionMode
from ui.toast_api import toast
from AI.SAM.sam_worker import SAMWorkerRunner
from AI.SAM.sam_controller import SAMController
from AI.SAM.sam_segmenter import SAMSegmenter

class SAMHandler:
    def __init__(self, parent_viewer):
        self.viewer = parent_viewer  # Reference to ViewerWidget
        self.sam = SAMSegmenter()
        self.sam_controller = SAMController(self.sam, self.viewer.data_manager)
        self.sam_runner = None
        self.show_mask_overlay = False

        self.viewer.graphics_view.clicked_in_sam_mode.connect(self.on_sam_click)

    def on_sam_click(self, scene_pos:QPointF):
        # print(f"Handling SAM click at: {scene_pos.x()}, {scene_pos.y()}")
        x = int(scene_pos.x())
        y = int(scene_pos.y())

        # self.graphics_view.setCursor(Qt.CursorShape.BusyCursor)
        QApplication.processEvents()

        # Get the current image
        image_np = self.viewer.dicom_slices[self.viewer.current_slice_index]

        self.sam_runner = SAMWorkerRunner(
            sam_controller=self.sam_controller,
            image_np=image_np,
            click_point=(x, y),
            slice_index=self.viewer.current_slice_index,
            on_sam_finished=self.on_sam_finished,
            on_sam_error=self.on_sam_error
        )
        self.sam_runner.start()

    def enable_sam(self, enabled:bool):
        """Enable SAM interaction mode if enabled is True."""
        if enabled:
            toast("SAM enabled. Choose a something to segment.")
            #print("sam enabled!")
            self.viewer.graphics_view.set_interaction_mode(InteractionMode.SAM)

    def toggle_mask_overlay(self):

        if self.viewer.data_manager.mask_data is None or np.max(self.viewer.data_manager.mask_data[self.viewer.current_slice_index]) == 0:
            toast("No mask for current slice")
            self.viewer.update_image(self.viewer.current_slice_index)
            return

        self.show_mask_overlay = not self.show_mask_overlay
        if self.show_mask_overlay:
            self.display_mask_overlay()
        else:
            self.viewer.update_image(self.viewer.current_slice_index)

    def display_mask_overlay(self):
        raw_image = self.viewer.data_manager.volume_data[self.viewer.current_slice_index]
        windowed_image = self.viewer.windowing_manager.apply(raw_image, self.viewer.window_width, self.viewer.window_center)

        mask = self.viewer.data_manager.mask_data[self.viewer.current_slice_index]
        image_rgb = ensure_rgb(windowed_image)  # Or however you convert grayscale to RGB
        overlay = overlay_mask(image_rgb, mask)
        self.viewer.display_image(overlay)

    def on_sam_finished(self):
        self.toggle_mask_overlay()
        #self.graphics_view.setCursor(Qt.CursorShape.ArrowCursor)

    def on_sam_error(self, error_message: str):
        toast(f"Error during SAM processing: {error_message}")
        #self.graphics_view.setCursor(Qt.CursorShape.ArrowCursor)


