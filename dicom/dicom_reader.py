import pydicom
import numpy as np
import os

class DicomReader():
    def __init__(self):
        pass


    def read_dicom_series(self, folder_path):
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".dcm")]
        datasets = [pydicom.dcmread(f) for f in files]
        datasets.sort(key=lambda ds: float(ds.get("InstanceNumber", 0)))

        #slices = [ds.pixel_array.astype(np.float32) for ds in datasets]
        slices = []
        for ds in datasets:
            img = ds.pixel_array.astype(np.float32)
            if hasattr(ds, 'RescaleSlope') or hasattr(ds, 'RescaleIntercept'):
                slope = float(getattr(ds, 'RescaleSlope', 1.0))
                intercept = float(getattr(ds, 'RescaleIntercept', 0.0))
                img = img * slope + intercept
            slices.append(img)

        volume = np.stack(slices, axis=0)  # shape: (num_slices, height, width)

        def extract_first(value, default):
            if isinstance(value, pydicom.multival.MultiValue):
                return int(value[0])
            try:
                return int(value)
            except Exception:
                return default

        window_center = extract_first(datasets[0].get("WindowCenter", 40), 40)
        window_width = extract_first(datasets[0].get("WindowWidth", 400), 400)

        print(f"center: {window_center}, width_ {window_width}")

        return volume, window_center, window_width

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
