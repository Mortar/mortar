# Copyright (c) 2007-2008 Simplistix Ltd
#
# All rights reserved.

import unittest

from zope.interface.verify import verifyObject

class FieldTests(unittest.TestCase):

    def test_interface(self):
        from mortar.interfaces import IField
        from mortar import content
        verifyObject(IField, content()['test'])

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FieldTests),
        ))
