#!/bin/bash

type processCcdLsstSim.py >/dev/null 2>&1 || { echo "Could not find processCcdLsstSim.py on your path. Have you sourced loadLSST.sh, and setup-ed pipe_tasks?"; exit 1; }
test -d input || { echo "Could not fine the 'input' directory. Run this script from the directory where the 'input' subdirectory resides."; exit 1; }
test -d astrometry_net_data || { echo "Could not fine the 'astrometry_net_data' directory."; exit 1; }
test "$(type -t setup)" == "function" || { export SHELL=/bin/bash; source $LSST_HOME/eups/default/bin/setups.sh; } # Ensure 'setup' alias is defined (may happen if the user is not running bash)
set -e

# Tell the stack where to find astrometric reference catalogs
setup --nolocks -v -r ./astrometry_net_data astrometry_net_data

rm -rf output detected-sources.txt
processCcdLsstSim.py lsstSim input --id visit=88689461 raft=2,3 sensor=1,1 --out output
./bin/export-results output > detected-sources.txt

echo
echo "Processing completed successfully. The results are in detected-sources.txt."
