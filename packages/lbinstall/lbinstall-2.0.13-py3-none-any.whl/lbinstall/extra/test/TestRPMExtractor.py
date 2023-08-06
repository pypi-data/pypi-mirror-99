###############################################################################
# (c) Copyright 2016 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
'''
Test for the RPMExtractor tool

@author: Ben Couturier
'''
import os
import unittest
import logging

from lbinstall.extra.RPMExtractor import getrpmgroup
from lbinstall.extra.RPMExtractor import getrpmprefixes
from lbinstall.extra.RPMExtractor import extract
from tempfile import mkdtemp


class Test(unittest.TestCase):

    def setUp(self):

        self.filename = "A-2.0.0-1.noarch.rpm"
        url = "http://lhcb-rpm.web.cern.ch/lhcb-rpm/lhcbdevtests/%s" \
            % self.filename
        self.url = url
        logging.basicConfig()
        if not os.path.exists(self.filename):
            from six.moves.urllib.request import urlretrieve
            urlretrieve(self.url, self.filename)

    def tearDown(self):
        pass

    def testGetGroup(self):
        ''' Check that we can get the group of a given RPM  '''
        grp = getrpmgroup(self.filename)
        print("RPM Group: <%s>" % grp)
        self.assertEqual(grp, "LHCb", "Error getting RPM group")

    def testGetPrefixes(self):
        ''' Check that we can get the group of a given RPM  '''
        grp = getrpmprefixes(self.filename)
        print("RPM Prefixes: %s" % grp)
        self.assertEqual(grp, "/opt/LHCbSoft", "Could not get prefixes")

    def testExtaction(self):
        basedir = mkdtemp()
        print("Extracting to %s" % basedir)
        extract([self.filename], basedir)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testFindPackage']
    unittest.main()
