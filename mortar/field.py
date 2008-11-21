# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from interfaces import IField,IFieldType
from types import text,type
from zope.interface import implements

class Field:

    implements(IField)

    def __init__(self,content,name):
        self.content = content
        self.name = name
    
    def __unicode__(self):
        return text(self.content.data.get(self.name))

    def __repr__(self):
        return '<Field %r containing %r>' % (
            self.name,
            self.content.data.get(self.name)
            )
    
    def get(self,default=None,type=None):
        v = self.content.data.get(self.name)
        if v is None:
            v = default
        if v is None:
            return v
        if type is not None:
            return type(v)
        return v

    def set(self,value,type=IFieldType):
        self.content[self.name]=type(value)
            
    @property
    def type(self):
        return type(self.content.data.get(self.name))
    
    def canSet(self,user=None):
        raise NotImplementedError 
        return True

    def canGet(self,user=None):
        raise NotImplementedError
        return self.data.has_key(name)

    def delete(self):
        del self.content[self.name]
