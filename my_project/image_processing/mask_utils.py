import numpy as np
import cv2

def overlay_mask(image: np.ndarray, mask: np.ndarray, alpha=0.5) -> np.ndarray:
    """Overlay a binary mask on an image"""
    color_mask = np.zeros_like(image)
    color_mask[:, :, 0] = mask * 255  # Red channel

    overlayed = cv2.addWeighted(image, 1 - alpha, color_mask, alpha, 0)

    return overlayed


def ensure_rgb(image):
    if image.ndim==2: #Grayscale
        image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 1:
        image_rgb = cv2.cvtColor(image.squeeze(), cv2.COLOR_GRAY2RGB)
    else:
        image_rgb = image

    return image_rgb