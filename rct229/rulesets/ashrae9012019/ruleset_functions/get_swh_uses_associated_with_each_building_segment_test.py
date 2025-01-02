from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

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
                                        {
                                            "id": "service water heating uses 1_1",
                                            "use": 100,
                                        },
                                        {
                                            "id": "service water heating uses 1_2",
                                            "use": 50,
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "Building Segment 2",
                    "zones": [
                        {
                            "id": "Zone 2",
                            "spaces": [
                                {
                                    "id": "Space 2",
                                    "service_water_heating_uses": [
                                        {
                                            "id": "service water heating uses 2_1",
                                            "use": 30,
                                        },
                                        {
                                            "id": "service water heating uses 2_2",
                                            "use": 15,
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                },
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
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_swh_uses_associated_with_each_building_segment__bldg_segment_ids_exist():
    assert get_swh_uses_associated_with_each_building_segment(TEST_RMD) == {
        "Building Segment 1": [
            {
                "id": "service water heating uses 1_1",
                "use": 100,
            },
            {
                "id": "service water heating uses 1_2",
                "use": 50,
            },
        ],
        "Building Segment 2": [
            {
                "id": "service water heating uses 2_1",
                "use": 30,
            },
            {
                "id": "service water heating uses 2_2",
                "use": 15,
            },
        ],
    }
