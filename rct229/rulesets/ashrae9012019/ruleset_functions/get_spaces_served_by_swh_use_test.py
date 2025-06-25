from rct229.rulesets.ashrae9012019.ruleset_functions.get_spaces_served_by_swh_use import (
    get_spaces_served_by_swh_use,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "service_water_heating_uses": ["SWH use 1"],
                                },
                                {
                                    "id": "Space 2",
                                    "service_water_heating_uses": ["SWH use 1"],
                                },
                                {
                                    "id": "Space 3",
                                    "service_water_heating_uses": ["SWH use 2"],
                                },
                                {
                                    "id": "Space 4",
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
    "service_water_heating_uses": [
        {
            "id": "SWH use 2",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "SWH use 1",
            "served_by_distribution_system": "SWH Distribution 1",
        },
    ],
    "service_water_heating_distribution_systems": [
        {
            "id": "SWH Distribution 1",
        }
    ],
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


def test__get_spaces_served_by_swh_use__apply_to_2_spaces():
    assert get_spaces_served_by_swh_use(
        TEST_RMD,
        "SWH use 1",
    ) == ["Space 1", "Space 2"]


def test__get_spaces_served_by_swh_use__apply_to_all_spaces():
    assert get_spaces_served_by_swh_use(
        TEST_RMD,
        "SWH use 5",
    ) == ["Space 1", "Space 2", "Space 3", "Space 4"]
