from rct229.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_5 import (
    is_baseline_system_5,
)
from rct229.schema.validate import schema_validate_rmr

SYS_5_TEST_RMD = {
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
                                            "id": "VAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 5",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 5B",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 5",
                                    "cooling_system": {
                                        "id": "DX Coil 1",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 5B",
                                    "cooling_system": {
                                        "id": "DX Coil 2",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 2",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 2",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 2"}],
                                        "return_fans": [{"id": "Return Fan 2"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "pumps": [
                {
                    "id": "Boiler Pump 1",
                    "loop_or_piping": "Boiler Loop 1",
                    "speed_control": "FIXED_SPEED",
                }
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
            ],
            "external_fluid_source": [
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                }
            ],
        }
    ],
}


def test__TEST_RMD_baseline_system_5__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_5_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_is_baseline_system_5_true():
    assert (
        is_baseline_system_5(
            SYS_5_TEST_RMD["ruleset_model_instances"][0],
            "System 5",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_5
    )


def test_is_baseline_system_5_test_json_true():
    assert (
        is_baseline_system_5(
            load_system_test_file("System_5_PVAV_HW_Reheat.json")[
                "ruleset_model_instances"
            ][0],
            "System 5",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_5
    )


def test_is_baseline_system_5B_true():
    assert (
        is_baseline_system_5(
            SYS_5_TEST_RMD["ruleset_model_instances"][0],
            "System 5B",
            ["VAV Air Terminal 2"],
            ["Thermal Zone 2"],
        )
        == HVAC_SYS.SYS_5B
    )


def test_is_baseline_system_5B_test_json_true():
    assert (
        is_baseline_system_5(
            load_system_test_file("System_5b_PVAV_HW_Reheat.json")[
                "ruleset_model_instances"
            ][0],
            "System 5",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_5B
    )
