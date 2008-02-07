from interfaces import IField,marker
from zope.interface import implements

class Field:

    value = marker
    
    implements(IField)

    
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
            raise NotImplementedError            
        return v

    def set(self,value,as=None):
        # xxx type conversion should go in here
        if as is not None:            
            value = as(value)
        self.value = value
            
    def canSet(self):
        raise NotImplementedError 
        return True

    def canGet(self):
        raise NotImplementedError
        return self.data.has_key(name)

