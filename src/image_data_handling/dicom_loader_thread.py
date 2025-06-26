from PyQt6.QtCore import QThread

def start_dicom_loader(folder, reader, on_finished, on_error):

    from src.image_data_handling.dicom_loader import DicomLoader

    dicom_thread = QThread()
    dicom_loader = DicomLoader(folder, reader)
    dicom_loader.moveToThread(dicom_thread)

    dicom_thread.started.connect(dicom_loader.run)
    dicom_loader.finished.connect(on_finished)
    dicom_loader.error.connect(on_error)

    dicom_loader.finished.connect(dicom_thread.quit)
    dicom_loader.error.connect(dicom_thread.quit)

    dicom_thread.finished.connect(dicom_loader.deleteLater)
    dicom_thread.finished.connect(dicom_thread.deleteLater)

    dicom_thread.start()

    return dicom_thread, dicom_loader
