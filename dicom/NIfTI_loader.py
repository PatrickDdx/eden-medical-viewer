from PyQt6.QtCore import QObject, pyqtSignal
import numpy as np

class NiftiLoader(QObject):
    finished = pyqtSignal(np.ndarray, int, int)
    error = pyqtSignal(str)

    def __init__(self, file_path, reader):
        super().__init__()
        self.file_path = file_path
        self.reader = reader

    def run(self):
        try:
            volume_data = self.reader.open_nifti(self.file_path)
            default_center = int(np.mean(volume_data))
            default_width = int(np.max(volume_data) - np.min(volume_data))
            self.finished.emit(volume_data, default_center, default_width)
        except Exception as e:
            self.error.emit(str(e))