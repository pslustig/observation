from astropy.io import fits
import numpy as np
from pathlib import Path


__all__ = ['load_flat', 'get_flat_filenames', 'get_flat_band_key',
           'load_flats', 'get_bias_name', 'get_dark_name',
           'load_calibration_files']


def load_flat(filename, normalize=np.median):
    flat = fits.getdata(filename)
    flat /= normalize(flat)
    return flat


def get_flat_filenames(path):
    path = Path(path)
    names = path.glob('*flat*.fits')
    return names


def get_flat_band_key(flatname):
    flatname = str(flatname)
    start = flatname.find('flat')
    stop = flatname.find('.fits')
    key = flatname[start+4:stop]

    return key


def get_filter_from_header(flatname):
    h = fits.getheader(flatname)
    filter = h['FILTER']
    return filter


def load_flats(flatnames, normalize=np.median, keygen=get_flat_band_key):

    flats = {}
    for flatname in flatnames:
        key = keygen(flatname)
        assert key not in flats
        flats[key] = load_flat(flatname, normalize=normalize)

    return flats


def get_bias_name(calibrationpath, biaskey='*offset*.fits'):
    path = Path(calibrationpath)
    names = list(path.glob(biaskey))
    assert len(names) == 1, ('more than one bias file found, don\'t know '
                             'which to use')
    return names[0]


def get_dark_name(calibrationpath, darkkey='*dark*.fits'):
    path = Path(calibrationpath)
    names = list(path.glob('*dark*.fits'))
    assert len(names) == 1, ('more than one dark file found, don\'t know '
                             'which to use')
    return names[0]


def load_calibration_files(calibrationpath, flatkeygen=get_filter_from_header,
                           normalizeflats=np.median, biaskey='*offset*.fits',
                           darkkey='*dark*.fits'):

    flatfilenames = get_flat_filenames(calibrationpath)
    flats = load_flats(flatfilenames, normalize=normalizeflats,
                       keygen=flatkeygen)

    bias = fits.getdata(get_bias_name(calibrationpath, biaskey=biaskey))

    dark = fits.getdata(get_dark_name(calibrationpath, darkkey=darkkey))

    return flats, bias, dark
