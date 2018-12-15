import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy


__all__ = ['log_scaler', 'scale_to_range', 'tiffsaver']


def log_scaler(image, base=np.exp(1)):
    ''' calculates logarithm of image for better visibility of faint objects

    Parameters
    ----------
    image : :class:`numpy.ndarray`
        image that has to be scaled
    base : float
        logarithm base

    Returns
    -------
    :class:`numpy.ndarray`
        scaled image
    '''

    image = np.log(image) / np.log(base)

    return image


def scale_to_range(image, range):
    ''' set values range and interpolate image values between limits'''
    image = np.interp(image, (image.min(), image.max()), range)
    return image


def tiffsaver(filename, image, scaling=log_scaler, bits=16):

    image = deepcopy(image)

    if scaling is not None:
        image = scaling(image)

    image = scale_to_range(image, (0, 2**bits))
    image = np.rint(image)
    plt.figure()
    plt.imshow(image, origin='lower')
    plt.colorbar()
