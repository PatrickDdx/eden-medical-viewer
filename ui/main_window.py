import pydicom.data
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QDockWidget, QProgressDialog, QMessageBox, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QMovie
import sys
import numpy as np
import os

from ui.metadata_widget import DicomMetadataViewer
from ui.viewer_widget import ViewerWidget
from dicom.dicom_reader import DicomReader
from ui.controls import DicomControls
from dicom.dicom_loader import DicomLoader


class UIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EDEN")
        self.setGeometry(110, 62, 800, 600)  # (Xpos, Ypos, width, height)
        self.setMinimumSize(800, 600)

        self.reader = DicomReader()

        self.viewer_widget = ViewerWidget()
        #self.setCentralWidget(self.viewer_widget)

        self.controls = DicomControls(self.viewer_widget)
        self.viewer_widget.set_slider(self.controls.slider,
                                      center_slider=self.controls.center_slider,
                                      width_slider=self.controls.width_slider
                                      )

        self.setup_central_layout()
        self.setupMenuBar()

        self.metadata_viewer = DicomMetadataViewer()
        self.metadata_dock = QDockWidget("DICOM Metadata", self)
        self.metadata_dock.setWidget(self.metadata_viewer)
        self.metadata_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.metadata_dock)


    def setup_central_layout(self):
        """Creates a central wieget with layout for viewer and controls"""
        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.viewer_widget)
        layout.addWidget(self.controls)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def setupMenuBar(self):
        menu = self.menuBar()

        #---------------------------------
        #creatin a menu dummy:
        """
        dummy_menu = menu.addMenu("dummy")

        test_data = QAction("dummy action", self)
        test_data.triggered.connect(self.dummy_func)
        dummy_menu.addAction(test_data) 
        """

        #----------------------------

        # File Menu
        file_menu = menu.addMenu("File")

        open_action = QAction("Open DICOM", self)
        open_action.triggered.connect(self.open_dicom_file_func)
        file_menu.addAction(open_action)

        #save_action = QAction("Save", self)
        #file_menu.addAction(save_action)

        save_as_action = QAction("Save As Image", self)
        save_as_action.triggered.connect(self.save_current_slice_as_image)
        file_menu.addAction(save_as_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit)
        file_menu.addAction(exit_action)

        #Windowing menu
        window_presets_menu = menu.addMenu("Windowing")

        for name in self.viewer_widget.window_presets:
            action = QAction(name, self)

            action.triggered.connect(lambda checked, n=name: self.viewer_widget.apply_window_preset(n))
            window_presets_menu.addAction(action)

        current_window = QAction("Current Window", self)
        current_window.triggered.connect(self.viewer_widget.get_current_window)
        window_presets_menu.addAction(current_window)

        # AI Menu
        ai_menu = menu.addMenu("AI")

        load_action = QAction("Load Model", self)
        load_action.triggered.connect(self.load_ai_model)
        ai_menu.addAction(load_action)

        help_menu = menu.addMenu("Help")

##################section for testing and prototyping for convenience ##########delete when publishing
        # loda test data
        test_data_menu = menu.addMenu("Test Data")

        load_CT = QAction("CT", self)
        load_CT.triggered.connect(lambda: self.load_test_data("CT"))
        test_data_menu.addAction(load_CT)

        load_MRI = QAction("MRI", self)
        load_MRI.triggered.connect(lambda: self.load_test_data("MRI"))
        test_data_menu.addAction(load_MRI)

    #-------------- Events -----------------------
    def dummy_func(self):
        print("dummy function clicked")

        test_data_path =  pydicom.data.get_testdata_file("CT_small.dcm")
        print(f"file path: {test_data_path}")

        #ds = pydicom.dcmread(test_data_path) # this works

        ds = self.reader.read_dicom_file(test_data_path)

        pixel_data = self.reader.get_pixel_array(ds)

        print(pixel_data.shape)

        self.viewer_widget.display_image(pixel_data)

        print("end of dummy")

    #---------------------
    def open_dicom_file_func(self):
        print("open DICOM file clicked")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm);;All Files (*)")
        print(file_path)
        if file_path:
            print(f"open: {file_path}")

            import os
            folder = os.path.dirname(file_path)

            try:
                volume, default_center, default_width, metadata_dict = self.reader.read_dicom_series(folder)

                self.viewer_widget.load_dicom_series(volume)  # load dicom series
                self.viewer_widget.update_windowing(default_center, default_width)  # apply initial windowing

                self.metadata_viewer.display_metadata(metadata_dict)  # show the metadata

                self.controls.slider.setMaximum(volume.shape[0] - 1)
                self.controls.center_slider.setValue(default_center)
                self.controls.width_slider.setValue(default_width)
            except Exception as e:
                print(f"Error loading dicom series:  {e}")

    def save_current_slice_as_image(self):
        print("Save as clicked")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (.bmp);;All Files (*)")

        if file_path:
            self.viewer_widget.save_current_slice(file_path)
        else:
            print("Save cancelled")

    def load_ai_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Load AI Model", "", "Model Files (*.h5 *pth *pkl *onnx *pb *tflite *keras *joblib *pmml);;All Files (*)")
        if model_path:
            print(f"loading following model: {model_path}")

    def exit(self):
        self.close()

##########################for prototyping/testing ############### delete when publishing
    def load_test_data(self, modality):
        print("loading test data")

        if modality == "CT":
            file_path = "C:/Users/patri/GIT/dicomViewer/assets/CT/series-000001/image-000003.dcm"
        elif modality == "MRI":
            file_path = "C:/Users/patri/GIT/dicomViewer/assets/MRI/Example_MRI_1/image-00001.dcm"
        else:
            return

        import os
        folder = os.path.dirname(file_path)

        self.viewer_widget.show_loading_animation()

        # --- 2. Create QThread and DicomLoader instances ---
        self.dicom_thread = QThread()  # Create a new thread
        self.dicom_loader = DicomLoader(folder, self.reader)  # Your existing loader instance

        # --- 3. Move the DicomLoader to the new thread ---
        self.dicom_loader.moveToThread(self.dicom_thread)

        # --- 4. Connect signals and slots ---
        # When the thread starts, call the loader's run method
        self.dicom_thread.started.connect(self.dicom_loader.run)
        # When the loader finishes, connect to our UI update slot
        self.dicom_loader.finished.connect(self._on_dicom_loading_finished)
        # When an error occurs, connect to our error handling slot
        self.dicom_loader.error.connect(self._on_dicom_loading_error)
        # When the loader finishes or errors, quit and delete the thread
        self.dicom_loader.finished.connect(self.dicom_thread.quit)
        self.dicom_loader.error.connect(self.dicom_thread.quit)
        # Optional: Clean up the worker and thread objects when the thread finishes
        self.dicom_thread.finished.connect(self.dicom_loader.deleteLater)
        self.dicom_thread.finished.connect(self.dicom_thread.deleteLater)

        # --- 5. Start the thread ---
        self.dicom_thread.start()

        # --- Slots for handling thread results (within YourMainViewerClass) ---

    def _on_dicom_loading_finished(self, volume, default_center, default_width, metadata_dict):
        print("DICOM loading finished (UI thread)")
        self.viewer_widget.hide_loading_animation()
        # Re-enable main window interaction
        self.setEnabled(True)

        # Update your UI with the loaded data
        self.viewer_widget.load_dicom_series(volume)
        self.viewer_widget.update_windowing(default_center, default_width)
        self.metadata_viewer.display_metadata(metadata_dict)
        self.controls.slider.setMaximum(volume.shape[0] - 1)
        self.controls.center_slider.setValue(default_center)
        self.controls.width_slider.setValue(default_width)

    def _on_dicom_loading_error(self, error_message):
        print(f"DICOM loading error (UI thread): {error_message}")
        # Hide and clean up the loading animation
        self.viewer_widget.hide_loading_animation()

        # Re-enable main window interaction
        self.setEnabled(True)

        # Show an error message to the user
        QMessageBox.critical(self, "Loading Error", f"Failed to load DICOM series:\n{error_message}")


