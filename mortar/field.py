# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from interfaces import IField,IFieldType
from types import text,type
from zope.interface import implements

class Field:

    value = None
    
    implements(IField)

    def __init__(self,content,name):
        self.content = content
        self.name = name
    
    def __unicode__(self):
        return text(self.value)

    def __repr__(self):
        return '<Field %r containing %r>' % (
            self.name,
            self.value
            )
    
    def get(self,default=None,type=None):
        if self.value is None:
            v = default
        else:
            v = self.value
        if v is None:
            return v
        if type is not None:
            return type(v)
        return v

    def set(self,value,type=IFieldType):
        self.value = type(value)
            
    @property
    def type(self):
        return type(self.value)
    
    def canSet(self,user=None):
        raise NotImplementedError 
        return True

    def canGet(self,user=None):
        raise NotImplementedError
        return self.data.has_key(name)

    def delete(self):
        del self.content[self.name]
