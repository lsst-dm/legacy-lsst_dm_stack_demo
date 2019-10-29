#!/bin/bash

# On OS X El Capitan we need to pass through the library load path
if [[ $(uname -s) = Darwin* ]]; then
    if [[ -z "$DYLD_LIBRARY_PATH" ]]; then
        export DYLD_LIBRARY_PATH=$LSST_LIBRARY_PATH
    fi
fi

# Assumes eups and DM packages: lsst_distrib obs_sdss, are eups-setup.
source "$EUPS_DIR/bin/setups.sh"

SIZE=""
SIZE_EXT=""
FILTER_SET_4192="u^g^r^i^z"
FILTER_SET_6377="u^g^r^i^z"

#--------------------------------------------------------------------------
usage() {
    echo "Usage: $0 [options]"
    echo "Run demonstration run."
    echo
    echo "Options:"
    echo "  --small : to use a small dataset; otherwise a mini-production size will be used."
    echo "   --help : print this message."
    echo "       -- : an unadorned '--' stops argument processing at that point."
    exit
}
#--------------------------------------------------------------------------

options=(getopt --long small,help -- "$@")
while true
do
    case "$1" in
        --small)   SIZE='small';
                   SIZE_EXT="_small";
                   FILTER_SET_4192="g^i^z";
                   FILTER_SET_6377="u^r^i";
                   shift 1 ; break ;;
        --help)    usage;;
        --)        shift ; break ;;
        *)         [ "$*" != "" ] && usage;
                   break;;
    esac
done


eups list --setup obs_sdss >/dev/null 2>&1 || ( echo "obs_sdss does not appear to be setup, or eups is not configured correctly."; exit 1; )
type processCcd.py >/dev/null 2>&1 || { echo "Could not find processCcd.py on your path. It is supposed to be in obs_sdss."; exit 1; }
test -d input || { echo "Could not find the 'input' directory. Run this script from the directory where the 'input' subdirectory resides."; exit 1; }
set -e


rm -rf output detected-sources.txt output_small detected-sources_small.txt
# Reconfigure to use the included reference catalog
CONFIG=config/processCcd.py
# The following config overrides are necessary for the demo to run, until new 'truth' values are computed
# based on the new stack default of growing footprints and running the deblender. See issue 4801
processCcd.py input --id run=4192 filter=$FILTER_SET_4192 camcol=4 field=300 --id run=6377 filter=$FILTER_SET_6377 camcol=4 field=399 --output output$SIZE_EXT --configfile=$CONFIG

# We need to explicitly run Python here as the command to allow
#   the library load path environment to be passed to export-results
#   on modern OS X versions.
# The `#!/usr/bin/env python` in the first line of export-results
#   no longer loads the correct environment.
python ./bin.src/export-results.py output$SIZE_EXT > detected-sources$SIZE_EXT.txt

echo
echo "Processing completed successfully. The results are in detected-sources$SIZE_EXT.txt."
