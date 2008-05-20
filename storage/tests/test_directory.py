# Copyright (c) 2008 Simplistix Ltd
#
# All rights reserved.

import unittest

from common import ReadOnlyStorageTests

class StorageDirectoryTests(ReadOnlyStorageTests):

    pass

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(StorageDirectoryTests),
        ))
