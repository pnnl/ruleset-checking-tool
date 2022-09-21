from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_CV import \
    is_hvac_sys_fan_sys_cv

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
                            "fan_system": {
                                "id": "fan_1",
                                "fan_control": "CONSTANT",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "fan_system": {
                                "id": "fan_2",
                                "fan_control": "MULTISPEED",
                            },
                        },
                        {
                            # Case where there is no preheat system
                            "id": "hvac_3",
                            "fan_system": {"id": "fan_3"},
                        },
                    ],
                }
            ],
        }
    ],
}


def test_hvac_sys_fan_control_cd():
    assert is_hvac_sys_fan_sys_cv(TEST_RMD, "hvac_1") == True


def test_hvac_sys_fan_control_ms():
    assert is_hvac_sys_fan_sys_cv(TEST_RMD, "hvac_2") == False


def test_hvac_sys_fan_control_null():
    assert is_hvac_sys_fan_sys_cv(TEST_RMD, "hvac_3") == False