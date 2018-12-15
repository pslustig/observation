from astropy.io import fits
from loadutils import get_filter_from_header
from pathlib import Path
import warnings
import tiffsaving as tf


__all__ = ['correct_image', 'last_char_in_str', 'band_from_filename',
           'load_rawfile', 'make_target_directory', 'isreduced',
           'hold_in_limits', 'reduce_images']


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

    return reduced_image, h


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


def isreduced(header):

    try:
        isreduced = header['REDUCED']
    except KeyError:
        isreduced = False

    return isreduced


def hold_in_limits(image, limits):
    ''' image values that are not in limits are set to minimum or
        maximum values'''

    vmin, vmax = limits
    image[image > vmax] = vmax
    image[image < vmin] = vmin

    return image


def reduce_images(datapath, flats, bias, dark, targetpath='subfolder',
                  bandgetter=get_filter_from_header, format='fits'):

    rawdatas = datapath.glob('*.fit*')
    targetpath = make_target_directory(datapath, targetpath)

    for rawdata in rawdatas:
        header, data = load_rawfile(rawdata)
        if not isreduced(header):
            filter = bandgetter(rawdata)
            data, exthead = correct_image(data, bias, flats[filter], dark)
            data /= header['EXPTIME']

            header.extend(exthead)
            if format == 'fits':
                fits.PrimaryHDU(header=header, data=data).writeto(
                                    targetpath / ('reduced_' + rawdata.name),
                                    overwrite=True)
            elif format == 'tif':
                tf.tiffsaver(targetpath / ('reduced_' + rawdata.stem + '.tif'),
                             data)
