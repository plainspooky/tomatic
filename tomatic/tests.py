"""
Test routines for Tomatic.
"""
from os import environ
from typing import Any, Callable, Tuple

import pytest

from . import Tomatic, fix
from .buckets import DummyBucket, EnvironBucket, type_cast
from .helpers import TomaticTypeCast

# data types used by test routines
EnvironType = Tuple[str, Any]
EnvironDataType = Tuple[EnvironType, ...]

SampleType = Tuple[str, str, Any]
SampleDataType = Tuple[SampleType, ...]


DUMMY_PROFILE = "DUMMY"
ENVIRON_PROFILE = "ENVIRON"

# reflect from environment list on 'before_tests.d'
BUCKET_ENVIRON_LIST: EnvironDataType = (
    ("TEST", "test"),
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
def valid_datatype(request) -> SampleDataType:
    """
    Fixture to return a set of valid datatypes.
    """
    return (
        ("bool", "true", True),
        ("dict", '{"a":123}', {"a": 123}),
        ("bool", "false", False),
        ("float", "3.14159", 3.14159),
        ("int", "9", 9),
        ("list", "[]", []),
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
        ("dict", "{'a':2}", None),
        ("float", "abc", None),
        ("int", "3.14159", None),
        ("list", "abc", None),
        ("????", "abc", "abc"),
    )


class TestTomaticBuckets:
    """
    Class for test bucket classes and functions.
    """

    def test_if_type_cast_handle_supported_data_types(
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
                print("->", value, " = ", expected)
                # does 'value' convert to data type 'datatype' is 'expect'?
                assert (type_cast(datatype, value)) == expected

    def test_dummy_bucket_new_instance(self) -> None:
        """
        Test `DummyBucket` instance creation.
        """
        dummy = DummyBucket(DUMMY_PROFILE)

        # does returns the correct instance?
        assert isinstance(dummy, DummyBucket)
        assert dummy.get("KEY") is None

    def test_environ_bucket_new_instance(self) -> None:
        """
        Test `EnvironBucket` instance creation.
        """
        env = EnvironBucket(ENVIRON_PROFILE)

        # does returns the correct instance?
        assert isinstance(env, EnvironBucket)

    def test_if_environ_bucket_get_raw_value(self) -> None:
        """
        Test if `EnvironBucket` gets a raw value.
        """
        env = EnvironBucket(ENVIRON_PROFILE)
        key, value = BUCKET_ENVIRON_LIST[0]

        # does returns the correct value?
        assert env.get(key) == value

    def test_if_environ_bucket_get_value_with_cast(self) -> None:
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
    def test_tomatic_fail_if_instance_are_missing_argments(self) -> None:
        """
        Test fail creating a new instance without set a profile.
        """
        Tomatic(DummyBucket)

    @catch_value_error
    def test_tomatic_fail_with_wrong_bucket_subclass(self) -> None:
        """
        Test fail creating with a not BaseBucket subclass.
        """
        Tomatic(int, static_profile="test")

    def test_tomatic_with_dummy_new_instance(self) -> None:
        """
        Test a new instance creation using dummy bucket.
        """
        dummy = Tomatic(DummyBucket, static_profile="dummy")

        assert isinstance(dummy, Tomatic)

    def test_tomatic_with_environ_new_instance(self) -> None:
        """
        Test a new instance creation using environ bucket.
        """
        environ["APP_PROFILE"] = "test"
        env = Tomatic(EnvironBucket, env_profile="APP_PROFILE")

        assert isinstance(env, Tomatic)

    @catch_value_error
    def test_if_tomatic_fail_in_case_of_exception(self) -> None:
        """
        Test if a custom exception given is an Exception subclass.
        """
        Tomatic(
            DummyBucket,
            static_profile=DUMMY_PROFILE,
            raise_if_none=AssertionError,
        )
        Tomatic(DummyBucket, static_profile=DUMMY_PROFILE, raise_if_none=int)

    def test_if_tomatic_get_a_key(self) -> None:
        """
        Test if Tomatic class return a value for a key.
        """
        dummy = Tomatic(DummyBucket, static_profile="dummy")

        assert dummy.get_a_value is None

    @catch_value_error
    def test_if_tomatic_get_key_with_expeption(self) -> None:
        """
        Test if `None` value raises an expected exceptiopn.
        """
        dummy = Tomatic(
            DummyBucket, static_profile=DUMMY_PROFILE, raise_if_none=ValueError
        )

        dummy.get_a_value

    def test_if_tomatic_use_fix_for_empty_values(self) -> None:
        """
        Test if '.fix()' method returns correct values for empty results.
        """
        assert fix(False, True) is False
        assert fix(None, True) is True


class TestTomaticTypeCast:
    """
    Class for test TomaticTypeCast methods.
    """

    def test_if_class_return_its_types(self) -> None:
        """
        Test if methodclass types() returns a populated list.
        """
        types = TomaticTypeCast.types()

        assert types and isinstance(types, list)

    def test_if_clas_cast_from_string(self) -> None:
        """
        Test if TomaticTypeCast convet a given value as string.
        """
        source = "abcdef"
        value = TomaticTypeCast(source)

        assert value.as_str == source

    def test_if_clas_cast_from_bytes(self) -> None:
        """
        Test if TomaticTypeCast convet a given value as Bytes.
        """
        source = b"ABC"
        value = TomaticTypeCast(source)

        assert value.as_str == source.decode()

    def test_if_clas_cast_return_bool(self) -> None:
        """
        Test if TomaticTypeCast return value as bool.
        """
        source = "True"
        value = TomaticTypeCast(source)

        assert isinstance(value.as_bool, bool)

    def test_if_clas_cast_return_dict(self) -> None:
        """
        Test if TomaticTypeCast return value as dict.
        """
        source = "{}"
        value = TomaticTypeCast(source)

        assert isinstance(value.as_dict, dict)

    def test_if_clas_cast_return_float(self) -> None:
        """
        Test if TomaticTypeCast return alue as float.
        """
        source = "3.14159"
        value = TomaticTypeCast(source)

        assert isinstance(value.as_float, float)

    def test_if_clas_cast_return_int(self) -> None:
        """
        Test if TomaticTypeCast return alue as int.
        """
        source = "32768"
        value = TomaticTypeCast(source)

        assert isinstance(value.as_int, int)

    def test_if_clas_cast_return_list(self) -> None:
        """
        Test if TomaticTypeCast return alue as list.
        """
        source = "[]"
        value = TomaticTypeCast(source)

        assert isinstance(value.as_list, list)

    def test_if_clas_cast_return_string(self) -> None:
        """
        Test if TomaticTypeCast return value as string.
        """
        source = "abcdefghijklmnopqrstuvwxyz"
        value = TomaticTypeCast(source)

        assert isinstance(value.as_str, str)
