"""
Object model.
"""
from warnings import warn

from openapi.base import (
    SCHEMA,
    SchemaAwareDict,
    SchemaAwareList,
    SchemaAwareString,
)
from openapi.naming import make_class_name
from openapi.registry import register


def make(class_name, base, schema):
    """
    Create a new schema aware type.
    """
    return type(class_name, (base,), dict(SCHEMA=schema))


def make_definition(name, base, schema):
    """
    Create a new definition.

    """
    class_name = make_class_name(name)
    cls = register(make(class_name, base, schema))
    globals()[class_name] = cls


# generate top-level type
Swagger = make("Swagger", SchemaAwareDict, SCHEMA)


# generate types for definitions
for name, schema in SCHEMA["definitions"].items():
    if any(ignore in schema for ignore in ["$ref", "oneOf"]):
        # don't generate types for choices and references
        continue

    schema_type = schema.get("type", "object")
    if schema_type == "object":
        make_definition(name, SchemaAwareDict, schema)
    elif schema_type == "array":
        make_definition(name, SchemaAwareList, schema)
    elif schema_type == "string":
        make_definition(name, SchemaAwareString, schema)
    else:
        warn(f"Unsupported schema type: '{schema_type}'")
