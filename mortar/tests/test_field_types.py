# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

import unittest

from datetime import datetime, date, time
from mortar import types
from mortar.interfaces import empty
from fixtures import check

class TestType(unittest.TestCase):

    # object -> type, we use a tuple of tuples as dicts are unhashable,
    mapping = (
        (None                    ,None),
        # should never have an empty sequence returned
        (()                      ,IndexError('tuple index out of range')),
        # should never have a None sequence
        ((None,)                 ,KeyError(type(None))), 
        (datetime(2008,1,1,20,00),types.datetime),
        # the type function is happy with lists or tuples
        ((datetime(2008,1,1,20),),types.datetimes),
        (date(2008,1,1)          ,types.date),
        ([date(2008,1,1)]        ,types.dates),
        (time(20,00)             ,types.time),
        ([time(20,00)]           ,types.times),
        (0                       ,types.number),
        (0.0                     ,types.number),
        ([0]                     ,types.numbers),
        ([0.0]                   ,types.numbers),
        # the type function only looks at the first element of sequences,
        # as it's only designed to be called with sane data
        ([0,'']                  ,types.numbers),
        (u'text'                 ,types.text),
        ([u'text']               ,types.texts),
        # XXX reference(s)?
        ('a string'              ,types.binary),
        (['a string']            ,types.binaries),
        (empty                   ,None)
        )

    def test_type(self):
        errors = []
        for o,e in self.mapping:
            check(types.type,o,e,errors)
        if errors:
            self.fail('Type mapping not as expected:\n'+('\n'.join(errors)))



def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestType),
        ))
