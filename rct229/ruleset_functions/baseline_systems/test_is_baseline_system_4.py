# hvac_id = "System 4" => Sys_3, [Thermal Zone 1], [Air Terminal]

SYS_4_RMD = {
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
                                            "id": "Air Terminal",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilation_air_conditioning_system": "System Type 4",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilation_air_conditioning_systems": [
                                {
                                    "id": "System Type 4",
                                    "cooling_system": {
                                        "id": "DX Coil 1",
                                        "cooling_system_type": "DIRECT_EXPANSION",
                                    },
                                    "heating_system": {
                                        "id": "HP Coil 1",
                                        "heating_system_type": "HEAT_PUMP",
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
