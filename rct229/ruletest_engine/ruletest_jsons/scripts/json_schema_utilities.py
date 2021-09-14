
import re
import os
import json
import re


def clean_json_path(json_path_string):
    """Ingests a string representing a JSON path. Replaces all the '[N]' substrings.
    For example: 'transformers[0]/efficiency' => 'transformers/efficiency'

     Parameters
     ----------
     json_path_string : str
         String representing a JSON path that includes integers in square brackets. E.g., 'transformers[0]/efficiency'

     Returns
    -------
    cleaned_path_string: str
        JSON path string without square brackets.E.g., 'transformers/efficiency'

    """

    # Replace all integers within square brackets from path
    cleaned_path_string = re.sub(r'\[\d+\]', '', json_path_string)

    return cleaned_path_string


def clean_schema_units(schema_unit_str):
    """Ingests a string representing a unit as described by the schema. Sometimes these have "-" in them, making
    the Pint package confused. This function leans it up so that Pint can understand the units.
    For example: W/K-m2 --> W/(K*m2)

     Parameters
     ----------
     json_path_string : str
         String representing a JSON path that includes integers in square brackets. E.g., 'transformers[0]/efficiency'

     Returns
    -------
    cleaned_path_string: str
        JSON path string without square brackets.E.g., 'transformers/efficiency'

    """

    # Clean up dash symbol used with fractional units for pint to understand (e.g. W/K-m2 --> W/(K*m2))
    if "-" in schema_unit_str:
        substring_list = schema_unit_str.split("/")

        for i, substring in enumerate(substring_list):

            # Wrap element in parentheses and replace - with *
            if "-" in substring:
                substring_list[i] = "(" + re.sub("-", "*", substring) + ")"

        # Put it all together
        schema_unit_str = ''.join(substring_list)

    return schema_unit_str


def find_schema_unit_for_json_path(json_quantity_path):
    """Ingests a JSON path that has associated units the ASHRAE229 schema. This function returns the units for that
    JSON path as defined by the ASHRAE229 schema.
    For example: 'transformers/capacity' => 'V-A'

     Parameters
     ----------
     json_quantity_path : str
         String representing a JSON path has associated units. E.g., 'transformers/capacity'

     Returns
    -------
    unit: str
        Unit for the json_quantity_path. E.g., 'V-A'

    """
    file_dir = os.path.abspath(os.path.dirname(__file__))
    json_schema_path = os.path.join(file_dir, "..", "..", "..", "schema", "ASHRAE229.schema.json")

    with open(json_schema_path) as f:
        schema_dict = json.load(f)
        schema_dict = schema_dict["definitions"]

    root_key = "ASHRAE229"

    # Remove index references
    json_quantity_path = clean_json_path(json_quantity_path)

    key_list = json_quantity_path.split('/')

    # Initialize first reference to top level key
    dict_ref = schema_dict[root_key]

    last_key = key_list[-1]

    # Iterate through each key until you get to the end and return the units
    for key in key_list:

        if key == last_key:

            if 'units' in dict_ref["properties"][key]:
                return dict_ref["properties"][key]['units']
            else:
                raise ValueError(
                    f"OUTCOME: Could not find associated units for JSON path: {json_quantity_path}"
                )

        else:

            reference_string = return_json_schema_reference(dict_ref, key)
            dict_ref = schema_dict[reference_string]


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
    if 'items' in properties_dict:

        # Return the reference string (the last element separated by the '/'s)
        return properties_dict['items']['$ref'].split('/')[-1]

    elif '$ref' in properties_dict:

        # Return the reference string (the last element separated by the '/'s)
        return properties_dict['$ref'].split('/')[-1]

    else:

        raise ValueError(
            f"OUTCOME: Could not find a $ref key for {properties_dict} "
        )
