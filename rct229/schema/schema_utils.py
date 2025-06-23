import json
import os
import re
from collections.abc import Sequence
from copy import deepcopy

from jsonpath_ng.ext import parse as parse_jsonpath
from pydash.objects import set_

import rct229.schema.config as config
from rct229.schema.schema_store import SchemaStore


def clean_schema_units(schema_unit_str):
    """Ingests a string representing a unit as described by the schema. Sometimes these have "-" in them, making
    the Pint package confused. This function leans it up so that Pint can understand the units.
    For example: W/K-m2 --> W/(K*m2)

     Parameters
     ----------
     schema_unit_str : str
         String representing a display or service name representation that may be misunderstood by pint. This function
         cleans up this unit (e.g., W/K-m2)

     Returns
    -------
    cleaned_unit_str: str
        The schema_unit_str string value translated to a string value the Pint library unit registry can understand.
        (e.g., W/(K*m2)

    """
    cleaned_unit_str = schema_unit_str

    # Clean up dash symbol used with fractional units for pint to understand (e.g. W/K-m2 --> W/(K*m2))
    if "-" in schema_unit_str:
        substring_list = schema_unit_str.split("/")

        for i, substring in enumerate(substring_list):
            # Wrap element in parentheses and replace - with *
            if "-" in substring:
                substring_list[i] = "(" + re.sub("-", "*", substring) + ")"

        # Put it all together
        cleaned_unit_str = "/".join(substring_list)

    return cleaned_unit_str


def find_schema_unit_for_json_path(key_list):
    """Ingests a JSON path that has associated units int the ASHRAE229 schema. This function returns the units for that
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

    root_key = "RulesetProjectDescription"

    secondary_schema_files = [SchemaStore.get_output_schema_by_ruleset()]
    schema_dict = config.schema_dict

    # Initialize first reference to top level key
    dict_ref = schema_dict[root_key]

    key_list_head = key_list[:-1]  # All but last key
    last_key = key_list[-1]

    # Iterate through each key until you get the final dictionary reference
    for key in key_list_head:
        reference_string = return_json_schema_reference(dict_ref, key)

        # If reference string references a secondary json reference, update root JSON dictionary to new secondary schema
        if reference_string.split("#")[0] in secondary_schema_files:
            schema_dict = get_secondary_schema_root_dictionary(
                reference_string.split("#")[0]
            )

            # Split out root dictionary object key. It's found in the schema object's file name
            # (e.g., 'Output2019ASHRAE901' in 'Output2019ASHRAE901.schema.json')
            root_key = reference_string.split("/")[-1].split(".")[0]
            dict_ref = schema_dict[root_key]
        else:
            dict_ref = schema_dict[reference_string]

    # Check the final dictionary reference for units
    if "units" in dict_ref["properties"][last_key]:
        return dict_ref["properties"][last_key]["units"]
    else:
        # If no units are found, return none
        return None


def get_secondary_schema_root_dictionary(secondary_json_string):
    """Returns schema definition JSON object other than ASHRAE229 as a dictionary at root level

    Parameters
    ----------
    secondary_json_string : str
    String representing a JSON schema definition file other than ASHRAE 229 E.g., 'Output2019ASHRAE901.schema.json'


     Returns
    -------
    schema_dictionary: dict
        Alternative schema definition JSON object as a dictionary

    """

    file_dir = os.path.dirname(__file__)
    json_schema_path = os.path.join(file_dir, secondary_json_string)

    with open(json_schema_path) as f:
        schema_dictionary = json.load(f)
        schema_dictionary = schema_dictionary["definitions"]

    return schema_dictionary


def quantify_rmd(rmd):
    """Replaces rmd items with pint quantities based on schema units

    Parameters
    ----------
    rmd : dict
        An rmd dictionary

    Returns
    -------
    dict
        A copy of the original rmd dictionary with all numbers that have units
        in the schema replaced with their corresponding pint quantities
    """
    rmd = deepcopy(rmd)

    # Match all rmd field items
    # Note, this does not match array items, but will pass through an array to get to a field item
    all_rmd_field_item_matches = parse_jsonpath("$..*").find(rmd)

    # Pick out the number fields and fields that hold an array of numbers
    number_rmd_item_matches = list(
        filter(
            lambda rmd_item_match: (type(rmd_item_match.value) in [int, float])
            or (
                type(rmd_item_match.value) is list
                and all(
                    [
                        type(list_item) in [int, float]
                        for list_item in rmd_item_match.value
                    ]
                )
            ),
            all_rmd_field_item_matches,
        )
    )

    # Replace all number items that have associated units in the schema
    # with the appropriate pint quantity
    for number_rmd_item_match in number_rmd_item_matches:
        # Get the full path to the item
        full_path = str(number_rmd_item_match.full_path)

        # Split the full path at dots and list indexing
        key_list = re.split(r"\.\[\d+\]\.|\.", full_path)

        # Get the units string for the item from the schema
        schema_unit_str = find_schema_unit_for_json_path(key_list)

        if schema_unit_str is not None:
            # Make the units string pint-compatible
            pint_unit_str = clean_schema_units(schema_unit_str)
            val = number_rmd_item_match.value
            if isinstance(val, Sequence) and not isinstance(val, str):
                # Replace each number in the list with a pint quantity
                pint_qty_list = [v * config.ureg(pint_unit_str) for v in val]
                set_(rmd, full_path, pint_qty_list)
            else:
                # Create the pint quantity to replace the number
                pint_qty = number_rmd_item_match.value * config.ureg(pint_unit_str)
                # Replace the number with the appropriate pint quantity
                set_(rmd, full_path, pint_qty)
    return rmd


def return_json_schema_reference(object_dict, key):
    """This function takes a schema object's dictionary, passes it a key, and returns it's respective reference
    definition dictionary. For example, the Building object in ASHRAE229.schema.json dictionary has a
    "building_segments" key. Passing in the Building dictionary with the "building_segments" key would return
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

    secondary_schema_files = ["Output2019ASHRAE901.schema.json"]

    properties_dict = object_dict["properties"][key]

    # $ref elements are either at the top level or buried inside "items"
    if "items" in properties_dict:
        # Return the reference string (the last element separated by the '/'s)
        if "$ref" in properties_dict["items"]:
            return properties_dict["items"]["$ref"].split("/")[-1]
        else:
            # Some elements have an oddball "oneOf" that allows for a reference or "string".
            return properties_dict["items"]["oneOf"][0]["$ref"].split("/")[-1]

    elif "$ref" in properties_dict:
        # Return the reference string (the last element separated by the '/'s)
        return properties_dict["$ref"].split("/")[-1]

    # Check 'oneOf' key for secondary json schema references
    elif "oneOf" in properties_dict:
        if "$ref" in properties_dict["oneOf"][0]:
            secondary_json = properties_dict["oneOf"][0]["$ref"].split("#")[0]

            # If it's a secondary schema file, return it
            if secondary_json in secondary_schema_files:
                return properties_dict["oneOf"][0]["$ref"]

            # If it's actually just referencing the main schema, return the reference (the last element separated by
            # the '/'s)
            elif secondary_json == SchemaStore.SCHEMA_KEY:
                return properties_dict["oneOf"][0]["$ref"].split("/")[-1]

            else:
                raise ValueError(
                    f"OUTCOME: Secondary json '{secondary_json}' not found in {secondary_schema_files}"
                )

        raise ValueError(
            f"OUTCOME: Could not find a $ref key inside 'oneOf' key {properties_dict} "
        )

    else:
        raise ValueError(f"OUTCOME: Could not find a $ref key for {properties_dict} ")
