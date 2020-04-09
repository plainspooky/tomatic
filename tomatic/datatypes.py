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

TomaticTypeBool = Optional[bool]
TomaticTypeInt = Optional[SupportsInt]
TomaticTypeFloat = Optional[SupportsFloat]
TomaticTypeList = Optional[List[Any]]
TomaticTypeDict = Optional[Dict[str, Any]]
TomaticTypeStr = Optional[str]

ValueRawType = Union[None, str, bytes]

ValidValueType = Union[None, bool, Dict, List, str, SupportsFloat, SupportsInt]

ValueType = Union[
    None,
    bool,
    bytes,
    Dict[str, Any],
    List[Any],
    str,
    SupportsFloat,
    SupportsInt,
]
