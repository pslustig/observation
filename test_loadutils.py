import loadutils as lu


def test_get_flat_band_key():
    fname = "evnuvfieuflatRGB.fits"
    band = lu.get_flat_band_key(fname)
    assert band == 'RGB'
