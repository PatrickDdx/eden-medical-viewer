import nibabel as nib
import numpy as np
from pathlib import Path


def export_nifti(volume_data, affine_matrix, filepath):
    if volume_data is None or affine_matrix is None:
        raise ValueError("Missing volume data or affine matrix")


    save_volume = np.transpose(volume_data, (2, 1, 0))

    nifti_img = nib.Nifti1Image(save_volume, affine_matrix)
    nib.save(nifti_img, Path(filepath))

    return True
