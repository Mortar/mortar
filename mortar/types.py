# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

import datetime as python_datetime

from interfaces import IFieldType

class datetime(IFieldType):
    pass

class datetimes:
    pass

class date(IFieldType):
    pass

class dates:
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

class binaries:
    pass

class_to_type_singular = {
    type(None):None,
    python_datetime.datetime:datetime,
    python_datetime.date:date,
    python_datetime.time:time,
    int:number,
    float:number,
    unicode:text,
    str:binary,
    }

class_to_type_plural = {
    python_datetime.datetime:datetimes,
    python_datetime.date:dates,
    python_datetime.time:times,
    int:numbers,
    float:numbers,
    unicode:texts,
    str:binaries,
    }

def type(value):
    if isinstance(value,(list,tuple)):
        value = value[0]
        mapping = class_to_type_plural
    else:
        mapping = class_to_type_singular
    return mapping[value.__class__]
