import pydicom.data
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction
import sys
import numpy as np
from ui.viewer_widget import ViewerWidget
from dicom.dicom_reader import DicomReader
from ui.controls import DicomControls


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
        dummy_menu = menu.addMenu("dummy")

        dummy_action = QAction("dummy action", self)
        dummy_action.triggered.connect(self.dummy_func)
        dummy_menu.addAction(dummy_action)

        #----------------------------


        # File Menu
        file_menu = menu.addMenu("File")

        open_action = QAction("Open DICOM", self)
        open_action.triggered.connect(self.open_dicom_file_func)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_as_func)
        file_menu.addAction(save_as_action)

        exit_action = QAction("Exit", self)
        file_menu.addAction(exit_action)

        #V View Menu
        view_menu = menu.addMenu("View")

        # AI Menu
        ai_menu = menu.addMenu("AI")

        load_action = QAction("Load Model", self)
        load_action.triggered.connect(self.load_ai_model)
        ai_menu.addAction(load_action)

        help_menu = menu.addMenu("Help")

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
        if file_path:
            print(f"open: {file_path}")

            import os
            folder = os.path.dirname(file_path)

            try:
                volume, default_center, default_width = self.reader.read_dicom_series(folder)

                self.viewer_widget.load_dicom_series(volume)

                self.controls.slider.setMaximum(volume.shape[0] - 1)
                self.controls.center_slider.setValue(default_center)
                self.controls.width_slider.setValue(default_width)
            except Exception as e:
                print(f"Error loading dicom series:  {e}")




    def save_as_func(self):
        print("Save as clicked")

    def load_ai_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Load AI Model", "", "Model Files (*.h5 *pth *pkl *onnx *pb *tflite *keras *joblib *pmml);;All Files (*)")
        if model_path:
            print(f"loading following model: {model_path}")