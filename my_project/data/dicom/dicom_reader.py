import pydicom
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
import time
from my_project.ui.toast_api import toast

class DicomReader():
    def __init__(self):
        pass

    def process_single_dicom(self, filepath):
        """Reads a single DICOM file"""
        ds = pydicom.dcmread(filepath)
        img = ds.pixel_array.astype(np.float32)

        instance_number = float(ds.get("InstanceNumber", 0))

        #slope = float(getattr(ds, 'RescaleSlope', 1.0))
        #intercept = float(getattr(ds, 'RescaleIntercept', 0.0))
        #img = img * slope + intercept

        return instance_number, img, ds


    def read_dicom_series(self, folder_path):
        start_time = time.time()

        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".dcm")]

        if not files:
            toast("No files found")
            return

        processed_data = []

        with ThreadPoolExecutor() as executor:
            processed_data = list(executor.map(self.process_single_dicom, files))

        processed_data.sort(key=lambda x: x[0])

        _, sorted_slices, sorted_datasets = zip(*processed_data)

        volume = np.stack(sorted_slices, axis = 0) #shape (num_slices, height, width)

        first_dataset = sorted_datasets[0]

        def extract_first_int(value, default):
            """Helper function to safely extract the first int from potentially MultiValue DICOM tag"""
            if isinstance(value, pydicom.multival.MultiValue):
                try:
                    return int(value[0])
                except (ValueError, TypeError):
                    return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        window_center = extract_first_int(first_dataset.get("WindowCenter", 40), 40)
        window_width = extract_first_int(first_dataset.get("WindowWidth", 400), 400)

        metadata = self.get_metadata(first_dataset)

        end_time = time.time()
        total_time = end_time - start_time
        #toast(f"{total_time} seconds needed to open {len(files)} DICOM files in {folder_path}")

        return volume, window_center, window_width, metadata, list(sorted_datasets)

    def get_metadata(self, ds):
        """Extracts metadata from dicom data"""
        """
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
        """

        metadata = {
            "PatientName": str(getattr(ds, "PatientName", "N/A")),
            "PatientID": str(getattr(ds, "PatientID", "N/A")),
            "PatientBirthDate": str(getattr(ds, "PatientBirthDate", "N/A")),
            "PatientSex": str(getattr(ds, "PatientSex", "N/A")),
            "StudyDate": str(getattr(ds, "StudyDate", "N/A")),
            "StudyDescription": str(getattr(ds, "StudyDescription", "N/A")),
            "SeriesDescription": str(getattr(ds, "SeriesDescription", "N/A")),
            "Modality": str(getattr(ds, "Modality", "N/A")),
            "ProtocolName": str(getattr(ds, "ProtocolName", "N/A")),
            "BodyPartExamined": str(getattr(ds, "BodyPartExamined", "N/A")),
            "SeriesNumber": getattr(ds, "SeriesNumber", "N/A"),
            "InstanceNumber": getattr(ds, "InstanceNumber", "N/A"),
            "Manufacturer": str(getattr(ds, "Manufacturer", "N/A")),
            "Rows": getattr(ds, "Rows", "N/A"),
            "Columns": getattr(ds, "Columns", "N/A"),
            "PixelSpacing": getattr(ds, "PixelSpacing", "N/A"),
            "SliceThickness": getattr(ds, "SliceThickness", "N/A"),
            "SpacingBetweenSlices": getattr(ds, "SpacingBetweenSlices", "N/A"),
            "ImagePositionPatient": getattr(ds, "ImagePositionPatient", "N/A"),
            "ImageOrientationPatient": getattr(ds, "ImageOrientationPatient", "N/A"),
            "WindowCenter": getattr(ds, "WindowCenter", "N/A"),
            "WindowWidth": getattr(ds, "WindowWidth", "N/A"),
            "RescaleIntercept": getattr(ds, "RescaleIntercept", "N/A"),
            "RescaleSlope": getattr(ds, "RescaleSlope", "N/A"),
        }

        return metadata

