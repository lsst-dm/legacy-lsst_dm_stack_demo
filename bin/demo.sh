#!/bin/bash

eups list --setup obs_sdss >/dev/null 2>&1 || ( echo "obs_sdss does not appear to be setup, or eups is not configured correctly."; exit 1; )
type processCcdSdss.py >/dev/null 2>&1 || { echo "Could not find processCcdSdss.py on your path. It is supposed to be in obs_sdss."; exit 1; }
test -d input || { echo "Could not find the 'input' directory. Run this script from the directory where the 'input' subdirectory resides."; exit 1; }
test -d astrometry_net_data || { echo "Could not fine the 'astrometry_net_data' directory."; exit 1; }
test "$(type -t setup)" == "function" || { export SHELL=/bin/bash; source $LSST_HOME/eups/default/bin/setups.sh; } # Ensure 'setup' alias is defined (may happen if the user is not running bash)
set -e

# Tell the stack where to find astrometric reference catalogs
setup --nolocks -v -r ./astrometry_net_data astrometry_net_data

rm -rf output detected-sources.txt
processCcdSdss.py input --id run=4192 filter=u^g^r^i^z camcol=4 field=300 --id run=6377 filter=u^g^r^i^z camcol=4 field=399 --output output
if [ $? != 0 ]; then
    echo "Failed during execution of:  lsst_dm_stack_demo/bin/processCcdSdss.py"
    exit 1
]
./bin/export-results output > detected-sources.txt
if [ $? != 0 ]; then
    echo "Failed during execution of:  lsst_dm_stack_demo/bin/export-results.py"
    exit 1
]

echo
echo "Processing completed successfully. The results are in detected-sources.txt."
exit 0
