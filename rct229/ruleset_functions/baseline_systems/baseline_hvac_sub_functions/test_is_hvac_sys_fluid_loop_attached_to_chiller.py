from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
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
                                "id": "cooling_system",
                                "chilled_water_loop": "CHW_Loop_1",
                            },
                        },
                        {
                            # Case where the cooling system has a wrong chilled_water_loop id
                            "id": "hvac_2",
                            "cooling_system": {
                                "id": "cooling_system",
                                "chilled_water_loop": "CHW_Loop_2",
                            },
                        },
                        {
                            # Case where there is no cooling system
                            "id": "hvac_3",
                        },
                    ],
                }
            ],
        }
    ],
    "chillers": [
        {
            "id": "chiller_1",
            "cooling_loop": "CHW_Loop_1",
        }
    ],
    "fluid_loops": [
        {
            "id": "CHW_Loop_1",
            "type": "COOLING",
        }
    ],
}

TEST_RMD_FULL = {"id": "229_01", "ruleset_model_instances": [TEST_RMD]}


def test__cooling_attached_to_chiller():
    assert is_hvac_sys_fluid_loop_attached_to_chiller(TEST_RMD, "hvac_1") == True


def test__cooling_attached_to_chiller_failed_fluidloop():
    assert is_hvac_sys_fluid_loop_attached_to_chiller(TEST_RMD, "hvac_2") == False


def test__cooling_attached_to_chiller_failed_no_cooling():
    assert is_hvac_sys_fluid_loop_attached_to_chiller(TEST_RMD, "hvac_3") == False
