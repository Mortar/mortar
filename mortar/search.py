# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

"""
Stuff to allow building of complicated search specs.
"""

class Operator:

    def __init__(self,*args):
        self.args = args
        
    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__,','.join([repr(a) for a in self.args]))

    
class AND(Operator): pass

class OR(Operator): pass

class BinaryOperator:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return '<%r %s %r>' % (self.x,self.__class__.__name__,self.y)

    
class OR(Operator): pass

class EQ(Operator): pass

class NE(Operator): pass

class LT(Operator): pass

class GT(Operator): pass
