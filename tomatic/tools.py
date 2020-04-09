"""
Tools classes and routines.
"""
import json
from typing import Any, List, Union

from .datatypes import GotType, ValueType, ValidValueType, ValueRawType

from .datatypes import (
    TomaticTypeBool,
    TomaticTypeDict,
    TomaticTypeFloat,
    TomaticTypeInt,
    TomaticTypeList,
    TomaticTypeStr,
)

SEP = "__"


class TomaticTypeCast:
    """
    Implements all abstracion logic to convert values to Python data
    types.
    """

    default = None

    def __init__(self, value_raw: ValueRawType) -> None:
        """
        Initialize class receiving value as `value`.
        """
        self.__value: str = ""

        if isinstance(value_raw, bytes):
            # if directly converted by str(), bytearray got an 'b'
            self.__value = value_raw.decode()

        elif value_raw is not None:
            # except by NoneType, use str()
            self.__value = str(value_raw)

    @property
    def as_bool(self) -> TomaticTypeBool:
        """
        Convert `__value` to boolean value.
        """
        if self.__value.lower() == "true":
            return True
        elif self.__value.lower() == "false":
            return False

        return self.default

    @property
    def as_dict(self) -> TomaticTypeDict:
        """
        Convert `__value` to dictionary using JSON module, if convert
        value isn't a list, `self.default` is returned.
        """
        try:
            value: Any = json.loads(self.__value)
            return value if isinstance(value, dict) else self.default

        except json.decoder.JSONDecodeError:
            return self.default

    @property
    def as_float(self) -> TomaticTypeFloat:
        """
        Convert `__value` to floating point number.
        """
        try:
            return float(self.__value)

        except (TypeError, ValueError):
            return self.default

    @property
    def as_int(self) -> TomaticTypeInt:
        """
        Convert `__value` to integer number.
        """
        try:
            return int(self.__value)

        except (TypeError, ValueError):
            return self.default

    @property
    def as_list(self) -> TomaticTypeList:
        """
        Convert `__value` to list using JSON module, if convert value
        isn't a list, `self.default` is returned.
        """
        try:
            value: Any = json.loads(self.__value)
            return value if isinstance(value, list) else self.default

        except json.decoder.JSONDecodeError:
            return self.default

    @property
    def as_str(self) -> TomaticTypeStr:
        """
        Return `__value` as string.
        """
        return self.__value if self.__value else self.default

    @classmethod
    def types(cls) -> List[str]:
        """
        (Class Method) Return all supported data types from this class.
        """
        return [item[3:] for item in dir(cls) if item[0:3] == "as_"]


def fix(value: ValueType, default_value: ValidValueType) -> ValidValueType:
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
        return key, datatype if datatype in TomaticTypeCast.types() else None

    key = key_raw

    return key, None


def type_cast(datatype: str, value_raw: ValueRawType) -> ValidValueType:
    """
    Convert a given string to a specific data type, receive type to
    use as `datatype` and value to convert as `value_raw`. Supported
    data types are hardcoded but you can retrieve them
    fromTomaticTypeCast.types() class method as well.

    There are the following data types supported by buckets:

    * `__bool__` to convert VALUE to a boolean;
    * `__dict__` to convert VALUE to a dictionary;
    * `__float__` to convert VALUE to a floating point number;
    * `__int__` to convert VALUE to a integer number;
    * `__list__` to convert VALUE to dictionaries or lists and
    * `__str__` to convert VALUE to a string (default bahavior).

    Don't forget to keep "type" in lower case. All unrecognized
    data types are treated as string.
    """
    value = TomaticTypeCast(value_raw)

    if datatype == "bool":
        return value.as_bool

    elif datatype == "dict":
        return value.as_dict

    elif datatype == "float":
        return value.as_float

    elif datatype == "int":
        return value.as_int

    elif datatype == "list":
        return value.as_list

    # guess? yes, string...
    return value.as_str
