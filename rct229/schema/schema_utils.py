import json
import os
import re

import rct229.schema.config as config


def clean_schema_units(schema_unit_str):
    """Ingests a string representing a unit as described by the schema. Sometimes these have "-" in them, making
    the Pint package confused. This function leans it up so that Pint can understand the units.
    For example: W/K-m2 --> W/(K*m2)

     Parameters
     ----------
     schema_unit_str : str
         String representing a JSON path that includes integers in square brackets. E.g., 'transformers[0]/efficiency'

     Returns
    -------
    cleaned_unit_str: str
        The schema_unit_str string value translated to a string value the Pint library unit registry can understand.

    """

    # Clean up dash symbol used with fractional units for pint to understand (e.g. W/K-m2 --> W/(K*m2))
    if "-" in schema_unit_str:
        substring_list = schema_unit_str.split("/")

        for i, substring in enumerate(substring_list):

            # Wrap element in parentheses and replace - with *
            if "-" in substring:
                substring_list[i] = "(" + re.sub("-", "*", substring) + ")"

        # Put it all together
        cleaned_unit_str = "".join(substring_list)

    # Nothing to clean
    else:
        cleaned_unit_str = schema_unit_str

    return cleaned_unit_str


def find_schema_unit_for_json_path(key_list):
    """Ingests a JSON path that has associated units the ASHRAE229 schema. This function returns the units for that
    JSON path as defined by the ASHRAE229 schema.
    For example: ['transformers','capacity'] => 'V-A'

     Parameters
     ----------
     key_list : list
         List representing a JSON path has associated units. E.g., 'transformers/capacity' represented as
         ['transformers', 'capacity']

     Returns
    -------
    unit: str
        Unit for the json_quantity_path. E.g., 'V-A'

    """

    root_key = "ASHRAE229"

    # Initialize first reference to top level key
    dict_ref = config.schema_dict[root_key]

    key_list_head = key_list[:-1]  # All but last key
    last_key = key_list[-1]

    # Iterate through each key until you get the final dictionary reference
    for key in key_list_head:
        reference_string = return_json_schema_reference(dict_ref, key)
        dict_ref = config.schema_dict[reference_string]

    # Check the final dictionary reference for units
    if "units" in dict_ref["properties"][last_key]:
        return dict_ref["properties"][last_key]["units"]
    else:
        # If no units are found, return none
        return None


def return_json_schema_reference(object_dict, key):
    """This function takes an schema object's dictionary, passes it a key, and returns it's respective reference
    definition dictionary. For example, the Building object in ASHRAE229.schema.json dictionary has a
    "building_segments" key. Passing in the Building dictionary with the "building_segments" key would return a
    the definition for the BuildingSegment element in the ASHRAE229 schema.

    Parameters
    ----------
    object_dict : dict
        Dictionary representing an element from a JSON schema. E.g. The "Building" element from ASHRAE229.schema.json

    key : str
        String representing a key in the object_dict dictionary. This function will return the $ref for this object


    Returns
    -------
    definition: str


    """

    properties_dict = object_dict["properties"][key]

    # $ref elements are either at the top level or buried inside "items"
    if "items" in properties_dict:

        # Return the reference string (the last element separated by the '/'s)
        return properties_dict["items"]["$ref"].split("/")[-1]

    elif "$ref" in properties_dict:

        # Return the reference string (the last element separated by the '/'s)
        return properties_dict["$ref"].split("/")[-1]

    else:

        raise ValueError(f"OUTCOME: Could not find a $ref key for {properties_dict} ")
