from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QWidget, QDockWidget

from my_project.controllers.save_controller import SaveController
from my_project.image_processing.windowing_manager import WindowingManager
from my_project.ui.floating_tool_bar import FloatingControlsWindow
from my_project.ui.metadata_widget import DicomMetadataViewer
from my_project.ui.save_menu import SaveDialog
from my_project.ui.viewer_widget import ViewerWidget
from my_project.data.dicom.dicom_reader import DicomReader
from my_project.ui.menu_builder import (
    _build_file_menu,
    _build_windowing_menu,
    _build_view_menu,
    _build_tools_menu
)
from my_project.controllers.load_controller import LoadController
from my_project.data.nifti.NIfTI_reader import NIfTIReader
from my_project.data.data_manager import VolumeDataManager
from my_project.ui.toast_api import toast, init_toast


class MainWindow(QMainWindow):
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

        self.floating_controls_window = FloatingControlsWindow(self.viewer_widget, self.windowing_manager, parent=self)

        self.viewer_widget.set_slider(self.floating_controls_window.controls.slider,
                                      center_slider=self.floating_controls_window.controls.center_slider,
                                      width_slider=self.floating_controls_window.controls.width_slider
                                      )

        self.metadata_viewer = DicomMetadataViewer()

        self.load_controller = LoadController(self, self.data_manager, self.viewer_widget, self.metadata_viewer)
        self.save_controller = SaveController(self.viewer_widget, self.data_manager)

        self.floating_controls_window.show()
        self.update_floating_window_position()

        self.setup_central_layout()

        self.setupMenuBar()

        self.metadata_dock = QDockWidget("DICOM Metadata", self)
        self.metadata_dock.setWidget(self.metadata_viewer)
        self.metadata_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.metadata_dock)

        init_toast(self)

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

            target_x = main_window_rect.right() - floating_window_width - int(main_window_rect.width()*0.05)
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
        _build_view_menu(self, menu)
        _build_tools_menu(self, menu)

        self.viewer_widget.graphics_view.request_exit_measure_mode.connect(lambda : self.measure_action.setChecked(False))
        self.viewer_widget.request_start_measure_mode.connect(lambda  : self.measure_action.setChecked(True))

    def toggle_floating_controls(self, checked):
        """Toggles the visibility of  the floating control window on/off"""
        self.floating_controls_window.setVisible(not checked == self.floating_controls_window.isVisible())

    def open_dicom_file_func(self):
        """Open a DICOM file via QFileDialog and start threaded loading"""
        self.load_controller.open_dicom_file()

    def open_nifti_func(self):
        """Open a NIfTI file via QFileDialog and start threaded loading"""
        self.load_controller.open_nifti_file()

    def open_image_func(self):
        """Open an image file (.png/.jpg)"""
        self.load_controller.open_image_file()

    def load_ai_model(self):
        """Loads an AI Model - at least later ;)"""
        model_path, _ = QFileDialog.getOpenFileName(self, "Load AI Model", "", "Model Files (*.h5 *pth *pkl *onnx *pb *tflite *keras *joblib *pmml);;All Files (*)")
        if model_path:
            toast(f"Loading following model: {model_path}")

    def close_application(self):
        """Closes the application"""
        self.close()

    def show_save_dialog(self):
        if self.data_manager.volume_data is None:
            toast("No data to save...")
            return

        save_dialog = SaveDialog(self)

        # Calculate the center position
        main_window_center = self.geometry().center()
        save_dialog_size = save_dialog.size()

        # Calculate the top-left corner for the dialog to be centered
        x = main_window_center.x() - save_dialog_size.width() // 2
        y = main_window_center.y() - save_dialog_size.height() // 2

        save_dialog.move(x, y)

        save_dialog.save_requested.connect(self.execute_save_action)
        save_dialog.exec()

    def execute_save_action(self, format_type, file_path):
        """Executes the appropriate save function based on dialog selection."""
        if format_type == "image":
            self.save_controller.save_image(file_path)
        elif format_type == "mp4":
            self.save_controller.save_mp4(file_path)
        elif format_type == "dicom":
            self.save_controller.save_dicom(file_path)  # For DICOM, file_path is actually a directory
        elif format_type == "nifti":
            self.save_controller.save_nifti(file_path)
        elif format_type == "overlay":
            self.save_controller.save_overlay(file_path)
        else:
            toast(f"Unknown Format. Attempted to save in an unknown format: {format_type}")


