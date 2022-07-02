import json
from enum import Enum
from os.path import dirname, join

from jsonpath_ng import parse

"""This module exports the dictionary schema_enums that provides access to the
enumerations in the schema files.

The keys of schema_enums are the names of the enumeration objects; each value
is a class with an attribute for each item in the enumeration. The value
of the attribute is the same as the attribute name.
"""


class _ListEnum:
    """A utility class used to convert a list into a class

    Each item in the list becomes a class attribute whose value is the attribute
    name as a string. This is intended as a more convenient version of Enum.
    """

    def __init__(self, _dict):
        for key in _dict:
            setattr(self, key, key)

    def get_list(self):
        return list(self.__dict__.keys())


# Load the enumeration schema file
_enum_schema_path = join(
    dirname(__file__), "..", "schema", "Enumerations2019ASHRAE901.schema.json"
)
with open(_enum_schema_path) as json_file:
    _enum_schema_obj = json.load(json_file)

# Load the schema file
schema_path = join(dirname(__file__), "..", "schema", "ASHRAE229.schema.json")
with open(schema_path) as json_file:
    _schema_obj = json.load(json_file)

# Query for all objects having an enum field
# See jsonpath docs for parse syntax: https://pypi.org/project/jsonpath-ng/
_enum_schema_matches = parse("$..* where enum").find(_enum_schema_obj)
_schema_matches = parse("$..* where enum").find(_schema_obj)
# Concatinate the two match lists
_match_list = [*_enum_schema_matches, *_schema_matches]

# Create a dictionary of all the enumerations as dictionaries
_enums_dict = {
    str(match.full_path).split(".")[-1]: match.value["enum"] for match in _match_list
}

# Convert the enumerations as dictionaries to classess for easier access
schema_enums = {key: _ListEnum(enum_list) for key, enum_list in _enums_dict.items()}


def print_schema_enums():
    """Print all the schema enumerations with their names and values

    This is primarily useful for debugging purposes
    """
    for key in schema_enums:
        print(f"{key}:")
        for e in schema_enums[key].get_list():
            print(f"    {e}")
        print()


# Uncomment this for checking the enumerations after a schema change
# print_schema_enums()
