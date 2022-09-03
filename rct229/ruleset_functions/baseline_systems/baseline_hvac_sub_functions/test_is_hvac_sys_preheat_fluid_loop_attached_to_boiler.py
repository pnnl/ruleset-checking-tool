from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_attached_to_boiler import (
    is_hvac_sys_preheat_fluid_loop_attached_to_boiler,
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
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                            "preheat_system": {
                                "id": "preheat_system",
                                "hot_water_loop": "HW_Loop_1",
                            },
                        },
                        {
                            # Case where the preheat system has a wrong hot_water_loop id
                            "id": "hvac_2",
                            "preheat_system": {
                                "id": "preheat_system",
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


def test__preheat_attached_to_boiler():
    assert is_hvac_sys_preheat_fluid_loop_attached_to_boiler(TEST_RMD, "hvac_1") == True


def test__preheat_attached_to_boiler_failed_fluidloop():
    assert (
        is_hvac_sys_preheat_fluid_loop_attached_to_boiler(TEST_RMD, "hvac_2") == False
    )


def test__preheat_attached_to_boiler_failed_no_preheat():
    assert (
        is_hvac_sys_preheat_fluid_loop_attached_to_boiler(TEST_RMD, "hvac_3") == False
    )
