# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

import os.path

from lxml import etree
from mortar import content
from mortar.interfaces import IStorage
from mortar.exceptions import NotSupported,NotFound
from zope.interface import implements

class Storage:

    implements(IStorage)

    def __init__(self,directory):
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            raise ValueError('%r does not exist' % directory)
        self.directory = directory
        
    def load(self,id):
        path = os.path.join(self.directory,id)+'.xml'
        if not os.path.exists(path):
            raise NotFound('No content with id %r could be found'%id)
        c = content()
        t = etree.parse(open(path))
        for e in t.xpath('field'):
            value = e.text
            for child in e:
                value += etree.tostring(child)
            c[e.get('name')]=value
        return c

    def save(self,content):
        raise NotSupported('Cannot save as this storage is read only.')
