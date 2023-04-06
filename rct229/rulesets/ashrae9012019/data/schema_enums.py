import json
from enum import Enum
from os.path import dirname, join

from rct229.utils.jsonpath_utils import create_jsonpath_value_dict

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
    dirname(__file__), "../../..", "schema", "Enumerations2019ASHRAE901.schema.json"
)
with open(_enum_schema_path) as json_file:
    _enum_schema_obj = json.load(json_file)

# Load the schema file
_schema_path = join(dirname(__file__), "../../..", "schema", "ASHRAE229.schema.json")
with open(_schema_path) as json_file:
    _schema_obj = json.load(json_file)

# Query for all objects having an enum field
# See jsonpath2 docs for parse syntax: https://jsonpath2.readthedocs.io/en/latest/exampleusage.html
_enum_schema_enum_jsonpath_value_dict = create_jsonpath_value_dict(
    "$..*[?(@.enum)]", _enum_schema_obj
)
_schema_enum_jsonpath_value_dict = create_jsonpath_value_dict(
    "$..*[?(@.enum)]", _schema_obj
)
# Merge the two dictionaries
enum_jsonpath_value_dict = {
    **_enum_schema_enum_jsonpath_value_dict,
    **_schema_enum_jsonpath_value_dict,
}

# Create a dictionary of all the enumerations as dictionaries
_enums_dict = {
    # NOTE: The jsonpath() has the form '$["a"]...["b"]' so
    # .split('"')[-2] will pick out the 'b' from the path in this example
    enum_jsonpath.split('"')[-2]: value["enum"]
    for (enum_jsonpath, value) in enum_jsonpath_value_dict.items()
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
