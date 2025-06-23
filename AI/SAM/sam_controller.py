import numpy as np

from AI.SAM.sam_segmenter import SAMSegmenter
from image_data_handling.data_manager import VolumeDataManager
from image_data_handling.logic.mask_utils import overlay_mask, ensure_rgb


class SAMController:
    def __init__(self, sam_model:SAMSegmenter, data_manager: VolumeDataManager):
        self.sam_model = sam_model
        self.data_manager = data_manager

    def handle_click(self, image: np.ndarray, coords: tuple[int, int], slice_index: int) -> np.ndarray:
        image_rgb = self.sam_model.set_image(image)
        masks, scores, logits = self.sam_model.segment_from_point(coords)
        # Pick the best mask
        best_mask = masks[np.argmax(scores)]

        # Ensure _mask_data exists and has proper shape
        if self.data_manager.mask_data is None:
            shape = self.data_manager.volume_data.shape
            self.data_manager.mask_data = np.zeros(shape, dtype=np.uint8)

        # Store the mask for the current slice
        self.data_manager.mask_data[slice_index] = best_mask.astype(np.uint8)

        return image_rgb, best_mask
