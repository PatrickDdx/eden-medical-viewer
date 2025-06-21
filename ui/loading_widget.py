from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QApplication, QStackedLayout, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QTimer, QStandardPaths, QDir
from PyQt6.QtGui import QPixmap, QImage, QMovie, QPainter
import os

class LoadingWidget(QWidget):
    def __init__(self, gif_path= None, parent=None):
        super().__init__(parent)
        self.gif_path = gif_path
        self.loading_movie = None
        self._setup_ui()

    def _setup_ui(self):
        #Animation label
        self.loading_animation_label = QLabel(self)
        self.loading_animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.loading_movie = QMovie(self.gif_path)  # Adjust path as needed
        if self.loading_movie.isValid():
            self.loading_animation_label.setMovie(self.loading_movie)
        else:
            print("Warning: Loading GIF not found or invalid. Using text placeholder.")
            self.loading_animation_label.setText("Loading...")
            self.loading_animation_label.setStyleSheet("color: white;")  # Example style

        # Add a placeholder label for loading text
        self.loading_text_label = QLabel("Loading DICOM files, please wait...", self)
        self.loading_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_text_label.setStyleSheet("color: white;")

        loading_layout = QVBoxLayout()
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(self.loading_animation_label)
        loading_layout.addWidget(self.loading_text_label)
        self.setLayout(loading_layout)

    def start(self):
        """Start the loading animation (if valid)."""
        if self.loading_movie and self.loading_movie.isValid():
            self.loading_movie.start()

    def stop(self):
        """Stop the loading animation (if running)."""
        if self.loading_movie and self.loading_movie.isValid():
            self.loading_movie.stop()
