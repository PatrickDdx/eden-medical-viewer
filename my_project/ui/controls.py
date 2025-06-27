from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt

class SliceSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setMinimum(0)
        self.setMaximum(0)
        self.setSingleStep(1)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.setToolTip("Navigate through DICOM slices")

class WindowWidthSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setMinimum(1)
        self.setMaximum(4000)
        self.setSingleStep(10)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.setToolTip("Adjust the window width for contrast")

class WindowCenterSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setMinimum(-1000)
        self.setMaximum(1000)
        self.setValue(0)
        self.setSingleStep(5)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.setToolTip("Adjust the window center for brightness")

class DicomControls(QWidget):
    def __init__(self, canvas, windowing_manager):
        super().__init__()

        self.canvas = canvas #is the viewer Widget that should be controlled with the slider etc.
        self.windowing_manager = windowing_manager
        # Value labels for sliders
        self.slice_value_label = QLabel("0/0")
        self.center_value_label = QLabel("0")
        self.width_value_label = QLabel("1")

        #Label for nearest neighbor (preset window)
        self.nearest_neighbor_label = QLabel("Nearest Window: N/A")
        #self.nearest_neighbor_label.setStyleSheet("font-weight: bold;")

        # slider to change the current slice
        self.slider = SliceSlider()
        self.slider.valueChanged.connect(self.update_image_from_slider)
        self.slider.valueChanged.connect(lambda v: self.slice_value_label.setText(f"{v}/{self.slider.maximum()}"))

        # window center slider
        self.center_slider = WindowCenterSlider()
        self.center_slider.valueChanged.connect(self.update_windowing)
        self.center_slider.valueChanged.connect(lambda v: self.center_value_label.setText(str(v)))

        # window width slider
        self.width_slider = WindowWidthSlider()
        self.width_slider.valueChanged.connect(self.update_windowing)
        self.width_slider.valueChanged.connect(lambda v: self.width_value_label.setText(str(v)))

        # Initial label updates
        self.slice_value_label.setText(f"{self.slider.value()}/{self.slider.maximum()}")
        self.center_value_label.setText(str(self.center_slider.value()))
        self.width_value_label.setText(str(self.width_slider.value()))

        # Layout using QGridLayout for better alignment
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setVerticalSpacing(10)
        grid_layout.setHorizontalSpacing(10)

        # Slice Slider
        grid_layout.addWidget(QLabel("Slice:"), 0, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.slice_value_label, 0, 1, Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.slider, 1, 0, 1, 2)  # Span two columns

        # Window Center Slider
        grid_layout.addWidget(QLabel("Level:"), 2, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.center_value_label, 2, 1, Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.center_slider, 3, 0, 1, 2)

        # Window Width Slider
        grid_layout.addWidget(QLabel("Width:"), 4, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.width_value_label, 4, 1, Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.width_slider, 5, 0, 1, 2)

        grid_layout.addWidget(self.nearest_neighbor_label, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(grid_layout)

        self.update_nearest_neighbor_display()

    def update_image_from_slider(self, value):
        if self.canvas:
            self.canvas.update_image(value)

    def update_windowing(self):
        new_center = self.center_slider.value()
        new_width = self.width_slider.value()
        self.canvas.update_windowing(new_center, new_width)

        self.update_nearest_neighbor_display()

    def update_nearest_neighbor_display(self):
        """Calculates the nearest window preset based on current width/level and updates the display"""


        current_width = self.width_slider.value()
        current_level= self.center_slider.value()

        result = self.windowing_manager.get_closest_preset(current_width, current_level)

        if result:
            display_text = (
                f"Nearest Window: {result}"
            )
        else:
            display_text = "N/A"

        self.nearest_neighbor_label.setText(display_text)