import torch
import numpy as np
from pydicom.datadict import masks
from segment_anything import sam_model_registry, SamPredictor

class SAMSegmenter:
    def __init__(self, model_type="vit_h", checkpoint_path="C:/Users/patri/GIT/dicomViewer/AI/SAM/sam_vit_h_4b8939.pth"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = sam_model_registry[model_type](checkpoint=checkpoint_path)
        self.model.to(self.device)
        self.predictor = SamPredictor(self.model)

    def set_image(self, image: np.ndarray):
        """Sets the image for segmentation"""
        self.predictor.set_image(image)

    def segment(self, input_point, input_label):
        """Segments based on the user-provided input point (e.g., a click)"""
        masks, scores, logits = self.predictor.predict(
            point_coords=np.array([input_point]),
            point_labels=np.array([input_label]),
            multimask_output=True
        )
        return masks, scores