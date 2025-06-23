from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QStackedLayout, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QLabel
from PyQt6.QtCore import Qt, QTimer, QPointF, QPoint, pyqtSignal  # Ensure QPoint is imported
from PyQt6.QtGui import QPixmap, QImage, QMovie, QPainter, QTransform
import numpy as np
import cv2
from enum import Enum
from ui.toast_api import toast

class InteractionMode(Enum):
    NONE = 0
    PAN = 1
    WINDOWING = 2
    SAM = 3
    MEASURE = 4


class CustomGraphicsView(QGraphicsView):
    clicked_in_sam_mode = pyqtSignal(QPointF)  # Signal with the scene coords
    send_measurement_points = pyqtSignal(QPointF, QPointF) #Signal with the two points for measurement

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setBackgroundBrush(Qt.GlobalColor.black)

        # Disable scrollbars to prevent image shifting during zoom/pan
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)  # We will implement our own drag

        self.viewer_widget = parent if isinstance(parent, QWidget) else None # Reference to the parent ViewerWidget

        self._mode = InteractionMode.NONE

        self._pan_start_mouse_pos = QPointF()

        self._window_start_mouse_pos = QPointF()
        self._start_window_center = 0
        self._start_window_width = 0

        self.sensitivity = 1

        self.viewer_widget = parent if isinstance(parent, QWidget) else None  # Reference to the parent ViewerWidget

        # for measuring
        self.start_point = None

    #def enterEvent(self, event):
    #    self.setCursor(Qt.CursorShape.OpenHandCursor)

    #def leaveEvent(self, event):
    #    self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):

        # Always check the current _mode first
        if self._mode == InteractionMode.SAM:
            if event.button() == Qt.MouseButton.LeftButton:
                #print("left click while interaction mode == sam")
                self._mode= InteractionMode.NONE
                pos = event.position().toPoint()
                #print(pos)

                pos_in_scene = self.mapToScene(pos)
                #print(f"Clicked at scene coordinates: x={pos_in_scene.x()}, y={pos_in_scene.y()}")

                self.clicked_in_sam_mode.emit(pos_in_scene)  # Emit signal with coords

                event.accept()
            # In SAM mode, other mouse buttons might do nothing or specific SAM actions
            return  # Don't fall through to other modes


        #Measure
        if self._mode == InteractionMode.MEASURE:
            if event.button() == Qt.MouseButton.LeftButton:
                pos = self.mapToScene(event.position().toPoint())

                if not self.start_point:
                    self.start_point = pos
                    #print(f"start: {self.start_point}")
                else:
                    end_point = pos
                    #self.draw_measurement(self.start_point, end_point)
                    #print(f"end {end_point}")
                    self.send_measurement_points.emit(self.start_point, end_point)
                    self.start_point = None  # Reset for next measurement


                    event.accept()

            elif event.button() == Qt.MouseButton.RightButton and self._mode == InteractionMode.MEASURE:
                self._mode = InteractionMode.NONE
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.start_point = None
                event.accept()
                return

            return

        if event.button() == Qt.MouseButton.LeftButton:
            self._mode = InteractionMode.PAN
            self._pan_start_mouse_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()  # Accept the event to prevent further propagation
        elif event.button() == Qt.MouseButton.RightButton:
            self._mode = InteractionMode.WINDOWING
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
        if self._mode == InteractionMode.PAN:
            delta = event.position() - self._pan_start_mouse_pos
            # Translate the view, not the item. QGraphicsView handles this by translating its transformation matrix.
            self.translate(delta.x(), delta.y())
            self._pan_start_mouse_pos = event.position()  # Update start position for continuous pan
            event.accept()
        elif self._mode == InteractionMode.WINDOWING:
            delta = event.position() - self._window_start_mouse_pos
            dx = delta.x()
            dy = delta.y()

            # Calculate new window center and width based on mouse movement
            new_center = self._start_window_center + int(dx * self.sensitivity)  # Adjust self.sensitivity as needed
            new_width = self._start_window_width + int(dy * self.sensitivity)  # Adjust self.sensitivity as needed

            new_width = max(1, new_width)  # Ensure width is at least 1 to avoid division by zero

            if self.viewer_widget:
                self.viewer_widget.update_windowing(new_center, new_width)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        if self._mode == InteractionMode.MEASURE:
            event.accept()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self._mode = InteractionMode.NONE
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            self._mode = InteractionMode.NONE
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

    def set_interaction_mode(self, mode: InteractionMode):
        """Sets the current interaction mode of the graphics view."""
        # You might want to add logic here to reset cursors or other states
        # when the mode changes.
        if self._mode != mode:
            #print(f"Interaction mode changed from {self._mode.name} to {mode.name}")
            self._mode = mode
            if mode == InteractionMode.SAM:
                self.setCursor(Qt.CursorShape.CrossCursor)  # Or a custom SAM cursor
            elif mode == InteractionMode.MEASURE:
                self.setCursor(Qt.CursorShape.CrossCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)  # Default cursor when not in SAM mode

    def mapToImageCoordinates(self, view_pos: QPoint) -> QPoint:
        """
        Converts a point from view coordinates to image pixel coordinates.

        Args:
            view_pos (QPoint): The point in the QGraphicsView's coordinate system.

        Returns:
            QPoint: The corresponding point in the original image's pixel coordinate system.
                    Returns QPoint(0,0) or handles appropriately if pixmap_item is not set.
        """
        if not self.viewer_widget or not self.viewer_widget.pixmap_item:
            # Handle case where pixmap_item is not available
            toast("Warning: pixmap_item not available for coordinate mapping. Returning (0,0).")
            return QPoint(0, 0)

        # 1. Map from view coordinates to scene coordinates
        scene_pos = self.mapToScene(QPointF(view_pos))

        # 2. Map from scene coordinates to the pixmap item's local coordinates
        # The pixmap item's local coordinates are its pixel coordinates.
        image_coords = self.viewer_widget.pixmap_item.mapFromScene(scene_pos).toPoint()

        # You might want to clamp the coordinates to ensure they are within the image bounds
        # Get image dimensions from the pixmap item
        image_width = self.viewer_widget.pixmap_item.pixmap().width()
        image_height = self.viewer_widget.pixmap_item.pixmap().height()

        x = max(0, min(image_coords.x(), image_width - 1))
        y = max(0, min(image_coords.y(), image_height - 1))

        return QPoint(x, y)

