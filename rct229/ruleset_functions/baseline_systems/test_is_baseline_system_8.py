# hvac_id = "System 8" => Sys_8, [Thermal Zone 8], [Air Terminal 8]
# hvac_id = "System 8a" => Sys_8a, [Thermal Zone 8a], [Air Terminal 8a]
# hvac_id = "System 8b" => Sys_8b, [Thermal Zone 8b], [Air Terminal 8b]
# hvac_id = "System 8c" => Sys_8c, [Thermal Zone 8c], [Air Terminal 8c]

from rct229.schema.validate import schema_validate_rmr

SYS_8_RMD = {
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
                                            "id": "VAV Air Terminal 8",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8",
                                            "heating_source": "ELECTRIC",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8a",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8a",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8a",
                                            "heating_source": "ELECTRIC",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8b",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8b",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8b",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8c",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8c",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8c",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 8",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "heating_system_type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 8a",
                                    "cooling_system": {
                                        "id": "CHW Coil 8a",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8a",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8a",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 8a"}],
                                        "return_fans": [{"id": "Return Fan 8a"}],
                                    },
                                },
                                {
                                    "id": "System 8b",
                                    "cooling_system": {
                                        "id": "CHW Coil 8b",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8b",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8b",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 8C",
                                    "cooling_system": {
                                        "id": "CHW Coil 8C",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8C",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8C",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
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
            "external_fluid_source": [
                {
                    "id": "Purchased CW 1",
                    "loop": "Chilled Water Loop 1",
                    "type": "CHILLED_WATER",
                },
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CW 2",
                    "loop": "Chilled Water Loop 2",
                    "type": "CHILLED_WATER",
                },
            ],
            "chillers": [{"id": "Chiller 1", "cooling_loop": "Chiller Loop 1"}],
            "pumps": [
                {
                    "id": "Boiler Pump 1",
                    "loop_or_piping": "Boiler Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Chiller Pump 1",
                    "loop_or_piping": "Chiller Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Secondary CHW Pump",
                    "loop_or_piping": "Secondary CHW Loop 1",
                    "speed_control": "VARIABLE_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
                },
                {"id": "Chilled Water Loop 1", "type": "COOLING"},
            ],
        }
    ],
}


def test__TEST_RMD_baseline_system_8__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_8_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
