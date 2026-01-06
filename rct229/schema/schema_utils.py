import json
import os
import re
from copy import deepcopy

from jsonpath_ng.ext import parse as parse_jsonpath
from pydash.objects import set_

import rct229.schema.config as config
from rct229.schema.schema_store import SchemaStore

# ------------------------------------------------------------------------------
# Global caches (safe)
# ------------------------------------------------------------------------------
_SCHEMA_CACHE: dict[str, dict] = {}
_CLEAN_UNIT_CACHE: dict[str, str] = {}


# ------------------------------------------------------------------------------
# Schema helpers
# ------------------------------------------------------------------------------


def get_schema_definitions_dictionary():
    cache_key = SchemaStore.SCHEMA_KEY

    if cache_key in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[cache_key]

    file_dir = os.path.dirname(__file__)
    json_schema_path = os.path.join(file_dir, cache_key)

    with open(json_schema_path) as f:
        schema_dictionary = json.load(f)["definitions"]

    _SCHEMA_CACHE[cache_key] = schema_dictionary
    return schema_dictionary


def get_secondary_schema_root_dictionary(secondary_json_string):
    if secondary_json_string in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[secondary_json_string]

    file_dir = os.path.dirname(__file__)
    json_schema_path = os.path.join(file_dir, secondary_json_string)

    with open(json_schema_path) as f:
        schema_dictionary = json.load(f)["definitions"]

    _SCHEMA_CACHE[secondary_json_string] = schema_dictionary
    return schema_dictionary


def clean_schema_units(schema_unit_str: str) -> str:
    cached = _CLEAN_UNIT_CACHE.get(schema_unit_str)
    if cached is not None:
        return cached

    cleaned = schema_unit_str
    if "-" in schema_unit_str:
        parts = schema_unit_str.split("/")
        for i, part in enumerate(parts):
            if "-" in part:
                parts[i] = "(" + re.sub("-", "*", part) + ")"
        cleaned = "/".join(parts)

    _CLEAN_UNIT_CACHE[schema_unit_str] = cleaned
    return cleaned


def return_json_schema_reference(object_dict, key):
    secondary_schema_files = ["Output2019ASHRAE901.schema.json"]
    properties_dict = object_dict["properties"][key]

    if "items" in properties_dict:
        if "$ref" in properties_dict["items"]:
            return properties_dict["items"]["$ref"].split("/")[-1]
        return properties_dict["items"]["oneOf"][0]["$ref"].split("/")[-1]

    if "$ref" in properties_dict:
        return properties_dict["$ref"].split("/")[-1]

    if "oneOf" in properties_dict:
        ref = properties_dict["oneOf"][0]["$ref"]
        secondary_json = ref.split("#")[0]

        if secondary_json in secondary_schema_files:
            return ref
        if secondary_json == SchemaStore.SCHEMA_KEY:
            return ref.split("/")[-1]

        raise ValueError(f"Secondary schema '{secondary_json}' not found")

    raise ValueError(f"No $ref found for {properties_dict}")


def find_schema_unit_for_json_path(key_list):
    root_key = "RulesetProjectDescription"
    secondary_schema_files = [SchemaStore.get_active_output_schema()]

    schema_dict = get_schema_definitions_dictionary()
    dict_ref = schema_dict[root_key]

    key_list_head = key_list[:-1]
    last_key = key_list[-1]

    for key in key_list_head:
        reference_string = return_json_schema_reference(dict_ref, key)

        if reference_string.split("#")[0] in secondary_schema_files:
            schema_dict = get_secondary_schema_root_dictionary(
                reference_string.split("#")[0]
            )
            root_key = reference_string.split("/")[-1].split(".")[0]
            dict_ref = schema_dict[root_key]
        else:
            dict_ref = schema_dict[reference_string]

    props = dict_ref.get("properties", {})
    if last_key in props and "units" in props[last_key]:
        return props[last_key]["units"]

    return None


# ------------------------------------------------------------------------------
# Quantification
# ------------------------------------------------------------------------------


def quantify_rmd(rmd):
    """
    Replace numeric values with Pint quantities using schema-defined units.
    Optimized but behavior-identical to the original implementation.
    """
    rmd = deepcopy(rmd)

    ureg = config.ureg
    set_value = set_

    schema_unit_cache = {}
    path_key_cache = {}

    for match in parse_jsonpath("$..*").find(rmd):
        val = match.value

        if isinstance(val, (int, float)):
            is_list = False
        elif (
            isinstance(val, list)
            and val
            and all(isinstance(v, (int, float)) for v in val)
        ):
            is_list = True
        else:
            continue

        full_path = str(match.full_path)

        key_list = path_key_cache.get(full_path)
        if key_list is None:
            key_list = re.split(r"\.\[\d+\]\.|\.", full_path)
            path_key_cache[full_path] = key_list

        key_tuple = tuple(key_list)
        schema_unit_str = schema_unit_cache.get(key_tuple)

        if schema_unit_str is None:
            schema_unit_str = find_schema_unit_for_json_path(key_list)
            schema_unit_cache[key_tuple] = schema_unit_str

        if schema_unit_str is None:
            continue

        pint_unit_str = clean_schema_units(schema_unit_str)

        if is_list:
            set_value(
                rmd,
                full_path,
                [v * ureg(pint_unit_str) for v in val],
            )
        else:
            set_value(
                rmd,
                full_path,
                val * ureg(pint_unit_str),
            )

    return rmd
