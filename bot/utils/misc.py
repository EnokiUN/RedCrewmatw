from __future__ import annotations
from typing import Optional, TypeVar

T = TypeVar('T')

def unwrap(x: Optional[T]) -> T:
    """
    A function inspired by Rust's Option::unwrap.

    If the argument is None, raise a ValueError else, returns the value.
    """
    if x is None:
        raise ValueError("Found None.")
    return x
