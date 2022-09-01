from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_there_only_one_hvac_sys_heating_system import (
    is_there_only_one_hvac_sys_heating_system,
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
                            "heating_system": [
                                {
                                    "id": "heating_1",
                                }
                            ],
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "heating_system": [
                                {"id": "heating_2"},
                                {"id": "heating_3"},
                            ],
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


def test__only_one_hvac_sys_heating_system():
    assert is_there_only_one_hvac_sys_heating_system(TEST_RMD, "hvac_1") == True


def test__two_hvac_sys_heating_system():
    assert is_there_only_one_hvac_sys_heating_system(TEST_RMD, "hvac_2") == False


def test__no_hvac_sys_heating_system():
    assert is_there_only_one_hvac_sys_heating_system(TEST_RMD, "hvac_3") == False
