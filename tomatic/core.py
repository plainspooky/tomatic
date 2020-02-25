"""
Core class and functions.
"""
from os import environ
from typing import Any, Callable, Optional

from .buckets import BaseBucket
from .datatypes import RaiseIfNoneType


class Tomatic:
    """
    Implements the main logic of Tomatic library.
    """

    def __init__(
        self,
        bucket: type,
        static_profile: str = "",
        env_profile: str = "",
        raise_if_none: RaiseIfNoneType = None,
        bucket_args: dict = {},
    ) -> None:
        """
        Initialize class receiving bucket object as `bucket` and profile
        in `static_profile` **or** as `env_profile`. Optionaly receive
        an exception to be raised in case of `None` values.
        """
        self.__exception: RaiseIfNoneType = None
        self.__raise: bool = False

        # does get profile from environment variable or by name?
        profile = environ.get(env_profile) or static_profile

        if profile:
            if issubclass(bucket, BaseBucket):
                self.__bucket: Callable = bucket(profile, bucket_args)
            else:
                raise ValueError("Bucket must be a subclass of 'BaseBucket'!")

            if raise_if_none:
                if issubclass(raise_if_none, Exception):
                    self.__raise = True
                    self.__exception = raise_if_none
                else:
                    raise ValueError(
                        "`raise_if_none` must be subclass of 'Exception'."
                    )
        else:
            raise ValueError("A profile hasn't defined!")

    def __getattr__(self, key: str) -> Any:
        """
        Override standard __getattr__ method to provide dynamic
        attributes. Check if `self.__exception` is set and raise an
        exceception pointed by its content if value returned is `None`.
        """
        value: Any = self.__bucket.get(key)

        if self.__raise and (value is None):
            # raise an exception if value is None
            raise self.__exception(
                "Undefined value for '{key}' key!".format(key=key)
            )

        return value
