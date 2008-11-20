# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import unittest

from zope.interface.verify import verifyObject

class FieldTests(unittest.TestCase):

    def setUp(self):
        from mortar import content
        self.content = content()
        
    def test_interface(self):
        from mortar.interfaces import IField
        verifyObject(IField,self.content['test'])

    def test_default_no_default(self):
        self.assertEqual(self.content['test'].get(),None)
        
    def test_default_default_supplied(self):
        self.assertEqual(self.content['test'].get(default='123'),'123')
        
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FieldTests),
        ))
