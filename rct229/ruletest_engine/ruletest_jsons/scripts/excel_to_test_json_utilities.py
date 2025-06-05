import copy
import json
import math
import os

import pandas as pd
import pint
from rct229.rule_engine.rulesets import RuleSet
from rct229.ruletest_engine.ruletest_jsons.scripts.excel_generation_utilities import (
    generate_rule_test_dictionary,
)
from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import *
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_utils import *


def get_rmd_key_list_from_tcd_key_list(tcd_key_list):
    """Ingests a python list of 'keys' from the test JSON spreadsheet and returns the relevant ASHRAE229 key list
    Without the extra specifications used in TCD spreadsheet.
    For example ['rmd_transformations', 'user', 'schedules[0]', 'hourly_values'] -> ['schedules', 'hourly_values'].

     Parameters
     ----------
     tcd_key_list : list
         List of strings representing keys used to build the ruletest JSON, from Ruletest spreadsheet

     Returns
    -------
    rmd_schema_key_list: list
        JSON path string (as understood by this script) representing the key_list's ASHRAE229 JSON path.

    """

    # Get index for the beginning of the RMD JSON.
    # Order is always 'rmd_transformations' or 'rmd_template', <RMD_TYPE>, <RMD_JSON>, therefore add 2 index to
    # either 'rmd_transformation' or 'rmd_template' indices. If neither 'rmd_transformations' or 'rmd_template' is
    # included, assume it begins at index 1 (typically what you see in the Templates tab)
    if "rmd_transformations" in tcd_key_list:
        begin_rmd_index = tcd_key_list.index("rmd_transformations") + 2
    elif "rmd_template" in tcd_key_list:
        begin_rmd_index = tcd_key_list.index("rmd_template") + 2
    else:
        begin_rmd_index = 0

    final_index = len(tcd_key_list)

    # put together all RMD keys together to form a JSON path
    rmd_schema_key_list = tcd_key_list[begin_rmd_index:final_index]

    # Remove index references
    for index, unclean_key in enumerate(rmd_schema_key_list):
        rmd_schema_key_list[index] = remove_index_references_from_key(unclean_key)

    rmd_schema_key_list = [item for item in rmd_schema_key_list if item != "\xa0"]

    return rmd_schema_key_list


def convert_units_from_tcd_to_rmd_schema(tcd_value, tcd_units, key_list):
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
    rmd_value: float
        The converted TCD value into the units required by the ASHRAE229 schema

    """
    # if the value is bool type - then return the value
    if isinstance(tcd_value, bool):
        return tcd_value

    # Clean TCD units to something pint can understand
    tcd_units = clean_schema_units(tcd_units)

    # Take the TCD's list of keys and return RMD JSON schema's unit definition for the given JSON path
    # Example: 'transformers[0]/capacity' => 'V*A'
    rmd_pint_units = get_schema_units_from_tcd_json_path(key_list)

    # Define TCD quantity with units in pint (convert to float if necessary)
    if isinstance(tcd_value, str):
        tcd_value = float(tcd_value)

    # Set TCD quantity and catch issues with non-multiplicative units, e.g., temperatures
    try:
        tcd_quantity = tcd_value * ureg(tcd_units)
    except pint.errors.OffsetUnitCalculusError:
        tcd_quantity = ureg.Quantity(tcd_value, tcd_units)

    # Convert TCD quantity to units required by schema
    rmd_quantity = tcd_quantity.to(rmd_pint_units)

    rmd_value = rmd_quantity.magnitude

    return rmd_value


def get_schema_units_from_tcd_json_path(tcd_key_list):
    """Ingests a key_list that follows the TCD spreadsheet convention and returns the RMD schema units for it.

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
    # Example: ['rmd_transformations', 'user', 'schedules[0]', 'hourly_values'] => '['schedules', 'hourly_values']
    rmd_schema_key_list = get_rmd_key_list_from_tcd_key_list(tcd_key_list)

    # Extract the schema's required units for this given JSON path
    rmd_schema_units = find_schema_unit_for_json_path(rmd_schema_key_list)

    # If no units are returned, raise an error
    if rmd_schema_units == None:
        raise ValueError(
            f"OUTCOME: Could not find associated units for JSON path: {tcd_key_list}"
        )

    # Take the schema unit's string from the RMD JSON schema and convert it to something Pint will understand
    # Example: W/K-m2 --> W/(K*m2)
    pint_units = clean_schema_units(rmd_schema_units)

    return pint_units


def create_dictionary_from_excel(spreadsheet_name, sheet_name, rule_set):
    """Converts a ruletest JSON spreadsheet into a python dictionary. This dictionary can easily be converted
    to JSON by other scripts

    Parameters
    ----------

    spreadsheet_name : str

        Name of the ruletest spreadsheet in ./rct229/ruletest_engine/ruletest_jsons directory/ruletest_spreadsheets

    sheet_name : str

        The sheet in the spreadsheet with the ruletest information, typically 'TCDs'

    rule_set : str

        The rule set being evaluated (e.g., 'ashrae902019'). Should correspond to a directory name in ruletests_jsons


    Returns
    -------
    json_dict: dict
        Python dictionary representation of the JSON described ty the ruletest JSON spreadsheet

    """

    file_dir = os.path.dirname(__file__)

    # Define test spreadsheet path
    spreadsheet_dir = "ruletest_spreadsheets"
    spreadsheet_path = os.path.join(
        file_dir, "..", rule_set, spreadsheet_dir, spreadsheet_name
    )

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
    for test_id, columnData in tests_df.items():
        # List of this rule's column data
        rule_value_list = columnData.values

        # Initialize a dictionary to flag whether or not an RMD triplet uses a JSON template
        rmd_template_dict = {}

        # Initialize a dictionary that maps system types to a list of zones. Utilized when using the
        # rmd_template/system_zone_assignment/system[0]/baseline_system type system
        # FORMAT:
        # -system_to_zone_dict["systems"][N]["baseline_system"] = [SYSTEM_NAME]
        # -system_to_zone_dict["systems"][N]["zones"] = [ZONE_1, ZONE_2,...ZONE_N]
        system_to_zone_dict = {}

        # Flag used to determine if systems have been added to
        zones_have_been_mapped = False

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

                # Ignore values that somehow return a blank ASCII string = '\xa0'
                if row_value == "\xa0":
                    continue

                # Skip empty rows
                if not isinstance(row_value, str):
                    if math.isnan(row_value):
                        continue

                # Initialize this row's list of keys (e.g. ['rule-15-1a', 'rmd_transformations', 'user', 'transformer'])
                key_list = [test_id]

                for key in keys:
                    key_value = keys_df[key][row_i]
                    # Ignore values that somehow return a blank ASCII string = '\xa0'
                    if key_value == "\xa0":
                        continue

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
                    # get the json_path from key list ( e.g. simplify ['rule-15-1a', 'rmd_transformations', 'user', 'transformer'])
                    tcd_units = units_list[row_i]

                    # Convert row_value to match the units found in the ASHRAE 229 schema
                    row_value = convert_units_from_tcd_to_rmd_schema(
                        row_value, tcd_units, key_list[1:]
                    )

                # If this is a template definition, store the template for the RMD transformations
                if "rmd_template" in key_list:
                    # If a JSON template, set the values for flagged RMD triplets
                    if "json_template" in key_list:
                        # Iterate through triplets and set values from template if flagged for it
                        for rmd_triplet in triplet_strs:
                            # Only copy the template for RMD triplets flagged as being included
                            if (
                                rmd_triplet
                                in rmd_template_dict[test_id]["rmd_template"]
                            ):
                                # If anything other than True used to flag the triplet (e.g., False), skip it
                                if (
                                    rmd_template_dict[test_id]["rmd_template"][
                                        rmd_triplet
                                    ]
                                    != True
                                ):
                                    continue

                                # Create new keylist with respect to this triplet and set value
                                triplet_key_list = [
                                    test_id,
                                    "rmd_transformations",
                                    rmd_triplet,
                                ] + key_list[3:]
                                set_nested_dict(json_dict, triplet_key_list, row_value)

                    elif "system_zone_assignment" in key_list:
                        # Remove irrelevant keys and set the rest of the keys into system_to_zone_dict
                        keys_to_ignore = [test_id, "rmd_template"]
                        key_list = [
                            item for item in key_list if item not in keys_to_ignore
                        ]
                        set_nested_dict(system_to_zone_dict, key_list, row_value)

                    # If not a JSON template or system to zone assignment, this implies it's setting a true/false
                    # flag for triplets
                    else:
                        set_nested_dict(rmd_template_dict, key_list, row_value)

                else:
                    # Once you've worked down to the final rmd_transformation sections of the spreadsheet, check
                    # to see if zones have been mapped to systems
                    if not zones_have_been_mapped and system_to_zone_dict:
                        # Set to true to avoid setting them again
                        zones_have_been_mapped = True
                        set_systems_to_zones(json_dict, system_to_zone_dict, rule_set)

                    # Skip irrelevant rows (e.g., "Notes")
                    if key_list[1] in invalid_first_keys:
                        continue

                    # Set nested dictionary
                    set_nested_dict(json_dict, key_list, row_value)

    return json_dict


def create_test_json_from_excel(
    spreadsheet_name, sheet_name, json_name, rule_set="ashrae9012019"
):
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

    rule_set : str

        The rule set being evaluated (e.g., 'ashrae902019'). Should correspond to a directory name in ruletests_jsons

    """

    file_dir = os.path.dirname(__file__)

    # Define output json file path
    json_file_path = os.path.join(file_dir, "..", rule_set, json_name)

    # Load Schemas
    if rule_set == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        SchemaEnums.update_schema_enum()

    json_dict = create_dictionary_from_excel(spreadsheet_name, sheet_name, rule_set)

    json_dict = add_ruleset_model_types(json_dict)

    # Dump JSON to string for writing
    json_string = json.dumps(json_dict, indent=4)

    # Write JSON string to file
    with open(json_file_path, "w") as json_file:
        json_file.write(json_string)
        print("JSON complete and written to file: " + json_name)


def add_ruleset_model_types(json_dict: dict):
    # dirty code to check if this works.
    for test_context in json_dict.values():
        if test_context.get("rmd_transformations"):
            rmd_transformation_context = test_context["rmd_transformations"]
            if rmd_transformation_context.get("baseline"):
                rmd_transformation_context["baseline"]["ruleset_model_descriptions"][0][
                    "type"
                ] = "BASELINE_0"
            if rmd_transformation_context.get("proposed"):
                rmd_transformation_context["proposed"]["ruleset_model_descriptions"][0][
                    "type"
                ] = "PROPOSED"
            if rmd_transformation_context.get("user"):
                rmd_transformation_context["user"]["ruleset_model_descriptions"][0][
                    "type"
                ] = "USER"
    return json_dict


def update_unit_convention_record(
    spreadsheet_name, sheet_name, rule_set="ashrae9012019"
):
    """Parses a ruletest JSON spreadsheet for units and unit types to compare against existing unit_conventions.json
    records. This JSON keeps record of existing display names for various unit types throughout the ASHRAE229 JSON
    schema.
    Example: For a unit_type == area, the TCDs might use 'ft2' while the RMD schema uses 'm2'. This would get recorded
    in unit_conventions.json for other scripts to use when displaying reports.

    Parameters
    ----------

    spreadsheet_name : str

        Name of the ruletest spreadsheet in ./rct229/ruletest_engine/ruletest_jsons directory/ruletest_spreadsheets

    sheet_name : str

        The sheet in the spreadsheet with the ruletest information, typically 'TCDs'

    rule_set : str

        The rule set being evaluated (e.g., 'ashrae902019'). Should correspond to a directory name in ruletests_jsons

    """

    file_dir = os.path.dirname(__file__)

    # Define test spreadsheet path
    spreadsheet_dir = "ruletest_spreadsheets"
    spreadsheet_path = os.path.join(
        file_dir, "..", rule_set, spreadsheet_dir, spreadsheet_name
    )

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
    # necessary for mapping units from the TCD and RMD to the unit convention JSON
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
        rmd_key = "si"

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
        # Example: ['rmd_transformations', 'user', 'schedules[0]', 'hourly_values'] => '['schedules', 'hourly_values']
        rmd_schema_key_list = get_rmd_key_list_from_tcd_key_list(tcd_key_list)

        # Extract the schema's required units for this given JSON path
        rmd_schema_units = find_schema_unit_for_json_path(rmd_schema_key_list)

        # If no units are returned, raise an error
        if rmd_schema_units == None:
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

        # Update RMD units too
        if unit_type in unit_def_dict[rmd_key]:
            # Get existing definition
            existing_unit = unit_def_dict[rmd_key][unit_type]

            # Compare against TCD spreadsheet's units
            if rmd_schema_units != existing_unit:
                raise ValueError(
                    f"Existing {rmd_key} unit definition for unit type '{unit_type}' is '{existing_unit}' but new TCD"
                    f" spreadsheet is trying to set it to '{rmd_schema_units}'. Please pick a more specific name"
                    f" for this unit definition"
                )

        # If no record of unit_type in unit definition dictionary, add it
        else:
            unit_def_dict[rmd_key][unit_type] = rmd_schema_units
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


def set_systems_to_zones(json_dict, system_to_zone_dict, rule_set):
    """Takes the JSON structure generated by the system_zone_assignment section of the ruletest JSON spreadsheet
    and assigns the pre-set HVAC system type RMD examples to those zones

    Parameters
    ----------

    json_dict : dict

        The dictionary RMD with the thermal zones that require assignment

    system_to_zone_dict : dict

        The dictionary described in the ruletest JSON spreadsheet. Keys are:
         -system_zone_assignment
         --systems[N]
         ---baseline_system = string that matches names in
                              .rct229\ruletest_engine\ruletest_jsons\<rule_set>\system_types
         ---zones[N]


    rule_set : str

        The rule set being evaluated (e.g., 'ashrae902019'). Should correspond to a directory name in ruletests_jsons

    """

    file_dir = os.path.dirname(__file__)

    for system in system_to_zone_dict["system_zone_assignment"]["systems"]:
        system_name = system["baseline_system"]
        zone_list = system["zones"]

        system_type_path = os.path.join(
            file_dir, "..", rule_set, "system_types", f"{system_name}.json"
        )

        # Get system RMD
        with open(system_type_path) as f:
            system_rmd = json.load(f)

        # Add relevant terminals to zones in zone_list
        add_baseline_terminals(json_dict, system_rmd, system_name, zone_list)

        # Adjust building segment HVACs
        add_hvac_systems(json_dict, system_rmd, system_name, zone_list)

        # Add plant loop equipment
        add_plant_loop_equipment(json_dict, system_rmd)

    # Get latest test ID
    test_id = list(json_dict)[-1]

    # Cycle through each rmd triplet and ensure there are no shallow copies between elements.
    for rmd_triplet, rmd_dict in json_dict[test_id]["rmd_transformations"].items():

        json_dict[test_id]["rmd_transformations"][rmd_triplet] = deepcopy(
            json_dict[test_id]["rmd_transformations"][rmd_triplet]
        )


def get_rmd_triplet_from_ruletest_json_dict(ruletest_json_test_dict):
    """Reads in a ruletest JSON dictionary and returns list of RMDs for any triplet flagged in the ruletest JSON

    Parameters
    ----------

    ruletest_json_test_dict : dict

        Dictionary corresponding to the JSON structure dictated by a ruletest spreadsheet test instance. This
        is currently the top level instance and has keys such as Section, Rule, Test, standard (a dictionary)
        and rmd transformations (the most relevant element for this function)

    Returns
    -------
    rmd_triplet_dict_list: list
        Returns a list of dictionaries, each representing an instance of an RMD

    """

    # Strings used by triplets
    triplet_strs = ["user", "proposed", "baseline"]

    # List of RMD instances that live in the ruletest JSON dictionary
    rmd_triplet_dict_list = []

    # Check ruletest_json_dict for instances of triplets. Append any that are found to a list and return it
    for triplet in triplet_strs:
        if triplet in ruletest_json_test_dict["rmd_transformations"]:
            rmd_triplet_dict_list.append(
                ruletest_json_test_dict["rmd_transformations"][triplet]
            )

    return rmd_triplet_dict_list


def add_baseline_terminals(json_dict, system_rmd, system_name, zone_list):
    """Takes a template RMD and injects terminals found in an HVAC system example RMD for a list of zones

    Parameters
    ----------

    json_dict : dict

        The ruletest json dictionary with the last test ID containing an RMD with the thermal zones that require
        terminal assignment

    system_rmd : dict

        The bare bone dictionary example of an HVAC system type. Terminals are pulled from this dictionary

    system_name : str
        The name of the RMD json referenced by system_rmd. Should match a file name from
                          .rct229\ruletest_engine\ruletest_jsons\<rule_set>\system_types

    zone_list: list
        List of strings representing zones found in template_rmd

    """

    terminal_keys = get_json_path_key_list_from_enumeration(
        json_path_enumeration="terminals"
    )
    terminal_keys[-1] = (
        terminal_keys[-1] + "[0]"
    )  # append a [0] to final terminals key to reference first terminal
    terminal_copy = deepcopy(get_nested_dic_from_key_list(system_rmd, terminal_keys))

    # Get latest test ID to which we're adding terminals
    test_id = list(json_dict)[-1]

    # Get this test_id's zones for each RMD that exist in the template (e.g., user, baseline, proposed)
    rmd_triplet_dict_list = get_rmd_triplet_from_ruletest_json_dict(json_dict[test_id])

    for rmd_instance_dict in rmd_triplet_dict_list:
        zone_keys = get_json_path_key_list_from_enumeration(
            json_path_enumeration="zones"
        )

        zones = get_nested_dic_from_key_list(rmd_instance_dict, zone_keys)

        # If another duplicate of this system exists, iterate the name to ensure unique IDs between systems
        system_name = iterate_system_id_if_duplicate_exists(
            rmd_instance_dict, system_name
        )

        for zone in zones:
            # Only add terminals for zones assigned to this system
            if zone["id"] in zone_list:
                zone_id = zone["id"]

                # Inject new terminals
                zone["terminals"] = []
                zone["terminals"].append(deepcopy(terminal_copy))
                zone["terminals"][0]["id"] = f"{system_name} - Terminal for {zone_id}"

                zone["terminals"][0][
                    "served_by_heating_ventilating_air_conditioning_system"
                ] = f"{system_name}"


def iterate_system_id_if_duplicate_exists(rmd_dict, system_name):
    """Checks the RMD dictionary for a particular system name in the list of HVAC systems. Iterates the name of this
    system to ensure IDs aren't duplicated.

         Parameters
         ----------

         rmd_dict : dict

             Dictionary with all HVAC systems

         system_name: str
             String representing the system name to check for in the HVAC systems in rmd_dict

         Returns
         -------

         system_name: str

             The updated system name, if necessary. If no iteration is necessary, this will return the same
             system name

    """

    # Check if the system name already exists in the model. If so, update name to allow for multiple multizone systems
    hvac_keys = get_json_path_key_list_from_enumeration(
        json_path_enumeration="heating_ventilating_air_conditioning_systems"
    )

    # If rmd_dict has HVAC systems added, check if this system name is already taken. If so, update it.
    if element_exists_at_key_address_in_dictionary(rmd_dict, hvac_keys):
        hvac_systems = get_nested_dic_from_key_list(rmd_dict, hvac_keys)

        for hvac_system in hvac_systems:

            # If this system ID/name has already been taken, iterate it by one
            if system_name == hvac_system["id"]:

                # Start index at one and go up until no matches are found
                index = 1

                # Continue iterating index until no matches are found
                while any(
                    hvac["id"] == f"{system_name} {index}" for hvac in hvac_systems
                ):
                    index += 1

                return f"{system_name} {index}"

    # No change needed
    return system_name


def iterate_ids_in_dict(iterable_object):
    """Takes an RMD dictionary (at any level) and checks every element for an ID. If an ID is found, the ID is
    updated to ensure no duplicates. This happens recursively to ensure every element is drilled down.

         Parameters
         ----------

         iterable_object : dict|list

             Dictionary or list being checked for ID elements to update


    """

    # Check if the iterable object is a list
    if isinstance(iterable_object, list):
        # Recursively check elements for ID and update them
        for item in iterable_object:
            if isinstance(item, list):
                iterate_ids_in_dict(item)

            elif isinstance(item, dict):
                iterate_ids_in_dict(item)

    # If not a list, it should be a dict, but check. Check dictionary for IDs and iterate their value by 1
    elif isinstance(iterable_object, dict):
        if "id" in iterable_object:
            # If already numbered, iterate by 1
            if iterable_object["id"][-1].isdigit():
                final_index = int(iterable_object["id"][-1])
                iterable_object["id"] = iterable_object["id"][:-1] + str(
                    final_index + 1
                )

            # If this ID has no number, add a 1 to it
            else:
                iterable_object["id"] = iterable_object["id"] + " 1"

        # Recursively check elements for ID and update them
        for value in iterable_object.values():
            if isinstance(value, list):
                iterate_ids_in_dict(value)

            elif isinstance(value, dict):
                iterate_ids_in_dict(value)


def add_hvac_systems(json_dict, system_rmd, system_name, zone_list):
    """Adds HVAC system from system_rmd to template RMD for zones in zone list

    Parameters
    ----------

    json_dict : dict

        The ruletest json dictionary with the last test ID containing an RMD requiring HVAC assignment

    system_rmd : dict

        The bare bone dictionary example of an HVAC system type. HVAC systems are pulled from this dictionary


    system_name : str
        The name of the RMD json referenced by system_rmd. Should match a file name from
                          .rct229\ruletest_engine\ruletest_jsons\<rule_set>\system_types

    zone_list: list
        List of strings representing zones found in template_rmd

    """

    # Copy of baseline system HVAC system
    hvac_keys = get_json_path_key_list_from_enumeration(
        json_path_enumeration="heating_ventilating_air_conditioning_systems"
    )
    hvac_keys[-1] = (
        hvac_keys[-1] + "[0]"
    )  # append a [0] to final terminals key to reference first terminal
    hvac_copy = deepcopy(get_nested_dic_from_key_list(system_rmd, hvac_keys))

    # Get latest test ID to which we're adding an HVAC system
    test_id = list(json_dict)[-1]

    # Get this test_id's zones for each RMD that exist in the template (e.g., user, baseline, proposed)
    rmd_triplet_dict_list = get_rmd_triplet_from_ruletest_json_dict(json_dict[test_id])

    for rmd_instance_dict in rmd_triplet_dict_list:
        # Get building segments in the RMD instance
        building_segment_keys = get_json_path_key_list_from_enumeration(
            json_path_enumeration="building_segments"
        )
        building_segments = get_nested_dic_from_key_list(
            rmd_instance_dict, building_segment_keys
        )

        # Iterate through building segments and add HVAC systems
        for building_segment in building_segments:
            # Check if this building segment has any relevant zones
            zones = building_segment["zones"]

            segment_contains_relevant_zone = False

            # Ensure that this segment contains a relevant zone
            for zone in zones:
                if zone["id"] in zone_list:
                    segment_contains_relevant_zone = True
                    break

            if segment_contains_relevant_zone:
                # Intialize HVAC systems if not found in this building segment yet
                if (
                    "heating_ventilating_air_conditioning_systems"
                    not in building_segment
                ):
                    building_segment[
                        "heating_ventilating_air_conditioning_systems"
                    ] = []

                # Flag used to determine if any 'system_name' HVAC types have been already been established already in
                # the RMD
                base_hvac_initialized = False

                # Check for duplicate system. If this system type already exists, create a copy of it and
                # update IDs to avoid duplicates.
                for hvac_system in building_segment[
                    "heating_ventilating_air_conditioning_systems"
                ]:
                    # Iterate IDs to avoid duplicate IDs if this system type already exists in the building
                    if system_name in hvac_system["id"]:
                        hvac_copy = deepcopy(hvac_system)
                        iterate_ids_in_dict(hvac_copy)
                        base_hvac_initialized = True

                building_segment["heating_ventilating_air_conditioning_systems"].append(
                    hvac_copy
                )

                # This ensures the system ID is unique and matches the system type name for first copy. This ensures
                # consistency that HVAC system names are fully described and helps avoid duplicates
                if not base_hvac_initialized:
                    # Adjust HVAC system ID to match system type
                    hvac_system = building_segment[
                        "heating_ventilating_air_conditioning_systems"
                    ][-1]
                    hvac_system["id"] = f"{system_name}"

                    # Ensure unique fan names based on system type
                    if "fan_system" in hvac_system:
                        fan_system = hvac_system["fan_system"]
                        if "supply_fans" in fan_system:
                            for supply_fan in fan_system["supply_fans"]:
                                supply_fan["id"] = f"{system_name} Supply Fan"
                        if "return_fans" in fan_system:
                            for return_fan in fan_system["return_fans"]:
                                return_fan["id"] = f"{system_name} Return Fan"


# Adds plant equipment at ruleset model instance level
def add_plant_loop_equipment(json_dict, system_rmd):
    """Adds HVAC system plant equipment from system_rmd to template RMD

    Parameters
    ----------

    json_dict : dict

        The ruletest dictionary with the test RMD which require plant loop equipment injection

    system_rmd : dict

        The bare bone dictionary example of an HVAC system type. Plant equipment is pulled from this
        dictionary

    """

    equipment_str_list = [
        "boilers",
        "chillers",
        "pumps",
        "fluid_loops",
        "heat_rejections",
    ]

    sys_ruleset_model_instance = system_rmd["ruleset_model_descriptions"][0]

    # Get latest test ID to which we're adding plant loops
    test_id = list(json_dict)[-1]

    # Get this test_id's zones for each RMD that exist in the template (e.g., user, baseline, proposed)
    rmd_triplet_dict_list = get_rmd_triplet_from_ruletest_json_dict(json_dict[test_id])

    # Iterate through each RMD triplet dictionary
    for rmd_instance_dict in rmd_triplet_dict_list:
        template_ruleset_model_instance = rmd_instance_dict[
            "ruleset_model_descriptions"
        ][0]

        # Iterate through piece of plant loop equipment and check if any exist. Add any that are missing.
        for equipment in equipment_str_list:
            if equipment in sys_ruleset_model_instance:
                # If this equipment type is already listed, check id of each component and see if it matches ID of
                # element in the system RMD. Add missing ones.
                if equipment in template_ruleset_model_instance:
                    template_equipment_id_list = []

                    # Create list of equipment from template ID
                    for template_equipment_instance in template_ruleset_model_instance[
                        equipment
                    ]:
                        template_equipment_id_list.append(
                            template_equipment_instance["id"]
                        )

                    # Add any missing pieces of equipment from system RMD (i.e., if an ID doesn't
                    # already exist in template's list of plant equipment)
                    for system_equipment_instance in sys_ruleset_model_instance[
                        equipment
                    ]:
                        if (
                            system_equipment_instance["id"]
                            not in template_equipment_id_list
                        ):
                            template_ruleset_model_instance[equipment].append(
                                system_equipment_instance
                            )

                # If this equipment type didn't exist in the template, simply copy from system RMD
                else:
                    template_ruleset_model_instance[
                        equipment
                    ] = sys_ruleset_model_instance[equipment]
