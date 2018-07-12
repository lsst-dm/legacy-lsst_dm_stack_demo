#
# LSST Data Management System
# Copyright 2012-2017 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

import unittest
import os

import lsst.utils.tests
from lsst.utils import getPackageDir

package_root = getPackageDir('lsst_dm_stack_demo')

executable_dir = os.path.join(package_root, 'bin')


class DemoTestCase(lsst.utils.tests.ExecutablesTestCase):
    """Test the demo scrpts for executablility."""
    def testDemo(self):
        """Test demo"""
        self.assertExecutable("demo.sh",
                              root_dir=executable_dir,
                              args=["--small"],
                              msg="Running demo failed")
        self.assertExecutable("compare",
                              root_dir=executable_dir,
                              args=['detected-sources_small.txt'],
                              msg="Compare failed")


if __name__ == "__main__":
    unittest.main()
