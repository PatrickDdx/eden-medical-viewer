import nibabel as nib
import numpy as np


class NIfTIReader():

    def __init__(self):
        pass

    def open_nifti(self, file_path):

        nii_img = nib.load(file_path)
        nii_data = nii_img.get_fdata() #shape (x,y,z)
        nii_data = np.transpose(nii_data, (2,1,0)) #to shape (z,y,x)

        affine = nii_img.affine

        #header = nii_img.header

        return nii_data, affine

