import reduceutils as ru
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt


class Observation(np.ndarray):

    def __new__(cls, data, header, filter=None, mask=None):
        obj = np.asarray(data).view(cls)
        obj.isreduced = ru.isreduced(header)
        obj.filter = header['FILTER']
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.isreduced = getattr(obj, 'isreduced', None)
        self.filter = getattr(obj, 'filter', None)

    def plot(self, ax=None, scaling=None, **kwargs):

        data = self
        if scaling is not None:
            data = scaling(self, **kwargs)

        if ax is None:
            fig, ax = plt.subplots(1, 1)
            ax.imshow(data, origin='lower')

        return ax


h = fits.header.Header()
h['FILTER'] = 'dsgds'
d = np.arange(4).reshape((2, 2))
a = Observation(d, h)
a.plot()
a.plot(scaling=lambda x: np.log(x))
