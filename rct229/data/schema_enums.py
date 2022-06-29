import json
from enum import Enum
from os.path import dirname, join

from jsonpath_ng import parse

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
# Concatinate the two match lists using a list comprehension
# _match_list = [
#     match for matches in [_enum_schema_matches, _schema_matches] for match in matches
# ]
_match_list = [*_enum_schema_matches, *_schema_matches]

# Create a dictionary of all the enumerations as dictionaries
_enum_dicts = {
    str(match.full_path).split(".")[-1]: dict(
        (key, value)
        for key, value in zip(match.value["enum"], match.value["descriptions"])
    )
    for match in _match_list
}

# Convert the enumerations as dictionaries to actual Enums
schema_enums = {key: Enum(key, enum_dict) for key, enum_dict in _enum_dicts.items()}


def print_schema_enums():
    """Print all the schema enumerations with their names and values

    This is primarily useful for debuggin purposes
    """
    for key in schema_enums:
        print(f"{key}:")
        for e in schema_enums[key]:
            print(f"    {e.name}: {e.value}")
        print()


# Uncomment this for checking the enumerations after a schema change
print_schema_enums()
