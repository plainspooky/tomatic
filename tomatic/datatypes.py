"""
Custom datatypes.
"""
from typing import (
    Any,
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

ValueRawType = Union[None, str, bytearray]

ValidValueType = Union[
    None, bool, Dict, List, str, SupportsFloat, SupportsInt
]

ValueType = Union[
    None, bool, bytes, bytearray, Dict[str, Any], List[Any], str, SupportsFloat, SupportsInt
]

TomaticTypeBool = Optional[bool]
TomaticTypelInt = Optional[SupportsInt]
TomaticTypelFloat = Optional[SupportsFloat]
TomaticTypeList = Optional[List[Any]]
TomaticTypelDict = Optional[Dict[str, Any]]
TomaticTypelStr = Optional[str]
