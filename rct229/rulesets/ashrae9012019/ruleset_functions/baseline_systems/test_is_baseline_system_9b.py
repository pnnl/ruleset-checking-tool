from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.is_baseline_system_9b import (
    is_baseline_system_9b,
)
from rct229.schema.validate import schema_validate_rmr

SYS_9B_TEST_RMD = {
    "id": "ASHRAE229 1",
    "ruleset_model_instances": [
        {
            "id": "RMD 1",
            "buildings": [
                {
                    "id": "Building 1",
                    "building_open_schedule": "Required Building Schedule 1",
                    "building_segments": [
                        {
                            "id": "Building Segment 1",
                            "zones": [
                                {
                                    "id": "Thermal Zone 9B",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Constant Air Terminal 9B",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "heating_source": "HOT_WATER",
                                            "fan": {"id": "fan 1"},
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 9B",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 9B",
                                }
                            ],
                        }
                    ],
                }
            ],
            "external_fluid_source": [
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                }
            ],
            "pumps": [
                {
                    "id": "HW Pump 1",
                    "loop_or_piping": "Purchased HW Loop 1",
                    "speed_control": "FIXED_SPEED",
                }
            ],
            "fluid_loops": [{"id": "Purchased HW Loop 1", "type": "HEATING"}],
        }
    ],
}


def test__TEST_RMD_baseline_system_9B__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_9B_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_is_baseline_system_9B_true():
    assert (
        is_baseline_system_9b(
            SYS_9B_TEST_RMD["ruleset_model_instances"][0],
            "System 9B",
            ["Constant Air Terminal 9B"],
            ["Thermal Zone 9B"],
        )
        == True
    )


def test_is_baseline_system_9B_test_json_true():
    assert is_baseline_system_9b(
        load_system_test_file("System_9b_Warm_Air_Furnace_Gas.json")[
            "ruleset_model_instances"
        ][0],
        "System 9B",
        ["Air Terminal"],
        ["Thermal Zone 1"],
    )
