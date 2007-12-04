from content import Content
from interfaces import IContent

def search(*args,**kw):
    "returns an IResultSet, spec allows searching, sorting, etc"
    pass

def setRoot():
    "sets the root IContent object"
    
def getRoot():
    "returns the root as an IContent"
    pass

def getById(id):
    "returns the IContent specified by the id"
    pass

def new(type):
    "return a new IContent"
    if not IContent.isImplementedBy(type):
        type = getById(type)
    return Content(type)
