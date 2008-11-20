# Copyright (c) 2007-2008 Simplistix Ltd
# See license.txt for license details.

from content import Content
from interfaces import IContent

def content():
    return Content()

# bleugh
import convertors

def search(query,sort=None):
    "returns an IResultSet, spec allows searching, sorting, etc"
    pass

def get(id):
    "returns the IContent specified by the id"
    pass

def store(content):
    "stores the supplied content object"
