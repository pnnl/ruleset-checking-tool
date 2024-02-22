from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
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
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                            "preheat_system": {
                                "id": "preheat_system",
                                "hot_water_loop": "HW_Loop_1",
                                "type": "FLUID_LOOP",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "preheat_system": {
                                "id": "preheat_system",
                                "hot_water_loop": "HW_Loop_2",
                                "type": "HEAT_PUMP",
                            },
                        },
                        {
                            # Case where there is no preheat system
                            "id": "hvac_3",
                        },
                    ],
                }
            ],
        }
    ],
    "boilers": [
        {
            "id": "boiler_1",
            "loop": "HW_Loop_1",
        }
    ],
    "fluid_loops": [
        {
            "id": "HW_Loop_1",
            "type": "HEATING",
        }
    ],
    "type": "BASELINE_0",
}

TEST_RMD_FULL = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
    "data_timestamp": "2024-02-12T09:00Z",
}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__preheatheating_type_fluid_loop():
    assert is_hvac_sys_preheating_type_fluid_loop(TEST_RMD, "hvac_1") == True


def test__preheatheating_type_heat_pump():
    assert is_hvac_sys_preheating_type_fluid_loop(TEST_RMD, "hvac_2") == False


def test__preheatheating_type_data_missing():
    assert is_hvac_sys_preheating_type_fluid_loop(TEST_RMD, "hvac_3") == False
