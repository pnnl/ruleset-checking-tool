from rct229.rulesets.ashrae9012019.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_area_type_window_wall_area_dict import (
    get_area_type_window_wall_area_dict,
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


# This single rmd is intended to exercise all the get_zone_conditioning_category_dict() code
TEST_rmd = {
    "id": "test_rmd",
    "constructions": [
        {
            "id": "const_1_5_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "interior_wall_3_1_1",
            "u_factor": 0.222,  # W/(m2 * K)
        },
        {
            "id": "interior_wall_3_2_1",
            "u_factor": 0.222,  # W/(m2 * K)
        },
    ],
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                # area_type_vertical_fenestration is nonresidential type
                # In total this building segment has 10m2 windows and 20m2 walls.
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
                    ],
                    "zones": [
                        # hvac_1_1 => directly_conditioned_zone
                        # zone has a space with a residential lighting_space_type
                        #   => zone_has_residential_spaces
                        # zone has a space with a nonresidential lighting_space_type
                        #   => zone_has_nonresidential_spaces
                        # zone_has_nonresidential_spaces AND zone_has_nonresidential_spaces
                        #   => zone_conditioning_category is "CONDITIONED MIXED"
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
                                {
                                    # Non-residential
                                    "id": "space_1_1_2",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
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
                                    "tilt": 90,  # above grade wall
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_1_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 5,
                                            "opaque_area": 0,  # m2
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
                        # zone has no residential spaces but a space has a lighting_space_type
                        #   => zone_has_nonresidential_spaces
                        # Not zone_has_residential_spaces and zone_has_nonesidential_spaces
                        #  => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
                        {
                            "id": "zone_1_2",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_1_2_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_2_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_1",
                                    "area": 10,  # m2
                                    "tilt": 90,  # above grade wall
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_2_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 5,
                                            "opaque_area": 0,  # m2
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
                    ],
                },
                # area_type_vertical_fenestration is nonresidential type
                # In total this building segment has 10m2 windows and 20m2 walls.
                {
                    "id": "bldg_seg_1_2",
                    "lighting_building_area_type": "MULTIFAMILY",
                    "area_type_vertical_fenestration": "HOTEL_MOTEL_SMALL",
                    "heating_ventilating_air_conditioning_systems": [
                        # Use for zone_1_2_1, directly conditioned zone
                        {
                            "id": "hvac_1_2_1",
                            "cooling_system": {
                                "id": "csys_1_2_1_1",
                                "design_sensible_cool_capacity": 2 * POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        },
                        # Used for zone_1_2_2, directly conditioned zone
                        {
                            "id": "hvac_1_2_2",
                            "heating_system": {
                                "id": "hsys_1_2_2_1",
                                "design_capacity": SYSTEM_MIN_HEATING_OUTPUT
                                + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_1_1 => directly_conditioned_zone
                        # zone has a space with a residential lighting_space_type
                        #   => zone_has_residential_spaces
                        # zone has a space with a nonresidential lighting_space_type
                        #   => zone_has_nonresidential_spaces
                        # zone_has_nonresidential_spaces AND zone_has_nonresidential_spaces
                        #   => zone_conditioning_category is "CONDITIONED MIXED"
                        {
                            "id": "zone_1_2_1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_1_2_1_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                                {
                                    # Non-residential
                                    "id": "space_1_2_1_2",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_2_1_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_2_2",
                                    "area": 10,  # m2
                                    "tilt": 90,  # above grade wall
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_2_1_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 5,
                                            "opaque_area": 0,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_2_1_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_2_1",
                                }
                            ],
                        },
                        # hvac_1_2 => directly_conditioned_zone
                        # zone has no residential spaces but a space has a lighting_space_type
                        #   => zone_has_nonresidential_spaces
                        # Not zone_has_residential_spaces and zone_has_nonesidential_spaces
                        #  => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
                        {
                            "id": "zone_1_2_2",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_1_2_2_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_2_2_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_2_1",
                                    "area": 10,  # m2
                                    "tilt": 90,  # above grade wall
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_2_2_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 5,
                                            "opaque_area": 0,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_2_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_2_2",
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
                        # Used for directly conditioned zone
                        {
                            "id": "hvac_2_1",
                            "cooling_system": {
                                "id": "csys_2_1_1",
                                "design_sensible_cool_capacity": POWER_THRESHOLD_100
                                + POWER_DELTA,
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
                        # hvac_2_1 => directly_conditioned_zone
                        # zone only has residential spaces
                        #   => zone_conditioning_category is "CONDITIONED RESIDENTIAL"
                        # has 5m2 window and 10m2 wall
                        {
                            "id": "zone_2_1",
                            "spaces": [
                                {
                                    "id": "space_2_1_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "HEALTHCARE_FACILITY_PATIENT_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_2_1_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_2",
                                    "area": 10,  # m2
                                    "tilt": 90,  # above grade wall
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_1_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 5,
                                            "opaque_area": 0,  # m2
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        }
                                    ],
                                }
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
                        # It has a Door subsurface but the opaque surface is greater than window surface
                        # So its total surface does not count towards total window area
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
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "tilt": 90,  # above grade wall
                                    "construction": "const_1_5_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_2_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 3,
                                            "opaque_area": 2,  # m2
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
                # Building segment has no area_type_vertical_fenestration
                # The total window area in this building segment is 5 m2
                # The total wall area in this building segment is 10 m2
                {
                    "id": "bldg_seg_3",
                    "lighting_building_area_type": "CONVENTION_CENTER",
                    "heating_ventilating_air_conditioning_systems": [
                        # Used for directly conditioned zone
                        {
                            "id": "hvac_3_1",
                            "cooling_system": {
                                "id": "csys_3_1_1",
                                "design_sensible_cool_capacity": POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        }
                    ],
                    "zones": [
                        # hvac_3_1 => directly_conditioned_zone
                        # has a door subsurface, the glazed area is greater than the opaque area,
                        # so its total area count towards window area.
                        {
                            "id": "zone_3_1",
                            "spaces": [
                                {
                                    "id": "space_3_1_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "HEALTHCARE_FACILITY_PATIENT_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_1_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_2",  # semi-heated
                                    "area": 10,  # m2
                                    "tilt": 90,  # above grade wall
                                    "construction": "interior_wall_3_1_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_1_1_1",
                                            "classification": "DOOR",
                                            "glazed_area": 3,
                                            "opaque_area": 2,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                }
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
                        # no hvac, lighting_space_type == "PARKING_AREA_INTERIOR" => unenclosed
                        # has a 2 m2 window, however it should not count towards the total wall and window area
                        {
                            "id": "zone_3_2",
                            "spaces": [
                                {
                                    "id": "space_3_2_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "PARKING_AREA_INTERIOR",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_2_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_3_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "tilt": 90,  # above grade wall
                                    "construction": "interior_wall_3_2_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_2_1_1",
                                            "classification": "WINDOW",
                                            "glazed_area": 2,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 2.4,  # W/(m2 * K)
                                        },
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
            "id": "const_1_5_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "interior_wall_3_1_1",
            "u_factor": 0.222,  # W/(m2 * K)
        },
        {
            "id": "interior_wall_3_2_1",
            "u_factor": 0.222,  # W/(m2 * K)
        },
    ],
    "type": "BASELINE_0",
}

TEST_rmd_12 = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_rmd],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}

TEST_BUILDING = quantify_rmd(TEST_rmd_12)["ruleset_model_descriptions"][0]["buildings"][
    0
]
TEST_CONSTRUCTIONS = quantify_rmd(TEST_rmd_12)["ruleset_model_descriptions"][0][
    "constructions"
]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_rmd_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_area_type_window_wall_area():
    assert get_area_type_window_wall_area_dict(
        CLIMATE_ZONE, TEST_CONSTRUCTIONS, TEST_BUILDING
    ) == {
        "HOTEL_MOTEL_SMALL": {
            "total_wall_area": 40 * ureg("m2"),
            "total_window_area": 20 * ureg("m2"),
        },
        "RETAIL_STAND_ALONE": {
            "total_wall_area": 20 * ureg("m2"),
            "total_window_area": 10 * ureg("m2"),
        },
        "NONE": {
            "total_wall_area": 10 * ureg("m2"),
            "total_window_area": 5 * ureg("m2"),
        },
    }
