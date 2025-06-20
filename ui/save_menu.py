import pydicom.data
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget,
    QDockWidget, QProgressDialog, QMessageBox, QLabel, QDialog,
    QComboBox, QPushButton, QLineEdit, QHBoxLayout, QFormLayout
)
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QMovie
import sys
import numpy as np
import os

from dicom.NIfTI_loader_thread import start_nifti_loader
from ui.floating_tool_bar import FloatingControlsWindow
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
    _build_tools_menu,
    _build_help_menu

)
from dicom.dicom_loader_thread import start_dicom_loader
from dicom.NIfTI_reader import NIfTIReader
from dicom.data_manager import DataSaver

class SaveDialog(QDialog):

    #Signal emitted when the user clicks "Save"
    save_requested = pyqtSignal(str, str) #format, file_path

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Save Data")
        self.setGeometry(200,200,400,200) # (Xpos, Ypos, width, height)
        self.setMinimumSize(400, 200)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        self.init_ui()

    def init_ui(self):
        # Main layout for the dialog
        main_layout = QVBoxLayout(self)

        # form layout for labels and input fields
        form_layout = QFormLayout()

        # 1. Format selection
        self.format_label = QLabel("Select Format:")
        self.format_combo = QComboBox()
        #Add formats
        self.format_combo.addItem("PNG/JPG Image", "image")
        self.format_combo.addItem("MP4 Video", "mp4")
        self.format_combo.addItem("DICOM Series", "dicom")
        self.format_combo.addItem("NIfTI File", "nifti")
        self.format_combo.currentIndexChanged.connect(self.update_file_path_placeholder)
        form_layout.addRow(self.format_label, self.format_combo)

        # 2. File Path selection
        self.path_label = QLabel("Save Location")
        self.path_line_edit = QLineEdit()
        self.path_line_edit.setPlaceholderText("Select a folder or file path...")
        self.path_line_edit.setReadOnly(True) #-> only browse button can change it

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_save_location)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_line_edit)
        path_layout.addWidget(self.browse_button)
        form_layout.addRow(self.path_label, path_layout)

        main_layout.addLayout(form_layout)

        # Buttons (Save, Cancel)
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept_save)
        self.save_button.setEnabled(False) # disable until a path is selected

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch(1) #pushes buttons to the right
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        self.update_file_path_placeholder()

    def update_file_path_placeholder(self):
        # Update the placeholder text based on the selected format
        selected_format_data = self.format_combo.currentData()
        if selected_format_data == "dicom":
            self.path_line_edit.setPlaceholderText("Select a directory for DICOM series...")
            self.path_line_edit.setText("")  # Clear existing path as it's a directory
        else:
            self.path_line_edit.setPlaceholderText("Select a file path...")
            # If current text is a directory, clear it for file formats
            if not os.path.isfile(self.path_line_edit.text()) and not self.path_line_edit.text().endswith(
                    (".png", ".jpg", ".mp4", ".nii", ".nii.gz")):
                self.path_line_edit.setText("")
        self.save_button.setEnabled(bool(self.path_line_edit.text()))  # Re-evaluate save button state

    def browse_save_location(self):
        selected_format_data = self.format_combo.currentData()
        file_path = ""

        if selected_format_data == "dicom":
            # For DICOM, get a directory
            directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save DICOM Series")
            if directory:
                file_path = directory
        elif selected_format_data == "image":
            # For PNG/JPG, get a file name
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Image As", "",
                "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (*.bmp);;All Files (*)"
            )
        elif selected_format_data == "mp4":
            # For MP4, get a file name
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export as MP4", "", "MP4 Video (*.mp4);;All Files (*)"
            )
        elif selected_format_data == "nifti":
            # For NIfTI, get a file name
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save as NIfTI", "",
                "NIfTI (*.nii);;NIfTI GZ (*.nii.gz);;All Files (*)"
            )

        if file_path:
            self.path_line_edit.setText(file_path)
            self.save_button.setEnabled(True)
        else:
            self.path_line_edit.setText("")
            self.save_button.setEnabled(False)

    def accept_save(self):
        # Emit the signal with selected format and path
        selected_format = self.format_combo.currentData()
        file_path = self.path_line_edit.text()

        if file_path:
            self.save_requested.emit(selected_format, file_path)
            self.accept()  # Close the dialog
        else:
            QMessageBox.warning(self, "No Save Location", "Please select a save location.")







