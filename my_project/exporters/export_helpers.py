import numpy as np
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from datetime import datetime
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
import os

from sympy.physics.units import volume

def create_synthetic_dicom_headers(volume_data):
    if volume_data.volume_data is None or volume_data.nifti_affine_matrix is None:
        raise ValueError("Volume data or affine matrix is missing")

    headers = []
    affine = volume_data.nifti_affine_matrix
    now = datetime.now()
    series_uid = generate_uid()

    for i in range(volume_data._volume_data.shape[0]):
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
        file_meta.MediaStorageSOPInstanceUID = generate_uid()
        file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
        file_meta.ImplementationClassUID = generate_uid()

        ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)

        ds.PatientName = "Synthetic^Patient"
        ds.PatientID = "123456"
        ds.StudyInstanceUID = generate_uid()
        ds.SeriesInstanceUID = series_uid
        ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
        ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
        ds.Modality = "OT"
        ds.StudyDate = ds.SeriesDate = now.strftime("%Y%m%d")
        ds.StudyTime = ds.SeriesTime = now.strftime("%H%M%S")
        ds.InstanceNumber = i + 1

        slice_data = volume_data._volume_data[i]
        ds.Rows, ds.Columns = slice_data.shape
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 1

        spacing = [abs(affine[1, 1]), abs(affine[0, 0])]
        thickness = abs(affine[2, 2])
        ds.PixelSpacing = spacing
        ds.SliceThickness = thickness

        # Position/orientation
        position = affine[:3, 3] + affine[:3, 2] * i
        orientation_x = affine[:3, 0] / np.linalg.norm(affine[:3, 0])
        orientation_y = affine[:3, 1] / np.linalg.norm(affine[:3, 1])
        ds.ImagePositionPatient = [float(p) for p in position]
        ds.ImageOrientationPatient = [*orientation_x, *orientation_y]

        ds.PixelData = b"" # Placeholder so the DICOM dataset is accepted

        headers.append(ds)

    return headers

def build_affine_from_dicom(volume_data):
    if not volume_data.original_dicom_headers:
        raise ValueError("No DICOM headers available to build affine matrix.")

    ds0 = volume_data.original_dicom_headers[0]
    orientation = np.array(ds0.ImageOrientationPatient, dtype=np.float64).reshape(2, 3)
    spacing = np.array(ds0.PixelSpacing, dtype=np.float64)
    position = np.array(ds0.ImagePositionPatient, dtype=np.float64)

    row_cosine = orientation[0]
    col_cosine = orientation[1]
    normal = np.cross(row_cosine, col_cosine)

    slice_spacing = float(volume_data.original_dicom_headers[1].ImagePositionPatient[2] -
                          ds0.ImagePositionPatient[2]) if len(volume_data.original_dicom_headers) > 1 else 1.0

    affine = np.eye(4)
    affine[:3, 0] = row_cosine * spacing[1]  # column direction
    affine[:3, 1] = col_cosine * spacing[0]  # row direction
    affine[:3, 2] = normal * slice_spacing   # slice direction
    affine[:3, 3] = position  # origin

    return affine

