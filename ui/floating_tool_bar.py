from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QPoint
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QDockWidget, QProgressDialog, QMessageBox, QLabel,QFrame, QHBoxLayout, QPushButton
from ui.controls import DicomControls

class FloatingControlsWindow(QWidget):
    def __init__(self, viewer_widget, windowing_manager, parent=None):
        super().__init__(parent)
        # Set window flags for a frameless window that stays on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # If you want to use rgba colors
        self.offset = QPoint() # To store mouse press offset for dragging

        # Main frame for styling (background, border, shadow)
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("FloatingControlsFrame") # For CSS styling
        self.main_frame.setLayout(QVBoxLayout())
        self.main_frame.layout().setContentsMargins(0, 0, 0, 0) # No margins inside frame initially

        # Custom Title Bar
        title_bar = QWidget(self.main_frame)
        title_bar.setObjectName("FloatingTitleBar") # For CSS styling
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 5, 5, 5) # Padding for title bar

        self.title_label = QLabel("DICOM Controls")
        self.title_label.setObjectName("titleLabel") # For CSS styling
        title_bar_layout.addWidget(self.title_label)
        title_bar_layout.addStretch()

        close_button = QPushButton("x") # Simple 'x' for close, could be an icon
        close_button.setObjectName("FloatingCloseButton") # For CSS styling
        close_button.clicked.connect(self.hide)
        close_button.setFixedSize(20, 20) # Fixed size for the circular button
        title_bar_layout.addWidget(close_button)

        # Set up the layout and add DicomControls
        self.controls = DicomControls(viewer_widget, windowing_manager)

        self.main_frame.layout().addWidget(title_bar)
        self.main_frame.layout().addWidget(self.controls)

        # Main layout for the window itself
        window_layout = QVBoxLayout(self)
        window_layout.addWidget(self.main_frame)
        window_layout.setContentsMargins(0, 0, 0, 0) # Remove default window margins

        # Apply dark theme to this floating window -> global stylesheet
        #self.setStyleSheet(dark_theme())


    # --- Custom Dragging Implementation ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if click is on the title bar
            if self.childAt(event.pos()) == self.title_label or self.childAt(event.pos()) == self.main_frame.findChild(QWidget, "FloatingTitleBar"):
                self.offset = event.globalPosition().toPoint() - self.pos()
                event.accept()
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.offset is not None:
            self.move(event.globalPosition().toPoint() - self.offset)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)