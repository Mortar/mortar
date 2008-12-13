# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from testfixtures import Comparison

class Identity:
    def __repr__(self):
        return '<identity>'

identity = Identity()

def check(callable,arg,expected,errors):
    try:
        actual = callable(arg)
    except Exception,ex:
        actual = Comparison(ex)
    base = 'Expected %r of %r %%s %r, but was %r' % (
        callable,arg,expected,actual
        )
    if expected is identity:
        if actual is not arg:
            errors.append(base%('to be'))
    else:
        if actual!=expected:
            errors.append(base%('equal to'))
