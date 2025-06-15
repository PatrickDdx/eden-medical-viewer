from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QStackedLayout, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QLabel
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPixmap, QImage, QMovie, QPainter, QTransform
import numpy as np
import cv2

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setBackgroundBrush(Qt.GlobalColor.black)

        # Disable default scrollbars and drag mode for custom handling
        # disable scrollbars so the image doesn't shift on wheel events
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)  # We will implement our own drag

        self.viewer_widget = parent if isinstance(parent, QWidget) else None # Reference to the parent ViewerWidget

        self._panning = False
        self._pan_start_mouse_pos = QPointF()

        self._windowing = False
        self._window_start_mouse_pos = QPointF()
        self._start_window_center = 0
        self._start_window_width = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._panning = True
            self._pan_start_mouse_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()  # Accept the event to prevent further propagation
        elif event.button() == Qt.MouseButton.RightButton:
            self._windowing = True
            self._window_start_mouse_pos = event.position()
            # Store initial windowing values from the ViewerWidget
            if self.viewer_widget:
                self._start_window_center = self.viewer_widget.window_center
                self._start_window_width = self.viewer_widget.window_width
            self.setCursor(Qt.CursorShape.CrossCursor)  # A cross cursor for windowing
            event.accept()
        else:
            super().mousePressEvent(event)  # Pass other button events to default handler

    def mouseMoveEvent(self, event):
        if self._panning:
            delta = event.position() - self._pan_start_mouse_pos
            # Translate the view, not the item. QGraphicsView handles this by translating its transformation matrix.
            self.translate(delta.x(), delta.y())
            self._pan_start_mouse_pos = event.position()  # Update start position for continuous pan
            event.accept()
        elif self._windowing:
            delta = event.position() - self._window_start_mouse_pos
            dx = delta.x()
            dy = delta.y()

            sensitivity = 1
            # Calculate new window center and width based on mouse movement
            new_center = self._start_window_center + int(dy * sensitivity)  # Adjust sensitivity as needed
            new_width = self._start_window_width + int(dx * sensitivity)  # Adjust sensitivity as needed

            new_width = max(1, new_width)  # Ensure width is at least 1 to avoid division by zero

            if self.viewer_widget:
                self.viewer_widget.update_windowing(new_center, new_width)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            self._windowing = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if self.viewer_widget:
            # Pass the wheel event to the viewer_widget's wheelEvent for slice scrolling/zooming
            self.viewer_widget.wheelEvent(event)
            event.accept()
        else:
            super().wheelEvent(event)