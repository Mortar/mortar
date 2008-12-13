# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from datetime import date
from dateutil.parser import parse
from interfaces import IFieldType,IContent
from time import strptime
from types import date as date_type
from types import datetime as datetime_type
from types import not_sequence
from types import number as number_type
from types import reference
from types import sequence
from types import text as text_type

from zope.component import provideAdapter
from zope.interface import classImplements

classImplements(unicode,text_type)
classImplements(int,number_type)
classImplements(float,number_type)
classImplements(date,date_type)
classImplements(tuple,sequence)
classImplements(list,sequence)

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

def to_sequence(obj):
    return (not_sequence(obj),)

# NB: order matters here :-S
provideAdapter(to_sequence,(None,),sequence)
provideAdapter(str_to_date,(str,),date_type)
provideAdapter(str_to_datetime,(str,),datetime_type)
provideAdapter(date_to_text,(date,),text_type)
provideAdapter(str_to_text,(str,),text_type)
provideAdapter(unicode,(int,),text_type)
provideAdapter(reference_to_text,(reference,),text_type)
