#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import re
import sys
import numpy as np
import lsst.daf.persistence as dafPersist
import lsst.log

lsst.log.configure_prop("""
log4j.rootLogger=INFO, A1
log4j.appender.A1=ConsoleAppender
log4j.appender.A1.Target=System.err
log4j.appender.A1.layout=PatternLayout
""")

if len(sys.argv) != 2:
    print("Usage: export-results <output_directory>", file=sys.stderr)
    exit(1)
outputdir = sys.argv[1]

# Load sources and print interesting columns

cols = ("id",
        "coord_ra",
        "coord_dec",
        "flags_negative",
        "base_SdssCentroid_flag",
        "base_PixelFlags_flag_edge",
        "base_PixelFlags_flag_interpolated",
        "base_PixelFlags_flag_interpolatedCenter",
        "base_PixelFlags_flag_saturated",
        "base_PixelFlags_flag_saturatedCenter",
        "base_SdssCentroid_x",
        "base_SdssCentroid_y",
        "base_SdssCentroid_xErr",
        "base_SdssCentroid_yErr",
        "base_SdssShape_xx",
        "base_SdssShape_xy",
        "base_SdssShape_yy",
        "base_SdssShape_xxErr",
        "base_SdssShape_xyErr",
        "base_SdssShape_yyErr",
        "base_SdssShape_flag",
        "base_GaussianFlux_instFlux",
        "base_GaussianFlux_instFluxErr",
        "base_PsfFlux_instFlux",
        "base_PsfFlux_instFluxErr",
        "base_CircularApertureFlux_6_0_instFlux",
        "base_CircularApertureFlux_6_0_instFluxErr",
        "base_ClassificationExtendedness_value",
        )

headerPrinted = False
butler = dafPersist.Butler(outputdir)
for filter in "ugriz":
    for dataId in (dict(run=4192, filter=filter, field=300, camcol=4),
                   dict(run=6377, filter=filter, field=399, camcol=4),
                   ):
        if not butler.datasetExists("src", **dataId):
            continue

        srcs = butler.get("src", **dataId)
        if not headerPrinted:
            print('#' + ' '.join(cols))
            headerPrinted = True
        vecs = []
        for col in cols:
            if col not in srcs.schema:
                # If the column is not in the source table, we fill it
                # with a "-". We can therefore check optional columns
                # like ``flags_negative``.
                v = ["-"] * len(srcs)
            elif col.endswith(".ra") or col.endswith(".dec") or col.endswith("_ra") or col.endswith("_dec"):
                v = np.rad2deg(srcs.get(col))
            elif re.search(r"\.err\.(xx|yy|xy)$", col):
                field, which = re.search(r"^(.*\.err)\.(xx|yy|xy)$", col).groups()
                key = srcs.schema.find(field).key
                key = key[0, 0] if which == "xx" else key[1, 1] if which == "yy" else key[0, 1]

                v = srcs.get(key)
            else:
                v = srcs.get(col)
            v = np.asarray(v)
            vecs.append(v)

        for vals in zip(*vecs):
            # To future proof the comparison, we use an explicit format for floating point types since a
            # default format could be ambiguous.
            print(' '.join(['{0:.12g}'.format(el) if issubclass(el.dtype.type, np.floating)
                            else str(el) for el in vals]))
