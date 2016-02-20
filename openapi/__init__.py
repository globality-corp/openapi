"""
Public API.
"""
from openapi.model import Swagger


def load(fileobj):
    """
    Load swagger model objects (from json).

    """
    return Swagger.load(fileobj)


def loads(s):
    """
    Load swagger model objects (from json).

    """
    return Swagger.loads(s)


def dump(obj, fileobj):
    """
    Dump swagger model objects (to json).

    """
    return obj.dump(fileobj)


def dumps(obj):
    """
    Dump swagger model objects (to json).

    """
    return obj.dumps()
