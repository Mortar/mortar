# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import unittest

from mortar import types
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

    def test_names_empty(self):
        self.assertEqual(self.content.names,[])

    def test_names_sorting(self):
        self.content['2']=2
        self.content['1']=1
        self.content['3']=3
        self.assertEqual(self.content.names,['1','2','3'])
        
    def test_set_with_empty(self):
        self.content['x']=()
        self.assertEqual(self.content['x'].get(),None)
        
    def test_getas_after_empty_set(self):
        self.content['x']=()
        self.assertEqual(self.content['x'].get(type=types.text),'')
        
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
    
    def test_delete_not_there(self):
        pass
    
