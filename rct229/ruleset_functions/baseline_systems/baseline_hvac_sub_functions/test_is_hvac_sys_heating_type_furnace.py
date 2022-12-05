from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_furnace import (
    is_hvac_sys_heating_type_furnace,
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
                            "heating_system": {
                                "id": "heating_1",
                                "heating_system_type": "FURNACE",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "heating_system": {
                                "id": "heating_2",
                                "heating_system_type": "FLUID_LOOP",
                                "hot_water_loop": "HW_Loop_2",
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
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_hvac_sys_heating_type_furnace_true():
    assert is_hvac_sys_heating_type_furnace(TEST_RMD, "hvac_1") == True


def test__hvac_sys_heating_type_furnace_false():
    assert is_hvac_sys_heating_type_furnace(TEST_RMD, "hvac_2") == False


def test__hvac_sys_heating_type_furnace_no_heating_system():
    assert is_hvac_sys_heating_type_furnace(TEST_RMD, "hvac_3") == False
