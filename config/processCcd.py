# This sets the reference catalog name for Gen2.
for refObjLoader in (config.calibrate.astromRefObjLoader,
                     config.calibrate.photoRefObjLoader,
                     config.charImage.refObjLoader,
                     ):
    refObjLoader.ref_dataset_name = "sdss_demo_ref_cat"

# This sets up the reference catalog for Gen3.
# Note that in Gen3, we've stopped pretending (which is what Gen2 does,
# for backwards compatibility) that charImage uses a reference catalog.
config.calibrate.connections.astromRefCat = "sdss_demo_ref_cat"
config.calibrate.connections.photoRefCat = "sdss_demo_ref_cat"

config.calibrate.photoCal.photoCatName = "sdss_demo_ref_cat"
