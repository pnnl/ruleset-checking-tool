from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "zones": [
                        {
                            # case with one terminal
                            "id": "zone_1",
                            "terminals": [
                                {"id": "terminal_1", "cooling_source": "NONE"}
                            ],
                        },
                        {
                            # case with more than one terminal
                            "id": "zone_2",
                            "terminals": [
                                {"id": "terminal_1", "cooling_source": "NONE"},
                                {"id": "terminal_2", "cooling_source": "NONE"},
                            ],
                        },
                        {
                            # case with empty terminal
                            "id": "zone_3",
                            "terminals": [],
                        },
                        {
                            # case with no terminal
                            "id": "zone_4",
                        },
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__each_zone_have_only_one_terminal():
    assert does_each_zone_have_only_one_terminal(TEST_RMD, ["zone_1"]) == True


def test__zone_have_two_terminal():
    assert does_each_zone_have_only_one_terminal(TEST_RMD, ["zone_2"]) == False


def test__zone_have_empty_terminal():
    assert does_each_zone_have_only_one_terminal(TEST_RMD, ["zone_3"]) == False


def test__zone_have_no_terminal():
    assert does_each_zone_have_only_one_terminal(TEST_RMD, ["zone_4"]) == False
