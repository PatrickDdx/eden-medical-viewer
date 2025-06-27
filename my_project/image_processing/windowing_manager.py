import numpy as np

class WindowingManager:
    def __init__(self):
        self.window_presets = {
            # head and neck
            "Brain": {"width": 80, "level": 40},
            "Subdural": {"width": 130, "level": 50},
            "Stroke": {"width": 8, "level": 32},
            "Temporal bones": {"width": 2800, "level": 600},
            # "soft tissues": {"width": 350, "level": 20},

            # chest
            "Lungs": {"width": 1500, "level": -600},
            "Mediastinum": {"width": 350, "level": 50},
            "Vascular/heart": {"width": 600, "level": 200},

            # abdomen
            "Soft tissues": {"width": 400, "level": 50},
            "Liver": {"width": 150, "level": 30},

            # spine
            # "soft tissues": {"width": 250, "level": 50},
            "Bone": {"width": 1800, "level": 400},
        }

    def apply(self, image: np.ndarray, width, level) -> np.ndarray:
        """Apply windowing to a DICOM/NIfTI image and return 8-bit display image"""
        img = np.copy(image).astype(np.float32)
        lower_bound = level - (width / 2)
        upper_bound = level + (width / 2)

        clipped_img = np.clip(img, lower_bound, upper_bound)
        windowed_img = ((clipped_img - lower_bound) /  width) * 255.0

        return windowed_img.astype(np.uint8)

    def get_presets(self):
        """Returns a list of available preset names"""
        return list(self.window_presets.keys())

    def get_preset(self, preset_name):
        """Return (width, level) tuple for a given preset"""
        return (self.window_presets[preset_name]["width"], self.window_presets[preset_name]["level"])

    def get_closest_preset(self, width, level):
        """Return the name of the closets matching preset"""

        def calculate_distance(preset_name):
            preset = self.window_presets[preset_name]
            w, l = preset["width"], preset["level"]
            return np.sqrt((width - w) ** 2 + (level - l) ** 2)

        closest = min(
            (p for p in self.window_presets if self.window_presets[p] is not None),
            key=calculate_distance,
            default="Custom"
        )

        return  closest

