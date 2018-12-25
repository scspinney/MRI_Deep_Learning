import nibabel as nib
import numpy as np
import os
import pandas as pd
from glob import glob
from pathlib import Path


def validateDims(images):
    """
    Verifies that all images have the same dimensions
    and then returns them.

    :param images:
    :return:
    """
    dims = images[0]['data'].shape
    for img in images:
        if img['data'].shape != dims:
            print('Problem with subject {}'.format(Path(img['path']).parents[0].parts[-1]))
    return dims


def nii2Numpy(imagePaths):

    if type(imagePaths) != list:
        imagePaths = [imagePaths]
        if len(imagePaths) == 0:
            print("No paths for nii2Numpy to process.")
            return -1

    images = [{'data': nib.load(p), 'path': p} for p in imagePaths]
    #print(images)
    dims = validateDims(images)
    numpyImages = np.zeros( (dims + (len(images),)) )

    for i, img in enumerate(images):
        numpyImages[:,:,:,i] = img['data'].get_fdata()

    return numpyImages

def updateSubjectDf(newImg,path):

    dfPath = glob(os.path.join(str(path.parents[0]), 'sMRI_*'))
    imagesDf = pd.read_csv(dfPath)
    subjName = path.parts[-1]
    subjData = {'subjects': subjName,
                'paths': path,
                'labels': imagesDf.loc[imagesDf.subjects == subjName[:-1], ['labels']],
                'category': imagesDf.loc[imagesDf.subjects == subjName[:-1], ['category']]
                }
    imagesDf = imagesDf.append(subjData, ignore_index=True)
    imagesDf.to_csv(dfPath)

def normalize():
    pass

def unitTest1():
    path = '/Volumes/Storage/Work/Data/Neuroventure/sub-002/brainmask.nii'
    images = nii2Numpy(path)
    print(images.shape)



