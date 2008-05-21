# Copyright (c) 2007-2008 Simplistix Ltd
#
# All rights reserved.

from content import Content
from interfaces import IContent

def content():
    return Content()

# bleugh
import convertors

def search(*args,**kw):
    "returns an IResultSet, spec allows searching, sorting, etc"
    pass

def get(id):
    "returns the IContent specified by the id"
    pass

def store(content):
    "stores the supplied content object"
