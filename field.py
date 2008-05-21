from interfaces import IField,marker
from types import text
from zope.interface import implements

class Field:

    value = marker
    
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
    
    def get(self,as=None,default=marker):
        if self.value is marker:
            # xxx content type should figure in here
            if self.default is marker:
                v = None
            else:
                v = default
        else:
            v = self.value
        if as is not None:
            v = as(v)
        return v

    def set(self,value,as=None):
        if as is not None:            
            value = as(value)
        self.value = value
            
    def canSet(self):
        raise NotImplementedError 
        return True

    def canGet(self):
        raise NotImplementedError
        return self.data.has_key(name)

    def delete(self):
        del self.content[self.name]
