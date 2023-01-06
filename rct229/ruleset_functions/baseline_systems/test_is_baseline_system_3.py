# hvac_id = "System 3" => Sys_3, [Thermal Zone 3], [Air Terminal 3]
# hvac_id = "System 3a" => Sys_3a, [Thermal Zone 3a], [Air Terminal 3a]
# hvac_id = "System 3b" => Sys_3b, [Thermal Zone 3b], [Air Terminal 3b]
# hvac_id = "System 3c" => Sys_3c, [Thermal Zone 3c], [Air Terminal 3c]
from rct229.schema.validate import schema_validate_rmr

SYS_3_RMD = {
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
                                            "id": "Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 3",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 3a",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "Air Terminal 3a",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System Type 3a",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System Type 3",
                                    "cooling_system": {
                                        "id": "DX Coil 3",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "Furnace Coil 3",
                                        "heating_system_type": "FURNACE",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System Type 3a",
                                    "cooling_system": {
                                        "id": "Cooling Coil 3a",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Furnace Coil 3a",
                                        "heating_system_type": "FURNACE",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3a",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 3a"}],
                                    },
                                },
                                {
                                    "id": "System Type 3b",
                                    "cooling_system": {
                                        "id": "DX Coil 3b",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "Heating Coil 3b",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3b",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 3b"}],
                                    },
                                },
                                {
                                    "id": "System Type 3c",
                                    "cooling_system": {
                                        "id": "Cooling Coil 3c",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased CHW Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Heating Coil 3c",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 3c",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 3c"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "fluid_loops": [
                {
                    "id": "Purchased HW Loop 1",
                    "type": "HEATING",
                },
                {
                    "id": "Purchased CHW Loop 1",
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


def test__TEST_RMD_baseline_system_3__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_3_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
