# hvac_id = "PTAC 1" => Sys_1, [Thermal Zone 1], [PTAC Terminal 1]
# hvac_id = "PTAC 1a" => Sys_1a, [Thermal Zone 1a], [PTAC Terminal 1a]
# hvac_id = "PTAC 1b" => Sys_1b, [Thermal Zone 1b], [PTAC Terminal 1b]
# hvac_id = "PTAC 1c" => Sys_1c, [Thermal Zone 1c], [PTAC Terminal 1c]
from rct229.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_1 import (
    is_baseline_system_1,
)
from rct229.schema.validate import schema_validate_rmr

SYS_1_TEST_RMD = {
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
                                            "id": "PTAC Terminal 1",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1b",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "PTAC Terminal 1b",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1b",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1a",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "PTAC Terminal 1a",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "fan": {"id": "fan 1a"},
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "cooling_source": "CHILLED_WATER",
                                            "cooling_from_loop": "Purchased CHW Loop 1",
                                            # this is necessary in the current setup.
                                            # This parameter connects hvac_b with specific terminal so that the
                                            # function is_baseline_system_1 can execute within the correct zone list.
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1a",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1c",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "PTAC Terminal 1c",
                                            "is_supply_ducted": False,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "fan": {"id": "fan 1c"},
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "cooling_source": "CHILLED_WATER",
                                            "cooling_from_loop": "Purchased CHW Loop 1",
                                            # this is necessary in the current setup.
                                            # This parameter connects hvac_b with specific terminal so that the
                                            # function is_baseline_system_1 can execute within the correct zone list.
                                            "served_by_heating_ventilating_air_conditioning_system": "PTAC 1c",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "PTAC 1",
                                    "cooling_system": {
                                        "id": "DX Coil 1",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                    },
                                },
                                {
                                    "id": "PTAC 1b",
                                    "cooling_system": {
                                        "id": "DX Coil 1b",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1b",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1b",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1b"}],
                                    },
                                },
                                {
                                    "id": "PTAC 1a",
                                },
                                {
                                    "id": "PTAC 1c",
                                },
                            ],
                        }
                    ],
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "condensing_loop": "Condenser Loop 1",
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "fluid_loops": [
                {
                    "id": "Boiler Loop 1",
                    "type": "HEATING",
                    "heating_design_and_control": {
                        "id": "DAC1",
                        "minimum_flow_fraction": 0.25,
                    },
                },
                {
                    "id": "Purchased HW Loop 1",
                    "type": "HEATING",
                },
                {
                    "id": "Purchased CHW Loop 1",
                    "type": "COOLING",
                },
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                },
            ],
            "external_fluid_source": [
                {
                    "id": "Purchased HW",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CHW",
                    "loop": "Purchased CHW Loop 1",
                    "type": "CHILLED_WATER",
                },
            ],
        }
    ],
}


def test__TEST_RMD_baseline_system_1__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_1_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_is_baseline_system_1_true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_instances"][0],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1
    )


def test_is_baseline_system_1a_true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_instances"][0],
            "PTAC 1a",
            ["PTAC Terminal 1a"],
            ["Thermal Zone 1a"],
        )
        == HVAC_SYS.SYS_1A
    )


def test_is_baseline_system_1b_true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_instances"][0],
            "PTAC 1b",
            ["PTAC Terminal 1b"],
            ["Thermal Zone 1b"],
        )
        == HVAC_SYS.SYS_1B
    )


def test_is_baseline_system_1c_true():
    assert (
        is_baseline_system_1(
            SYS_1_TEST_RMD["ruleset_model_instances"][0],
            "PTAC 1c",
            ["PTAC Terminal 1c"],
            ["Thermal Zone 1c"],
        )
        == HVAC_SYS.SYS_1C
    )


def test_is_baseline_system_1_test_json_true():
    assert (
        is_baseline_system_1(
            load_system_test_file("System_1_PTAC.json")["ruleset_model_instances"][0],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1
    )


def test_is_baseline_system_1_a_test_json_true():
    assert is_baseline_system_1(
        load_system_test_file("System_1a_PTAC.json")["ruleset_model_instances"][0],
        "PTAC 1",
        ["PTAC Terminal 1"],
        ["Thermal Zone 1"],
    )


def test_is_baseline_system_1_b_test_json_true():
    assert (
        is_baseline_system_1(
            load_system_test_file("System_1b_PTAC.json")["ruleset_model_instances"][0],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1B
    )


def test_is_baseline_system_1_c_test_json_true():
    assert (
        is_baseline_system_1(
            load_system_test_file("System_1c_PTAC.json")["ruleset_model_instances"][0],
            "PTAC 1",
            ["PTAC Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_1C
    )

# YJ: Need to check the following systems
# 1C, 8, 9B, 10, 11.1A
