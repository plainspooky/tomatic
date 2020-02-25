"""
Bucket classes and routines.
"""
from os import environ
from typing import Any

from .datatypes import ValueType, ValueRawType
from .tools import SEP, TYPES, get_type, type_cast


class BaseBucket:
    """
    This class implements basic attributes and methods for Buckets.
    """

    def get(self, key: str) -> None:
        """
        Receive KEY as `key` and return `None`.
        """
        return None


class DummyBucket(BaseBucket):
    """
    It's a bucket for test purpose use only, use it to make sure that
    changes didn't break your code. It always returns `None` for all
    KEY you try to get a VALUE.
    """

    def __init__(self, profile: str, args: dict = {}) -> None:
        """
        Initialize class using profile name as `profile` (but it's
        not used).
        """
        self.__profile = profile
        self.__args = args


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

    def __init__(self, profile: str, args: dict = {}) -> None:
        """
        Initialize class uising profile name as `profile`.
        """
        self.__profile = profile
        self.__args = args

    def get(self, key_raw: str) -> Any:
        """
        Retrieve VALUE from a given KEY as `key_raw` and return it.

        To force type cast for a giver KEY use:

        ``` shell
        «PROFILE»>__«KEY»__«type»__
        ```

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
        """
        # filter key name and check fort datatype
        key, datatype = get_type(key_raw)

        # get environment variable name
        variable = "{profile}{sep}{key}".format(
            profile=self.__profile, sep=SEP, key=key
        )

        # retrieve environment variable value
        value_raw: ValueRawType = environ.get(variable)

        return type_cast(datatype, value_raw) if datatype else value_raw
