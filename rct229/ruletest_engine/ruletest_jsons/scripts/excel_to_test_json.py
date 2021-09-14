import copy
import json
import math
import os

import pandas as pd

from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import *
from rct229.ruletest_engine.ruletest_jsons.scripts.json_schema_utilities import  *
from rct229.schema.schema_unit_pint_definitions import get_pint_unit_registry

# ---------------------------------------USER INPUTS---------------------------------------

spreadsheet_name = "transformer_tests_draft.xlsx"
json_name = "transformer_tests.json"
sheet_name = "TCDs"

# --------------------------------------SCRIPT STARTS--------------------------------------

def get_rmr_json_path_from_key_list(key_list):

    """Ingests a python list of 'keys' from the test JSON spreadsheet and returns the ASHRAE229 schema JSON path
    associated with it. For example ['rmr_transformations', 'user', 'schedules[0]', 'hourly_values'] would return:
    'schedules[0]/hourly_values'.

     Parameters
     ----------
     key_list : list
         List of strings representing keys used to build the ruletest JSON

     Returns
    -------
    json_path: str
        JSON path string (as understood by this script) representing the key_list's ASHRAE229 JSON path.

    """


    # Get index for the beginning of the RMR JSON.
    # Order is always 'rmr_transformations' or 'rmr_template', <RMR_TYPE>, <RMR_JSON>, therefore add 2 index to
    # either 'rmr_transformation' or 'rmr_template' indices
    if 'rmr_transformations' in key_list:
        begin_rmr_index = key_list.index('rmr_transformations') + 2
    else:
        begin_rmr_index = key_list.index('rmr_template') + 2

    final_index = len(key_list)

    # put together all RMR keys together to form a JSON path
    json_path = '/'.join(key_list[begin_rmr_index: final_index])

    return json_path


def convert_units_from_tcd_to_rmr_schema(ureg, tcd_value, tcd_units, key_list):

    """Converts a quantity defined in the test case description's (TCD) to units compatible with the ASHRAE229 value.

    Parameters
    ----------

    ureg : pint.UnitRegistry

        A UnitRegistry from the pint package. This element handles interpreting and converting quantities of various
        units

    tcd_value : float

        A numeric value imported from the TCD spreadsheet. Has units of "tcd_units"

    tcd_units : str

        A string describing the units of the TCD. These must be understandable by the "ureg" parameter

    key_list : list
        List of strings representing keys used to build the ruletest JSON. This gets parsed to retrieve the ASHRAE229
        schema's unit

    Returns
    -------
    rmr_value: float
        The converted TCD value into the units required by the ASHRAE229 schema

    """

    # Build JSON path from key list
    json_path = get_rmr_json_path_from_key_list(key_list)

    # Extract the schema's required units for this given JSON path
    schema_units = find_schema_unit_for_json_path(json_path)
    schema_units = clean_schema_units(schema_units)

    # Define TCD quantity with units in pint (convert to float if necessary)
    if isinstance(tcd_value, str):
        tcd_value = float(tcd_value)

    tcd_quantity = tcd_value * ureg(tcd_units)

    # Convert TCD quantity to units required by schema
    rmr_quantity = tcd_quantity.to(schema_units)

    rmr_value = rmr_quantity.magnitude

    return rmr_value


def create_test_json_from_excel(spreadsheet_name, sheet_name, json_name):
    """Converts a ruletest JSON spreadsheet into a ruletest JSON. The generated JSON is output to
    ./rct229/ruletest_engine/ruletest_jsons directory

    Parameters
    ----------

    spreadsheet_name : str

        Name of the ruletest spreadsheet in ./rct229/ruletest_engine/ruletest_jsons directory/ruletest_spreadsheets

    sheet_name : str

        The sheet in the spreadsheet with the ruletest information, typically 'TCDs'

    json_name : str

        The name of the resulting ruletest JSON file

    """

    # Set pint translator
    ureg = get_pint_unit_registry()

    file_dir = os.path.dirname(__file__)

    # Define test spreadsheet path
    spreadsheet_dir = "ruletest_spreadsheets"
    spreadsheet_path = os.path.join(file_dir, "..", spreadsheet_dir, spreadsheet_name)

    # Define output json file path
    json_file_path = os.path.join(file_dir, "..", json_name)

    # Pull out TCDs from spreadsheet
    master_df = pd.read_excel(spreadsheet_path, sheet_name=sheet_name)

    # Get headers to begin separating dictionary 'keys' from 'values'
    headers = master_df.columns

    # Initialize the key headers
    keys = []

    # If header has substring 'key', consider it a key
    for header in headers:
        if "key" in header:
            keys.append(header)

    # Copy columns from the spreadsheet that correspond to keys
    keys_df = master_df[keys].copy()

    # Get value columns (i.e. not key columns) from spreadsheet
    rules_df = master_df.drop(keys, axis=1)

    # If units column exist, drop it too and set as a separate list
    if 'units' in headers:
        units_list = master_df['units'].values
        rules_df = rules_df.drop('units', axis=1)

    # Initiailize dictionary for JSON
    json_dict = {}

    # Strings used by triplets
    triplet_strs = ["user", "proposed", "baseline"]

    # Iterate column by column through values_df
    for (rule_name, columnData) in rules_df.iteritems():

        # List of this rule's column data
        rule_value_list = columnData.values

        # If rule doesnt exist in dictionary
        if rule_name not in json_dict:

            # Initialize a potential json template used to build any of the RMR triplets
            rmr_template_dict = {}

            # Iterate through both keys and rule values
            for row_i in range(rule_value_list.size):

                # row_value = what will be set to the dictionary's key/value pair
                row_value = rule_value_list[row_i]

                # Skip empty rows
                if not isinstance(row_value, str):
                    if math.isnan(row_value):
                        continue

                # Initialize this row's list of keys (e.g. ['rule-15-1a', 'rmr_transformations', 'user', 'transformer'])
                key_list = [rule_name]

                for key in keys:
                    key_value = keys_df[key][row_i]
                    if isinstance(key_value, str):

                        # If the key includes a JSON_PATH, parse for the short hand enumeration name and adjust the key list
                        if "JSON_PATH" in key_value:
                            # Inject elements to key_list based on shorthand JSON_PATH enumeration
                            # (e.g., JSON_PATH:spaces = ["buildings","building_segments","thermal_blocks","zones","spaces"])
                            inject_json_path_from_enumeration(key_list, key_value)

                        else:
                            key_list.append(key_value)

                # If this row's value has units, convert to the schema's units first
                if isinstance(units_list[row_i], str):
                    # get the json_path from key list ( e.g. simplify ['rule-15-1a', 'rmr_transformations', 'user', 'transformer'])
                    tcd_units = units_list[row_i]

                    # Convert row_value to match the units found in the ASHRAE 229 schema
                    row_value = convert_units_from_tcd_to_rmr_schema(ureg, row_value, tcd_units, key_list)


                # If this is a template definition, store the template for the RMR transformations
                if "rmr_template" in key_list:

                    set_nested_dict(rmr_template_dict, key_list, row_value)

                else:

                    # Set nested dictionary
                    set_nested_dict(json_dict, key_list, row_value)

            # Once all dictionaries are set, check if any of the RMR triplets utilize json templates
            if rmr_template_dict:

                # If no transformations are defined, set an empty dictionary
                if "rmr_transformations" not in json_dict[rule_name]:
                    json_dict[rule_name]["rmr_transformations"] = {}

                # Read in transformations dictionary. This will perturb a template or fully define an RMR (if no template defined)
                rmr_transformations_dict = json_dict[rule_name]["rmr_transformations"]

                # Cycle through user, proposed, and baseline RMRs. Merge the template and their transformations
                for rmr_string in triplet_strs:

                    # If this RMR utilizes the RMR template, merge its RMR transformations into the template and set
                    # the RMR dictionary.
                    if rmr_string in rmr_template_dict[rule_name]["rmr_template"]:

                        # If this RMR has no perturbations, set the RMR value equal to the template
                        if rmr_string not in rmr_transformations_dict:
                            rmr_transformations_dict[rmr_string] = copy.deepcopy(
                                rmr_template_dict[rule_name]["rmr_template"][
                                    "json_template"
                                ]
                            )

                        # If perturbations to the template exist, merge the transformations with the template
                        else:
                            rmr_transformations_dict[rmr_string] = merge_nested_dictionary(
                                copy.deepcopy(
                                    rmr_template_dict[rule_name]["rmr_template"][
                                        "json_template"
                                    ]
                                ),
                                rmr_transformations_dict[rmr_string],
                            )

    # Dump JSON to string for writing
    json_string = json.dumps(json_dict, indent=4)

    # Write JSON string to file
    with open(json_file_path, "w") as json_file:
        json_file.write(json_string)
        print("JSON complete and written to file: " + json_name)


create_test_json_from_excel(spreadsheet_name, sheet_name, json_name)