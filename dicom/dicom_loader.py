from PyQt6.QtCore import QObject, pyqtSignal
import os

class DicomLoader(QObject):
    finished = pyqtSignal(object, int, int, dict) # Signal for success
    error = pyqtSignal(str) # Signal for failure

    def __init__(self, folder, reader):
        super().__init__()
        self.folder = folder
        self.reader = reader

    def run(self):
        try:
            volume, default_center, default_width, metadata_dict = self.reader.read_dicom_series(self.folder)
            self.finished.emit(volume, default_center, default_width, metadata_dict)
        except Exception as e:
            self.error.emit(str(e))