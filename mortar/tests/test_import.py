# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

# check all source modules are importable.

import mortar
import os
import unittest

class TestImports(unittest.TestCase):

    def test_imports(self):
        rootdir = os.path.dirname(mortar.__file__)
        for dirpath,dirnames,filenames in os.walk(rootdir):
            path = dirpath[len(rootdir):]
            segments = path.split(os.sep)
            if '.svn' in segments:
                continue
            base = 'mortar'+'.'.join(segments)
            for filename in filenames:
                if not filename.endswith('.py') or filename.startswith('__init__'):
                    continue
                __import__(base+'.'+filename[:-3])
        
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestImports),
        ))
        
