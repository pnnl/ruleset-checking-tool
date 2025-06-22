from rct229.rulesets.ashrae9012019.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_scc_skylight_roof_ratios_dict import (
    get_building_scc_skylight_roof_ratios_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CAPACITY_THRESHOLD as CAPACITY_THRESHOLD_QUANTITY,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CRAWLSPACE_HEIGHT_THRESHOLD as CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

CLIMATE_ZONE = "CZ0A"
POWER_DELTA = 1
SYSTEM_MIN_HEATING_OUTPUT_QUANTITY = table_3_2_lookup(CLIMATE_ZONE)[
    "system_min_heating_output"
]

# Convert pint quantities to match schema units
SYSTEM_MIN_HEATING_OUTPUT = (
    (SYSTEM_MIN_HEATING_OUTPUT_QUANTITY * 100 * ureg("m2")).to("W").magnitude
)
POWER_THRESHOLD_100 = (CAPACITY_THRESHOLD_QUANTITY * 100 * ureg("m2")).to("W").magnitude
CRAWLSPACE_HEIGHT_THRESHOLD = CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY.to("m").magnitude


# This single rmd is intended to exercise all the get_building_scc_skylight_roof_ratios_dict function
TEST_rmd = {
    "id": "test_rmd",
    "constructions": [
        {
            "id": "const_1_5_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_6_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_3_5_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_3_6_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
    ],
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                # area_type_vertical_fenestration is residential type
                {
                    "id": "bldg_seg_1",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "area_type_vertical_fenestration": "HOTEL_MOTEL_SMALL",
                    "heating_ventilating_air_conditioning_systems": [
                        # Use for zone_1_1, directly conditioned zone
                        {
                            "id": "hvac_1_1",
                            "cooling_system": {
                                "id": "csys_1_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        },
                        # Used for zone_1_2, directly conditioned zone
                        {
                            "id": "hvac_1_2",
                            "heating_system": {
                                "id": "hsys_1_2_1",
                                "design_capacity": SYSTEM_MIN_HEATING_OUTPUT
                                + POWER_DELTA,
                            },
                        },
                        # Used for zone_1_3, directly conditioned zone
                        {
                            "id": "hvac_1_3",
                            "heating_system": {
                                "id": "hsys_1_3_1",
                                "design_capacity": SYSTEM_MIN_HEATING_OUTPUT
                                + POWER_DELTA,
                            },
                        },
                        # Used for zone_1_2, directly conditioned zone
                        {
                            "id": "hvac_1_4",
                            "heating_system": {
                                "id": "hsys_1_4_1",
                                "design_capacity": SYSTEM_MIN_HEATING_OUTPUT
                                + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_1_1 => directly_conditioned_zone
                        #   => zone_conditioning_category is "CONDITIONED RESIDENTIAL"
                        #   => door has greater opaque area than glazed area
                        # total_res_roof_area = 10
                        # total_res_skylight_area = 0
                        {
                            "id": "zone_1_1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_1_1_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_1_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_2",
                                    "area": 10,  # m2
                                    "tilt": 0,  # roof
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_1_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 1,
                                            "opaque_area": 3,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_1_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_1",
                                }
                            ],
                        },
                        # hvac_1_2 => directly_conditioned_zone
                        #   => zone_conditioning_category is "CONDITIONED RESIDENTIAL"
                        #   => door has greater glazed area than opaque area
                        # total_res_roof_area = 10
                        # total_res_skylight_area = 4
                        {
                            "id": "zone_1_2",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_1_2_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_2_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_1",
                                    "area": 10,  # m2
                                    "tilt": 0,  # roof
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_2_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 3,
                                            "opaque_area": 1,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_2",
                                }
                            ],
                        },
                        # hvac_1_3 => directly_conditioned_zone
                        #  => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
                        #   => door has greater opaque area than glazed area
                        # total_nonres_roof_area = 10
                        # total_nonres_skylight_area = 0
                        {
                            "id": "zone_1_3",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_1_3_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_3_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_4",
                                    "area": 10,  # m2
                                    "tilt": 0,  # roof
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_3_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 1,
                                            "opaque_area": 3,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_3_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_3",
                                }
                            ],
                        },
                        # hvac_1_4 => directly_conditioned_zone
                        #  => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
                        #   => door has greater glazed area than opaque area
                        # total_nonres_roof_area = 10
                        # total_nonres_skylight_area = 4
                        {
                            "id": "zone_1_4",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_1_4_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_4_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_3",
                                    "area": 10,  # m2
                                    "tilt": 0,  # roof
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_4_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 3,
                                            "opaque_area": 1,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_4_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_4",
                                }
                            ],
                        },
                    ],
                },
                # building segment area_type_vertical_fenestration is commercial type
                # Total window area: 10m2, Total wall area: 20m2
                {
                    "id": "bldg_seg_2",
                    "lighting_building_area_type": "FIRE_STATION",
                    "area_type_vertical_fenestration": "RETAIL_STAND_ALONE",
                    "heating_ventilating_air_conditioning_systems": [
                        # Used for semi-heated zone
                        {
                            "id": "hvac_2_1",
                            "heating_system": {
                                "id": "csys_2_1_1",
                                "design_capacity": POWER_THRESHOLD_100 + POWER_DELTA,
                            },
                        },
                        # Used for semi-heated zone
                        {
                            "id": "hvac_2_2",
                            "heating_system": {
                                "id": "csys_2_2_1",
                                "design_capacity": POWER_THRESHOLD_100 + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_2_1 => semiheated_zone
                        # zone_conditioning_category is "SEMI-HEATED"
                        #   => door has greater opaque area than glazed area
                        # total_semiheated_roof_area = 10
                        # total_semiheated_skylight_area = 0
                        {
                            "id": "zone_2_1",
                            "spaces": [
                                {
                                    "id": "space_2_1_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_2_1_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_2_2",  # directly conditioned
                                    "area": 10,  # m2
                                    "tilt": 0,  # above grade wall
                                    "construction": "const_1_5_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_1_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 1,
                                            "opaque_area": 3,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_2_1_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2_1",
                                }
                            ],
                        },
                        # hvac_2_2 => semiheated_zone
                        # zone_conditioning_category is "SEMI-HEATED"
                        #   => door has greater glazed area than opaque area
                        # total_semiheated_roof_area = 10
                        # total_semiheated_skylight_area = 4
                        {
                            "id": "zone_2_2",
                            "spaces": [
                                {
                                    "id": "space_2_2_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_2_2_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_2_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "tilt": 0,  # above grade wall
                                    "construction": "const_1_6_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_2_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 3,
                                            "opaque_area": 1,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_2_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_2_2",
                                }
                            ],
                        },
                    ],
                },
                {
                    "id": "bldg_seg_3",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "heating_ventilating_air_conditioning_systems": [
                        # Use for zone_3_1, directly conditioned zone
                        {
                            "id": "hvac_3_1",
                            "cooling_system": {
                                "id": "csys_3_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        },
                        {
                            "id": "hvac_3_2",
                            "cooling_system": {
                                "id": "csys_3_2_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_3_1 => directly_conditioned_zone
                        # zone has a space with a residential lighting_space_type
                        #   => zone_has_residential_spaces
                        # zone has a space with a nonresidential lighting_space_type
                        #   => zone_has_nonresidential_spaces
                        # zone_has_nonresidential_spaces AND zone_has_nonresidential_spaces
                        #   => zone_conditioning_category is "CONDITIONED MIXED"
                        {
                            "id": "zone_3_1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_3_1_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                                {
                                    # Non-residential
                                    "id": "space_3_1_2",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_3_1_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_3_2",  # directly conditioned
                                    "area": 10,  # m2
                                    "tilt": 0,  # above grade wall
                                    "construction": "const_3_5_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_1_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 1,
                                            "opaque_area": 3,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_3_1_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_3_1",
                                }
                            ],
                        },
                        # hvac_3_2 => directly_conditioned_zone
                        # zone has a space with a residential lighting_space_type
                        #   => zone_has_residential_spaces
                        # zone has a space with a nonresidential lighting_space_type
                        #   => zone_has_nonresidential_spaces
                        # zone_has_nonresidential_spaces AND zone_has_nonresidential_spaces
                        #   => zone_conditioning_category is "CONDITIONED MIXED"
                        {
                            "id": "zone_3_2",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_3_2_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                                {
                                    # Non-residential
                                    "id": "space_3_2_2",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_3_2_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_3_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "tilt": 0,  # above grade wall
                                    "construction": "const_3_6_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_2_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 3,
                                            "opaque_area": 1,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_3_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_3_2",
                                }
                            ],
                        },
                    ],
                },
            ],
        }
    ],
    "constructions": [
        {
            "id": "const_1_5_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_3_6_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_3_5_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_6_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
    ],
    "type": "BASELINE_0",
}

TEST_RMD_12 = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_rmd],
}

TEST_BUILDING = quantify_rmd(TEST_RMD_12)["ruleset_model_descriptions"][0]["buildings"][
    0
]
TEST_CONSTRUCTIONS = quantify_rmd(TEST_RMD_12)["ruleset_model_descriptions"][0][
    "constructions"
]

# The purpose of below is to test out when all the summed areas equal 0.
TEST_RMD_BRANCH_COVERAGE = {
    "id": "test_rmd_branch_coverage",
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                # area_type_vertical_fenestration is residential type
                {
                    "id": "bldg_seg_1",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "area_type_vertical_fenestration": "HOTEL_MOTEL_SMALL",
                    "heating_ventilating_air_conditioning_systems": [
                        # Use for zone_1, directly conditioned zone
                        {
                            "id": "hvac_1",
                            "cooling_system": {
                                "id": "csys_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_1 => directly_conditioned_zone
                        #   => zone_conditioning_category is "CONDITIONED RESIDENTIAL"
                        #   => window type subsurface
                        {
                            "id": "zone_1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                {
                                    "id": "surface_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1",
                                    "area": 10,  # m2
                                    "tilt": 90,  # wall
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_1_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 1,
                                            "opaque_area": 3,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1",
                                }
                            ],
                        },
                    ],
                },
            ],
        }
    ],
}

TEST_RMD_BRANCH_COVERAGE = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD_BRANCH_COVERAGE],
}

TEST_BUILDING_BRANCH_COVERAGE = quantify_rmd(TEST_RMD_BRANCH_COVERAGE)[
    "ruleset_model_descriptions"
][0]["buildings"][0]


TEST_RMD_BRANCH_COVERAGE2 = {
    "id": "test_rmd_branch_coverage2",
    "constructions": [
        {
            "id": "Construction 1",
            "u_factor": 0.35773064046128095,
        }
    ],
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                {
                    "id": "bldg_seg_1",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "area_type_vertical_fenestration": "HOTEL_MOTEL_SMALL",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "hvac_1_1",
                            "cooling_system": {
                                "id": "csys_1_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_1_1 => directly_conditioned_zone
                        #   => zone_conditioning_category is "UNREGULATED"
                        # total_res_roof_area = 10
                        # total_res_skylight_area = 4
                        {
                            "id": "zone_1_1",
                            "volume": 300,  # m3
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_1_1_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                {
                                    "id": "surface_1_1_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_2",
                                    "area": 10,  # m2
                                    "tilt": 30,  # roof
                                    "construction": "Construction 1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_1_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 1,
                                            "opaque_area": 3,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                },
            ],
        }
    ],
    "constructions": [
        {
            "id": "Construction 1",
            "u_factor": 0.35773064046128095,
        }
    ],
}


TEST_RMD_BRANCH_COVERAGE2 = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD_BRANCH_COVERAGE2],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_BUILDING_BRANCH_COVERAGE2 = quantify_rmd(TEST_RMD_BRANCH_COVERAGE2)[
    "ruleset_model_descriptions"
][0]["buildings"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_building_scc_skylight_roof_ratios_dict():
    assert get_building_scc_skylight_roof_ratios_dict(
        CLIMATE_ZONE, TEST_CONSTRUCTIONS, TEST_BUILDING
    ) == {
        SCC.EXTERIOR_RESIDENTIAL: 0.2,
        SCC.EXTERIOR_NON_RESIDENTIAL: 0.2,
        SCC.SEMI_EXTERIOR: 0.2,
        SCC.EXTERIOR_MIXED: 0.2,
    }


def test__get_building_scc_skylight_roof_ratios_dict__branch_coverage():
    assert get_building_scc_skylight_roof_ratios_dict(
        CLIMATE_ZONE, TEST_CONSTRUCTIONS, TEST_BUILDING_BRANCH_COVERAGE
    ) == {
        SCC.EXTERIOR_RESIDENTIAL: 0.0,
        SCC.EXTERIOR_NON_RESIDENTIAL: 0.0,
        SCC.SEMI_EXTERIOR: 0.0,
        SCC.EXTERIOR_MIXED: 0.0,
    }


def test__get_building_scc_skylight_roof_ratios_dict__branch_coverage2():
    assert get_building_scc_skylight_roof_ratios_dict(
        CLIMATE_ZONE, TEST_CONSTRUCTIONS, TEST_BUILDING_BRANCH_COVERAGE2
    ) == {
        SCC.EXTERIOR_RESIDENTIAL: 0.0,
        SCC.EXTERIOR_NON_RESIDENTIAL: 0.0,
        SCC.SEMI_EXTERIOR: 0.0,
        SCC.EXTERIOR_MIXED: 0.0,
    }
