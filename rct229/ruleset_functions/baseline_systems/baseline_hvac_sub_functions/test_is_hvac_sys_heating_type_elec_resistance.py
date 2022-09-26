from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_elec_resistance import (
    is_hvac_sys_heating_type_elec_resistance,
)

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                            "heating_system": {
                                "id": "heating_1",
                                "heating_system_type": "ELECTRIC_RESISTANCE",
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


def test_hvac_sys_heating_type_electric_resistance():
    assert is_hvac_sys_heating_type_elec_resistance(TEST_RMD, "hvac_1") == True


def test__hvac_sys_heating_type_fluid_loop():
    assert is_hvac_sys_heating_type_elec_resistance(TEST_RMD, "hvac_2") == False


def test__hvac_sys_heating_type_no_heating_system():
    assert is_hvac_sys_heating_type_elec_resistance(TEST_RMD, "hvac_3") == False
