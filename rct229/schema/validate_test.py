import json
import os
from copy import deepcopy

import pytest

from rct229.schema.validate import (
    check_unique_ids_in_ruleset_model_descriptions,
    json_paths_to_lists,
    json_paths_to_lists_from_dict,
    json_paths_to_lists_from_list,
    non_schema_validate_rmr,
    validate_rmr,
)

EXAMPLES_PATH = "examples"

# Testing validate_rmr; intended to make sure the referenced schemas are connected
# properly and that the example rmr files are schema valid


def test__validate_rmr__with_baseline_rmr():
    with open(os.path.join(EXAMPLES_PATH, "baseline_rmr.json")) as rmr_file:
        rmr_obj = json.load(rmr_file)
    assert validate_rmr(rmr_obj) == {"passed": True, "error": None}


def test__validate_rmr__with_proposed_rmr():
    with open(os.path.join(EXAMPLES_PATH, "proposed_rmr.json")) as rmr_file:
        rmr_obj = json.load(rmr_file)
    assert validate_rmr(rmr_obj) == {"passed": True, "error": None}


def test__validate_rmr__with_user_rmr():
    with open(os.path.join(EXAMPLES_PATH, "user_rmr.json")) as rmr_file:
        rmr_obj = json.load(rmr_file)
    assert validate_rmr(rmr_obj) == {"passed": True, "error": None}


## Testing the three companion functions that find json paths to list

TEST_IDS_RMD = {
    "ruleset_model_descriptions": [
        {
            "id": "rmi_1",
            "buildings": [
                {
                    "id": "bldg_1_1",
                    "building_segments": [
                        {"id": "bs_1_1_1"},
                        {"id": "bs_1_1_2"},
                    ],
                },
                {
                    "id": "bldg_1_2",
                    "building_segments": [
                        {"id": "bs_1_2_1"},
                        # A duplicate
                        {"id": "bs_1_1_2"},
                    ],
                },
            ],
        }
    ]
}

TEST_UNIQUE_IDS_RMD = deepcopy(TEST_IDS_RMD)
TEST_UNIQUE_IDS_RMD["ruleset_model_descriptions"][0]["buildings"][1][
    "building_segments"
][1]["id"] = "bs_1_2_2"


def test__json_paths_to_lists_from_dict():
    assert json_paths_to_lists_from_dict(TEST_IDS_RMD, "$") == {
        "$.ruleset_model_descriptions",
        "$.ruleset_model_descriptions[*].buildings",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments",
    }


def test__json_paths_to_lists_from_list():
    assert json_paths_to_lists_from_list(
        TEST_IDS_RMD["ruleset_model_descriptions"], "$.ruleset_model_descriptions"
    ) == {
        "$.ruleset_model_descriptions",
        "$.ruleset_model_descriptions[*].buildings",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments",
    }


def test__json_paths_to_lists():
    assert json_paths_to_lists(TEST_IDS_RMD) == {
        "$.ruleset_model_descriptions",
        "$.ruleset_model_descriptions[*].buildings",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments",
    }


# -----------------------------------------------


def test__check_unique_ids_in_ruleset_model_descriptions__not_unique():
    assert (
        check_unique_ids_in_ruleset_model_descriptions(TEST_IDS_RMD)
        == "Non-unique ids for paths: ruleset_model_descriptions[0].buildings[*].building_segments"
    )


def test__check_unique_ids_in_ruleset_model_descriptions__unique():
    assert check_unique_ids_in_ruleset_model_descriptions(TEST_UNIQUE_IDS_RMD) == ""


# -----------------------------------------------


def test__non_schema_validate_rmr__not_unique():
    assert non_schema_validate_rmr(TEST_IDS_RMD) == {
        "passed": False,
        "error": [
            "Non-unique ids for paths: ruleset_model_descriptions[0].buildings[*].building_segments",
        ],
    }


def test__non_schema_validate_rmr__unique():
    assert non_schema_validate_rmr(TEST_UNIQUE_IDS_RMD) == {
        "passed": True,
        "error": None,
    }
