from PyQt6.QtCore import QThread

def start_nifti_loader(file_path, reader, on_finished, on_error):

    from src.image_data_handling.NIfTI_loader import NiftiLoader

    nifti_thread = QThread()
    nifti_loader = NiftiLoader(file_path, reader)
    nifti_loader.moveToThread(nifti_thread)

    nifti_thread.started.connect(nifti_loader.run)
    nifti_loader.finished.connect(on_finished)
    nifti_loader.error.connect(on_error)

    nifti_loader.finished.connect(nifti_thread.quit)
    nifti_loader.error.connect(nifti_thread.quit)

    nifti_thread.finished.connect(nifti_loader.deleteLater)
    nifti_thread.finished.connect(nifti_thread.deleteLater)

    nifti_thread.start()

    return nifti_thread, nifti_loader
