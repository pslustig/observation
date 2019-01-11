import observation as obs


def test_band_from_filename():
    name = 'gfvvewiv-U.fits'
    band = obs.reducing.band_from_filename(name)
    assert band == 'U'
