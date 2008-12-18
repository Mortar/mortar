# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

import datetime
import unittest

from fixtures import identity,check
from mortar import types
from mortar.interfaces import IFieldType,empty

class TestConvertors(unittest.TestCase):

    # type -> [(source,expected),...]
    mapping = {
        types.datetime: [
            ('2008/02/01'                       ,datetime.datetime(2008, 2, 1, 0, 0)),
            (identity                           ,TypeError('Could not adapt',identity,types.datetime)),
            (datetime.datetime(2008, 2, 1, 0, 0),identity),
            ('junk'                             ,TypeError('Could not adapt','junk',types.datetime)),
        ],
        types.datetimes: [
        ],
        types.date: [
            ('2008/02/01'                       ,datetime.date(2008, 2, 1)),
            ('junk'                             ,TypeError('Could not adapt','junk',types.date)),
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
           (1.0         ,u'1.0'),
           (datetime.datetime(2008, 1, 2, 0, 0),'2008/01/02 00:00:00'),
           (datetime.date(2008, 1, 2)          ,'2008/01/02'),
           (None                               ,'')
        ],
        types.texts: [
           (datetime.datetime(2008, 1, 2, 0, 0)   ,(u'2008/01/02 00:00:00',)),
           (datetime.date(2008, 1, 2)             ,(u'2008/01/02',)),
           ([datetime.datetime(2008, 1, 2, 0, 0)] ,[u'2008/01/02 00:00:00']),
           ((datetime.date(2008, 1, 2),)          ,[u'2008/01/02']),
           # this ambiguosity will be hard :-S
           ('text'                             ,TypeError('Could not adapt','text',types.texts)),
           (u'text'                            ,(u'text',)),
           (1                                  ,(u'1',)),
           (1.0                                ,(u'1.0',)),
           (None                               ,[])
        ],
        types.reference: [
        ],
        types.references: [
        ],
        types.binary: [
        ],
        types.binaries: [
        ],
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
        ('some text'                           ,u'some text'),
        (u'some text'                          ,identity),
        (1.0,identity)                         ,
        (['some text']                         ,[u'some text']),
        (('some text',)                        ,(u'some text',)),
        (()                                    ,empty),
        ([]                                    ,empty),
        ([u'some text']                        ,identity),
        ((u'some text',)                       ,identity),
        ((1,'x')                               ,TypeError("Sequences must be of one type, could not convert 'x' to <InterfaceClass mortar.types.number>")),
        ([1,'x']                               ,TypeError("Sequences must be of one type, could not convert 'x' to <InterfaceClass mortar.types.number>")),
        (datetime.datetime(2008, 1, 2, 0, 0)   ,identity),
        (datetime.date(2008, 1, 2)             ,identity),
        ([datetime.datetime(2008, 1, 2, 0, 0)] ,[datetime.datetime(2008, 1, 2, 0, 0)]),
        ((datetime.datetime(2008, 1, 2, 0, 0),),(datetime.datetime(2008, 1, 2, 0, 0),)),
        ([datetime.date(2008, 1, 2)]           ,[datetime.date(2008, 1, 2)]),
        ((datetime.date(2008, 1, 2),)          ,(datetime.date(2008, 1, 2),)),
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
