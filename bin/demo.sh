#!/bin/bash

# Assumes eups and DM packages: lsst_distrib obs_sdss, are eups-setup.
source $EUPS_DIR/bin/setups.sh

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
type processCcdSdss.py >/dev/null 2>&1 || { echo "Could not find processCcdSdss.py on your path. It is supposed to be in obs_sdss."; exit 1; }
test -d input || { echo "Could not find the 'input' directory. Run this script from the directory where the 'input' subdirectory resides."; exit 1; }
test -d astrometry_net_data || { echo "Could not fine the 'astrometry_net_data' directory."; exit 1; }
set -e

# Tell the stack where to find astrometric reference catalogs
setup --nolocks -v -r ./astrometry_net_data astrometry_net_data

rm -rf output detected-sources.txt output_small detected-sources_small.txt
processCcdSdss.py input --id run=4192 filter=$FILTER_SET_4192 camcol=4 field=300 --id run=6377 filter=$FILTER_SET_6377 camcol=4 field=399 --output output$SIZE_EXT
./bin/export-results output$SIZE_EXT > detected-sources$SIZE_EXT.txt

echo
echo "Processing completed successfully. The results are in detected-sources$SIZE_EXT.txt."
