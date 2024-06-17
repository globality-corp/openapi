"""
Name translation.

"""
from inflection import camelize, underscore


def make_attribute_name(key_name):
    """
    Convert a key name to an attribute name.

    """
    return underscore(key_name)


def make_key_name(attribute_name):
    """
    Convert a key name to an attribute name.

    """
    return camelize(attribute_name, uppercase_first_letter=False)


def make_class_name(definition_name):
    """
    Convert a definition name into a class name.

    """
    return str(camelize(definition_name, uppercase_first_letter=True))


def make_definition_name(class_name):
    """
    Convert a class name into a definition name.

    """
    return f"#/definitions/{camelize(class_name, uppercase_first_letter=False)}"
