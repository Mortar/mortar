# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from datetime import date
from interfaces import IFieldType,IContent
from time import strptime
from types import date as date_type
from types import number as number_type
from types import reference
from types import text as text_type

from zope.component import provideAdapter
from zope.interface import classImplements

classImplements(unicode,text_type)
classImplements(int,number_type)
classImplements(date,date_type)

def str_to_text(str):
    # bleugh
    return unicode(str)
    
def str_to_date(str):
    # bleugh
    return date(*strptime(str,'%Y/%m/%d')[:3])
    
def date_to_text(date):
    # bleugh
    return unicode(date.strftime('%Y/%m/%d'))

def reference_to_text(ref):
    return u'Reference to '+unicode(ref.id)

# NB: order matters here :-S
provideAdapter(str_to_date,(str,),date_type)
provideAdapter(date_to_text,(date,),text_type)
provideAdapter(str_to_text,(str,),text_type)
provideAdapter(str_to_text,(str,),text_type)
provideAdapter(reference_to_text,(reference,),text_type)
