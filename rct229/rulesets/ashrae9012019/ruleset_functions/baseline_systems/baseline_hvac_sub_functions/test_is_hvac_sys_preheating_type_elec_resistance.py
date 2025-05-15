from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_elec_resistance import (
    is_hvac_sys_preheating_type_elec_resistance,
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
                                "type": "ELECTRIC_RESISTANCE",
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


def test__preheatheating_type__fluid_loop():
    assert is_hvac_sys_preheating_type_elec_resistance(TEST_RMD, "hvac_1") == False


def test__preheatheating_type__electric_resistance():
    assert is_hvac_sys_preheating_type_elec_resistance(TEST_RMD, "hvac_2") == True


def test__preheatheating_type__data_missing():
    assert is_hvac_sys_preheating_type_elec_resistance(TEST_RMD, "hvac_3") == False
