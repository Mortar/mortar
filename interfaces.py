#from zope.app.container.interfaces import IContainer,IContainer
from zope.interface import Interface, Attribute

marker = object()

class IIdentifier(Interface):

    storage = Attribute("""
              The name the storage was registered with in the storage module.
              """)
    
    name = Attribute("""
           """)

    def __str__(self):
        """
        """


class IContent(Interface):
    """
    Represents a content object with a dynamic, persistent schema.
    Security should be checked for each operation.
    """

    id = Attribute("""
         A unique identifier, that must be representable as a string,
         for this object across the whole site.

         This may also be None, indicating that it has not yet been
         stored anywhere.
         """)

    type = Attribute("""
           The type of this IContent. 
           """)

    names = Attribute("""
            The names currently available in this IContent
            """)

    def __getitem__(name):
        """
        can raise various things
        """

    def __setitem__(name,value):
        """
        can raise various things
        """

    def get(name,default=marker,asType=None):
        """
        can raise various things
        """

    def set(name,value,asType=None):
        """
        can raise various things
        """

    def view(name=None):
        """
        returns the view object or the default view if no name is specified.
        """

    def dimension(name,id=None):
        """
        Return the dimension of the specified name with the provided identity.

        eg: c.dimension('revision',1).dimension('language','french')
        """
        
    def canSet(name):
        """
        returns boolean saying whether the name can be set by the current
        user.
        """

    def canGet(name):
        """
        returns boolean saying whether the name can be accessed by the current
        user.
        """

class IResultSet(Interface):
    """
    The result of a search
    """

    def __len__():
        """
        The number of results in this set
        """

    def __getitem__(i):
        """
        Return the i'th item in this sequence
        """
    
    def filter(*args,**kw):
        """
        Filter this result set.
        """

    def sort(*args,**kw):
        """
        Sort this result set.
        """

    def add(value):
        """
        value can be an id or an IContent.
        """

    def remove(value):
        """
        value can be an id or an IContent.
        """
        
class IView(Interface):#zope3viewthingy,IControl):
    """
    A view control, for accumulating other controls
    """

    controls = Attribute(
        """
        dict? containing all sub-controls
        """)
        
    def __call__(self):
        pass

class IStorage(Interface):#IContainer):
    """
    A physical storage for content objects.
    This could be a relational, file system or zodb storage.
    Whatever implements IContentStorage is responsible for managing
    transactional integrity.

    The keys used in all IContainer methods are uids for IContentObjects
    """

    def search(search):
        """
        Provides a way to access the most efficient search infrastructure
        of the underlyings storage.

        eg: SELECT statements for a relational storage

        'search' must implement either ISearch or an interface for the storage
        in question.

        ie: when writing a storage, an adapter from ISearch must be provided
            to the interface describing the low level search terms.
            Alternatively, specific low level search terms can be provided
            directly.
        """

    def getByName(name):
        """
        """
        
"""
search utility
  |
  \/
vyper-based indexing
  |
  \/
storage-based indexing
"""

class IControl(Interface):
    """
    A control for inserting into things.

    Namespace isolation?

    Form processing?

    Urls?
    """

    #data = Attribute()

    def getUrl():
        """
        url for control interaction
        """
        
    def render():
        """
        """


