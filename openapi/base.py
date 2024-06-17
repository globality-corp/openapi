"""
Wrappers for JSON schema-specific wrappers.

For compatability with the standard JSON and JSON schema libraries,
these types inherit from the primitive types they extend, but add
extra behavior to support type-conversion and schema validation.
"""
from contextlib import closing
from io import StringIO
from json import dump, load
from os.path import dirname, join
from re import match

from jsonschema import RefResolver, validate

from openapi.naming import make_key_name
from openapi.registry import REGISTRY, lookup


# load the schema
with open(join(dirname(__file__), "schemas/v2.0/schema.json")) as fileobj:
    SCHEMA = load(fileobj)


class Schema(dict):
    """
    Wrapper around a JSON schema.

    """
    def __getitem__(self, key):
        """
        Allow root schema definitions to be accessible for sub-schema definitions.

        """
        try:
            return super().__getitem__(key)
        except KeyError:
            if key == "definitions":
                return SCHEMA["definitions"]
            raise


class SchemaAware:
    """
    Schema-aware mix-in.

    """
    def validate(self):
        """
        Validate that this instance matches its schema.

        """
        schema = Schema(self.__class__.SCHEMA)
        resolver = RefResolver.from_schema(
            schema,
            store=REGISTRY,
        )
        validate(self, schema, resolver=resolver)

    def dump(self, fileobj):
        """
        Dump this instance as YAML.

        """
        return dump(self, fileobj)

    def dumps(self):
        """
        Dump this instance as YAML.

        """
        with closing(StringIO()) as fileobj:
            self.dump(fileobj)
            return fileobj.getvalue()

    @classmethod
    def load(cls, fileobj):
        """
        Load an instance of this class from YAML.

        """
        return cls(load(fileobj))

    @classmethod
    def loads(cls, s):
        """
        Load an instance of this class from YAML.

        """
        with closing(StringIO(s)) as fileobj:
            return cls.load(fileobj)


class SchemaAwareDict(dict, SchemaAware):
    """
    Schema aware dictionary.

    Reinterprets non-primitive value types as model objects.

    """

    def __getitem__(self, key):
        """
        Override item access to constuct model objects.

        """
        value = super().__getitem__(key)
        if isinstance(value, SchemaAware):
            return value

        property_schema = self.property_schema(key)
        property_class = lookup(property_schema)
        if property_class is not None:
            value = property_class(value)
            self[key] = value
        return value

    def __getattr__(self, name):
        """
        Allow attribute-based access.

        Converts Pythonic names as needed.

        """
        key = make_key_name(name)
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                self.__class__.__name__,
                key,
            ))

    def __setattr__(self, name, value):
        """
        Allow attribute-based assignment.

        """
        self[name] = value

    def property_schema(self, key):
        """
        Lookup the schema for a specific property.

        """
        schema = self.__class__.SCHEMA

        # first try plain properties
        plain_schema = schema.get("properties", {}).get(key)
        if plain_schema is not None:
            return plain_schema
        # then try pattern properties
        pattern_properties = schema.get("patternProperties", {})
        for pattern, pattern_schema in pattern_properties.items():
            if match(pattern, key):
                return pattern_schema
        # finally try additional properties (defaults to true per JSON Schema)
        return schema.get("additionalProperties", True)


class SchemaAwareList(list, SchemaAware):
    """
    Schema aware list.

    Reinterprets non-primitive member types as model objects.

    """

    def __getitem__(self, index):
        """
        Override item access to convert types.

        """
        value = super().__getitem__(index)
        if isinstance(value, SchemaAware):
            return value

        items_schema = self.__class__.SCHEMA["items"]
        items_class = lookup(items_schema)
        if items_class is not None:
            value = items_class(value)
            self[index] = value
        return value


class SchemaAwareString(str, SchemaAware):
    """
    Schema aware dictionary.

    """
    pass


try:
    # If YAML is installed (see extras_require), ensure that base classes are
    # registered as multi representers; otherwise, dumping the object model
    # to YAML won't work properly as primitives.
    #
    # Note that loading from YAML is not recommended because numeric dictionary
    # keys (e.g. for HTTP status codes) are not forced to be strings in YAML
    # and pattern matching in `jsonschema` assumes does not work on numbers.
    from yaml import add_multi_representer
    from yaml.representer import SafeRepresenter

    add_multi_representer(SchemaAwareDict, SafeRepresenter.represent_dict)
    add_multi_representer(SchemaAwareList, SafeRepresenter.represent_list)
    add_multi_representer(SchemaAwareString, SafeRepresenter.represent_str)
except ImportError:
    pass
