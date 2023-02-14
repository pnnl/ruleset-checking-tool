from rct229.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_2 import (
    is_baseline_system_2,
)
from rct229.schema.validate import schema_validate_rmr

SYS_2_TEST_RMD = {
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
                                    "id": "Thermal Zone 1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "PTHP Terminal 1",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "PTHP 1",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "PTHP 1",
                                    "cooling_system": {
                                        "id": "HP Cooling Coil 1",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "HP Heating Coil 1",
                                        "heating_system_type": "HEAT_PUMP",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
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


def test__TEST_RMD_baseline_system_2__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_2_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__is_baseline_system_2__true():
    assert (
        is_baseline_system_2(
            SYS_2_TEST_RMD["ruleset_model_instances"][0],
            "PTHP 1",
            ["PTHP Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_2
    )


def test__is_baseline_system_2__test_json_true():
    assert (
        is_baseline_system_2(
            load_system_test_file("System_2_PTHP.json")["ruleset_model_instances"][0],
            "PTHP 1",
            ["PTHP Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_2
    )
