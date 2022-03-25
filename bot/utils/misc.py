from __future__ import annotations
from typing import Optional, TypeVar

T = TypeVar('T')

class NotFound(Exception):
    """
    An exception that is raised when a variable is not found.
    """
    pass

def unwrap(var: Optional[T]) -> T:
    """
    A function that returns the value of a variable if it is not None, otherwise raises a NotFound exception.

    Parameters
    ----------
    var: Optional[Any]
        The variable to unwrap.
    """
    if var is None:
        raise NotFound()
    return var
