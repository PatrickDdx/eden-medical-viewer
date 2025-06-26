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

class SAMWorkerRunner:
    def __init__(self, sam_controller, image_np, click_point, slice_index, on_sam_finished, on_sam_error):
        # Create thread and worker
        self.sam_thread = QThread()
        self.worker = SAMWorker(
            sam_controller=sam_controller,
            image_np=image_np,
            click_point=click_point,
            slice_index=slice_index
        )
        self.worker.moveToThread(self.sam_thread)

        # Connect signals
        self.sam_thread.started.connect(self.worker.run)
        self.worker.finished.connect(on_sam_finished)
        self.worker.error.connect(on_sam_error)
        self.worker.finished.connect(self.sam_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.sam_thread.finished.connect(self.sam_thread.deleteLater)


    def start(self):
        # Start the thread
        self.sam_thread.start()




