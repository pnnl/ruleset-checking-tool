from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_11_2 import (
    is_baseline_system_11_2,
)
from rct229.schema.validate import schema_validate_rmr

SYS_11_2_TEST_RMD = {
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
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11.2",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 1A",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1A",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 11.2A",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type 11.2",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1",
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
                                    "id": "System Type 11.2A",
                                    "cooling_system": {
                                        "id": "CHW Coil 1A",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "HHW Coil 1A",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1A",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1A"}],
                                        "return_fans": [{"id": "Return Fan 1A"}],
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
                    "design_capacity": 117228.44444444445,
                }
            ],
            "chillers": [
                {
                    "id": "Chiller 1",
                    "cooling_loop": "Chiller Loop 1",
                    "energy_source_type": "ELECTRICITY",
                }
            ],
            "external_fluid_source": [
                {
                    "id": "Purchased CHW 1",
                    "loop": "Purchased CHW Loop 1",
                    "type": "CHILLED_WATER",
                }
            ],
            "pumps": [
                {
                    "id": "HW Pump 1",
                    "loop_or_piping": "Boiler Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Chiller Pump 1",
                    "loop_or_piping": "Chiller Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
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
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary Loop 1", "type": "COOLING"}],
                },
                {"id": "Purchased CHW Loop 1", "type": "COOLING"},
            ],
        }
    ],
}


def test__TEST_RMD_baseline_system_11_2__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_11_2_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_is_baseline_system__11_2():
    assert (
        is_baseline_system_11_2(
            SYS_11_2_TEST_RMD["ruleset_model_instances"][0],
            "System Type 11.2",
            ["VAV Air Terminal 1"],
            ["Thermal Zone 1"],
        )
        == HVAC_SYS.SYS_11_2
    )


def test_is_baseline_system__11_2A():
    assert (
        is_baseline_system_11_2(
            SYS_11_2_TEST_RMD["ruleset_model_instances"][0],
            "System Type 11.2A",
            ["VAV Air Terminal 1A"],
            ["Thermal Zone 1A"],
        )
        == HVAC_SYS.SYS_11_2A
    )
