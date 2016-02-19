"""
Test fixtures.
"""
from os import listdir
from os.path import dirname, join


def iter_examples():
    """
    Iterate through example schemas.

    """
    for example in listdir(join(dirname(__file__), "examples")):
        with open(join(dirname(__file__), "examples", example)) as fileobj:
            yield fileobj.read()
