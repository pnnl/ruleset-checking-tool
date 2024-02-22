from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
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
                            "fan_system": {
                                "id": "fan_1",
                                "fan_control": "VARIABLE_SPEED_DRIVE",
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
    "type": "BASELINE_0",
}


TEST_RMD_FULL = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
    "data_timestamp": "2024-02-12T09:00Z",
}


def test__TEST_RMD__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_hvac_sys_fan_control_vsd():
    assert is_hvac_sys_fan_sys_vsd(TEST_RMD, "hvac_1") == True


def test_hvac_sys_fan_control_ms():
    assert is_hvac_sys_fan_sys_vsd(TEST_RMD, "hvac_2") == False


def test_hvac_sys_fan_control_null():
    assert is_hvac_sys_fan_sys_vsd(TEST_RMD, "hvac_3") == False
