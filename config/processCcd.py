# Configure astrometry.net reference loader, now that it is no longer the default.
# This file can be removed as part of DM-18036.
from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
config.calibrate.astromRefObjLoader.retarget(LoadAstrometryNetObjectsTask)
config.calibrate.photoRefObjLoader.retarget(LoadAstrometryNetObjectsTask)
config.charImage.refObjLoader.retarget(LoadAstrometryNetObjectsTask)
