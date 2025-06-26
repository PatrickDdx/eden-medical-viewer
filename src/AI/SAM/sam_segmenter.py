import torch
import numpy as np
import cv2
from segment_anything import sam_model_registry, SamPredictor

import os

# From src/script.py → go up two levels to dicomViewer/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
# Construct the full path to the checkpoint
checkpoint_path = os.path.join(project_root, "AI", "SAM", "sam_vit_b_01ec64.pth")

class SAMSegmenter:
    def __init__(self, model_type="vit_b", checkpoint_path=checkpoint_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = sam_model_registry[model_type](checkpoint=checkpoint_path)
        self.model.to(self.device)
        self.predictor = SamPredictor(self.model)

    def set_image(self, image: np.ndarray):
        """Sets the image for segmentation
            Convert grayscale or RGB image to RGB format and set image
        """
        if image.ndim==2: #Grayscale
            image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 1:
            image_rgb = cv2.cvtColor(image.squeeze(), cv2.COLOR_GRAY2RGB)
        else:
            image_rgb = image

        self.predictor.set_image(image_rgb)

        return image_rgb

    def segment_from_point(self, input_point, input_label=1):
        """
        Segment the object given an input point.

        input_point: (x, y) coordinate
        input_label: 1 for foreground, 0 for background
        """

        masks, scores, logits = self.predictor.predict(
            point_coords=np.array([input_point]),
            point_labels=np.array([input_label]),
            multimask_output=True
        )
        return masks, scores, logits