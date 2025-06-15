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
from ui.stylesheets import dark_theme
from ui.menu_builder import (
    _build_file_menu,
    _build_windowing_menu,
    _build_ai_menu,
    _build_view_menu,
    _build_help_menu,
)
from dicom.dicom_loader_thread import start_dicom_loader


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

        #set dark theme
        self.setStyleSheet(dark_theme())

    def setup_central_layout(self):
        """Creates a central widget with layout for viewer and controls"""
        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.viewer_widget)
        layout.addWidget(self.controls)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def setupMenuBar(self):
        """Creates the Menu Bar with the functions defined in 'menu_builder.py'"""
        menu = self.menuBar()

        #Build File Menu, #Windowing Menu, # AI Menu, View Menu, Help Menu
        _build_file_menu(self, menu)
        _build_windowing_menu(self, menu)
        _build_ai_menu(self, menu)
        _build_view_menu(self, menu)
        _build_help_menu(self, menu)


    def open_dicom_file_func(self):

        print("open DICOM file clicked")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm);;All Files (*)")
        print(file_path)
        if file_path:
            print(f"open: {file_path}")

            folder = os.path.dirname(file_path)

            self.viewer_widget.show_loading_animation()

            self.dicom_thread, self.dicom_loader = start_dicom_loader(
                folder,
                self.reader,
                self._on_dicom_loading_finished,
                self._on_dicom_loading_error
            )


    def save_current_slice_as_image(self):
        print("Save as clicked")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (.bmp);;All Files (*)")

        if file_path:
            self.viewer_widget.save_current_slice(file_path)
        else:
            print("Save cancelled")

    def save_as_mp4(self):
        print("save as mp4 clicked")
        file_path, _ = QFileDialog.getSaveFileName(self, "Export as MP4", "", "MP4 Video (*.mp4)")

        if file_path:
            try:
                self.viewer_widget.export_as_mp4(file_path)
                print("MP4 export completed successfully.")
            except Exception as e:
                print(f"MP4 export failed: {e}")
        else:
            print("Save cancelled")

    def load_ai_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Load AI Model", "", "Model Files (*.h5 *pth *pkl *onnx *pb *tflite *keras *joblib *pmml);;All Files (*)")
        if model_path:
            print(f"loading following model: {model_path}")

    def close_application(self):
        self.close()

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




