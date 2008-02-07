from field import Field
from interfaces import IContent,IField,IFieldType
from zope.interface import implements

class Content:

    implements(IContent)

    id = None

    def __init__(self):
        self.data = {}

    def __getitem__(self,name):
        if not self.data.has_key(name):
            self.data[name] = Field()
        return self.data[name]

    def __setitem__(self,name,value):
        if not IField.implementedBy(value):
            v = IFieldType(value)
            value = Field()
            value.set(v)
        self.data[name]=IField(value)

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
