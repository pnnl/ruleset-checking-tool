from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rmd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Zone 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "service_water_heating_uses": [
                                        {"id": "service water heating uses 1"}
                                    ],
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
    "data_timestamp": "2024-02-12T09:00Z",
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rmd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
