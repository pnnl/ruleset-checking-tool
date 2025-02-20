from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_purchased_heating import (
    is_hvac_sys_preheat_fluid_loop_purchased_heating,
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
                            "preheat_system": {
                                "id": "preheat_system_1",
                                "hot_water_loop": "HW_Loop_1",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "preheat_system": {
                                "id": "preheat_system_2",
                                "hot_water_loop": "ST_Loop_1",
                            },
                        },
                        {
                            # Case where there is no preheat system
                            "id": "hvac_3",
                            "preheat_system": {
                                "id": "preheat_system_3",
                                "hot_water_loop": "CHW_Loop_1",
                            },
                        },
                        {
                            # Case where there is no preheat system
                            "id": "hvac_4"
                        },
                    ],
                }
            ],
        }
    ],
    "fluid_loops": [
        {"id": "HW_Loop_1", "type": "HEATING"},
        {"id": "ST_Loop_1", "type": "HEATING"},
        {"id": "CHW_Loop_1", "type": "COOLING"},
    ],
    "external_fluid_sources": [
        {"id": "fluid_loop_1", "loop": "HW_Loop_1", "type": "HOT_WATER"},
        {"id": "fluid_loop_2", "loop": "ST_Loop_1", "type": "STEAM"},
        {"id": "fluid_loop_3", "loop": "CHW_Loop_1", "type": "CHILLED_WATER"},
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


def test__preheat_fluid_loop_purchased_heating_hw():
    assert is_hvac_sys_preheat_fluid_loop_purchased_heating(TEST_RMD, "hvac_1") == True


def test__preheat_fluid_loop_purchased_heating_steam():
    assert is_hvac_sys_preheat_fluid_loop_purchased_heating(TEST_RMD, "hvac_2") == True


def test__preheat_fluid_loop_purchased_heating_not_external():
    assert is_hvac_sys_preheat_fluid_loop_purchased_heating(TEST_RMD, "hvac_3") == False


def test__preheat_fluid_loop_purchased_heating_no_preheat_sys():
    assert is_hvac_sys_preheat_fluid_loop_purchased_heating(TEST_RMD, "hvac_4") == False
