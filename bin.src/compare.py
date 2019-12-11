#!/usr/bin/env python
from __future__ import division
from __future__ import print_function

import argparse
import os
import sys
import numpy as np

# Data columns in the output
# This needs to be kept in sync with the columns in export-results, until
# this script and the expected results files are modified to run directly
# on the binary table outputs.
# Note that we load the flags as 'str', since that's what export-results
# does, but that doesn't matter since we're just comparing for equality
# for all non-float fields.
DTYPE = np.dtype(
    [("id", np.int64),
     ("coord_ra", float),
     ("coord_dec", float),
     ("flags_negative", str, 5),
     ("base_SdssCentroid_flag", str, 5),
     ("base_PixelFlags_flag_edge", str, 5),
     ("base_PixelFlags_flag_interpolated", str, 5),
     ("base_PixelFlags_flag_interpolatedCenter", str, 5),
     ("base_PixelFlags_flag_saturated", str, 5),
     ("base_PixelFlags_flag_saturatedCenter", str, 5),
     ("base_SdssCentroid_x", float),
     ("base_SdssCentroid_y", float),
     ("base_SdssCentroid_xErr", float),
     ("base_SdssCentroid_yErr", float),
     ("base_SdssShape_xx", float),
     ("base_SdssShape_xy", float),
     ("base_SdssShape_yy", float),
     ("base_SdssShape_xxErr", float),
     ("base_SdssShape_xyErr", float),
     ("base_SdssShape_yyErr", float),
     ("base_SdssShape_flag", str, 5),
     ("base_GaussianFlux_instFlux", float),
     ("base_GaussianFlux_instFluxErr", float),
     ("base_PsfFlux_instFlux", float),
     ("base_PsfFlux_instFluxErr", float),
     ("base_CircularApertureFlux_2_instFlux", float),
     ("base_CircularApertureFlux_2_instFluxErr", float),
     ("base_ClassificationExtendedness_value", float),
     ])


def get_array(filename):
    with open(filename, 'r') as f:
        array = np.loadtxt(f, dtype=DTYPE)
    return array


def difference(arr1, arr2):
    """
    Compute the relative and absolute differences of numpy arrays arr1 & arr2.

    The relative difference R between numbers n1 and n2 is defined as per
    numdiff (http://www.nongnu.org/numdiff/numdiff.html):
    * R = 0 if n1 and n2 are equal,
    * R = Inf if n2 differs from n1 and at least one of them is zero,
    * R = A/ min(|n1|, |n2|) if n1 and n2 are both non zero and n2 differs from n1.
    """
    absDiff = np.abs(arr1 - arr2)

    # If there is a difference between 0 and something else, the result is
    # infinite.
    absDiff = np.where((absDiff != 0) & ((arr1 == 0) | (arr2 == 0)), np.inf, absDiff)

    # If both inputs are nan, the result is 0.
    absDiff = np.where(np.isnan(arr1) & np.isnan(arr2), 0, absDiff)

    # If one input is nan, the result is infinite.
    absDiff = np.where(np.logical_xor(np.isnan(arr1), np.isnan(arr2)), np.inf, absDiff)

    # Divide by the minimum of the inputs, unless 0 or nan.
    # If the minimum is 0 or nan, then either both inputs are 0/nan (so there's no
    # difference) or one is 0/nan (in which case the absolute difference is
    # already inf).
    divisor = np.where(np.minimum(arr1, arr2) == 0, 1, np.minimum(arr1, arr2))
    divisor = np.where(np.isnan(divisor), 1, divisor)

    return absDiff, absDiff/np.abs(divisor)


def compareWithNumPy(filename, reference, tolerance):
    """
    Compare a generated data file to a reference using NumPy.

    The comparison is successful if:
    * The files contain the same data columns (both by name and by data type);
    * Each numeric value is in the input is either:
        a) Within ``tolerance`` of the corresponding value in the reference, or
        b) The relative difference with the reference (defined as above) is
           within ``tolerance``;
    * Flags recorded in the input and the reference are identical.

    @param filename  Path to input data file.
    @param reference Path to reference file.
    @param tolerance Tolerance.
    """
    with open(filename, 'r') as data, open(reference, 'r') as ref:
        data_columns = data.readline().strip('#').split()
        ref_columns = ref.readline().strip('#').split()
    table1, table2 = get_array(filename), get_array(reference)
    if (table1.dtype != table2.dtype) or (data_columns != ref_columns):
        print("Files do not contain the same columns.")
        return False
    valid = True
    for name in table1.dtype.names:
        dtype, count = table1.dtype.fields[name]
        if dtype == np.dtype(float):
            absDiff, relDiff = difference(table1[name], table2[name])
            for pos in np.where((relDiff > tolerance) & (absDiff > tolerance))[0]:
                valid = False
                print("Failed (absolute difference %g, relative difference %g over tolerance %g) "
                      "in column %s." % (absDiff[pos], relDiff[pos], tolerance, name))
        else:
            if not np.all(table1[name] == table2[name]):
                nTotal = len(table1[name])
                nDiff = len(np.where(table1[name] != table2[name])[0])
                print("Failed (%s of %s flags do not match) in column %s." % (str(nDiff), str(nTotal), name))
                valid = False
    return valid


def determineFlavor():
    """
    Return a string representing the 'flavor' of the local system.

    Based on the equivalent logic in EUPS, but without introducing an EUPS
    dependency.
    """
    uname, machine = os.uname()[0:5:4]
    if uname == "Linux":
        if machine[-2:] == "64":
            return "Linux64"
        else:
            return "Linux"
    elif uname == "Darwin":
        if machine in ("x86_64", "i686"):
            return "DarwinX86"
        else:
            return "Darwin"
    else:
        raise RuntimeError("Unknown flavor: (%s, %s)" % (uname, machine))


def extantFile(filename):
    """
    Raise ArgumentTypeError if ``filename`` does not exist.
    """
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(filename + " is not a file.")
    return filename


def referenceFilename(checkFilename):
    """
    Attempt to guess the filename to compare our input against.
    """
    guess = os.path.join(os.path.split(os.path.dirname(__file__))[0], "expected",
                         determineFlavor(), os.path.basename(checkFilename))
    if os.path.isfile(guess):
        return guess
    else:
        raise ValueError("Cannot find reference data (looked for %s)." % (guess,))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=extantFile, help="Input data file.")
    parser.add_argument('--tolerance', default=1e-10, type=float, help="Tolerance for errors. "
                        "The test will fail if both the relative and absolute errors exceed the tolerance.")
    parser.add_argument('--reference', type=extantFile, help="Reference data for comparison.")
    args = parser.parse_args()

    if not args.reference:
        args.reference = referenceFilename(args.filename)

    if compareWithNumPy(args.filename, args.reference, args.tolerance):
        print("Ok.")
    else:
        sys.exit(1)
