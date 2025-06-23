# toast.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QColor, QFont

class Toast(QWidget):
    _instance = None
    _parent_ref = None  # store MainWindow reference

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.label = QLabel("", self)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(50, 50, 50, 180);
                color: white;
                padding: 12px 24px;
                border-radius: 20px;
                font-size: 14pt;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._animation = QPropertyAnimation(self, b"windowOpacity")
        self._animation.setDuration(500)

    @classmethod
    def set_parent(cls, parent):
        cls._parent_ref = parent

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = Toast(parent=cls._parent_ref)
        return cls._instance

    def show_message(self, message: str, duration=3000):
        self.label.setText(message)
        self.adjustSize()

        if self._parent_ref:
            parent_geom = self._parent_ref.geometry()
            x = parent_geom.x() + (parent_geom.width() - self.width()) // 2
            y = parent_geom.y() + (parent_geom.height() - self.height()) // 2
            self.move(x, y)

        self.setWindowOpacity(0.0)
        self.show()

        self._animation.stop()
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.start()

        QTimer.singleShot(duration, self.fade_out)

    def fade_out(self):
        self._animation.stop()
        self._animation.setStartValue(1.0)
        self._animation.setEndValue(0.0)
        self._animation.start()
        QTimer.singleShot(self._animation.duration(), self.hide)
