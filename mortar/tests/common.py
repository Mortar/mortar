# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import unittest

from zope.interface.verify import verifyObject

class ContentTests(unittest.TestCase):

    # These tests are the base tests for anything
    # that implements IContent and it's associated
    # IField implementation

    def setUp(self):
        raise NotImplementedError

    def test_interface(self):
        from mortar.interfaces import IContent
        verifyObject(IContent, self.content)

    def test_set(self):
        # - with value
        # - with as
        # - with other field
        pass

    def test_get(self):
        # - with default
        # - with as
        # - with a and default?
        pass
    
    def test_cast(self):
        # sterile lookup with our own adapter(s)

        # seperate tests(suite?) for default adapters
        pass

    def test_del(self):
        pass

    def test_delete(self):
        pass
    
    
