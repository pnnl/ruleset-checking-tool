from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_none import (
    is_hvac_sys_cooling_type_none,
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
                            "cooling_system": {
                                "id": "cooling_1",
                                "cooling_system_type": "NONE",
                                "chilled_water_loop": "CHW_Loop_1",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "cooling_system": {
                                "id": "cooling_2",
                                "cooling_system_type": "DIRECT_EXPANSION",
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
}


def test_hvac_sys_cooling_type_none():
    assert is_hvac_sys_cooling_type_none(TEST_RMD, "hvac_1") == True


def test__hvac_sys_cooling_type_DX():
    assert is_hvac_sys_cooling_type_none(TEST_RMD, "hvac_2") == False


def test__hvac_sys_cooling_type_null():
    assert is_hvac_sys_cooling_type_none(TEST_RMD, "hvac_3") == True
