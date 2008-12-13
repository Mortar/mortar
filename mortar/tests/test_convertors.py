# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

import datetime
import unittest

from fixtures import identity,check
from mortar import types
from mortar.interfaces import IFieldType

class TestConvertors(unittest.TestCase):

    # type -> [(source,expected),...]
    mapping = {
        types.datetime: [
            ('2008/01/01',datetime.datetime(2008, 1, 1, 0, 0)),
            (identity,TypeError('Could not adapt',identity,types.datetime)),
        ],
        types.datetimes: [
        ],
        types.date: [
        ],
        types.dates: [
        ],
        types.time: [
        ],
        types.times: [
        ],
        types.number: [
            (1.0,identity),
        ],
        types.numbers: [
        ],
        types.text: [
           ('some text' ,u'some text'),
           (u'a unicode',identity),
           (1           ,u'1'),
        ],
        types.texts: [
        ],
        types.reference: [
        ],
        types.references: [
        ],
        types.binary: [
        ],
        types.binaries: [
        ],
        # this is a special type that means "give me whatever is stored but
        # as a sequence"
        types.sequence: [
            ('some text'                      ,(u'some text',)),
            (u'unicode'                       ,(u'unicode',)),
            (1                                ,(1,)),
            (1.0                              ,(1.0,)),
            (datetime.date(2008,1,1)          ,(datetime.date(2008,1,1),)),
            ((datetime.date(2008,1,20),)      ,identity),
            ((datetime.datetime(2008,1,1,20),),identity),
            ([datetime.time(20,00)]           ,identity),
            ([0]                              ,identity),
            ([0.0]                            ,identity),
            ([0,'']                           ,identity),
            ([u'text']                        ,identity),
        ]
    }
    
    def test_convertors(self):
        # This tests explicit casting to a particular type
        errors = []
        for t,s2e in self.mapping.items():
            for s,e in s2e:
                check(t,s,e,errors)
        if errors:
            self.fail('Conversion not as expected:\n'+('\n'.join(errors)))

class TestConversion(unittest.TestCase):

    # expected -> actual, tuples as lists can't be hashed
    mapping = [
        ('some text',u'some text'),
        (u'some text',identity),
        (1.0,identity),
        ]
    
    def test_conversion(self):
        # This tests the precedence of the convertors when an object is
        # converted to IFieldType.
        # This currently runs from global config, but really should run 
        # from some kind of test setup.
        errors = []
        for s,e in self.mapping:
            check(IFieldType,s,e,errors)
        if errors:
            self.fail('Conversion not as expected:\n'+('\n'.join(errors)))

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestConvertors),
        unittest.makeSuite(TestConversion),
        ))
