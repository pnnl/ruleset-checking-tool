from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1c import (
    does_zone_meet_g3_1_1c,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RPD_FULL = {
    "id": "ASHRAE229 1",
    "ruleset_model_descriptions": [
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
                                # Regular case - False
                                {
                                    "id": "Thermal Zone 1",
                                    "floor_name": "floor_1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "spaces": [
                                        {
                                            "id": "space 1",
                                            "floor_area": 100,
                                            "number_of_occupants": 5,
                                            "interior_lighting": [
                                                {
                                                    "id": "interior_lighting_1",
                                                    "lighting_multiplier_schedule": "lighting_schedule_1",
                                                    "power_per_area": 1.0,
                                                }
                                            ],
                                            "miscellaneous_equipment": [
                                                {
                                                    "id": "miscellaneous_equipment_1",
                                                    "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                                    "power": 5000,
                                                }
                                            ],
                                            "occupant_multiplier_schedule": "occupant_schedule_1",
                                            "occupant_sensible_heat_gain": 125,
                                            "occupant_latent_heat_gain": 125,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                # Case it is high internal load
                                {
                                    "id": "Thermal Zone 2",
                                    "floor_name": "floor_1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "spaces": [
                                        {
                                            "id": "space 2",
                                            "floor_area": 500,
                                            "number_of_occupants": 5,
                                            "interior_lighting": [
                                                {
                                                    "id": "interior_lighting_2",
                                                    "lighting_multiplier_schedule": "lighting_schedule_1",
                                                    "power_per_area": 1.0,
                                                }
                                            ],
                                            "miscellaneous_equipment": [
                                                {
                                                    "id": "miscellaneous_equipment_2",
                                                    "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                                    "power": 50000,
                                                }
                                            ],
                                            "occupant_multiplier_schedule": "occupant_schedule_1",
                                            "occupant_sensible_heat_gain": 125,
                                            "occupant_latent_heat_gain": 125,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 2",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                # Case EFLH is higher
                                {
                                    "id": "Thermal Zone 3",
                                    "floor_name": "floor_2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "spaces": [
                                        {
                                            "id": "space 3",
                                            "floor_area": 200,
                                            "number_of_occupants": 5,
                                            "interior_lighting": [
                                                {
                                                    "id": "interior_lighting_3",
                                                    "lighting_multiplier_schedule": "lighting_schedule_2",
                                                    "power_per_area": 1.0,
                                                }
                                            ],
                                            "miscellaneous_equipment": [
                                                {
                                                    "id": "miscellaneous_equipment_2",
                                                    "multiplier_schedule": "miscellaneous_equipment_schedule_2",
                                                    "power": 5000,
                                                }
                                            ],
                                            "occupant_multiplier_schedule": "occupant_schedule_2",
                                            "occupant_sensible_heat_gain": 125,
                                            "occupant_latent_heat_gain": 125,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 3",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                # Dummy thermal zone for thermal zone 3 test
                                {
                                    "id": "Thermal Zone 4",
                                    "floor_name": "floor_2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "spaces": [
                                        {
                                            "id": "space 4",
                                            "floor_area": 200,
                                            "number_of_occupants": 5,
                                            "interior_lighting": [
                                                {
                                                    "id": "interior_lighting_4",
                                                    "lighting_multiplier_schedule": "lighting_schedule_1",
                                                    "power_per_area": 1.0,
                                                }
                                            ],
                                            "miscellaneous_equipment": [
                                                {
                                                    "id": "miscellaneous_equipment_4",
                                                    "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                                    "power": 5000,
                                                }
                                            ],
                                            "occupant_multiplier_schedule": "occupant_schedule_1",
                                            "occupant_sensible_heat_gain": 125,
                                            "occupant_latent_heat_gain": 125,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 4",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                # Dummy zone for thermal zone 1 test
                                {
                                    "id": "Thermal Zone 5",
                                    "floor_name": "floor_1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "spaces": [
                                        {
                                            "id": "space 5",
                                            "floor_area": 200,
                                            "number_of_occupants": 5,
                                            "interior_lighting": [
                                                {
                                                    "id": "interior_lighting_5",
                                                    "lighting_multiplier_schedule": "lighting_schedule_1",
                                                    "power_per_area": 1.0,
                                                }
                                            ],
                                            "miscellaneous_equipment": [
                                                {
                                                    "id": "miscellaneous_equipment_5",
                                                    "multiplier_schedule": "miscellaneous_equipment_schedule_1",
                                                    "power": 5000,
                                                }
                                            ],
                                            "occupant_multiplier_schedule": "occupant_schedule_1",
                                            "occupant_sensible_heat_gain": 125,
                                            "occupant_latent_heat_gain": 125,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 5",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 7",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 1",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "operating_schedule": "Operation Schedule 1",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                }
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
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
                },
            ],
            "schedules": [
                {
                    "id": "lighting_schedule_1",
                    "hourly_values": [1.0] * 6000 + [0.0] * 2760,
                    "hourly_heating_design_day": [0.0] * 24,
                    "hourly_cooling_design_day": [1.0] * 24,
                },
                {
                    "id": "miscellaneous_equipment_schedule_1",
                    "hourly_values": [1.0] * 6000 + [0.0] * 2760,
                    "hourly_heating_design_day": [0.0] * 24,
                    "hourly_cooling_design_day": [1.0] * 24,
                },
                {
                    "id": "occupant_schedule_1",
                    "hourly_values": [1.0] * 6000 + [0.0] * 2760,
                    "hourly_heating_design_day": [0.0] * 24,
                    "hourly_cooling_design_day": [1.0] * 24,
                },
                {
                    "id": "lighting_schedule_2",
                    "hourly_values": [1.0] * 8760,
                    "hourly_heating_design_day": [0.0] * 24,
                    "hourly_cooling_design_day": [1.0] * 24,
                },
                {
                    "id": "miscellaneous_equipment_schedule_2",
                    "hourly_values": [1.0] * 8760,
                    "hourly_heating_design_day": [0.0] * 24,
                    "hourly_cooling_design_day": [1.0] * 24,
                },
                {
                    "id": "occupant_schedule_2",
                    "hourly_values": [1.0] * 8760,
                    "hourly_heating_design_day": [0.0] * 24,
                    "hourly_cooling_design_day": [1.0] * 24,
                },
                {
                    "id": "Operation Schedule 1",
                    "hourly_values": [1.0] * 8760,
                    "hourly_heating_design_day": [0.0] * 24,
                    "hourly_cooling_design_day": [1.0] * 24,
                },
            ],
            "type": "BASELINE_0",
        }
    ],
}


TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__does_zone_meet_g_3_1_1c_thermal_zone_1__false():
    assert (
        does_zone_meet_g3_1_1c(
            TEST_RMD_UNIT,
            "Thermal Zone 1",
            {
                "Thermal Zone 1": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 2": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 3": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 4": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 5": {"expected_system_type": HVAC_SYS.SYS_7},
            },
        )
        == False
    )


def test__does_zone_meet_g_3_1_1c_thermal_zone_2__true():
    assert (
        does_zone_meet_g3_1_1c(
            TEST_RMD_UNIT,
            "Thermal Zone 2",
            {
                "Thermal Zone 1": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 2": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 3": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 4": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 5": {"expected_system_type": HVAC_SYS.SYS_7},
            },
        )
        == True
    )


def test__does_zone_meet_g_3_1_1c_thermal_zone_3__true():
    assert (
        does_zone_meet_g3_1_1c(
            TEST_RMD_UNIT,
            "Thermal Zone 3",
            {
                "Thermal Zone 1": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 2": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 3": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 4": {"expected_system_type": HVAC_SYS.SYS_7},
                "Thermal Zone 5": {"expected_system_type": HVAC_SYS.SYS_7},
            },
        )
        == True
    )
