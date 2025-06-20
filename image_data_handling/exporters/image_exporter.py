from PyQt6.QtGui import QImage, QPixmap

def export_slice_image(raw_slice, window_width, window_level, window_fn, filepath):

        img_8bit = window_fn(raw_slice, window_width, window_level)

        height, width = img_8bit.shape
        bytes_per_line = width  # For Grayscale8
        q_image = QImage(img_8bit.tobytes(), width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        final_pixmap_to_save = QPixmap.fromImage(q_image)
        success = final_pixmap_to_save.save(filepath)
        return success