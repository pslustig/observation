import numpy as np
from copy import deepcopy
from . import reducing as ru
from libtiff import TIFF


__all__ = ['log_scaler', 'scale_to_range', 'tiffsaver']


def log_scaler(image, base=np.exp(1), limits=None):
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

    if limits is not None:
        image = ru.hold_in_limits(image, limits)

    return image


def scale_to_range(image, range, limits='auto'):
    ''' set values range and interpolate image values between limits'''
    if limits == 'auto':
        limits = image.min(), image.max()

    image = ru.hold_in_limits(image, limits)

    image = np.interp(image, limits, range)
    return image


def tiffsaver(filename, image, scaling=log_scaler, cut='auto', bits=16):

    image = deepcopy(image)

    if scaling is not None:
        image = scaling(image)

    # TODO: zweites tuple in call muss scaling limit sein oder erster?
    image = scale_to_range(image, (0, 2**bits), cut)
    image = np.rint(image, dtype=np.uint16)
    tiff = TIFF.open('libtiff.tiff', mode='w')
    tiff.write_image(image)
    tiff.close()


if __name__ == '__main__':
    a = np.array([1,2, 3, 4, 5])
    b = np.array([1, 2, 3, 4, 5, 6])
    c = np.array([1,2, 3, 4])
    args = (1, 5), (1, 5)
    from functools import partial
    f = partial(scale_to_range, range=(1, 5), limits=(1, 5))
    print(f(a))
    print(f(b))
    print(f(c))
    print(scale_to_range(a, range=(1, 5)))
