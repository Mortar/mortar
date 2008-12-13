# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from datetime import date
from dateutil.parser import parse
from interfaces import IFieldType,empty
from time import strptime
from types import date as date_type
from types import datetime as datetime_type
from types import not_sequence
from types import number as number_type
from types import reference
from types import text as text_type
from types import texts
from types import type as type_of

from zope.component import provideAdapter
from zope.interface import classImplements

classImplements(unicode,text_type)
classImplements(int,number_type)
classImplements(float,number_type)
classImplements(date,date_type)

def str_to_text(str):
    # bleugh
    return unicode(str)
    
def str_to_datetime(str):
    # should be configurable
    return parse(str,dayfirst=True)
    
def str_to_date(str):
    return str_to_datetime(str).date()

def str_to_time(str):
    return str_to_datetime(str).time()
    
def date_to_text(date):
    # bleugh
    return unicode(date.strftime('%Y/%m/%d'))

def reference_to_text(ref):
    return u'Reference to '+unicode(ref.id)

def obj_to_sequence(obj):
    return (obj,)

def sequence_to_sequence(s):
    if not s:
        return empty
    type = type_of(IFieldType(s[0]))
    try:
        for i in s:
            type(i)
    except TypeError:
        raise TypeError('Sequences must be of one type, could not '
                        'convert %r to %r' %  (
            i,
            type
            ))
    return s
        
    
# NB: order matters here :-S
provideAdapter(str_to_date,(str,),date_type)
provideAdapter(str_to_datetime,(str,),datetime_type)
provideAdapter(date_to_text,(date,),text_type)
provideAdapter(obj_to_sequence,(text_type,),texts)
provideAdapter(sequence_to_sequence,(tuple,),IFieldType)
provideAdapter(sequence_to_sequence,(list,),IFieldType)
provideAdapter(str_to_text,(str,),text_type)
provideAdapter(unicode,(int,),text_type)
provideAdapter(reference_to_text,(reference,),text_type)
