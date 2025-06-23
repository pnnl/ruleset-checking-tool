from rct229.rulesets.ashrae9012019.ruleset_functions.get_lab_zone_hvac_systems import (
    get_lab_zone_hvac_systems,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD_B_ALL_ZONES_G311D_ONE_SYSTEM = {
    "id": "test_rmd",
    "constructions": [
        {
            "id": "Construction 3",
            "u_factor": 0.35773064046128095,
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
                                    "id": "Surface 1_1",
                                    "adjacent_to": "INTERIOR",
                                    "area": 100,
                                    "tilt": 0,
                                    "adjacent_zone": "Thermal Zone 1",
                                    "construction": "Construction 3",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,
                                            "u_factor": 0.5,
                                        }
                                    ],
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "volume": 3000,
                            "spaces": [
                                {
                                    "id": "Space 2",
                                    "function": "LABORATORY",
                                    "floor_area": 3000,
                                    "lighting_space_type": "CORRIDOR_MANUFACTURING_FACILITY",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac 1",
                                    "primary_airflow": 6500,
                                }
                            ],
                            "surfaces": [
                                {
                                    "id": "Surface 2_1",
                                    "adjacent_to": "INTERIOR",
                                    "area": 100,
                                    "tilt": 0,
                                    "adjacent_zone": "Thermal Zone 2",
                                    "construction": "Construction 3",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,
                                            "u_factor": 0.5,
                                        }
                                    ],
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
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
            "id": "Construction 3",
            "u_factor": 0.35773064046128095,
        }
    ],
    "type": "BASELINE_0",
}


TEST_RMD_B_ALL_ZONES_G311D_ONE_SYSTEM2_TWO_SYSTEMS = {
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
                        },
                        {
                            "id": "hvac 2",
                            "cooling_system": {
                                "id": "Cooling system 2",
                                "design_sensible_cool_capacity": 200000,
                            },
                            "heating_system": {
                                "id": "Heating system 2",
                                "design_capacity": 20000,
                            },
                            "fan_system": {
                                "id": "fan_system_2",
                                "exhaust_fans": [
                                    {
                                        "id": "exhaust_fans 2",
                                        "design_airflow": 9500,
                                    }
                                ],
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
                                    "id": "Surface 1_1",
                                    "adjacent_to": "INTERIOR",
                                    "area": 100,
                                    "tilt": 0,
                                    "adjacent_zone": "Thermal Zone 1",
                                    "construction": "Construction 3",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,
                                            "u_factor": 0.5,
                                        }
                                    ],
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "volume": 3000,
                            "spaces": [
                                {
                                    "id": "Space 2",
                                    "function": "LABORATORY",
                                    "floor_area": 3000,
                                    "lighting_space_type": "CORRIDOR_MANUFACTURING_FACILITY",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "Terminal 2",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac 2",
                                    "primary_airflow": 6500,
                                }
                            ],
                            "surfaces": [
                                {
                                    "id": "Surface 2_1",
                                    "adjacent_to": "INTERIOR",
                                    "area": 100,
                                    "tilt": 0,
                                    "adjacent_zone": "Thermal Zone 2",
                                    "construction": "Construction 3",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,
                                            "u_factor": 0.5,
                                        }
                                    ],
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
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
            "id": "Construction 3",
            "u_factor": 0.35773064046128095,
        }
    ],
    "type": "BASELINE_0",
}

TEST_RMD_B_G311D_G311F = {
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
                        },
                        {
                            "id": "hvac 2",
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
                                    "id": "Surface 1_1",
                                    "adjacent_to": "INTERIOR",
                                    "area": 100,
                                    "tilt": 0,
                                    "adjacent_zone": "Thermal Zone 1",
                                    "construction": "Construction 3",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,
                                            "u_factor": 0.5,
                                        }
                                    ],
                                }
                            ],
                            "zonal_exhaust_fans": [
                                {
                                    "id": "Exhaust Fan 1",
                                    "design_airflow": 1000,
                                }
                            ],
                        },
                        {
                            "id": "Thermal Zone 2",
                            "floor_name": "FLOOR 1",
                            "volume": 1000,
                            "terminals": [
                                {
                                    "id": "terminal_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac 2",
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
    "constructions": [
        {
            "id": "Construction 3",
            "u_factor": 0.35773064046128095,
        }
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

TEST_RMD_B_FULL_G311D_ONE_SYS = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_ALL_ZONES_G311D_ONE_SYSTEM],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}
TEST_RMD_B_UNIT_G311D_ONE_SYS = quantify_rmd(TEST_RMD_B_FULL_G311D_ONE_SYS)[
    "ruleset_model_descriptions"
][0]
TEST_RMD_B_FULL_G311D_TWO_SYS = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_ALL_ZONES_G311D_ONE_SYSTEM2_TWO_SYSTEMS],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}
TEST_RMD_B_UNIT_G311D_TWO_SYS = quantify_rmd(TEST_RMD_B_FULL_G311D_TWO_SYS)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_B_FULL_G311D_G311F = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD_B_G311D_G311F],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}
TEST_RMD_B_UNIT_G311D_G311F = quantify_rmd(TEST_RMD_B_FULL_G311D_G311F)[
    "ruleset_model_descriptions"
][0]

TEST_RMD_UNIT_P = quantify_rmd(TEST_RMD_P)["ruleset_model_descriptions"][0]


def test__TEST_RMD_B_ALL_ZONES_G311D_ONE_SYSTEM__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311D_ONE_SYS)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_B_ALL_ZONES_G311D_ONE_SYSTEM2_TWO_SYSTEMS__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_B_FULL_G311D_TWO_SYS)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RMD_P_is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_P)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_lab_zone_hvac_systems_all_zones_g311d_one_system__true():
    assert get_lab_zone_hvac_systems(
        TEST_RMD_B_UNIT_G311D_ONE_SYS, TEST_RMD_UNIT_P, "CZ4A"
    ) == {
        "lab_zones_only": ["hvac 1"],
        "lab_and_other": [],
    }


def test__get_lab_zone_hvac_systems_all_zones_g311d_two_systems__true():
    assert get_lab_zone_hvac_systems(
        TEST_RMD_B_UNIT_G311D_TWO_SYS, TEST_RMD_UNIT_P, "CZ4A"
    ) == {
        "lab_zones_only": ["hvac 1", "hvac 2"],
        "lab_and_other": [],
    }


def test__get_lab_zone_hvac_systems__zones_g311d_g311f_two_systems__true():
    assert get_lab_zone_hvac_systems(
        TEST_RMD_B_UNIT_G311D_G311F, TEST_RMD_UNIT_P, "CZ4A"
    ) == {
        "lab_zones_only": ["hvac 1"],
        "lab_and_other": [],
    }
