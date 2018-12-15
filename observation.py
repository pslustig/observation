import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import warnings


class Observation(np.ndarray):

    def __new__(cls, data, header, filename=None, isnormalized=False):
        obj = np.asarray(data).view(cls)
        obj.isreduced = isreduced(header)
        obj.filter = header['FILTER']
        obj.filename = filename
        obj._header = header
        obj.exptime = header['EXPTIME']
        obj.isnormalized = isnormalized
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.isreduced = getattr(obj, 'isreduced', None)
        self.filter = getattr(obj, 'filter', None)
        self.filename = getattr(obj, 'filename', None)
        self._header = getattr(obj, '_header', None)
        self.exptime = getattr(obj, 'exptime', None)
        self.isnormalized = getattr(obj, 'isnormalized', None)

    def isreduced(self):
        return self.isreduced

    def normalize(self):
        assert self.isnormalized is False, 'observation is already normalized'
        self = self / self.exptime
        self.isnormalized = True

    def plot(self, ax=None, scaling=None, **kwargs):

        data = self
        if scaling is not None:
            data = scaling(self, **kwargs)

        if ax is None:
            fig, ax = plt.subplots(1, 1)
            ax.imshow(data, origin='lower')

        return ax

    def save(self, filename, **kwargs):
        multiply = 1
        if self.isnormalized:
            multiply = self.exptime
        fits.PrimaryHDU(data=self * multiply, header=self._header).writeto(
                                                            filename, **kwargs)

    def reduce(self, bias, flat, dark):

        self, h = correct_image(self, bias, flat, dark)
        self.isreduced = True
        self._header.update(h)

    def export(self):
        raise NotImplementedError('Export functions are not implemented yet')


def read_observation(filename, idx=0):

    with fits.open(filename) as hdul:
        hdu = hdul[idx]
        data = hdu.data
        header = fits.header.Header(hdu.header)

    return Observation(data, header, filename)


def correct_image(image, bias, flat=None, dark=None):
    ''' correction algorithm '''

    h = fits.header.Header()
    h['REDUCED'] = True
    h['FLATCORR'] = False
    h['DARKCORR'] = False

    reduced_image = (image - bias)
    h['BIASCORR'] = True

    if flat is not None:
        reduced_image /= flat
        h['FLATCORR'] = True

    if dark is not None:
        warnings.warn('Dark correction is not implemented yet.')
        h['FLATCORR'] = False

    return image, h


def isreduced(header):

    try:
        isreduced = header['REDUCED']
    except KeyError:
        isreduced = False

    return isreduced
