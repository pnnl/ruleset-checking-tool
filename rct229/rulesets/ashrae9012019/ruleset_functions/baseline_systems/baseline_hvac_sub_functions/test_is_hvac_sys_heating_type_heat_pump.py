from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_heat_pump import (
    is_hvac_sys_heating_type_heat_pump,
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
                            "heating_system": {
                                "id": "heating_1",
                                "type": "HEAT_PUMP",
                                "hot_water_loop": "HW_Loop_1",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "heating_system": {
                                "id": "heating_2",
                                "type": "FLUID_LOOP",
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


def test_hvac_sys_heating_type_heat_pump_true():
    assert is_hvac_sys_heating_type_heat_pump(TEST_RMD, "hvac_1") == True


def test__hvac_sys_heating_type_heat_pump_false():
    assert is_hvac_sys_heating_type_heat_pump(TEST_RMD, "hvac_2") == False


def test__hvac_sys_heating_type_heat_pump_no_heating_system():
    assert is_hvac_sys_heating_type_heat_pump(TEST_RMD, "hvac_3") == False
