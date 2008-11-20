# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from  unittest import TestCase
from zope.interface.verify import verifyObject

class ReadOnlyStorageTests(TestCase):

    load_id = 'test'

    notfound_id = 'notfoundtest'
    
    def setUp(self):
        # this should provide an IStorage as self.storage
        # the contains content with the id of 'test'
        # this content should contain a field called 'testfield'
        # with the value of 'testvalue'
        raise NotImplementedError
    
    def test_interface(self):
        from mortar.interfaces import IStorage
        verifyObject(IStorage, self.storage)

    def test_load(self):
        from mortar.interfaces import IContent
        content = self.storage.load(self.load_id)
        verifyObject(IContent, content)
        self.assertEqual(content['testfield'].get(),'testvalue')
    
    def test_load_not_found(self):
        from mortar.exceptions import NotFound
        self.assertRaises(NotFound,self.storage.load,self.notfound_id)

    def test_save(self):
        from mortar.exceptions import NotSupported
        from mortar import content
        c = content()
        self.assertRaises(NotSupported,self.storage.save,self.load_id)

class WriteableStorageTests(ReadOnlyStorageTests):

    save_id = 'savetest'
    
    def test_save(self):
        from mortar.exceptions import NotFound
        from mortar import content
        self.assertRaises(NotFound,self.storage.load,self.save_id)
        c = content()
        c['test']='test'
        self.storage.save(self.save_id)
        content = self.storage.load(self.save_id)
        verifyObject(IContent, content)
        self.assertEqual(content['test'].get(),'test')

