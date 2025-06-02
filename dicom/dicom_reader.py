import pydicom
import numpy as np

class DicomReader():
    def __init__(self):
        pass

    def read_dicom_file(self, file_path):
        """Reads dicom file and returns pydicom Dataset"""
        return pydicom.dcmread(file_path)

    def get_metadata(self, data):
        """Extracts metadata from dicom data"""
        metadata = {
            "PatientName": str(getattr(data, 'PatientName', 'N/A')),
            "PatientID": str(getattr(data, 'PatientID', 'N/A')),
            "SeriesDescription": str(getattr(data, 'SeriesDescription', 'N/A')),
            "Modality": str(getattr(data, 'Modality', 'N/A')),
            "StudyDate": str(getattr(data, 'StudyDate', 'N/A')),
            "ImagePixelSpacing": getattr(data, 'PixelSpacing', 'N/A'),
            "Rows": getattr(data, 'Rows', 'N/A'),
            "Columns": getattr(data, 'Columns', 'N/A'),
        }

        return metadata

    def get_pixel_array(self, dicom_data):
        """Reads dicom data and returns normalized pixel array"""
        pixels = dicom_data.pixel_array.astype(np.float32)
        pixels = 255 * (pixels - np.min(pixels)) / (np.ptp(pixels) + 1e-5)
        pixels = pixels.astype(np.uint8)
        return pixels
