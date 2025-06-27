from PyQt6.QtCore import QObject, pyqtSignal

class DicomLoader(QObject):
    finished = pyqtSignal(object, int, int, dict, list) # Signal for success
    error = pyqtSignal(str) # Signal for failure

    def __init__(self, folder, reader):
        super().__init__()
        self.folder = folder
        self.reader = reader

    def run(self):
        try:
            volume, default_center, default_width, metadata_dict, original_dicom_headers = self.reader.read_dicom_series(self.folder)
            self.finished.emit(volume, default_center, default_width, metadata_dict, original_dicom_headers)
        except Exception as e:
            self.error.emit(str(e))