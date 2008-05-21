from field import Field
from interfaces import IContent,IField,IFieldType
from types import reference
from zope.interface import implements

class Content:

    implements(IContent,reference) # the reference bit is likely not a good idea!

    id = None

    def __init__(self):
        self.data = {}

    def __getitem__(self,name):
        if not self.data.has_key(name):
            self.data[name] = Field(self,name)
        return self.data[name]

    def __setitem__(self,name,value):
        field = Field(self,name)
        if IField.providedBy(value):
            field.set(value.get())
        else:
            field.set(IFieldType(value))
        self.data[name]=field

    def __delitem__(self,name):
        del self.data[name]
        
    @property
    def names(self):
        return self.data.keys()

    @property
    def type(self):
        return None
        raise NotImplementedError

    def view(self,name=None):
        raise NotImplementedError
        
    def dimension(self,name,id=None):
        raise NotImplementedError
