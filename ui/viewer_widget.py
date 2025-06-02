from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_label = QLabel()
        #self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.image_label.setScaledContents(True)

        self.image_label.setScaledContents(False)  # Let you control the scaling manually
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.image_label.setText("No file selected")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.current_pixmap = None
        self.original_image_data = None
        self.window_level = 0
        self.window_width = 0

    def resizeEvent(self, event):
        if hasattr(self, "current_pixmap") and self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)




    def display_image(self, image_data_2d):
        """receives 2D array of type np.uint8 and displays it"""
        #print(image_data_2d)

        self.original_image_data = image_data_2d.copy()

        display_image = image_data_2d

        height, width = image_data_2d.shape
        bytes_per_line = width

        q_image = QImage(display_image.tobytes(), width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        self.current_pixmap = QPixmap.fromImage(q_image)
        #self.image_label.setPixmap(self.current_pixmap)
        scaled_pixmap = self.current_pixmap.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        self.image_label.setText("") #clear Text


