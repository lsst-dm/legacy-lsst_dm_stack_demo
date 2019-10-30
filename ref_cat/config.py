# Retarget for fits file reader
from lsst.meas.algorithms.readFitsCatalogTask import ReadFitsCatalogTask
config.file_reader.retarget(ReadFitsCatalogTask)

# HTM depth
config.dataset_config.indexer['HTM'].depth=7

# Dataset name
config.dataset_config.ref_dataset_name='sdss_demo_ref_cat'

# Name of RA column
config.ra_name='ra'

# Name of Dec column
config.dec_name='dec'

# Name of column to use as an identifier (optional).
config.id_name='sdssid'

# The values in the reference catalog are assumed to be in AB magnitudes. List of column names to use for
# photometric information.  At least one entry is required.
config.mag_column_list=['u', 'g', 'r', 'i', 'z']

# A map of magnitude column name (key) to magnitude error column (value).
config.mag_err_column_map={'u': 'u_err', 'g': 'g_err', 'r': 'r_err', 'i': 'i_err', 'z': 'z_err'}

# Extra columns: id is just a sequential index, starnotgal is the extendedness flag
config.extra_col_names=['starnotgal']
