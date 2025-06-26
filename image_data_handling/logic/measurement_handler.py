
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPen, QColor, QFont

import numpy as np

from ui.graphics_view import InteractionMode

class MeasurementHandler:
    def __init__(self, viewer):
        self.viewer = viewer  # Reference to ViewerWidget
        self.scene = viewer.scene
        self.graphics_view = viewer.graphics_view
        self.data_manager = viewer.data_manager

        self.measurement_items = []

        self.graphics_view.send_measurement_points.connect(self.on_measure)

    def enable_measure(self, checked:bool = False):
        if not checked:
            self.graphics_view.set_interaction_mode(InteractionMode.NONE)
        else:
            self.graphics_view.set_interaction_mode(InteractionMode.MEASURE)

    def on_measure(self, p1:QPointF, p2:QPointF):
        #print(f"point 1: {p1}, point 2: {p2}")
        self.data_manager.add_measurement(self.viewer.current_slice_index, p1, p2)
        self.update_measurements_on_scene()

    def update_measurements_on_scene(self):
        # Remove old items
        for item in getattr(self, 'measurement_items', []):
            self.scene.removeItem(item)
        self.measurement_items = []

        measurements = self.data_manager.get_measurements(self.viewer.current_slice_index)
        if not measurements:
            return

        pixel_spacing = self.data_manager.pixel_spacing or [1.0, 1.0]

        font = QFont("Helvetica Neue")
        font.setPointSize(10)
        font.setWeight(QFont.Weight.Medium)

        pen = QPen(QColor(0, 122, 255, 200))
        pen.setWidthF(1.5)
        pen.setCosmetic(True)

        for p1, p2 in measurements:
            dy = (p2.y() - p1.y()) * pixel_spacing[0]
            dx = (p2.x() - p1.x()) * pixel_spacing[1]
            distance = np.sqrt(dx ** 2 + dy ** 2)

            line = self.scene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
            mid_x = (p1.x() + p2.x()) / 2
            mid_y = (p1.y() + p2.y()) / 2
            text = self.scene.addText(f"{distance:.2f} mm", font)
            text.setDefaultTextColor(QColor(255, 255, 255))
            text.setPos(mid_x + 5, mid_y + 5)

            self.measurement_items.extend([line, text])

    def delete_all_measurements(self):
        # Clear existing measurement visuals
        for item in getattr(self, 'measurement_items', []):
            self.scene.removeItem(item)
        self.measurement_items = []

        self.data_manager.slice_measurements = {}