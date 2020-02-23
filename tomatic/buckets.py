"""
Bucket classes and routines.
"""
import json
from os import environ
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

SEP = "__"

TYPES = (
    "bool",
    "float",
    "int",
    "json",
    "str",
)

ValueType = Union[
    None, bool, bytes, bytearray, Dict, List, str, SupportsFloat, SupportsInt
]


class BaseBucket:
    """
    This class implements basic attributes and methods for Buckets.
    """

    ...


class DummyBucket(BaseBucket):
    """
    It's a bucket for test purpose use only, use it to make sure that
    changes didn't break your code. It always returns `None` for all
    KEY you try to get a VALUE.
    """

    def __init__(self, profile: str) -> None:
        """
        Initialize class using profile name as `profile` (but it's
        not used).
        """
        self.__profile = profile

    def get(self, key: str) -> None:
        """
        Receive KEY as `key` and return `None`.
        """
        return None


class EnvironBucket(BaseBucket):
    """
    Uses Operating System environment variables to store KEY/VALUE
    pairs. To set a KEY create an environment variable using the
    following syntax:

    ```
    «PROFILE»>__«KEY»=«VALUE»
    ```

    Where:

    * `PROFILE` is a name that groups KEYS;
    * `KEY` is a name to identify a specific VALUE and
    * `VALUE` is a value itself (dont't care about data types here,
      for **Python** it's a _string_).

    Don't forget that a combinatiom of `profile` and `key` must be
    unique!

    ## Example
    A set of variables, just like on
    [Docker Compose](https://docs.docker.com/compose/) `.env` file:

    ``` shell
    TEST__HOSTNAME=127.0.0.1
    HOMOLOG__HOSTNAME=172.16.20.123
    PRODUCTION__HOSTNAME=app.myapplication.com
    ```

    Here `HOSTNAME` content is **127.0.0.1** for `TEST` profile,
    **172.16.20.123** for`HOMOLOG` and **app.myapplication.com** for
    `PRODUCTION`.
    """

    def __init__(self, profile: str) -> None:
        """
        Initialize class uising profile name as `profile`.
        """
        self.__profile = profile

    def get_type(self, key_raw: str) -> Tuple[str, Optional[str]]:
        """
        Check if there is a data type enconded on KEY as `key_raw`,
        extract data type if exist and check. Return KEY without data
        type encoded and type decoded (if exists) in a _tuple_.

        To force type cast for a giver KEY use:

        ``` shell
        «PROFILE»>__«KEY»__«type»__
        ```

        There are the following data types supported by this bucket:

        * `__bool__` to convert VALUE to a boolean;
        * `__float__` to convert VALUE to a floating point number;
        * `__int__` to convert VALUE to a integer number;
        * `__json__` to convert VALUE to dictionaries or lists and
        * `__str__` to convert VALUE to a string (default bahavior).

        Don't forget to keep "type" in lower case. All unrecognized
        data types are treated as _string_.

        ## Example

        KEYS as set on operating system:

        ``` shell
        HOMOLOG__HOSTNAME="192.168.0.200"
        HOMOLOG__MAX_RESULTS=200
        HOMOLOG__DEBUG=false
        HOMOLOG__HEALTH_CHECK='{"DISK_USAGE_MAX":80,"MEMORY_MIN":200}'
        ```

        **Python** code configured to properly handle with these KEYS:

        ``` python
        from tomatic import Tomaic, fix
        from tomatic.buckets import EnvironBucket

        t = Tomatic(EnvironBucket, static_profile="HOMOLOG")
        ...
        HOSTNAME = t.HOSTNAME__str__ or "localhost"
        MAX_RESULTS = t.MAX_RESULTS__int__ or 10
        DEBUG = t.fix(l.DEBUG__bool__, False)

        HEALTH_CHECK = t.HEALTH_CHECK__json__ or {
            "DISK_USAGE_MAX": 90,
            "MEMORY_MIN": 100,
        }
        ```

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

    def get(self, key_raw: str) -> Any:
        """
        Retrieve VALUE from a given KEY as `key_raw` and return it.
        """
        # filter key name and check fort datatype
        key, datatype = self.get_type(key_raw)

        # get environment variable name
        variable = "{profile}{sep}{key}".format(
            profile=self.__profile, sep=SEP, key=key
        )

        # retrieve environment variable value
        value_raw: Optional[str] = environ.get(variable)

        return type_cast(datatype, value_raw) if datatype else value_raw


def type_cast(datatype: str, value_raw: Union[None, str]) -> Any:
    """
    Convert a given _string_ to a specific data type, receive type to
    use as `datatype` and value to convert as `value_raw`. Supported
    data types are hardcoded here but there are on `TYPES` constant
    as well.
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
            # gues! yes, string...
            return value_raw

    except (AttributeError, TypeError, ValueError):
        ...

    return value
