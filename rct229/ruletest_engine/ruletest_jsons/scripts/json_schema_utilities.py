
import re
import os
import json


def clean_json_path(json_path_string):

    # Replace all integers within square brackets from path
    cleaned_path_string = re.sub(r'\[\d+\]', '', json_path_string)

    return cleaned_path_string


def find_schema_unit_for_json_path(json_quantity_path):

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

    properties_dict = object_dict["properties"][key]

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



json_quantity_path = "buildings[0]/building_segments[0]/thermal_blocks[0]/zones[0]/spaces[0]/interior_lighting[0]/power_per_area"
print(find_schema_unit_for_json_path(json_quantity_path))

json_quantity_path = "buildings[0]/building_segments[0]/thermal_blocks[0]/zones[0]/spaces[0]/floor_area"
print(find_schema_unit_for_json_path(json_quantity_path))

json_quantity_path = "transformers[0]/capacity"
print(find_schema_unit_for_json_path(json_quantity_path))