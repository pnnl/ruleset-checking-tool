from rct229.schema.validate import schema_validate_rmr

# hvac_id = "System 6" => Sys_6, [Thermal Zone 1], [VAV Air Terminal 1]
# hvac_id = "System 6b" => Sys_6b, [Thermal Zone 2], [VAV Air Terminal 2]

SYS_6_RMD = {
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
                                            "served_by_heating_ventilation_air_conditioning_system": "System 6",
                                            "heating_source": "ELECTRIC",
                                            "fan": {
                                                "id": "Terminal Fan 1",
                                            },
                                            "fan_configuration": "PARALLEL",
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
                                            "served_by_heating_ventilation_air_conditioning_system": "System 6B",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW 1",
                                            "fan": {
                                                "id": "Terminal Fan 2",
                                            },
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 6",
                                    "cooling_system": {
                                        "id": "DX Coil 1",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "heating_system_type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 6B",
                                    "cooling_system": {
                                        "id": "DX Coil 2",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 2",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW 1",
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


def test__TEST_RMD_baseline_system_6__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_6_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"
