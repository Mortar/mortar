# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from field import Field
from interfaces import IContent,IField,IFieldType,empty
from types import reference
from zope.interface import implements

class Content:

    implements(IContent,reference) # the reference bit is likely not a good idea!

    id = None

    def __init__(self):
        self.data = {}

    def __getitem__(self,name):
        return Field(self,name)

    def __setitem__(self,name,value):
        if IField.providedBy(value):
            value = value.get()
        elif value is empty:
            value = None
        else:
            value = IFieldType(value)
            if value is empty:
                value = None
        self.data[name]=value

    def __delitem__(self,name):
        del self.data[name]
        
    @property
    def names(self):
        return sorted(self.data.keys())

    @property
    def type(self):
        return None

    def view(self,name=None):
        raise NotImplementedError
        
    def dimension(self,name,id=None):
        raise NotImplementedError
