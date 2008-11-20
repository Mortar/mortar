# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

class NotPossible(Exception):
    """
    Base class for things that didn't work
    """

class NotAllowed(NotPossible):
    """
    User not authorised to perform action.
    """

class NotFound(NotPossible):
    """
    No value was found
    """
    
class NotSupported(NotPossible):
    """
    This action is never going to be possible.
    ie:writing to field whose name does not have a matching relational column.
    """

