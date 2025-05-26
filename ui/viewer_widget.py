from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.current_pixmap = None
        self.original_image_data = None
        self.window_level = 0
        self.window_width = 0


    def display_image(self, image_data_2d):
        """receives 2D array and displays it"""
        print(image_data_2d)

        self.original_image_data = image_data_2d.copy()

        display_image = image_data_2d

        height, width = image_data_2d.shape
        bytes_per_line = width
        q_image = QImage(display_image.tobytes(), width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        self.current_pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(self.current_pixmap)


