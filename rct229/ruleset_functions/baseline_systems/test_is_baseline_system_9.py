from rct229.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_9 import (
    is_baseline_system_9,
)
from rct229.schema.validate import schema_validate_rmr

SYS_9_TEST_RMD = {
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
                                    "id": "Thermal Zone 9",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Constant Air Terminal 9",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 9",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 9",
                                    "heating_system": {
                                        "id": "Furnace Coil 1",
                                        "heating_system_type": "FURNACE",
                                        "energy_source_type": "NATURAL_GAS",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ],
}


def test__TEST_RMD_baseline_system_9__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_9_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_is_baseline_system_9_true():
    assert (
        is_baseline_system_9(
            SYS_9_TEST_RMD["ruleset_model_instances"][0],
            "System 9",
            ["Constant Air Terminal 9"],
            ["Thermal Zone 9"],
        )
        == HVAC_SYS.SYS_9
    )


def test_is_baseline_system_9_test_json_true():
    assert is_baseline_system_9(
        load_system_test_file("System_9_Warm_Air_Furnace_Gas.json")[
            "ruleset_model_instances"
        ][0],
        "System 9",
        ["Air Terminal"],
        ["Thermal Zone 1"],
    )
