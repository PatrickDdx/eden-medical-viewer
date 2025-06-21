from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QDockWidget, QProgressDialog, QMessageBox, QLabel

import os

from image_data_handling.NIfTI_loader_thread import start_nifti_loader
from image_data_handling.windowing_manager import WindowingManager
from ui.floating_tool_bar import FloatingControlsWindow
from ui.metadata_widget import DicomMetadataViewer
from ui.save_menu import SaveDialog
from ui.viewer_widget import ViewerWidget
from image_data_handling.dicom_reader import DicomReader
from ui.menu_builder import (
    _build_file_menu,
    _build_windowing_menu,
    _build_ai_menu,
    _build_view_menu,
    _build_tools_menu,
    _build_help_menu

)
from image_data_handling.dicom_loader_thread import start_dicom_loader
from image_data_handling.NIfTI_reader import NIfTIReader
from image_data_handling.data_manager import VolumeDataManager


class UIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EDEN")
        self.setGeometry(110, 62, 800, 600)  # (Xpos, Ypos, width, height)
        self.setMinimumSize(800, 600)

        self.reader_dicom = DicomReader()
        self.reader_nifti = NIfTIReader()

        self.data_manager = VolumeDataManager()
        self.windowing_manager = WindowingManager()

        self.viewer_widget = ViewerWidget(data_manager = self.data_manager, windowing_manager=self.windowing_manager)

        self.floating_controls_window = FloatingControlsWindow(self.viewer_widget, self.windowing_manager)
        # Ensure the viewer widget in the main window gets the sliders from the floating controls
        # We need to access the controls instance inside the floating window
        self.viewer_widget.set_slider(self.floating_controls_window.controls.slider,
                                      center_slider=self.floating_controls_window.controls.center_slider,
                                      width_slider=self.floating_controls_window.controls.width_slider
                                      )
        self.floating_controls_window.show()
        self.update_floating_window_position()

        self.setup_central_layout()

        self.setupMenuBar()

        self.metadata_viewer = DicomMetadataViewer()
        self.metadata_dock = QDockWidget("DICOM Metadata", self)
        self.metadata_dock.setWidget(self.metadata_viewer)
        self.metadata_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.metadata_dock)

        self.original_dicom_headers = None
        self.nifti_affine_matrix = None

    def resizeEvent(self, event):
        """Override resize event to reposition floating window."""
        super().resizeEvent(event)
        self.update_floating_window_position()

    def closeEvent(self, event):
        """Called when the main window is about to close
        Ensures the floating control window is also closed"""
        if self.floating_controls_window:
            self.floating_controls_window.close()
        super().closeEvent(event)

    def moveEvent(self, event):
        super().moveEvent(event)
        self.update_floating_window_position()

    def update_floating_window_position(self):
        if self.floating_controls_window:
            main_window_rect = self.geometry()
            floating_window_width = self.floating_controls_window.width()
            floating_window_height = self.floating_controls_window.height()

            # Target X: main window's right edge - floating window's width - small margin
            # Target Y: main window's top edge + small margin
            target_x = main_window_rect.right() - floating_window_width - int(main_window_rect.width()*0.15)
            target_y = main_window_rect.bottom() - floating_window_height - int(main_window_rect.height()*0.1)  # Below menu bar
            self.floating_controls_window.move(target_x, target_y)

    def setup_central_layout(self):
        """Creates a central widget with layout for viewer and controls"""
        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.viewer_widget)

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
        _build_tools_menu(self, menu)
        _build_help_menu(self, menu)

    def toggle_floating_controls(self, checked):
        """Makes the floating control window visible"""
        self.floating_controls_window.setVisible(checked)
        print(f"Floating controls visibility toggled to {checked}")

    def open_dicom_file_func(self):
        """Open a DICOM file via QFileDialog and start threaded loading"""
        print("open DICOM file clicked")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm);;All Files (*)")
        print(file_path)
        if file_path:
            print(f"open: {file_path}")

            folder = os.path.dirname(file_path)

            self.viewer_widget.show_loading_animation()

            self.dicom_thread, self.dicom_loader = start_dicom_loader(
                folder,
                self.reader_dicom,
                self._on_dicom_loading_finished,
                self._on_volume_loading_error
            )

    def open_nifti_func(self):
        """Open a NIfTI file via QFileDialog and start threaded loading"""
        print("open NIfTI file clicked")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open NIfTI File", "", "NIfTI Files (*.nii);;All Files (*)")
        print(file_path)
        if file_path:
            print(f"open: {file_path}")

            self.viewer_widget.show_loading_animation()

            self.nifti_thread, self.nifti_loader = start_nifti_loader(
                file_path,
                self.reader_nifti,
                self._on_nifti_loading_finished,
                self._on_volume_loading_error
            )

    def save_current_slice_as_image(self, file_path = None):
        """Saves the current slice via the QFileDialog"""
        print("Save as clicked")
        #file_path, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (.bmp);;All Files (*)")

        if file_path:
            self.viewer_widget.save_current_slice_ui(file_path)
        else:
            print("Save cancelled")

    def save_as_dicom(self, directory = None):
        """Saves the current DICOM via the QFileDialog"""
        print("Save dicom clicked")
        if self.data_manager.volume_data is None:
            print("No Data")
            return
        if self.original_dicom_headers is None or not self.original_dicom_headers:
            print("Missing Data: header")
            return

        #directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save DICOM Series")

        if directory:
            self.viewer_widget.save_as_dicom_ui(directory)
        else:
            print("Dicom saving cancelled")

    def save_as_nifti(self, file_path = None):
        """Saves the current NIfTI via the QFileDialog"""
        print("Save nifti clicked")
        #file_path, _ = QFileDialog.getSaveFileName(self, "Save as NIfTI", "",
        #                                           "NIfTI (*.nii);; NIfTI (*.nii.gz);; All Files (*)")

        if file_path:
            self.viewer_widget.save_as_nifti_ui(file_path)
        else:
            print("Save cancelled")

    def save_as_mp4(self, file_path = None):
        """Saves the current image data as MP4 via the QFileDialog"""
        print("save as mp4 clicked")
        #file_path, _ = QFileDialog.getSaveFileName(self, "Export as MP4", "", "MP4 Video (*.mp4)")

        if file_path:
            try:
                self.viewer_widget.export_as_mp4_ui(file_path)
                print("MP4 export completed successfully.")
            except Exception as e:
                print(f"MP4 export failed: {e}")
        else:
            print("Save cancelled")

    def load_ai_model(self):
        """Loads an AI Model - at least later ;)"""
        model_path, _ = QFileDialog.getOpenFileName(self, "Load AI Model", "", "Model Files (*.h5 *pth *pkl *onnx *pb *tflite *keras *joblib *pmml);;All Files (*)")
        if model_path:
            print(f"loading following model: {model_path}")

    def close_application(self):
        """Closes the application"""
        self.close()

    def _on_dicom_loading_finished(self, volume, center, width, metadata, original_dicom_headers):
        self.original_dicom_headers = original_dicom_headers
        self.data_manager.set_original_dicom_headers(self.original_dicom_headers)
        self._on_volume_loaded(volume, center, width, metadata)

    def _on_nifti_loading_finished(self, volume, center, width, affine_matrix = None):
        self.nifti_affine_matrix = affine_matrix
        self.data_manager.set_nifti_affine_matrix(self.nifti_affine_matrix)
        self._on_volume_loaded(volume, center, width)

    def _on_volume_loaded(self, volume, default_center, default_width, metadata_dict=None):
        print("DICOM loading finished (UI thread)")
        self.viewer_widget.hide_loading_animation()
        # Re-enable main window interaction
        self.setEnabled(True)

        # Update your UI with the loaded data
        self.viewer_widget.load_dicom_series(volume)
        self.viewer_widget.update_windowing(default_center, default_width)

        if metadata_dict is None:
            metadata_dict = {}
        self.metadata_viewer.display_metadata(metadata_dict)

        #Set the control sliders
        slice_maximum = volume.shape[0] - 1
        self.floating_controls_window.controls.slider.setMaximum(slice_maximum)
        self.floating_controls_window.controls.slice_value_label.setText(f"1/{slice_maximum}")
        self.floating_controls_window.controls.center_slider.setValue(default_center)
        self.floating_controls_window.controls.width_slider.setValue(default_width)

    def _on_volume_loading_error(self, error_message):
        print(f"DICOM loading error (UI thread): {error_message}")
        # Hide and clean up the loading animation
        self.viewer_widget.hide_loading_animation()

        # Re-enable main window interaction
        self.setEnabled(True)

        # Show an error message to the user
        QMessageBox.critical(self, "Loading Error", f"Failed to load DICOM series:\n{error_message}")


    def show_save_dialog(self):
        if self.data_manager.volume_data is None:
            print("No data to save")
            return

        save_dialog = SaveDialog(self)
        save_dialog.save_requested.connect(self.execute_save_action)
        save_dialog.exec()

    def execute_save_action(self, format_type, file_path):
        """Executes the appropriate save function based on dialog selection."""
        print(f"Save requested: Format={format_type}, Path={file_path}")
        if format_type == "image":
            self.save_current_slice_as_image(file_path)
        elif format_type == "mp4":
            self.save_as_mp4(file_path)
        elif format_type == "dicom":
            self.save_as_dicom(file_path)  # For DICOM, file_path is actually a directory
        elif format_type == "nifti":
            self.save_as_nifti(file_path)
        else:
            print(f"Unknown Format. Attempted to save in an unknown format: {format_type}")


