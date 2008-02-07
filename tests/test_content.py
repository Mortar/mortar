# Copyright (c) 2007-2008 Simplistix Ltd
#
# All rights reserved.

import unittest

from zope.interface.verify import verifyObject

class ContentTests(unittest.TestCase):

    def test_interface(self):
        from mortar.interfaces import IContent
        from mortar import content
        verifyObject(IContent, content())

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ContentTests),
        ))
