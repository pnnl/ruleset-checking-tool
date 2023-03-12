import copy
import json
import math
import os

import pandas as pd
import pint

from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import *
from rct229.schema.config import ureg
from rct229.schema.schema_utils import *

# ---------------------------------------USER INPUTS---------------------------------------

spreadsheet_name = "envelope_tcd_master.xlsx"
json_name = "envelope_tests.json"
sheet_name = "TCDs"

# --------------------------------------SCRIPT STARTS--------------------------------------


def get_rmr_key_list_from_tcd_key_list(tcd_key_list):
    """Ingests a python list of 'keys' from the test JSON spreadsheet and returns the relevant ASHRAE229 key list
    Without the extra specifications used in TCD spreadsheet.
    For example ['rmr_transformations', 'user', 'schedules[0]', 'hourly_values'] -> ['schedules', 'hourly_values'].

     Parameters
     ----------
     tcd_key_list : list
         List of strings representing keys used to build the ruletest JSON, from Ruletest spreadsheet

     Returns
    -------
    rmr_schema_key_list: list
        JSON path string (as understood by this script) representing the key_list's ASHRAE229 JSON path.

    """

    # Get index for the beginning of the RMR JSON.
    # Order is always 'rmr_transformations' or 'rmr_template', <RMR_TYPE>, <RMR_JSON>, therefore add 2 index to
    # either 'rmr_transformation' or 'rmr_template' indices. If neither 'rmr_transformations' or 'rmr_template' is
    # included, assume it begins at index 1 (typically what you see in the Templates tab)
    if "rmr_transformations" in tcd_key_list:
        begin_rmr_index = tcd_key_list.index("rmr_transformations") + 2
    elif "rmr_template" in tcd_key_list:
        begin_rmr_index = tcd_key_list.index("rmr_template") + 2
    else:
        begin_rmr_index = 0

    final_index = len(tcd_key_list)

    # put together all RMR keys together to form a JSON path
    rmr_schema_key_list = tcd_key_list[begin_rmr_index:final_index]

    # Remove index references
    for index, unclean_key in enumerate(rmr_schema_key_list):
        rmr_schema_key_list[index] = remove_index_references_from_key(unclean_key)

    return rmr_schema_key_list


def convert_units_from_tcd_to_rmr_schema(tcd_value, tcd_units, key_list):
    """Converts a quantity defined in the test case description's (TCD) to units compatible with the ASHRAE229 value.

    Parameters
    ----------

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
    # if the value is bool type - then return the value
    if isinstance(tcd_value, bool):
        return tcd_value

    # Clean TCD units to something pint can understand
    tcd_units = clean_schema_units(tcd_units)

    # Take the TCD's list of keys and return RMR JSON schema's unit definition for the given JSON path
    # Example: 'transformers[0]/capacity' => 'V*A'
    rmr_pint_units = get_schema_units_from_tcd_json_path(key_list)

    # Define TCD quantity with units in pint (convert to float if necessary)
    if isinstance(tcd_value, str):
        tcd_value = float(tcd_value)

    # Set TCD quantity and catch issues with non-multiplicative units, e.g., temperatures
    try:
        tcd_quantity = tcd_value * ureg(tcd_units)
    except pint.errors.OffsetUnitCalculusError:
        tcd_quantity = ureg.Quantity(tcd_value, tcd_units)

    # Convert TCD quantity to units required by schema
    rmr_quantity = tcd_quantity.to(rmr_pint_units)

    rmr_value = rmr_quantity.magnitude

    return rmr_value


def get_schema_units_from_tcd_json_path(tcd_key_list):
    """Ingests a key_list that follows the TCD spreadsheet convention and returns the RMR schema units for it.

    Parameters
    ----------

    tcd_key_list : list
        List of strings representing keys used to build the ruletest JSON using the convention used in TCD spreadsheets.
        This gets parsed to retrieve the ASHRAE229 schema's unit.
        For example: ['transformers[0], 'capacity']

    Returns
    -------
    pint_units: str
        The ASHRAE229 schema's unit for the given tcd_key_list, cleaned to be understandable by Pint
        For example: ['transformers[0], 'capacity'] => 'V*A'

    """

    # Build JSON path from key list and remove list indices
    # Example: ['rmr_transformations', 'user', 'schedules[0]', 'hourly_values'] => '['schedules', 'hourly_values']
    rmr_schema_key_list = get_rmr_key_list_from_tcd_key_list(tcd_key_list)

    # Extract the schema's required units for this given JSON path
    rmr_schema_units = find_schema_unit_for_json_path(rmr_schema_key_list)

    # If no units are returned, raise an error
    if rmr_schema_units == None:
        raise ValueError(
            f"OUTCOME: Could not find associated units for JSON path: {tcd_key_list}"
        )

    # Take the schema unit's string from the RMR JSON schema and convert it to something Pint will understand
    # Example: W/K-m2 --> W/(K*m2)
    pint_units = clean_schema_units(rmr_schema_units)

    return pint_units


def create_dictionary_from_excel(spreadsheet_name, sheet_name):
    """Converts a ruletest JSON spreadsheet into a python dictionary. This dictionary can easily be converted
    to JSON by other scripts

    Parameters
    ----------

    spreadsheet_name : str

        Name of the ruletest spreadsheet in ./rct229/ruletest_engine/ruletest_jsons directory/ruletest_spreadsheets

    sheet_name : str

        The sheet in the spreadsheet with the ruletest information, typically 'TCDs'


    Returns
    -------
    json_dict: dict
        Python dictionary representation of the JSON described ty the ruletest JSON spreadsheet

    """

    file_dir = os.path.dirname(__file__)

    # Define test spreadsheet path
    spreadsheet_dir = "ruletest_spreadsheets"
    spreadsheet_path = os.path.join(file_dir, "..", spreadsheet_dir, spreadsheet_name)

    # Pull out TCDs from spreadsheet
    master_df = pd.read_excel(spreadsheet_path, sheet_name=sheet_name)

    # Get headers to begin separating dictionary 'keys' from 'values'
    headers = master_df.columns

    # Initialize headers
    keys = []
    non_test_related_columns = []
    unit_headers = ["unit_type", "units"]
    tcd_note_headers = ["data_group", "object_id", "parent_id", "data_element"]

    for header in headers:
        # If header has substring 'key', consider it a key
        if "key" in header:
            keys.append(header)

    # Copy columns from the spreadsheet that correspond to keys
    keys_df = master_df[keys].copy()
    non_test_related_columns += keys

    # If units columns exist, initialize list of units and add unit headers to non_test_related_columns
    if "units" in headers:
        # Initialize both units and unit_types list
        units_list = master_df["units"].values
        non_test_related_columns += unit_headers

    # If tcd book keeping columns exist, initialize list of units and add unit headers to non_test_related_columns
    if "data_group" in headers:
        non_test_related_columns += tcd_note_headers

    # Get test_id columns (i.e. not keys, unit, or TCD note keeping columns) from spreadsheet
    tests_df = master_df.drop(non_test_related_columns, axis=1)

    # Initiailize dictionary for JSON
    json_dict = {}

    # Strings used by triplets
    triplet_strs = ["user", "proposed", "baseline"]

    # Many rows in the spreadsheet are not required for the JSON. The spreadsheet will ignore all these key1 values
    invalid_first_keys = ["Notes", "template_lookup"]

    # Iterate column by column through values_df
    for test_id, columnData in tests_df.iteritems():
        # List of this rule's column data
        rule_value_list = columnData.values

        # Initialize a dictionary to flag whether or not an RMR triplet uses a JSON template
        rmr_template_dict = {}

        # Catch if a test_id is repeated in this tab. We wouldn't want to override an old one
        if test_id in json_dict:
            raise ValueError(
                f"Test ID: `{test_id}` repeated in `{spreadsheet_name}` on tab `{sheet_name}`"
            )

        # If test_id has not yet been added, add it's content to json_dict
        else:
            # Iterate through both keys and rule values
            for row_i in range(rule_value_list.size):
                # row_value = what will be set to the dictionary's key/value pair
                row_value = rule_value_list[row_i]

                # Skip empty rows
                if not isinstance(row_value, str):
                    if math.isnan(row_value):
                        continue

                # Initialize this row's list of keys (e.g. ['rule-15-1a', 'rmr_transformations', 'user', 'transformer'])
                key_list = [test_id]

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
                    row_value = convert_units_from_tcd_to_rmr_schema(
                        row_value, tcd_units, key_list[1:]
                    )

                # If this is a template definition, store the template for the RMR transformations
                if "rmr_template" in key_list:
                    # If a JSON template, set the values for flagged RMR triplets
                    if "json_template" in key_list:
                        # Iterate through triplets and set values from template if flagged for it
                        for rmr_triplet in triplet_strs:
                            # Only copy the template for RMR triplets flagged as being included
                            if (
                                rmr_triplet
                                in rmr_template_dict[test_id]["rmr_template"]
                            ):
                                # If anything other than True used to flag the triplet (e.g., False), skip it
                                if (
                                    rmr_template_dict[test_id]["rmr_template"][
                                        rmr_triplet
                                    ]
                                    != True
                                ):
                                    continue

                                # Create new keylist with respect to this triplet and set value
                                triplet_key_list = [
                                    test_id,
                                    "rmr_transformations",
                                    rmr_triplet,
                                ] + key_list[3:]
                                set_nested_dict(json_dict, triplet_key_list, row_value)

                    # If not a JSON template, this implies it's setting a true/false flag for triplets
                    else:
                        set_nested_dict(rmr_template_dict, key_list, row_value)

                else:
                    # Skip irrelevant rows (e.g., "Notes")
                    if key_list[1] in invalid_first_keys:
                        continue

                    # Set nested dictionary
                    set_nested_dict(json_dict, key_list, row_value)

    return json_dict


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

    file_dir = os.path.dirname(__file__)

    # Define output json file path
    json_file_path = os.path.join(file_dir, "..", json_name)

    json_dict = create_dictionary_from_excel(spreadsheet_name, sheet_name)

    # Dump JSON to string for writing
    json_string = json.dumps(json_dict, indent=4)

    # Write JSON string to file
    with open(json_file_path, "w") as json_file:
        json_file.write(json_string)
        print("JSON complete and written to file: " + json_name)


def update_unit_convention_record(spreadsheet_name, sheet_name):
    """Parses a ruletest JSON spreadsheet for units and unit types to compare against existing unit_conventions.json
    records. This JSON keeps record of existing display names for various unit types throughout the ASHRAE229 JSON
    schema.
    Example: For a unit_type == area, the TCDs might use 'ft2' while the RMR schema uses 'm2'. This would get recorded
    in unit_conventions.json for other scripts to use when displaying reports.

    Parameters
    ----------

    spreadsheet_name : str

        Name of the ruletest spreadsheet in ./rct229/ruletest_engine/ruletest_jsons directory/ruletest_spreadsheets

    sheet_name : str

        The sheet in the spreadsheet with the ruletest information, typically 'TCDs'

    """

    file_dir = os.path.dirname(__file__)

    # Define test spreadsheet path
    spreadsheet_dir = "ruletest_spreadsheets"
    spreadsheet_path = os.path.join(file_dir, "..", spreadsheet_dir, spreadsheet_name)

    # Define output json file path
    json_name = "unit_conventions.json"
    unit_def_json_path = os.path.join(
        file_dir, "..", "..", "..", "schema", "resources", json_name
    )

    # Pull out TCDs from spreadsheet
    master_df = pd.read_excel(spreadsheet_path, sheet_name=sheet_name)

    # Get headers to begin separating dictionary 'keys' and 'unit' columns
    headers = master_df.columns

    # Initialize column lists
    relevant_columns = []
    keys = []

    # If header has substring 'unit' or 'key', append it to list of important columns. These columns have information
    # necessary for mapping units from the TCD and RMR to the unit convention JSON
    for header in headers:
        if "unit" in header:
            relevant_columns.append(header)
        elif "key" in header:
            keys.append(header)

    # Combine units and keys column to get relevant columns from overall TCD spreadsheet
    relevant_columns.extend(keys)

    # Copy columns from the spreadsheet that correspond to units or keys
    units_df = master_df[relevant_columns].copy()
    keys_df = master_df[keys].copy()
    requires_update = False

    # Initialize unit definition dictionary
    with open(unit_def_json_path) as f:
        unit_def_dict = json.load(f)

    # Iterate row by row through units DF (not ideal by Pandas standards but these are small data frames)
    for index, row in units_df.iterrows():
        # Grab row values
        unit_type = row["unit_type"]
        tcd_unit = row["units"]

        # Skip rows with no unit definition
        if not isinstance(unit_type, str):
            if math.isnan(unit_type):
                continue

        tcd_key = "ip"
        rmr_key = "si"

        tcd_key_list = []

        # Get list of keys using TCD convention (e.g., ['transformers[0]', 'capacity'] )
        for key in keys:
            key_value = keys_df[key][index]
            if isinstance(key_value, str):
                # If the key includes a JSON_PATH, parse for the short hand enumeration name and adjust the key list
                if "JSON_PATH" in key_value:
                    # Inject elements to key_list based on shorthand JSON_PATH enumeration
                    # (e.g., JSON_PATH:spaces = ["buildings","building_segments","thermal_blocks","zones","spaces"])
                    inject_json_path_from_enumeration(tcd_key_list, key_value)

                else:
                    tcd_key_list.append(key_value)

        # Build JSON path from key list and remove list indices
        # Example: ['rmr_transformations', 'user', 'schedules[0]', 'hourly_values'] => '['schedules', 'hourly_values']
        rmr_schema_key_list = get_rmr_key_list_from_tcd_key_list(tcd_key_list)

        # Extract the schema's required units for this given JSON path
        rmr_schema_units = find_schema_unit_for_json_path(rmr_schema_key_list)

        # If no units are returned, raise an error
        if rmr_schema_units == None:
            raise ValueError(
                f"OUTCOME: Could not find associated units for JSON path: {tcd_key_list}"
            )

        # Check if existing JSON has values in IP and SI for this unit type and compare to the value extracted from
        # this TCD spreadsheet. Update the unit conventions if not, raise warning if there's a conflict with an existing
        # unit convention type
        if unit_type in unit_def_dict[tcd_key]:
            # Get existing definition
            existing_unit = unit_def_dict[tcd_key][unit_type]

            # Compare against TCD spreadsheet's units
            if tcd_unit != existing_unit:
                raise ValueError(
                    f"Existing {tcd_key} unit definition for unit type '{unit_type}' is '{existing_unit}' but new TCD"
                    f" spreadsheet is trying to set it to '{tcd_unit}'. Manually erase existing record to"
                    f" update this unit type definition"
                )

        # If no record of unit_type in unit definition dictionary, add it
        else:
            unit_def_dict[tcd_key][unit_type] = tcd_unit
            requires_update = True

        # Update RMR units too
        if unit_type in unit_def_dict[rmr_key]:
            # Get existing definition
            existing_unit = unit_def_dict[rmr_key][unit_type]

            # Compare against TCD spreadsheet's units
            if rmr_schema_units != existing_unit:
                raise ValueError(
                    f"Existing {rmr_key} unit definition for unit type '{unit_type}' is '{existing_unit}' but new TCD"
                    f" spreadsheet is trying to set it to '{rmr_schema_units}'. Please pick a more specific name"
                    f" for this unit definition"
                )

        # If no record of unit_type in unit definition dictionary, add it
        else:
            unit_def_dict[rmr_key][unit_type] = rmr_schema_units
            requires_update = True

    if requires_update:
        # Dump JSON to string for writing
        json_string = json.dumps(unit_def_dict, indent=4)

        # Write out updated unit definition JSON
        with open(unit_def_json_path, "w") as json_file:
            json_file.write(json_string)
            print("JSON complete and written to file: " + json_name)
    else:
        print("No changes necessary for: " + json_name)


# Create a test JSON for a given ruletest spreadsheet
create_test_json_from_excel(spreadsheet_name, sheet_name, json_name)

# Parse ruletest spreadsheet for unit types and update the unit conventions in unit_convention.json for:
# -RMR (typically SI)
# -Rule Tests (typically IP)
update_unit_convention_record(spreadsheet_name, sheet_name)
