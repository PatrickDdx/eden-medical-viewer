from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class SliceSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setMinimum(0)
        self.setMaximum(0)
        self.setSingleStep(1)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)

class WindowWidthSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setMinimum(1)
        self.setMaximum(2000)
        self.setSingleStep(400)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)

class WindowCenterSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setMinimum(-1000)
        self.setMaximum(1000)
        self.setValue(0)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)

class DicomControls(QWidget):
    def __init__(self, canvas):
        super().__init__()

        self.canvas = canvas #is the viewer Widget that should be controlled with the slider etc.

        # slider to change the current slice
        self.slider = SliceSlider()
        self.slider.valueChanged.connect(self.update_image_from_slider)

        # window center slider
        self.center_slider = WindowCenterSlider()
        self.center_slider.valueChanged.connect(self.update_windowing)

        # window width slider
        self.width_slider = WindowWidthSlider()
        self.width_slider.valueChanged.connect(self.update_windowing)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Slice Slider"))
        layout.addWidget(self.slider)
        layout.addWidget(QLabel("Window Center"))
        layout.addWidget(self.center_slider)
        layout.addWidget(QLabel("Window Width"))
        layout.addWidget(self.width_slider)

        self.setLayout(layout)

    def update_image_from_slider(self, value):
        self.canvas.update_image(value)   #########??????????


    def update_windowing(self):
        new_center = self.center_slider.value()
        new_width = self.width_slider.value()
        self.canvas.update_windowing(new_center, new_width)