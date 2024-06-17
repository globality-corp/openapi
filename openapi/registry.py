"""
Model registry.
"""
from openapi.naming import make_definition_name


# singleton type registry
#  -  acts as a store for the jsonschema validator
#  -  allows object models to construct each other
REGISTRY = {}


def register(cls):
    """
    Register a class.

    """
    definition_name = make_definition_name(cls.__name__)
    REGISTRY[definition_name] = cls
    return cls


def lookup(schema):
    """
    Lookup a class by property schema.

    """
    if not isinstance(schema, dict) or "$ref" not in schema:
        return None

    ref = schema["$ref"]

    return REGISTRY.get(ref)
