import json
import os

import pint


# Initialize pint ureg
def get_pint_unit_registry():

    # Import unit definitions from text file
    path_to_units = os.path.join(
        os.path.dirname(__file__), "resources", "unit_registry.txt"
    )
    ureg = pint.UnitRegistry(path_to_units)

    return ureg


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
