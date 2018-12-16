from astropy.io import fits
from loadutils import get_filter_from_header
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from observation import read_observation


__all__ = ['last_char_in_str', 'band_from_filename',
           'load_rawfile', 'make_target_directory',
           'reduce_images']


def last_char_in_str(string, char):
    ''' get index of last character char in a string (inverse order to
        str.find)'''

    string = string[::-1]
    invidx = string.find('-')
    idx = len(string) - invidx - 1

    return idx


def band_from_filename(filename):
    ''' extract band from filename. Better use header if present '''
    start = last_char_in_str(filename, '-')
    stop = filename.find('.fit')
    band = filename[start+1:stop]

    return band


def load_rawfile(filename):
    with fits.open(filename) as hdul:
        assert len(hdul) == 1, ('file contains more than one hdu, check raw '
                                'data format')
        header = fits.header.Header(hdul[0].header)
        data = hdul[0].data

    return header, data


def make_target_directory(datapath, targetpath):

    if targetpath == 'subfolder':
        targetpath = datapath / 'reduced'

    targetpath.mkdir(exist_ok=True)

    return Path(targetpath)


def hold_in_limits(image, limits):
    vmin, vmax = limits
    image[image > vmax] = vmax
    image[image < vmin] = vmin
    return image


def reduce_images(datapath, flats, bias, dark, targetpath='subfolder',
                  bandgetter=get_filter_from_header, format='fits',
                  datakey='*.fit', **kwargs):

    rawdatas = datapath.glob(datakey)
    targetpath = make_target_directory(datapath, targetpath)

    for rawdata in rawdatas:
        observation = read_observation(rawdata)
        if not observation.isreduced:
            filter = observation.filter
            observation = observation.reduce(bias, flats[filter], dark)
            observation.normalize()

            if format == 'fits':
                observation.save(
                    targetpath / ('reduced_' + rawdata.stem + '.fits'),
                    overwrite=True)
            elif format == 'tif':
                observation.export(
                    targetpath / ('reduced_' + rawdata.stem + '.tif'),
                    **kwargs)
