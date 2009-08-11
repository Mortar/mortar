# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import unittest
from glob import glob
from os.path import dirname,join,pardir
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

def test_suite():
    return DocFileSuite(
        optionflags=REPORT_NDIFF|ELLIPSIS,
        module_relative=False,
        *glob(join(dirname(__file__),pardir,'docs','*.txt'))
        )
        
