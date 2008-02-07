from datetime import date
from interfaces import IFieldType
from time import strptime
from types import date as date_type
from zope.component import provideAdapter
from zope.interface import classImplements

classImplements(int,IFieldType)
classImplements(date,IFieldType)

def str_to_date(str):
    # bleugh
    return date(*strptime(str,'%Y/%m/%d')[:3])
    

provideAdapter(str_to_date,(str,),date_type)

import pdb; pdb.set_trace()
