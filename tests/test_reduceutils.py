from astropy.io import fits
import reduceutils as ru


def test_isreduced_True():
    h = fits.header.Header()
    h["REDUCED"] = True

    isred = ru.isreduced(h)
    assert isred is True


def test_isreduced_False():
    h = fits.header.Header()
    h["REDUCED"] = False

    isred = ru.isreduced(h)
    assert isred is False
