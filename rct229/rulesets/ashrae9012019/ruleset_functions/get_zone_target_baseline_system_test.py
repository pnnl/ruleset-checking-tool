from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CAPACITY_THRESHOLD as CAPACITY_THRESHOLD_QUANTITY,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_target_baseline_system import (
    SYSTEMORIGIN,
    get_zone_target_baseline_system,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

POWER_DELTA = 1
POWER_THRESHOLD_100 = (CAPACITY_THRESHOLD_QUANTITY * 100 * ureg("m2")).to("W").magnitude

TEST_RMD_B_G311B = {
    "id": "test_rmd",
    "constructions": [
        {
            "id": "construction_1",
            "u_factor": 1.2,
        }
    ],
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "heating_ventilating_air_conditioning_systems": [
                        # directly conditioned zone
                        {
                            "id": "hvac_1_1",
                            "cooling_system": {
                                "id": "csys_1_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        }
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "volume": 2000,
                            "floor_name": "FL 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "floor_area": 2000,
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                }
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 1-1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_1",
                                }
                            ],
                        },
                    ],
                },
                {
                    "id": "Building Segment 2",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac_2_1",
                            "cooling_system": {
                                "id": "csys_2_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        }
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 2",
                            "volume": 4000,
                            "floor_name": "FL 1",
                            "spaces": [
                                {
                                    "id": "Space 2",
                                    "floor_area": 4000,
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                }
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 2-1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2_1",
                                }
                            ],
                        },
                    ],
                },
                {
                    "id": "Building Segment 3",
                    "zones": [
                        {
                            "id": "Thermal Zone 3",
                            "volume": 100,
                            "spaces": [
                                {
                                    "id": "Space 3",
                                    "floor_area": 200,
                                    "lighting_space_type": "LOBBY_HOTEL",
                                }
                            ],
                            "surfaces": [
                                {
                                    "id": "surface_3_1_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_2",
                                    "area": 10,
                                    "tilt": 90,
                                    "construction": "construction_1",
                                }
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "constructions": [
        {
            "id": "construction_1",
            "u_factor": 1.2,
        }
    ],
    "type": "BASELINE_0",
}

TEST_RMD_B_G311C = {
    "id": "RMD 1",
    "constructions": [
        {
            "id": "Construction 3",
            "u_factor": 0.35773064046128095,
        },
        {
            "id": "const_1_4_2",
            "u_factor": 0.1,
        },
    ],
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "number_of_floors_above_grade": 7,
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "area_type_heating_ventilating_air_conditioning_system": "RETAIL",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "floor_name": "floor_1",
                            "volume": 500,
                            "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                            "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                            "spaces": [
                                {
                                    "id": "space 1",
                                    "floor_area": 50000,
                                    "number_of_occupants": 5,
                                    "lighting_space_type": "LOBBY_ALL_OTHERS",
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
                            "surfaces": [
                                {
                                    "id": "Surface 3_1",
                                    "adjacent_to": "INTERIOR",
                                    "area": 100,
                                    "tilt": 0,
                                    "adjacent_zone": "Thermal Zone 1",
                                    "construction": "Construction 3",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,
                                            "u_factor": 0.5,
                                        }
                                    ],
                                },
                                {
                                    "id": "Surface 3_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "Thermal Zone 1",
                                    "area": 10,
                                    "tilt": 90,
                                    "construction": "const_1_4_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_4_2_1",
                                            "glazed_area": 10,
                                            "opaque_area": 0,
                                            "u_factor": 3,
                                        }
                                    ],
                                },
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
                                "design_sensible_cool_capacity": 5000000,
                            },
                            "preheat_system": {
                                "id": "Preheat Coil 1",
                                "type": "FLUID_LOOP",
                                "hot_water_loop": "Boiler Loop 1",
                                "design_capacity": 3000000,
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
    "constructions": [
        {
            "id": "Construction 3",
            "u_factor": 0.35773064046128095,
        },
        {
            "id": "const_1_4_2",
            "u_factor": 0.1,
        },
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
            "id": "Operation Schedule 1",
            "hourly_values": [1.0] * 8760,
            "hourly_heating_design_day": [0.0] * 24,
            "hourly_cooling_design_day": [1.0] * 24,
        },
    ],
    "type": "BASELINE_0",
}

TEST_RMD_P = {
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
                                {
                                    "id": "Thermal Zone 1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "volume": 2000,
                                    "floor_name": "FL 1",
                                    "spaces": [{"id": "Space 1", "floor_area": 50}],
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "heating_source": "HOT_WATER",
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 7",
                                            "heating_from_loop": "Boiler Loop 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 2",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "volume": 2000,
                                    "floor_name": "FL 1",
                                    "spaces": [
                                        {
                                            "id": "Space 2",
                                            "floor_area": 500,
                                        }
                                    ],
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 2",
                                            "served_by_heating_ventilating_air_conditioning_system": "Testing Sys",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "Testing Sys",
                                    "heating_system": {
                                        "id": "Preheat Coil 1",
                                        "type": "FURNACE",
                                    },
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "type": "NONE",
                                    },
                                }
                            ],
                        }
                    ],
                }
            ],
            "type": "PROPOSED",
        }
    ],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_RMD_B_G311D = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac 1",
                            "cooling_system": {
                                "id": "Cooling system 1",
                                "design_sensible_cool_capacity": 100000,
                            },
                            "heating_system": {
                                "id": "Heating system 1",
                                "design_capacity": 10000,
                            },
                            "fan_system": {
                                "id": "fan_system_1",
                                "exhaust_fans": [
                                    {
                                        "id": "exhaust_fans 1",
                                        "design_airflow": 7500,
                                    }
                                ],
                            },
                        }
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "volume": 1000,
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "function": "LABORATORY",
                                    "floor_area": 1000,
                                    "lighting_space_type": "CORRIDOR_MANUFACTURING_FACILITY",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac 1",
                                    "primary_airflow": 6500,
                                }
                            ],
                            "surfaces": [
                                {
                                    "id": "Surface 3_1",
                                    "adjacent_to": "INTERIOR",
                                    "area": 100,
                                    "tilt": 0,
                                    "adjacent_zone": "Thermal Zone 1",
                                    "construction": "Construction 3",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,
                                            "u_factor": 0.5,
                                        }
                                    ],
                                },
                                {
                                    "id": "Surface 3_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "Thermal Zone 1",
                                    "area": 10,
                                    "tilt": 90,
                                    "construction": "const_1_4_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_4_2_1",
                                            "glazed_area": 10,
                                            "opaque_area": 0,
                                            "u_factor": 3,
                                        }
                                    ],
                                },
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
                                }
                            ],
                        }
                    ],
                },
            ],
        },
    ],
    "constructions": [
        {
            "id": "Construction 3",
            "u_factor": 0.35773064046128095,
        },
        {
            "id": "const_1_4_2",
            "u_factor": 0.1,
        },
    ],
    "type": "BASELINE_0",
}

TEST_RMD_B_G311E = {
    "id": "test_rmd",
    "schedules": [{"id": "schedule_1", "hourly_values": [1.2] * 8670}],
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 2",
                            "cooling_system": {
                                "id": "Cooling System 1",
                                "type": "NONE",
                                "design_sensible_cool_capacity": 100000,
                            },
                            "heating_system": {
                                "id": "csys_2_1_2",
                                "type": "FURNACE",
                                "design_capacity": 1000000,
                            },
                        },
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 2",
                            "floor_name": "FLOOR 1",
                            "volume": 1000,
                            "terminals": [
                                {
                                    "id": "terminal_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                    "heating_source": "ELECTRIC",
                                },
                            ],
                            "spaces": [
                                {
                                    "id": "Space 3",
                                    "floor_area": 5,
                                    "lighting_space_type": "STAIRWELL",
                                },
                            ],
                            "surfaces": [
                                {
                                    "id": "surface 2",
                                    "adjacent_to": "EXTERIOR",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface 3",
                                            "classification": "DOOR",
                                            "glazed_area": 10,
                                            "opaque_area": 2,
                                            "u_factor": 0.2,
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "type": "BASELINE_0",
}

TEST_RMD_B_G311F = {
    "id": "test_rmd",
    "schedules": [{"id": "schedule_1", "hourly_values": [1.2] * 8670}],
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 2",
                            "cooling_system": {
                                "id": "Cooling System 1",
                                "type": "DIRECT_EXPANSION",
                                "design_sensible_cool_capacity": 100000,
                            },
                            "heating_system": {
                                "id": "csys_2_1_2",
                                "type": "FURNACE",
                                "design_capacity": 1000000,
                            },
                        },
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 2",
                            "floor_name": "FLOOR 1",
                            "volume": 1000,
                            "terminals": [
                                {
                                    "id": "terminal_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                    "heating_source": "ELECTRIC",
                                },
                            ],
                            "spaces": [
                                {
                                    "id": "Space 3",
                                    "floor_area": 5,
                                    "lighting_space_type": "STORAGE_ROOM_HOSPITAL",
                                },
                            ],
                            "surfaces": [
                                {
                                    "id": "surface 2",
                                    "adjacent_to": "EXTERIOR",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface 3",
                                            "classification": "DOOR",
                                            "glazed_area": 10,
                                            "opaque_area": 2,
                                            "u_factor": 0.2,
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "type": "BASELINE_0",
}

TEST_RMD_B_G311G = {
    "id": "test_rmd",
    "constructions": [
        {
            "id": "construction 1",
            "u_factor": 0.1,
        }
    ],
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 2",
                            "cooling_system": {
                                "id": "Cooling System 1",
                                "type": "DIRECT_EXPANSION",
                                "design_sensible_cool_capacity": 100000,
                            },
                            "heating_system": {
                                "id": "csys_2_1_2",
                                "type": "FURNACE",
                                "design_capacity": 1000000,
                            },
                        },
                    ],
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "volume": 1000,
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "floor_area": 500,
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
                                            "power": 1000000,
                                        }
                                    ],
                                    "occupant_multiplier_schedule": "occupant_schedule_1",
                                    "occupant_sensible_heat_gain": 125,
                                    "occupant_latent_heat_gain": 125,
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                    "heating_source": "ELECTRIC",
                                },
                            ],
                            "surfaces": [
                                {
                                    "id": "surface 2",
                                    "adjacent_to": "EXTERIOR",
                                    "area": 100,
                                    "tilt": 90,
                                    "construction": "construction 1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface 3",
                                            "classification": "DOOR",
                                            "glazed_area": 10,
                                            "opaque_area": 2,
                                            "u_factor": 0.2,
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
    "schedules": [
        {"id": "lighting_schedule_1", "hourly_cooling_design_day": [1] * 24},
        {
            "id": "miscellaneous_equipment_schedule_1",
            "hourly_cooling_design_day": [1] * 24,
        },
        {"id": "occupant_schedule_1", "hourly_cooling_design_day": [1] * 23 + [2] * 1},
    ],
    "constructions": [
        {
            "id": "construction 1",
            "u_factor": 0.1,
        }
    ],
    "type": "BASELINE_0",
}


TEST_RMD_B_FULL_G311B = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_G311B],
}
TEST_RMD_B_UNIT_G311B = quantify_rmd(TEST_RMD_B_FULL_G311B)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_B_FULL_G311C = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_G311C],
}
TEST_RMD_B_UNIT_G311C = quantify_rmd(TEST_RMD_B_FULL_G311C)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_B_FULL_G311D = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_G311D],
}
TEST_RMD_B_UNIT_G311D = quantify_rmd(TEST_RMD_B_FULL_G311D)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_B_FULL_G311E = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_G311E],
}
TEST_RMD_B_UNIT_G311E = quantify_rmd(TEST_RMD_B_FULL_G311E)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_B_FULL_G311F = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_G311F],
}
TEST_RMD_B_UNIT_G311F = quantify_rmd(TEST_RMD_B_FULL_G311F)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_B_FULL_G311G = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_G311G],
}
TEST_RMD_B_UNIT_G311G = quantify_rmd(TEST_RMD_B_FULL_G311G)[
    "ruleset_model_descriptions"
][0]


TEST_RMD_UNIT_P = quantify_rmd(TEST_RMD_P)["ruleset_model_descriptions"][0]


def test__TEST_RMD_G311B_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311B)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_G311C_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311C)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_G311D_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311D)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_G311E_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311E)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_G311F_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311F)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_G311G_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311G)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_P_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_P)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zone_target_baseline_system_G3_1_1_b__true():
    assert get_zone_target_baseline_system(
        TEST_RMD_B_UNIT_G311B, TEST_RMD_UNIT_P, "CZ4A"
    ) == {
        "Thermal Zone 1": {
            "expected_system_type": HVAC_SYS.SYS_5,
            "system_origin": SYSTEMORIGIN.G311B,
        },
        "Thermal Zone 2": {
            "expected_system_type": HVAC_SYS.SYS_1,
            "system_origin": "RESIDENTIAL CZ_3b_3c_or_4_to_8",
        },
    }


def test__get_zone_target_baseline_system_G3_1_1_c__true():
    assert get_zone_target_baseline_system(
        TEST_RMD_B_UNIT_G311C, TEST_RMD_UNIT_P, "CZ5A"
    ) == {
        "Thermal Zone 1": {
            "expected_system_type": HVAC_SYS.SYS_7,
            "system_origin": "OTHER_NON_RESIDENTIAL CZ_3b_3c_or_4_to_8 >150,000 ft2 or > 5 floors",
        }
    }


def test__get_zone_target_baseline_system_G3_1_1_d__true():
    assert get_zone_target_baseline_system(
        TEST_RMD_B_UNIT_G311D, TEST_RMD_UNIT_P, "CZ4A"
    ) == {
        "Thermal Zone 1": {
            "expected_system_type": HVAC_SYS.SYS_5,
            "system_origin": SYSTEMORIGIN.G311D,
        }
    }


def test__get_zone_target_baseline_system_G3_1_1_e__true():
    assert get_zone_target_baseline_system(
        TEST_RMD_B_UNIT_G311E, TEST_RMD_UNIT_P, "CZ3A"
    ) == {
        "Thermal Zone 2": {
            "expected_system_type": HVAC_SYS.SYS_10,
            "system_origin": SYSTEMORIGIN.G311E,
        }
    }


def test__get_zone_target_baseline_system_G3_1_1_f__true():
    assert get_zone_target_baseline_system(
        TEST_RMD_B_UNIT_G311F, TEST_RMD_UNIT_P, "CZ4A"
    ) == {
        "Thermal Zone 2": {
            "expected_system_type": HVAC_SYS.SYS_5,
            "system_origin": SYSTEMORIGIN.G311F,
        }
    }


def test__get_zone_target_baseline_system_G3_1_1_g__true():
    assert get_zone_target_baseline_system(
        TEST_RMD_B_UNIT_G311G, TEST_RMD_UNIT_P, "CZ4A"
    ) == {
        "Thermal Zone 1": {
            "expected_system_type": HVAC_SYS.SYS_11_1,
            "system_origin": "G3_1_1g_part2",
        }
    }
