import json
import os

import jsonschema

from rct229.utils.jsonpath_utils import find_all

file_dir = os.path.dirname(__file__)

SCHEMA_KEY = "ASHRAE229.schema.json"
SCHEMA_ENUM_KEY = "Enumerations2019ASHRAE901.schema.json"
SCHEMA_RESNET_ENUM_KEY = "EnumerationsRESNET.schema.json"
SCHEMA_T24_ENUM_KEY = "Enumerations2019T24.schema.json"
SCHEMA_OUTPUT_KEY = "Output2019ASHRAE901.schema.json"
SCHEMA_PATH = os.path.join(file_dir, SCHEMA_KEY)
SCHEMA_ENUM_PATH = os.path.join(file_dir, SCHEMA_ENUM_KEY)
SCHEMA_T24_ENUM_PATH = os.path.join(file_dir, SCHEMA_T24_ENUM_KEY)
SCHEMA_RESNET_ENUM_PATH = os.path.join(file_dir, SCHEMA_RESNET_ENUM_KEY)
SCHEMA_OUTPUT_PATH = os.path.join(file_dir, SCHEMA_OUTPUT_KEY)


def check_unique_ids_in_ruleset_model_descriptions(rmd):
    """Checks that the ids within each group inside a
    RuleSetModelInstance are unique

    The strategy is to first find all unique json paths to all lists inside the
    RuleSetModelInstance, with all list indexes set to [*]. For example,
    the general jsonpath to the building_segments is "buildings[*].building_segments".
    Then, for each of these unique list_paths, we use find_all using the jsonpath
    list_path[*].id to find all the ids for this path and check that they are unique.

    Parameters
    ----------
    rmd : dict
        A dictionary representing an RMD

    Returns
    -------
    str
        An error message listing any paths that do not have unique ids. The empty string
        indicates that all appropriate ids are unique.
    """
    # The schema does not require the ruleset_model_descriptions field, default to []
    ruleset_model_descriptions = rmd.get("ruleset_model_descriptions", [])

    bad_paths = []
    for rmi_index, rmi in enumerate(ruleset_model_descriptions):
        # Collect all jsonpaths to lists
        paths = json_paths_to_lists(rmi)

        for list_path in paths:
            ids = find_all(list_path + "[*].id", rmi)
            if len(ids) != len(set(ids)):
                # The ids are not unique
                # list_path starts with "$" that must be removed
                bad_path = f"ruleset_model_descriptions[{rmi_index}]{list_path[1:]}"
                bad_paths.append(bad_path)

    error_msg = f"Non-unique ids for paths: {'; '.join(bad_paths)}" if bad_paths else ""

    return error_msg


# json_paths_to_lists, json_paths_to_lists_from_dict, and json_paths_to_lists_from_list
# work together


def json_paths_to_lists(val, path="$"):
    """Determines all the generic json paths to lists inside an object

    If a json path has a list index, that index is replaced with [*] to make it
    generic.

    Parameters
    ----------
    val : any
        Only dict and list objects are processed, all others are ignored
    path : str
        A json path representing a generic path to val in a larger structure

    Returns
    -------
    set
        A set of unique generic json paths to lists inside val
    """
    paths = set()
    if isinstance(val, dict):
        paths = json_paths_to_lists_from_dict(val, path)
    elif isinstance(val, list):
        paths = json_paths_to_lists_from_list(val, path)

    return paths


def json_paths_to_lists_from_dict(rmd_dict, path):
    """Determines all the generic json paths to lists inside an dictionary

    If a json path has a list index, that index is replaced with [*] to make it
    generic.

    Parameters
    ----------
    rmd_dict : dict

    path : str
        A json path representing a generic path to rmd_dict in a larger structure

    Returns
    -------
    set
        A set of unique generic json paths to lists inside rmd_dict
    """
    paths = set()
    for key, val in rmd_dict.items():
        new_path = f"{path}.{key}"
        new_paths = json_paths_to_lists(val, new_path)
        paths = paths.union(new_paths)

    return paths


def json_paths_to_lists_from_list(rmd_list, path):
    """Determines all the generic json paths to lists inside a list

    If a json path has a list index, that index is replaced with [*] to make it
    generic.

    Parameters
    ----------
    rmd_list : dict

    path : str
        A json path representing a generic path to rmd_list in a larger structure

    Returns
    -------
    set
        A set of unique generic json paths to lists inside rmd_list
    """
    paths = {path}
    for val in rmd_list:
        new_path = f"{path}[*]"
        new_paths = json_paths_to_lists(val, new_path)
        paths = paths.union(new_paths)

    return paths


def non_schema_validate_rmr(rmr_obj):
    """Provides non-schema validation for an RMR"""

    unique_id_error = check_unique_ids_in_ruleset_model_descriptions(rmr_obj)
    passed = not unique_id_error
    error = unique_id_error or None

    return {"passed": passed, "error": error}


def schema_validate_rmr(rmr_obj):
    """Validates an RMR against the schema

    This code follows the outline given in
    https://stackoverflow.com/questions/53968770/how-to-set-up-local-file-references-in-python-jsonschema-document
    """

    # Load the schema files
    with open(SCHEMA_PATH) as json_file:
        schema = json.load(json_file)
    with open(SCHEMA_ENUM_PATH) as json_file:
        schema_enum = json.load(json_file)
    with open(SCHEMA_T24_ENUM_PATH) as json_file:
        schema_t24_enum = json.load(json_file)
    with open(SCHEMA_RESNET_ENUM_PATH) as json_file:
        schema_resnet_enum = json.load(json_file)
    with open(SCHEMA_OUTPUT_PATH) as json_file:
        schema_output = json.load(json_file)

    # Create a resolver which maps schema references to schema objects
    schema_store = {
        SCHEMA_KEY: schema,
        SCHEMA_ENUM_KEY: schema_enum,
        SCHEMA_T24_ENUM_KEY: schema_t24_enum,
        SCHEMA_RESNET_ENUM_KEY: schema_resnet_enum,
        SCHEMA_OUTPUT_KEY: schema_output,
    }
    resolver = jsonschema.RefResolver.from_schema(schema, store=schema_store)

    # Create a validator
    Validator = jsonschema.validators.validator_for(schema)
    validator = Validator(schema, resolver=resolver)

    try:
        # Throws ValidationError on failure
        validator.validate(rmr_obj)
        return {"passed": True, "error": None}
    except jsonschema.exceptions.ValidationError as err:
        return {"passed": False, "error": "schema invalid: " + err.message}


def validate_rmr(rmr_obj):
    """Validate an RMR against the schema and other high-level checks"""
    # Validate against the schema
    result = schema_validate_rmr(rmr_obj)

    if result["passed"]:
        # Provide non-schema validation
        result = non_schema_validate_rmr(rmr_obj)

    return result
