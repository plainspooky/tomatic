"""
Tools classes and routines.
"""
import json
from typing import Any

from .datatypes import GotType, ValueType, ValueRawType

SEP = "__"

TYPES = (
    "bool",
    "float",
    "int",
    "json",
    "str",
)


def fix(value: Any, default_value: Any) -> Any:
    """
    Force a correct behavior for boolean and other empty values, get
    retrieved value as `value` and default value as `default_value`.
    Return retrieved value if isnt's `None`, otherwise use default
    value.
    """
    return value if value is not None else default_value


def get_type(key_raw: str) -> GotType:
    """
    Check if there is a data type enconded on KEY as `key_raw`,
    extract data type if exist and check. Return KEY without data
    type encoded and type decoded (if exists) in a _tuple_.

    To avoid mistakes handling with boolean or even empty values,
    use `Tomatic.fix()` function.
    """
    # check if key name finishes with separator
    if key_raw[-2:] == SEP:
        # split key from bucket and datatype
        key, datatype, __ = key_raw.split(SEP)
        # and return key and its datatype (if supported)
        return key, datatype if datatype in TYPES else None

    key = key_raw

    return key, None


def type_cast(datatype: str, value_raw: ValueRawType) -> Any:
    """
    Convert a given string to a specific data type, receive type to
    use as `datatype` and value to convert as `value_raw`. Supported
    data types are hardcoded here but there are on `TYPES` constant
    as well.

    There are the following data types supported by buckets:

    * `__bool__` to convert VALUE to a boolean;
    * `__float__` to convert VALUE to a floating point number;
    * `__int__` to convert VALUE to a integer number;
    * `__json__` to convert VALUE to dictionaries or lists and
    * `__str__` to convert VALUE to a string (default bahavior).

    Don't forget to keep "type" in lower case. All unrecognized
    data types are treated as string.
    """
    value: ValueType = None

    try:
        if datatype == "bool":
            if str(value_raw).lower() == "true":
                value = True
            elif str(value_raw).lower() == "false":
                value = False

        elif datatype == "float":
            return float(str(value_raw))

        elif datatype == "int":
            return int(str(value_raw))

        elif datatype == "json":
            return json.loads(str(value_raw))

        else:
            # guess! yes, string...
            return value_raw

    except (AttributeError, TypeError, ValueError):
        ...

    return value
