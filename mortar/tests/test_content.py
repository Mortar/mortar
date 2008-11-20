# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import unittest

from common import ContentTests as Base

class ContentTests(Base):

    # These tests are for the simple implementation
    # of IContent
    
    def setUp(self):
        from mortar import content
        self.content = content()
        
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ContentTests),
        ))
