# Copyright (c) 2008 Simplistix Ltd
#
# All rights reserved.

from  unittest import TestCase
from zope.interface.verify import verifyObject

class ReadOnlyStorageTests(TestCase):

    def afterSetUp(self):
        # this should provide an IStorage as self.storage
        # the contains content with the id of 'test'
        raise NotImplementedError
    
    def test_interface(self):
        from mortar.interfaces import IStorage
        verifyObject(IStorage, self.storage)

    def test_load(self):
        from mortar.interfaces import IContent
        content = self.storage.load('test')
        verifyObject(IContent, content)
    
    def test_load_not_found(self):
        from mortar.exceptions import NotFound
        self.assertRaises(NotFound,self.storage.load,'notfoundtest')

class WriteableStorageTests(ReadOnlyStorageTests):

    def test_save(self):
        from mortar.exceptions import NotFound
        from mortar import content
        self.assertRaises(NotFound,self.storage.load,'savetest')
        c = content()
        c['test']='test'
        self.storage.save('savetest')
        content = self.storage.load('test')
        verifyObject(IContent, content)
        self.assertEqual(content['test'].get(),'test')

