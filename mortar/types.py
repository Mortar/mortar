# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

from datetime import datetime as python_datetime
from datetime import date as python_date

from interfaces import IFieldType

class date(IFieldType):
    pass

class dates:
    pass

class datetime(IFieldType):
    pass

class datetimes:
    pass

class time:
    pass

class times:
    pass

class number(IFieldType):
    pass

class numbers:
    pass

class text(IFieldType):
    pass

class texts:
    pass

class reference(IFieldType):
    pass

class references:
    pass

class binary:
    pass

class_to_type = {
    type(None):None,
    unicode:text,
    int:number,
    python_datetime:datetime,
    python_date:date,
    }

def type(value):
    return class_to_type[value.__class__]
