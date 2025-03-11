from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
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
                            "id": "zone 1",
                            "terminals": [
                                {"id": "terminal_1"},
                                {"id": "terminal_2", "heating_source": "HOT_WATER"},
                                {"id": "terminal_3", "heating_source": "ELECTRIC"},
                            ],
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


def test__all_terminal_heat_source__hot_water():
    assert are_all_terminal_heat_sources_hot_water(TEST_RMD, ["terminal_2"]) == True


def test__all_terminal_heat_source__hot_water_or_null():
    assert (
        are_all_terminal_heat_sources_hot_water(TEST_RMD, ["terminal_1", "terminal_2"])
        == False
    )


def test__all_terminal_heat_source__not_hot_water():
    assert (
        are_all_terminal_heat_sources_hot_water(TEST_RMD, ["terminal_2", "terminal_3"])
        == False
    )
