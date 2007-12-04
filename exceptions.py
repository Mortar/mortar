class NotPossible(Exception):
    """
    Base class for things that didn't work
    """

class NotAllowed(NotPossible):
    """
    User nto authorised to perform action.
    """

class NotFound(NotPossible):
    """
    No value was found
    """
    
class NotSupported(NotPossible):
    """
    This action is never going to be possible.
    ie:writing to field not present in rdb column.
    """

