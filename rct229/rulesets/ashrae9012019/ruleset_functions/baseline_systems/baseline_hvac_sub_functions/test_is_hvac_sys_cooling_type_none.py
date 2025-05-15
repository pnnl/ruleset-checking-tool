from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_none import (
    is_hvac_sys_cooling_type_none,
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
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                            "cooling_system": {
                                "id": "cooling_1",
                                "type": "NONE",
                                "chilled_water_loop": "CHW_Loop_1",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "cooling_system": {
                                "id": "cooling_2",
                                "type": "DIRECT_EXPANSION",
                            },
                        },
                        {
                            # Case where there is no preheat system
                            "id": "hvac_3",
                            "cooling_system": {"id": "cooling_3"},
                        },
                    ],
                }
            ],
        }
    ],
    "fluid_loops": [
        {
            "id": "CHW_Loop_1",
            "type": "COOLING",
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


def test_hvac_sys_cooling_type_none():
    assert is_hvac_sys_cooling_type_none(TEST_RMD, "hvac_1") == True


def test__hvac_sys_cooling_type_DX():
    assert is_hvac_sys_cooling_type_none(TEST_RMD, "hvac_2") == False


def test__hvac_sys_cooling_type_null():
    assert is_hvac_sys_cooling_type_none(TEST_RMD, "hvac_3") == True
