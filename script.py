from pathlib import Path
import loadutils as lu
import reduceutils as ru
from importlib import reload
reload(ru)
reload(lu)

datapath = Path('ohp_dsg/')
flatpath = datapath
observationpath = datapath / 'M51'
list(flatpath.glob('*.fits'))

# flats, bias, dark = lu.load_calibration_files(flatpath)

ru.reduce_images(observationpath, *lu.load_calibration_files(flatpath, flatkey='m*flat*.fits', biaskey='m*offset.fits', darkkey='master_dark.fits'))
print('done')
