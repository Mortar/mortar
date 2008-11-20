# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import os
import unittest
from glob import glob
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

def test_suite():
    suite = unittest.TestSuite()
    for path in glob(os.path.join(os.path.dirname(__file__),'..','docs','*.txt')):
        # BODGE!
        if os.path.split(path)[-1] in ('traversing.txt',):
            continue
        suite.addTest(
            DocFileSuite(path, optionflags=REPORT_NDIFF|ELLIPSIS)
            )
    return suite

if __name__ == '__main__':
    unittest.main(default='test_suite')
