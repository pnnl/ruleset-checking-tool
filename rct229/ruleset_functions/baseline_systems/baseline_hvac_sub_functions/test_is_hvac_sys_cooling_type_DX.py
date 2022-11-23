from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
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
                                "cooling_system_type": "DIRECT_EXPANSION",
                            },
                        },
                        {
                            "id": "hvac_2",
                            "cooling_system": {
                                "id": "cooling_2",
                                "cooling_system_type": "NON_MECHANICAL",
                            },
                        },
                    ],
                }
            ],
        }
    ],
}


def test_hvac_sys_cooling_type_DX_true():
    assert is_hvac_sys_cooling_type_dx(TEST_RMD, "hvac_1") == True


def test_hvac_sys_cooling_type_DX_false():
    assert is_hvac_sys_cooling_type_dx(TEST_RMD, "hvac_2") == False
