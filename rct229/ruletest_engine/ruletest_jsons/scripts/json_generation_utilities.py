import json
import os
import re
from collections import OrderedDict

from rct229.rulesets.ashrae9012019 import rules_dict


def get_nested_dict(dic, keys):
    """Used to get nested python dictionary strings
    Example: get_nested_reference_dict(my_dict, ['a', 'b', 'c']) returns my_dict['a']['b']['c']

    Parameters
    ----------
    dic : dictionary
        Dictionary of nested dictionaries.
    keys: list
        Key names used for writing in the nested dictionary

    Returns
    -------
    dic: dictionary

        Returns the referenced Python dictionary.
    """

    last_key, last_index = parse_key_string(keys[-1])
    first_key, first_index = parse_key_string(keys[0])

    # Generate a nested dictionary, slowly building on a reference nested dictionary each iteration through the loop.
    for key in keys:
        # Parse key and determine if this key references a list or a value. If list_index returns an integer (i.e., a
        # reference index in a list) this key represents a list in the dictionary and needs to be set differently
        # EXAMPLE: The key "buildings[0]" implies the "buildings" key represents a list. We set the value at
        # element 0 in this list

        key, list_index = parse_key_string(key)
        is_list = isinstance(list_index, int)

        # If this is the first key, set the reference dictionary to the highest level dictionary and work down from
        # there.
        if key == first_key:
            # If first key isn't initialized, set it as a dictionary
            if key not in dic:
                if first_index == None:
                    dic[key] = {}
                else:
                    dic[key] = []

            if is_list:
                reference_dict = dic[key][first_index]
            else:
                reference_dict = dic[key]

        # If the final key, return the referenced final, nested dictionary
        elif key == last_key:
            if key not in reference_dict:
                # If this is a dictionary, the last index on the last key parse will be None
                if last_index == None:
                    reference_dict[key] = {}
                else:
                    reference_dict[key] = []

            return reference_dict

        # If neither the first nor final key in list, continue drilling down through nested dictionaries.
        else:
            if key not in reference_dict:
                if is_list:
                    reference_dict[key] = [{}]
                else:
                    reference_dict[key] = {}

            # If this element in the key_list references a list, index the value defined in 'list_index', else reference
            # the single value specified by the key.
            if is_list:
                # If list isn't long enough, append a new dictionary to it to avoid index out of bounds
                # print(reference_dict[key])
                while len(reference_dict[key]) < list_index + 1:
                    reference_dict[key].append({})
                reference_dict = reference_dict[key][list_index]
            else:
                reference_dict = reference_dict[key]


def get_nested_dic_from_key_list(dic, keys):
    nested_dict = get_nested_dict(dic, keys)

    # Parse final key to see if it's a list or dictionary/key value
    key, list_index = parse_key_string(keys[-1])

    # Set value. If list_index is None, this is just a key/value pair
    if list_index == None:
        return nested_dict[key]

    # If list_index is not None, return element, not list
    else:
        return nested_dict[key][list_index]


# Determines if a dictionary has an element after at a particular key list address
def element_exists_at_key_address_in_dictionary(dic, keys):

    last_key, last_index = parse_key_string(keys[-1])
    first_key, first_index = parse_key_string(keys[0])

    # Determine if a nested dictionary exists, slowly building on a reference nested dictionary each iteration through the loop.
    for key in keys:
        # Parse key and determine if this key references a list or a value. If list_index returns an integer (i.e., a
        # reference index in a list) this key represents a list in the dictionary and needs to be set differently
        # EXAMPLE: The key "buildings[0]" implies the "buildings" key represents a list. We set the value at
        # element 0 in this list

        key, list_index = parse_key_string(key)
        is_list = isinstance(list_index, int)

        # If this is the first key, set the reference dictionary to the highest level dictionary and work down from
        # there.
        if key == first_key:
            # If first key isn't initialized, return False
            if key not in dic:
                return False

            if is_list:
                reference_dict = dic[key][first_index]
            else:
                reference_dict = dic[key]

        # If the final key and something is found, return True
        elif key == last_key:
            if key not in reference_dict:
                return False

            return True

        # If neither the first nor final key in list, continue drilling down through nested dictionaries.
        else:
            if key not in reference_dict:
                return False

            # If this element in the key_list references a list, index the value defined in 'list_index', else reference
            # the single value specified by the key.
            if is_list:
                # If list isn't long enough, append a new dictionary to it to avoid index out of bounds
                # print(reference_dict[key])
                while len(reference_dict[key]) < list_index + 1:
                    reference_dict[key].append({})
                reference_dict = reference_dict[key][list_index]
            else:
                reference_dict = reference_dict[key]


def parse_key_string(key_string):
    """Inspects a string representing a key for any list references. Returns the parsed 'key' and 'list_index' reference
    Example: 'surfaces[1]' references a key = 'surfaces' which represents a list. The '[1]' implies a reference
              to the second element in the 'surfaces' list. This would return both 'surfaces' and 1.

    Parameters
    ----------
    key_string: str
        String representing a key and possibly a reference to a list index. Example: 'surfaces[1]'

    Returns
    -------
    key: str
        String parsed out of key_string representing a referenced key.
    list_index: int
        Integer representing a list index parsed out of key_string. 'None' if no list reference is found

    """

    # If key specifies an in index (e.g.., something like "[1]" appended afterward a key name), parse the key and
    # index out from the string
    if "[" in key_string:
        split_str = key_string.split("[")
        key = split_str[0]
        list_index = int(split_str[1].replace("]", ""))
    else:
        key = key_string
        list_index = None

    return key, list_index


def set_nested_dict(dic, keys, value):
    """Used to set nested python dictionary strings. Useful for setting dictionary values for JSON generation.
    Example: nested_set(my_dict, ['a', 'b', 'c'], 'my_value') is same as my_dict['a']['b']['c'] = 'my_value'

    Parameters
    ----------
    dic : dictionary
        Dictionary on which to append new nested value
    keys: list
        Key names used for writing in the nested dictionary

    value: string
        Value set to the nested dictionary

    """

    # Get reference to where to set the value in the original nested dictionary, creating new lists and dictionaries
    # as necessary
    nested_dict = get_nested_dict(dic, keys)

    # Parse final key to see if it's a list or dictionary/key value
    key, list_index = parse_key_string(keys[-1])

    # Set value. If list_index is None, this is just a key/value pair
    if list_index == None:
        nested_dict[key] = clean_value(value)

    # If list_index is not None, the final key is a list, not a dictionary
    else:
        # Set list value
        nested_dict[key].append(clean_value(value))


def inject_json_path_from_enumeration(key_list, json_path_ref_string):
    """A few JSON paths are shorthanded with an enumeration. This function appends the key_list with the list of keys
    found in this shorthand enumeration. These are found in json_pointer_enumerations.json.
     Example: JSON_PATH:spaces = ["buildings","building_segments","thermal_blocks","zones","spaces"]

     Parameters
     ----------
     key_list : list
         List of keys describing the JSON path. The shorthand enumeration's key list is appended onto this list

     json_path_ref_string: str

        String describing which enumeration to use. E.g., "JSON_PATH:spaces"
    """

    # JSON path enumerations. Used to simplify JSON path references in test spreadsheets
    file_dir = os.path.dirname(__file__)
    json_path_enums_file_path = os.path.join(
        file_dir, "resources", "json_pointer_enumerations.json"
    )

    with open(json_path_enums_file_path) as f:
        # Construct dictionary to map shorthand names for JSON Paths
        # (e.g., path_enum_dict['spaces] = 'buildings/building_segments/thermal_blocks/zones/spaces')
        path_enum_dict = json.load(f)

    # Pull out enumeration key from json_path_ref_string
    json_path_enumeration = json_path_ref_string.split(":")[1].strip()

    # Strip off any list references, will be added back on afterward
    json_path_enumeration, list_index = parse_key_string(json_path_enumeration)

    # Split enumeration path into a list and append it to existing key_list
    # (e.g. 'buildings/building_segments/thermal_blocks/zones/spaces' ->
    #       ['buildings', 'building_segments', 'thermal_blocks', 'zones', 'spaces']
    enumeration_list = path_enum_dict[json_path_enumeration].split("/")

    # Append index back onto final key if JSON_PATH was defined as a list:
    if list_index != None:
        enumeration_list[-1] = f"{enumeration_list[-1]}[{list_index}]"

    # Inject enumeration list into keylist
    key_list.extend(enumeration_list)


def get_json_path_key_list_from_enumeration(json_path_enumeration):
    # JSON path enumerations. Used to simplify JSON path references in test spreadsheets
    file_dir = os.path.dirname(__file__)
    json_path_enums_file_path = os.path.join(
        file_dir, "resources", "json_pointer_enumerations.json"
    )

    with open(json_path_enums_file_path) as f:
        # Construct dictionary to map shorthand names for JSON Paths
        # (e.g., path_enum_dict['spaces] = 'buildings/building_segments/thermal_blocks/zones/spaces')
        path_enum_dict = json.load(f)

    # Split enumeration path into a list and append it to existing key_list
    # (e.g. 'buildings/building_segments/thermal_blocks/zones/spaces' ->
    #       ['buildings', 'building_segments', 'thermal_blocks', 'zones', 'spaces']
    enumeration_list = path_enum_dict[json_path_enumeration].split("/")

    return enumeration_list


def clean_value(value):
    """Used to change strings to numerics, if possible.

    Parameters
    ----------
    value : str
        String to be cleaned

    """

    # Set value directly if a list or dict
    if isinstance(value, dict) or isinstance(value, list):
        return value
    else:
        # If value is neither a list or dict, and a string, process it
        if isinstance(value, str):
            # Set value as boolean if possible
            if value.lower() == "true" or value.lower() == "false":
                return value.lower() == "true"

            # If the value references a schedule, parse string to create the list
            if "SCHEDULE:" in value:
                return create_schedule_list(value)

            try:
                # Check if integer or float if convertible
                value = float(value)

                # Check for integer
                if value % 1 == 0:
                    value = int(value)
                    return value
                else:  # If not an integer, return the float
                    return value

            except ValueError:
                # normal string
                return value

        else:  # if not a list, dict, or string, this value is likely already cleaned
            return value


def merge_nested_dictionary(master_dict, new_data_dict, path=None):
    """Merges a nested dictionary into another nested_dictionary. Adapted from stackoverflow question found here:
    https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries

     Parameters
     ----------
     master_dict : dict
         Nested dictionary being merged into master dictionary

     new_data_dict: dict
         Nested dictionary receiving new data

    """

    if path is None:
        path = []
    for key in new_data_dict:
        if key in master_dict:
            if isinstance(master_dict[key], dict) and isinstance(
                new_data_dict[key], dict
            ):
                merge_nested_dictionary(
                    master_dict[key], new_data_dict[key], path + [str(key)]
                )
            elif isinstance(master_dict[key], list) and isinstance(
                new_data_dict[key], list
            ):
                for master, new_data in zip(master_dict[key], new_data_dict[key]):
                    merge_nested_dictionary(master, new_data, path + [str(key)])

            elif master_dict[key] == new_data_dict[key]:
                pass  # same leaf value
            else:
                # Overwrite old key value with one from new dictionary
                master_dict[key] = new_data_dict[key]
        else:
            master_dict[key] = new_data_dict[key]
    return master_dict


def create_schedule_list(schedule_str):
    """Generates an 8760 list for schedules. If the value from a key/value pair has 'SCHEDULE' in it, this function
    is called to parse the function parameters and creates the list.

     Parameters
     ----------
     schedule_str : str
         Nested dictionary being merged into master dictionary

     Returns
    -------
    schedule_list: list
        List of floats between 0 to 1. Represents a schedule. Length is 8760.

    """

    # Parse schedule string for schedule name and potential value.
    # EX: "SCHEDULE:CONSTANT-0.2" will result in a list = ["CONSTANT","0.2"]
    parsed_strings = schedule_str.split(":")[1].split("-")

    schedule_name = parsed_strings[0]
    schedule_parameter = parsed_strings[1]

    if schedule_name == "CONSTANT":
        # Return the schedule parameter 8760 times
        schedule_list = [float(schedule_parameter)] * 8760
        return schedule_list

    elif schedule_name == "CONSTANT_DAY":
        # Return the schedule parameter 24 times
        schedule_list = [float(schedule_parameter)] * 24
        return schedule_list

    # If utilizing a predefined schedule from the schedule library, load it here
    elif schedule_name == "LIBRARY":
        # Load schedule JSON
        file_dir = os.path.dirname(__file__)

        # Define output json file path
        schedule_json_path = os.path.join(
            file_dir, "resources", "schedule_library.json"
        )

        with open(schedule_json_path) as f:
            schedule_dict = json.load(f)

        schedule_list = schedule_dict[schedule_parameter]
        return schedule_list

    else:
        raise Exception(f"Schedule named: {schedule_name} is not a valid schedule name")


def remove_index_references_from_key(key):
    """Ingests a string representing a JSON path. Replaces all the '[N]' substrings.
    For example: 'transformers[0]' ->'transformers'

     Parameters
     ----------
     key : str
         String representing a JSON path element that includes integers in square brackets.
         E.g., 'transformers[0]'

     Returns
    -------
    clean_key: str
        JSON path string without square brackets.E.g., 'transformers[0]' ->'transformers'

    """

    # Replace all integers within square brackets in key
    clean_key = re.sub(r"\[\d+\]", "", key)

    return clean_key


def disaggregate_master_ruletest_json(master_json_name, ruleset_doc):
    """Ingests a string representing a JSON file name from rct229/ruletest_engine/ruletest_jsons. JSONs in that
    directory contain ALL ruletests for a particular grouping of rules (e.g., 'envelope_tests.json' has every test case
    for envelope based rules). This scripts breaks out test cases into individual section + rule JSONs.


         Parameters
         ----------
         master_json_name : str
             String representing a name of master JSON file in rct229/ruletest_engine/ruletest_jsons
             E.g., 'envelope_tests.json''
         ruleset_doc : str


    """

    # Get this file's directory
    file_dir = os.path.dirname(__file__)

    # master JSON should be in the ruletest_jsons directory
    master_json_path = os.path.join(
        file_dir, "..", ruleset_doc, master_json_name
    )  # os.path.join(file_dir, "..", ruleset_doc, master_json_name)
    master_dict = None
    try:
        # Check if the master JSON file exists
        if not os.path.exists(master_json_path):
            raise FileNotFoundError(f"File not found: {master_json_path}")

        # Initialize master JSON dictionary
        with open(master_json_path) as f:
            master_dict = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Initialize dictionary used to break out master dictionary into sections and rules
    rule_dictionary = {}

    # Initialize elements used to check section + rule combination
    prev_section = ""
    prev_rule = ""

    # Inner function used for writing out ruletest JSONs
    def write_ruletest_json(section, rule, ruleset_doc):
        # Initialize ruletest json name
        json_name = f"rule_{section}_{rule}.json"
        ruletest_json_name = os.path.join(f"section{section}", f"{json_name}")
        json_file_path = os.path.join(file_dir, "..", ruleset_doc, ruletest_json_name)

        # Dump JSON to string for writing
        json_string = json.dumps(rule_dictionary, indent=4)

        # Write JSON string to file
        with open(json_file_path, "w") as json_file:
            json_file.write(json_string)
            print(
                f"Ruletests for Section {section}, Rule {rule} complete and written to file: {json_name}"
            )

    # Iterate through each key (i.e., ruletest), checking if a subsequent ruletest matches the section and rule number
    # of the previous key. Ruletests of the same section and rule should go in their own JSON.
    for ruletest in master_dict:
        # Initialize this ruletest's dictionary
        ruletest_dict = master_dict[ruletest]

        if len(ruletest.split("-")) != 3:
            raise ValueError(
                f"Ruletest {ruletest} does not have a valid rule id format. Expected format, for example: rule-73j65-a"
            )

        # Map the rule ID to the rule name
        rule_name = rules_dict.get(f"prm9012019rule{ruletest.split('-')[1]}")

        if not rule_name:
            raise ValueError(f"Rule {ruletest.split('-')[1]} not found in rule_map")

        # Extract section and rule number from rule name
        section = int(rule_name.split("rule")[0].split("section")[1])
        rule = int(rule_name.split("rule")[1])
        test_case = ruletest_dict["Test"]

        ordered_ruletest_dict = OrderedDict()
        ordered_ruletest_dict["Section"] = section
        ordered_ruletest_dict["Rule"] = rule
        ordered_ruletest_dict["Test"] = test_case

        # Add remaining keys, preserving their original order
        for key, value in ruletest_dict.items():
            if key not in {"Test", "Section", "Rule"}:  # Avoid duplicating keys
                ordered_ruletest_dict[key] = value

        # Replace the standard rule_id
        ordered_ruletest_dict["standard"]["rule_id"] = f"{section}-{rule}"
        # Create unique ID for this rule and previous
        rule_id = f"{section}-{rule}"
        prev_rule_id = f"{prev_section}-{prev_rule}"

        # New section + rule. Write out last rule test dictionary before creating a new one
        if prev_section != "":
            if rule_id != prev_rule_id:
                # Write out previous rule dictionary, then initialize a new one
                write_ruletest_json(prev_section, prev_rule, ruleset_doc)

                # Wipe and reinitailize rule_dictionary for new section + rule
                rule_dictionary = {}

        # Add this test case to the existing rule_dictionary
        rule_dictionary[f"rule-{rule_id}-{test_case}"] = ordered_ruletest_dict

        # Record previous section
        prev_section = section
        prev_rule = rule

    # Write out final rule dictionary
    write_ruletest_json(prev_section, prev_rule, ruleset_doc)


def disaggregate_master_rmd_json(master_json_name, output_dir, ruleset_doc):
    """Ingests a string representing a JSON file name from rct229/ruletest_engine/ruletest_jsons. JSONs in that
    directory contain either ALL ruletests for a particular grouping of rules (e.g., 'envelope_tests.json' has every
    test case for envelope based rules) or sometimes just RMDs. This scripts breaks out master JSONs without test
    case information (i.e., those that are multiple copies of 229 JSON RMDs)

         Parameters
         ----------
         master_json_name : str
             String representing a name of master JSON file in rct229/ruletest_engine/ruletest_jsons
             E.g., 'system_types.json'

                output_dir : str
                        String representing the output directory (e.g., 'system_types')


    """

    # Get this file's directory
    file_dir = os.path.dirname(__file__)

    # master JSON should be in the ruletest_jsons directory
    master_json_path = os.path.join(file_dir, "..", ruleset_doc, master_json_name)

    # Initialize master JSON dictionary
    with open(master_json_path) as f:
        master_dict = json.load(f)

    # Inner function used for writing out ruletest JSONs
    def write_ruletest_json(rmd_dict, json_name, output_dir):
        # Initialize json name and pathing
        json_name = os.path.join(f"{output_dir}", f"{json_name}")
        json_file_path = os.path.join(file_dir, "..", ruleset_doc, json_name)

        # Dump JSON to string for writing
        json_string = json.dumps(rmd_dict, indent=4)

        # Write JSON string to file
        with open(json_file_path, "w") as json_file:
            json_file.write(json_string)
            print(
                f"RMD for {json_name} complete and written to directory: {output_dir}"
            )

    # Iterate through each key (i.e., ruletest), checking if a subsequent ruletest matches the section and rule number
    # of the previous key. Ruletests of the same section and rule should go in their own JSON.
    for rmd_name in master_dict:
        # Initialize this RMD's dictionary and JSON name
        rmd_dict = master_dict[rmd_name]
        json_name = f"{rmd_name}.json"

        # New section + rule. Write out last rule test dictionary before creating a new one
        write_ruletest_json(rmd_dict, json_name, output_dir)
