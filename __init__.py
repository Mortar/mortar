# Copyright (c) 2007-2008 Simplistix Ltd
#
# All rights reserved.

from content import Content
from interfaces import IContent

def content():
    return Content()

# bleugh
import convertors

## def search(*args,**kw):
##     "returns an IResultSet, spec allows searching, sorting, etc"
##     pass

## def getById(id):
##     "returns the IContent specified by the id"
##     pass

## def new(type):
##     "return a new IContent"
##     if not IContent.isImplementedBy(type):
##         type = getById(type)
##     return Content(type)
