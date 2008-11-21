# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import unittest

from mortar import content,types
from zope.interface.verify import verifyObject

class FieldTests(unittest.TestCase):

    def setUp(self):
        self.content = content()
        self.field = self.content['test']
        
    def test_interface(self):
        from mortar.interfaces import IField
        verifyObject(IField,self.field)

    def test_get_simple(self):
        self.field.set('value')
        self.assertEqual(self.field.get('name'),u'value')
    
    def test_get_default_no_default(self):
        self.assertEqual(self.field.get(),None)
        
    def test_get_default_default_supplied(self):
        self.assertEqual(self.field.get(default='123'),'123')
        
    def test_type_simple(self):
        self.field.set('value')
        self.failUnless(self.field.type is types.text)
    
    def test_get_type_not_there(self):
        self.failUnless(self.field.type is None)
    
    def test_delete(self):
        self.assertEqual(self.content.names,[])
        pass
    
    def test_delete_not_there(self):
        pass

class TestSet(unittest.TestCase):

    method = 'set'
    
    def setUp(self):
        self.content = content()
        self.field = self.content['test']

    def check(self,e_value,e_type,*args,**kw):
        getattr(self.field,self.method)(*args,**kw)
        self.assertEqual(e_value,self.field.get())
        self.assertEqual(e_type,self.field.type)
                         
    def test_default(self):
        self.check('value',types.text,'value')

    def test_default_non_string(self):
        self.check(1,types.number,1)

    def test_string(self):
        pass

    def test_string_non_string(self):
        pass

    def test_date(self):
        pass

    def test_number(self):
        pass

    def test_number_from_string(self):
        pass

    def test_path(self):
        pass

class TestAdd(TestSet):

    method = 'add'
    
    def test_add_to_existing(self):
        pass

    def test_add_wrong_type_attempt(self):
        pass

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FieldTests),
        unittest.makeSuite(TestSet),
        # unittest.makeSuite(TestAdd),
        ))
