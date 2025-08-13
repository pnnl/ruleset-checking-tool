from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_on_same_floor_list import (
    get_zones_on_same_floor_list,
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
                        {"id": "zone 1", "floor_name": "floor 1"},
                        {"id": "zone 2", "floor_name": "floor 2"},
                    ],
                },
                {
                    "id": "building_segment_2",
                    "zones": [
                        {"id": "zone 2-1", "floor_name": "floor 1"},
                        {"id": "zone 2-2", "floor_name": "floor 1"},
                    ],
                },
            ],
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
}


def test__TEST_RPD_FIXED_TYPE__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zones_on_floor_1__success():
    assert get_zones_on_same_floor_list(TEST_RMD, "zone 1") == [
        "zone 1",
        "zone 2-1",
        "zone 2-2",
    ]


def test__get_zones_on_floor_2__success():
    assert get_zones_on_same_floor_list(TEST_RMD, "zone 2") == ["zone 2"]
