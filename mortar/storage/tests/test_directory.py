# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

import os.path
import unittest

from common import ReadOnlyStorageTests,WriteableStorageTests
from mortar.storage.directory import Storage

test_dir = os.path.split(__file__)[0]
class StorageDirectoryTests(ReadOnlyStorageTests):

    def setUp(self):
        self.storage = Storage(os.path.join(test_dir,'data','directory'))

    def test_directory_does_not_exist(self):
        self.assertRaises(ValueError,Storage,os.path.join(test_dir,'does_not_exist'))

    def test_xml_in_field(self):
        self.assertEqual(
            self.storage.load('test')['testxml'].get(),
            'some <xml>things\n</xml> different.'
            )

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(StorageDirectoryTests),
        ))
