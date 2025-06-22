import numpy as np
from PyQt6.QtCore import QObject, QThread, pyqtSignal

class SAMWorker(QObject):
    finished = pyqtSignal(np.ndarray, np.ndarray)  # Emits image_rgb, best_mask
    error = pyqtSignal(str)

    def __init__(self, sam_controller, image_np, click_point, slice_index):
        super().__init__()
        self.sam_controller = sam_controller
        self.image_np = image_np
        self.click_point = click_point
        self.slice_index = slice_index

    def run(self):
        try:
            image_rgb, best_mask = self.sam_controller.handle_click(
                self.image_np, self.click_point, self.slice_index
            )
            self.finished.emit(image_rgb, best_mask)
        except Exception as e:
            self.error.emit(str(e))
