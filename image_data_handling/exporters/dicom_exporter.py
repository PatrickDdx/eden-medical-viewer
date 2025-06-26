import pydicom
import copy
from pathlib import Path
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
import numpy as np

def export_dicom_series(volume_data, headers, output_dir_path):

    if volume_data is None or headers is None:
        raise ValueError("Missing volume data or headers")

    output_dir = Path(output_dir_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    series_uid = pydicom.uid.generate_uid()

    for i, original_header in enumerate(headers):

        header = copy.deepcopy(original_header)
        slice_data = volume_data[i]

        # Force uncompressed transfer syntax
        header.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
        header.is_implicit_VR = False
        header.is_little_endian = True

        # Ensure the pixel data has correct shape/type
        header.PixelData = slice_data.astype(np.int16).tobytes()
        header.Rows, header.Columns = slice_data.shape
        header.SeriesInstanceUID = series_uid
        # Update InstanceNumber to ensure ordering in viewers
        header.InstanceNumber = i + 1

        # Update SOPInstanceUID to make sure each slice is unique
        header.SOPInstanceUID = pydicom.uid.generate_uid()

        # Check if original_header has Window Center/Width and copy them
        if 'WindowCenter' in original_header:
            header.WindowCenter = original_header.WindowCenter
        if 'WindowWidth' in original_header:
            header.WindowWidth = original_header.WindowWidth

        if 'RescaleIntercept' in original_header:
            header.RescaleIntercept = original_header.RescaleIntercept
        if 'RescaleSlope' in original_header:
            header.RescaleSlope = original_header.RescaleSlope

        output_file = output_dir / f"slice_{i:04d}.dcm"
        header.save_as(str(output_file), write_like_original=True)

    return True