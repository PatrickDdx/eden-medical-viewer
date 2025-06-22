import torch
import numpy as np
import cv2
from pydicom.datadict import masks
from segment_anything import sam_model_registry, SamPredictor

class SAMSegmenter:
    def __init__(self, model_type="vit_b", checkpoint_path="C:/Users/patri/GIT/dicomViewer/AI/SAM/sam_vit_b_01ec64.pth"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"device: {self.device}")
        self.model = sam_model_registry[model_type](checkpoint=checkpoint_path)
        self.model.to(self.device)
        self.predictor = SamPredictor(self.model)

    def set_image(self, image: np.ndarray):
        """Sets the image for segmentation
            Convert grayscale or RGB image to RGB format and set image
        """
        #print(f"image shape at start of set_image: {image.shape}")
        if image.ndim==2: #Grayscale
            image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 1:
            image_rgb = cv2.cvtColor(image.squeeze(), cv2.COLOR_GRAY2RGB)
        else:
            image_rgb = image
        #print(f"shape of image_rgb after conversion (if-else): {image_rgb}")
        #print("before predictor.set_image(image_rgb")
        self.predictor.set_image(image_rgb)
        #print(f"image set! image_rgb shape at end of set_image: {image_rgb}")
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