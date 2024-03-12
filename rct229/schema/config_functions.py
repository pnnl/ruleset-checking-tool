import json
import os

import pint


# Initialize pint ureg
def get_pint_unit_registry():
    # Import unit definitions from text file
    path_to_units = os.path.join(
        os.path.dirname(__file__), "resources", "unit_registry.txt"
    )
    ureg = pint.UnitRegistry(path_to_units, autoconvert_offset_to_baseunit=True)

    return ureg


def get_schema_version():
    """Returns ASHRAE229 schema version as a string

     Returns
    -------
    schema_version: string
        Version of the ASHRAE229 schema

    """
    file_dir = os.path.dirname(__file__)
    json_schema_path = os.path.join(file_dir, "ASHRAE229.schema.json")
    with open(json_schema_path) as f:
        schema_dictionary = json.load(f)
        schema_version = schema_dictionary["version"]

    return schema_version


def get_schema_definitions_dictionary():
    """Returns ASHRAE229 schema definition JSON object as a dictionary

     Returns
    -------
    schema_dictionary: dict
        ASHRAE229 schema definition JSON object as a dictionary as defined in ASHRAE229.schema.json

    """

    file_dir = os.path.dirname(__file__)
    json_schema_path = os.path.join(file_dir, "ASHRAE229.schema.json")

    with open(json_schema_path) as f:
        schema_dictionary = json.load(f)
        schema_dictionary = schema_dictionary["definitions"]

    return schema_dictionary


def get_unit_conventions_dictionary():
    """Returns dictionary of unit conventions from ./rct229/schema/resources/unit_conventions.json

     Returns
    -------
    convention_dict: dict
        Python dictionary representation of ./rct229/schema/resources/unit_conventions.json. This dictionary contains
        the SI and IP unit conventions for various unit types (e.g., area, power_density).

    """

    file_dir = os.path.dirname(__file__)
    unit_convention_path = os.path.join(file_dir, "resources", "unit_conventions.json")

    with open(unit_convention_path) as f:
        convention_dict = json.load(f)

    return convention_dict
