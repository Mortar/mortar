from zope.interface import Interface, Attribute

marker = object()

class IContent(Interface):
    """
    All content must implement this schema.
    Security should be checked for each operation.
    """

    id = Attribute(
       """
       A unique identifier, that must be representable as a string,
       for this object across the whole system.

       This may also be None, indicating that it has not yet been
       stored anywhere.
       """
       )

    type = Attribute(
       """
       The type of this IContent. 
       """)

    names = Attribute(
       """
       The names of the fields currently available in this IContent
       """
       )

    def __getitem__(name):
        """
        Get a field of the specified name.
        Returns an object implementing IField.
        """

    def __setitem__(name,value):
        """
        Set a field of the specified name.
        The value may implement IField or be of a type for which a
        converter to IField has been registered.  
        """

    def view(name=None):
        """
        returns the view object or the default view if no name is specified.

        A KeyError is raised if the named view cannot be found or if
        there is no default view available for this IContent.
        """

    def dimension(name,id=None):
        """
        Return the dimension of the specified name with the provided identity.

        eg: c.dimension('revision',1).dimension('language','french')
        """
        
class IField(Interface):
    "A single field of a piece of content"

    def get(as=None,default=marker):
        """
        Return the value of the field in the type specified.
        If the IContent does not have a value, return the default
        specified or, if the default is the marker, the default value
        specified in the content type. If this IContent has no content
        type, return None.
        The type specified must implement IFieldType.
        """

    def set(value,as=None):
        """
        Set this field to the supplied value. If a type is supplied,
        the value will be converted to this type before being
        stored. Any type supplied must implement IFieldType.
        """

    def canSet():
        """
        returns boolean saying whether this field can be set by the current
        user.
        """

    def canGet():
        """
        returns boolean saying whether this field can be accessed by the current
        user.
        """

    def delete():
        """
        Deletes this field from the IContent containing it.
        If a field cannot be deleted, it should be reset to its default value.
        """
        
class ICollection(Interface):
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
        
class IStorage(Interface):
    """
    A physical storage for content objects.
    This could be a relational, file system or zodb storage.
    """

    def store(content):
        """
        This should store the supplied content in the current
        storage.
        If the content is already contained within this storage, then
        any changes made to it should be saved.

        If this storage does not support changing of its content or if
        the supplied content cannot be stored (eg: because it contains
        fields that do not map to a relational table) then a
        mortar.exceptions.NotSupported exception should be raised
        giving appropriate details.
        """

    def load(id):
        """
        This should load the content related to the supplied id.

        If the content does not exist in this storage, a
        mortar.exeptions.NotFound exception should be raised giving
        appropriate details.
        """

class ISearch(Interface):
    """
    """

    def search(query):
        """
        """
        
class IQueryAtom(Interface):
    """
    """
    
class IView(Interface):
    """
    A view control, for accumulating other controls
    """

    def __call__(self):
        """
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

class IFieldType(Interface):
    """
    Not quite sure yet...
    """
    pass



