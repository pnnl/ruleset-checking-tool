from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_bats_and_swh_use import (
    get_swh_bats_and_swh_use,
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
                                    "service_water_heating_area_type": "HOTEL",
                                    "service_water_heating_uses": [
                                        "service water heating uses 1_1",
                                        "service water heating uses 1_2",
                                    ],
                                }
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
                                    "service_water_heating_area_type": "OFFICE",
                                    "service_water_heating_uses": [
                                        "service water heating uses 2_1",
                                        "service water heating uses 2_2",
                                    ],
                                }
                            ],
                        }
                    ],
                },
            ],
        }
    ],
    "service_water_heating_uses": [
        {
            "id": "service water heating uses 1_1",
            "use": 400,
            "use_units": "POWER",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "service water heating uses 1_2",
            "use": 500,
            "use_units": "POWER",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "service water heating uses 2_1",
            "use": 400,
            "use_units": "POWER",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "service water heating uses 2_2",
            "use": 500,
            "use_units": "POWER",
            "served_by_distribution_system": "SWH Distribution 1",
        },
    ],
    "service_water_heating_distribution_systems": [
        {
            "id": "SWH Distribution 1",
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
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

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_swh_bats_and_swh_use__two_bldg_seg():
    assert get_swh_bats_and_swh_use(TEST_RMD) == {
        "HOTEL": ["service water heating uses 1_1", "service water heating uses 1_2"],
        "OFFICE": ["service water heating uses 2_1", "service water heating uses 2_2"],
    }
