"""
Test routines for Tomatic.
"""
from os import environ
from typing import Any, Callable, Tuple

import pytest

from . import Tomatic, fix
from .buckets import DummyBucket, EnvironBucket, type_cast

# data types used by test routines
EnvironType = Tuple[str, Any]
EnvironDataType = Tuple[EnvironType, ...]

SampleType = Tuple[str, str, Any]
SampleDataType = Tuple[SampleType, ...]


DUMMY_PROFILE = "DUMMY"
ENVIRON_PROFILE = "ENVIRON"

BUCKET_ENVIRON_LIST: EnvironDataType = (
    ("TEST", "test"),
    ("BOOL", True),
    ("FLOAT", 3.14159),
    ("INT", 10),
    ("JSON", {}),
    ("STR", "abcdef"),
)


def catch_value_error(function_obj: Callable) -> Callable:
    """
    (decorator) Run a function and checks if it raises a `ValueError`
    exception.
    """

    def catch_exception(*args: str, **kvargs: int) -> None:
        """
        Run a function inside a try/except block and do assertion.
        """
        try:
            result: bool = False
            function_obj(*args, **kvargs)

        except ValueError:
            result = True

        assert result

    return catch_exception


@pytest.fixture(scope="module")
def inject_env_variables(request) -> None:
    """
    Fixture to set OS environment variables.
    """
    for key, value in BUCKET_ENVIRON_LIST:
        environ[
            "{profile}__{key}".format(profile=ENVIRON_PROFILE, key=key)
        ] = str(value)


@pytest.fixture(scope="module")
def valid_datatype(request) -> SampleDataType:
    """
    Fixture to return a set of valid datatypes.
    """
    return (
        ("bool", "true", True),
        ("bool", "false", False),
        ("float", "3.14159", 3.14159),
        ("int", "9", 9),
        ("json", '{"a":123}', {"a": 123}),
        ("json", "[]", []),
        ("str", "abc", "abc"),
    )


@pytest.fixture(scope="module")
def invalid_datatype(request) -> SampleDataType:
    """
    Fixture to return a set of invalid datatypes.
    """
    return (
        ("bool", "f", None),
        ("bool", "t r u e", None),
        ("float", "abc", None),
        ("int", "3.14159", None),
        ("json", "abc", None),
        ("????", "abc", "abc"),
    )


class TestTomaticBuckets:
    """
    Class for test bucket classes and functions.
    """

    def test_type_cast(
        self, valid_datatype: SampleDataType, invalid_datatype: SampleDataType
    ) -> None:
        """
        Test if `type_cast` function handles with all supported data types
        and its exceptions.
        """
        for datatypes in [valid_datatype, invalid_datatype]:
            for sample in datatypes:
                # split data
                datatype, value, expected = sample

                # does 'value' conveert to data type 'datatype' is 'expect'?
                assert (type_cast(datatype, value)) == expected

    def test_dummy_bucket_instance(self) -> None:
        """
        Test `DummyBucket` instance creation.
        """
        dummy = DummyBucket(DUMMY_PROFILE)

        # does returns the correct instance?
        assert isinstance(dummy, DummyBucket)
        assert dummy.get("KEY") is None

    def test_environ_bucket_instance(self) -> None:
        """
        Test `EnvironBucket` instance creation.
        """
        env = EnvironBucket(ENVIRON_PROFILE)

        # does returns the correct instance?
        assert isinstance(env, EnvironBucket)

    def test_environ_bucket_get_raw_value(self, inject_env_variables) -> None:
        """
        Test if `EnvironBucket` gets a raw value.
        """
        env = EnvironBucket(ENVIRON_PROFILE)
        key, value = BUCKET_ENVIRON_LIST[0]

        # does returns the correct value?
        assert env.get(key) == value

    def test_environ_bucket_get_value_with_cast(
        self, inject_env_variables
    ) -> None:
        """
        Test if `EnvironBucket` gets a value using type casting.
        """
        env = EnvironBucket(ENVIRON_PROFILE)

        # does returns correct typed values?
        for key, value in BUCKET_ENVIRON_LIST[1:]:
            variable = "{key}__{type}__".format(key=key, type=key.lower())

            assert env.get(variable) == value


class TestTomaticCore:
    """
    Class for test bucket classes and functions.
    """

    @catch_value_error
    def test_tomatic_fail_new_instance(self) -> None:
        """
        Test fail creating a new instance without set a profile.
        """
        Tomatic(DummyBucket)

    @catch_value_error
    def test_tomatic_fail_wrong_bucket_subclass(self) -> None:
        """
        Test fail creating with a not BaseBucket subclass.
        """
        Tomatic(int, static_profile="test")

    def test_tomatic_dummy_new_instance(self) -> None:
        """
        Test a new instance creation using dummy bucket.
        """
        dummy = Tomatic(DummyBucket, static_profile="dummy")

        assert isinstance(dummy, Tomatic)

    def test_tomatic_environ_new_instance(self) -> None:
        """
        Test a new instance creation using environ bucket.
        """
        environ["APP_PROFILE"] = "test"
        env = Tomatic(EnvironBucket, env_profile="APP_PROFILE")

        assert isinstance(env, Tomatic)

    @catch_value_error
    def test_tomatic_fail_exception(self) -> None:
        """
        Test if a custom exception given is an Exception subclass.
        """
        Tomatic(
            DummyBucket,
            static_profile=DUMMY_PROFILE,
            raise_if_none=AssertionError,
        )
        Tomatic(DummyBucket, static_profile=DUMMY_PROFILE, raise_if_none=int)

    def test_tomatic_get_key(self) -> None:
        """
        Test if Tomatic class return a value for a key.
        """
        dummy = Tomatic(DummyBucket, static_profile="dummy")

        assert dummy.get_a_value is None

    @catch_value_error
    def test_tomatic_get_key_with_expeption(self) -> None:
        """
        Test if `None` value raises an expected exceptiopn.
        """
        dummy = Tomatic(
            DummyBucket, static_profile=DUMMY_PROFILE, raise_if_none=ValueError
        )

        dummy.get_a_value

    def test_tomatic_use_fix_for_empty_values(self) -> None:
        """
        Test if '.fix()' method returns correct values for empty results.
        """
        assert fix(False, True) is False
        assert fix(None, True) is True
