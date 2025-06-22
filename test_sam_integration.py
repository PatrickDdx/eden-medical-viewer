import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Import your SamSegmentor class from your new package
# Assuming segment_anything_integration is a direct subfolder of your project root
from AI.SAM.sam_segmenter import SAMSegmenter

# --- Helper functions for visualization (can be similar to what you used in Colab) ---
def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6]) # A nice blue with transparency
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='x', s=marker_size, edgecolor='white', linewidth=1.25)

def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))

# --- Main Test Logic ---
def run_sam_test():
    # --- Configuration Paths ---
    # Adjust these paths as needed based on your actual file locations
    sample_image_path = "sample_medical_image.png" # Make sure you have this image in your project root
    sam_checkpoint_path = "models/sam_vit_h_4b8939.pth" # Adjust if you use vit_b or vit_l
    model_type = "vit_h" # Matches the checkpoint type

    print("--- Starting SAM Integration Test ---")

    # 1. Load a sample medical image
    if not os.path.exists(sample_image_path):
        print(f"Error: Sample image not found at '{sample_image_path}'.")
        print("Please place a sample image (e.g., sample_medical_image.png) in your project root.")
        return

    # Use OpenCV to load the image. Remember SAM expects RGB.
    image_bgr = cv2.imread(sample_image_path)
    if image_bgr is None:
        print(f"Error: Could not load image from '{sample_image_path}'. Check file integrity.")
        return
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    print(f"Successfully loaded image: {sample_image_path} (Shape: {image_rgb.shape})")

    # 2. Initialize your SamSegmentor
    try:
        segmentor = SAMSegmenter(
            checkpoint_path="AI/SAM/sam_vit_h_4b8939.pth",
            #model_type=model_type
        )
        print("SamSegmentor initialized successfully.")
    except FileNotFoundError as e:
        print(f"Error initializing SamSegmentor: {e}")
        print(f"Please ensure '{sam_checkpoint_path}' exists.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during SamSegmentor initialization: {e}")
        return

    # 3. Simulate a simple interaction (e.g., a point click)
    # Define a point at the center of the image.
    # In a real UI, this would come from mouse clicks.
    center_x = image_rgb.shape[1] // 2
    center_y = image_rgb.shape[0] // 2
    input_points = [[center_x, center_y]]
    input_labels = [1] # 1 for foreground

    print(f"\nSimulating point click at: ({center_x}, {center_y})")

    # Set the image for the predictor before making predictions
    segmentor.set_image(image_rgb)

    # 4. Perform prediction
    try:
        masks, scores, _ = segmentor.segment(input_points, input_labels)#, multimask_output=True)
        print(f"Segmentation successful! Generated {len(masks)} masks.")
        print(f"Mask scores: {scores}")

        # 5. Display the result
        plt.figure(figsize=(12, 12))
        plt.imshow(image_rgb)
        ax = plt.gca()

        # Show all generated masks (SAM often gives multiple with multimask_output=True)
        # You might choose the one with the highest score in a real app.
        for i, mask in enumerate(masks):
            show_mask(mask, ax, random_color=True) # Use random colors to distinguish multiple masks
        show_points(np.array(input_points), np.array(input_labels), ax)

        plt.title(f"SAM Segmentation Test (Top Score: {np.max(scores):.2f})")
        plt.axis('off')
        plt.show()

    except Exception as e:
        print(f"An error occurred during segmentation prediction: {e}")

    print("\n--- SAM Integration Test Complete ---")

if __name__ == "__main__":
    run_sam_test()