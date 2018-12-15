import reduceutils as ru
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt


class Observation(np.ndarray):

    def __new__(cls, data, header, filename=None):
        obj = np.asarray(data).view(cls)
        obj.isreduced = ru.isreduced(header)
        obj.filter = header['FILTER']
        obj.filename = filename
        obj._header = header
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.isreduced = getattr(obj, 'isreduced', None)
        self.filter = getattr(obj, 'filter', None)
        self.filename = getattr(obj, 'filename', None)
        self._header = getattr(obj, '_header', None)

    def plot(self, ax=None, scaling=None, **kwargs):

        data = self
        if scaling is not None:
            data = scaling(self, **kwargs)

        if ax is None:
            fig, ax = plt.subplots(1, 1)
            ax.imshow(data, origin='lower')

        return ax


def read_observation(filename, idx=0):

    with fits.open(filename) as hdul:
        hdu = hdul[idx]
        data = hdu.data
        header = fits.header.Header(hdu.header)

    return Observation(data, header, filename)
