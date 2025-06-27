import cv2
import numpy as np

def export_as_mp4(volume_data, output_path, fps, data_type, window_fn):
    """Exports the current volume as MP4 video"""

    num_slices, height, width = volume_data.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for i in range(num_slices):
        if data_type == "dicom":
            img = window_fn(i) # Apply rescale + window
        else:
            img = window_fn(volume_data[i])

        frame = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        writer.write(frame)

    writer.release()
    return True