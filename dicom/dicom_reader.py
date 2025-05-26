import pydicom
import numpy as np

class DicomReader():
    def __init__(self):
        pass

    def read_dicom_file(self, file_path):
        """Reads dicom file and returns pydicom Dataset"""
        return pydicom.dcmread(file_path)

    def get_metedata(self, data):
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