"""
Tests for validation.
"""
from hamcrest import (
    assert_that,
    calling,
    raises,
)

from jsonschema import ValidationError

from openapi import loads
from openapi.tests.fixtures import iter_examples
from openapi.model import Info, Swagger


def _assert_valid(data):
    swagger = loads(data)

    # validation works as expected
    swagger.validate()

    # validation of internal model also works
    swagger.info.validate()


def test_validation():
    """
    Examples validate.

    """
    for example in iter_examples():
        yield _assert_valid, example
        break


def test_invalid_swagger():
    """
    Validation of top-level Swagger model raises Validation error if incomplete.

    """
    assert_that(calling(Swagger().validate), raises(ValidationError))


def test_invalid_info():
    """
    Validation of internal Swagger model raises Validation error if incomplete.

    """
    assert_that(calling(Info().validate), raises(ValidationError))
