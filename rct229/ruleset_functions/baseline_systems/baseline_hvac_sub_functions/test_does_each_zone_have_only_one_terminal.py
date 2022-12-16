from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.schema.validate import schema_validate_rmr

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
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
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
