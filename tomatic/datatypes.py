"""
Custom datatypes.
"""
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    SupportsFloat,
    SupportsInt,
)

GotType = Tuple[str, Optional[str]]

RaiseIfNoneType = Optional[type]

ValueRawType = Union[None, str]

ValueType = Union[
    None, bool, bytes, bytearray, Dict, List, str, SupportsFloat, SupportsInt
]
