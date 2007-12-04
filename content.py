from exceptions import NotFound
from interfaces import IContent,marker
from zope.interface import implements

class Content:

    implements(IContent)

    id = None

    def __init__(self,type):
        self.type = type
        self.data = {}

    def __getitem__(self,name):
        return self.get(name)

    def __setitem(self,name,value):
        self.data[name]=value

    def get(self,name,default=marker,asType=None):
        v = self.data.get(name,default)
        if v is marker:
            raise NotFound(name)
        # XXX asType?
        return v

    def set(self,name,value,asType=None):
        # XXX asType?
        self.data[name]=value
            
    def canSet(name):
        return True

    def canGet(name):
        return self.data.has_key(name)

    
        
