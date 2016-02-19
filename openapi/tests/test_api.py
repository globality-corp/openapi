"""
Tests for load and dump.
"""
from hamcrest import (
    assert_that,
    instance_of,
    is_,
    not_none,
)

from openapi import dumps, loads
from openapi.model import (
    Info,
    License,
    MimeType,
    MediaTypeList,
    PathItem,
    Paths,
    Swagger,
)
from openapi.tests.fixtures import iter_examples
from openapi.tests.matchers import equal_to_json


def _assert_load_and_dump(data):
    # load the data as a Swagger object
    swagger = loads(data)
    assert_that(swagger, is_(instance_of(Swagger)))

    # attribute access produces model objects
    assert_that(swagger.info, is_(instance_of(Info)))
    assert_that(swagger.info.license, is_(instance_of(License)))
    assert_that(swagger.consumes, is_(instance_of(MediaTypeList)))
    assert_that(swagger.paths, is_(instance_of(Paths)))

    # key access produces model objects
    assert_that(swagger.paths[swagger.paths.keys()[0]], is_(instance_of(PathItem)))

    # index access produces model objects
    assert_that(swagger.consumes[0], is_(instance_of(MimeType)))

    # attribute access handles Pythonic syntax
    assert_that(swagger.base_path, is_(not_none())),
    assert_that(swagger.basePath, is_(not_none())),

    # dumping the data back as a raw data returns equivalent input
    assert_that(dumps(swagger), is_(equal_to_json(data)))


def test_load_and_dump():
    """
    Examples can be loaded and dumped back.

    """
    for example in iter_examples():
        yield _assert_load_and_dump, example
