from pathlib import Path
import loadutils as lu
from importlib import reload
import matplotlib.pyplot as plt
from plotutils import imshow_zscaled
import reduceutils as ru


datapath = Path().home() / 'Pictures/ohp_dsg'
flatpath = datapath
observationpath = datapath / 'M51'

# flats, bias, dark = lu.load_calibration_files(flatpath)

ru.reduce_images(observationpath, *lu.load_calibration_files(flatpath))
