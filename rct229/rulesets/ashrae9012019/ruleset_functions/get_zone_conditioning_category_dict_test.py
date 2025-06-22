from rct229.rulesets.ashrae9012019.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CAPACITY_THRESHOLD as CAPACITY_THRESHOLD_QUANTITY,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    CRAWLSPACE_HEIGHT_THRESHOLD as CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd
from rct229.utils.jsonpath_utils import find_all

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

# This single RMD is intended to exercise all the get_zone_conditioning_category_dict() code
TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                # lighting_building_area_type is one of the residential types
                # => building_segment_is_residential
                {
                    "id": "bldg_seg_1",
                    "lighting_building_area_type": "MULTIFAMILY",
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
                        # Used for directly conditioned zone
                        {
                            "id": "hvac_1_2",
                            "heating_system": {
                                "id": "hsys_1_2_1",
                                "design_capacity": SYSTEM_MIN_HEATING_OUTPUT
                                + POWER_DELTA,
                            },
                        },
                        # Used for semi-heated zone
                        {
                            "id": "hvac_1_3",
                            "heating_system": {
                                "id": "hsys_1_3_1",
                                "design_capacity": POWER_THRESHOLD_100 + POWER_DELTA,
                            },
                        },
                        # Used for semi-heated zone
                        {
                            "id": "hvac_1_4",
                            "heating_system": {
                                "id": "hsys_1_3_1",
                                "design_capacity": POWER_THRESHOLD_100 + POWER_DELTA,
                            },
                        },
                        # Used for semi-heated zone
                        {
                            "id": "hvac_1_5",
                            "heating_system": {
                                "id": "hsys_1_5_1",
                                "design_capacity": POWER_THRESHOLD_100 + POWER_DELTA,
                            },
                        },
                        # Used for neither directly nor semi-heated zone
                        {
                            "id": "hvac_1_6",
                            "heating_system": {
                                "id": "hsys_1_5_1",
                                "design_capacity": min(
                                    POWER_THRESHOLD_100, SYSTEM_MIN_HEATING_OUTPUT
                                )
                                - POWER_DELTA,
                            },
                        },
                        # Used for neither directly nor semi-heated zone
                        {
                            "id": "hvac_1_6",
                            "heating_system": {
                                "id": "hsys_1_5_1",
                                "design_capacity": min(
                                    POWER_THRESHOLD_100, SYSTEM_MIN_HEATING_OUTPUT
                                )
                                - POWER_DELTA,
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
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_2_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_2",
                                }
                            ],
                        },
                        # hvac_1_3 => semiheated_zone
                        # zone has Atrium space => indirectly_conditioned_zone
                        # zone has no space with a residential lighting_space_type
                        #   AND a space does have a lighting_space_type specified
                        #   => zone_has_nonresidential_spaces
                        # indirectly_conditioned_zone
                        #   AND _has_nonresidential_spaces
                        #   AND NOT zone_has_residential_spaces
                        #   => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
                        {
                            "id": "zone_1_3",
                            "spaces": [
                                {
                                    "id": "space_1_3_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "ATRIUM_HIGH",
                                    "occupant_multiplier_schedule": "om_sched_1",
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
                        # hvac_1_4 => semiheated_zone
                        # More strongly thermally connected to directly conditioned zones
                        #   => indirectly_conditioned_zone
                        # building_segment_is_residential
                        # zone has no spaces with specified lighting_space_type
                        #   AND building_segment_is_residential
                        #   => zone_has_residential_spaces
                        # NOT zone_has_nonresidential_spaces
                        #   AND zone_has_residential_spaces
                        #   => zone_conditioning_category is "CONDITIONED RESIDENTIAL"
                        {
                            "id": "zone_1_4",
                            "spaces": [
                                {
                                    "id": "space_1_4_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_4_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_3",  # semi-heated
                                    "area": 10,  # m2
                                    "construction": "const_1_4_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_4_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_1_4_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "construction": "const_1_4_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_4_2_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Omits `u_factor`, `f_factor`, `c_factor` to test if `except Exception as e:` works as expected (for branch coverage)
                                {
                                    "id": "surface_1_4_3",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "construction": "const_1_4_3",
                                },
                            ],
                            "terminals": [
                                {
                                    "id": "terminal_1_4_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_4",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                        # hvac_1_5 => semiheated_zone
                        # NOT zone_directly_conditioned_ua > zone_other_ua
                        #   => NOT indirectly_conditioned_zone
                        # NOT directly_conditioned_zone
                        #   AND NOT indirectly_conditioned_zone
                        #   AND semiheated_zone
                        #   => zone_conditioning_category is "SEMI-HEATED"
                        {
                            "id": "zone_1_5",
                            "spaces": [
                                {
                                    "id": "space_1_5_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_1_5_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "construction": "const_1_5_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_4",  # semi-heated
                                    "area": 10,  # m2
                                    "construction": "const_1_5_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_5_2_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_5_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_5",
                                }
                            ],
                        },
                        # hvac_1_6 => neither directly nor semi-heated zone
                        # NOT directly_conditioned_ua > other_ua
                        #   => NOT indirectly_conditioned_zone
                        # building_segment_is_residential
                        # zone has PARKING_AREA_INTERIOR space
                        #   => zone_conditioning_category is UNENCLOSED
                        {
                            "id": "zone_1_6",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_6_1",
                                    "floor_area": 100,  # m2
                                    "lighting_space_type": "PARKING_AREA_INTERIOR",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_1_6_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_4",  # semi-heated
                                    "area": 10,  # m2
                                    "construction": "const_1_6_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_6_1_1",
                                            "glazed_area": 10,
                                            "opaque_area": 0,  # m2
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_6_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "construction": "const_1_6_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_6_2_1",
                                            "glazed_area": 0,  # m2
                                            "opaque_area": 10,
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "terminals": [
                                {
                                    "id": "terminal_1_6_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "hvac_1_6",
                                }
                            ],
                        },
                        # No terminals => neither directly nor semi-heated zone
                        # NOT directly_conditioned_ua > other_ua
                        #   => NOT indirectly_conditioned_zone
                        # zone volume / zone area < CRAWLSPACE_HEIGHT_THRESHOLD
                        #   AND a FLOOR is adjacent_to GROUND
                        #   => zone_conditioning_category is UNENCLOSED
                        {
                            "id": "zone_1_7",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_7_1",
                                    "floor_area": 80,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_1_7_1",
                                    "adjacent_to": "GROUND",
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "construction": "const_1_7_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_7_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.1,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 180,  # FLOOR
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_7_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_4",  # semi-heated
                                    "area": 10,  # m2
                                    "construction": "const_1_7_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_7_2_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 90,  # WALL
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "volume": 20,  # m3
                        },
                        # No terminals => neither directly nor semi-heated zone
                        # NOT directly_conditioned_ua > other_ua
                        #   => NOT indirectly_conditioned_zone
                        # zone has EXTERIOR CEILING
                        #   => zone_conditioning_category is UNENCLOSED
                        {
                            "id": "zone_1_8",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_8_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_1_8_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_4",  # semi-heated
                                    "area": 10,  # m2
                                    "construction": "const_1_8_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_8_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 0,  # ROOF
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_8_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "construction": "const_1_8_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_8_2_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 90,  # WALL
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "volume": 1000,  # m3
                        },
                        # No terminals => neither directly nor semi-heated zone
                        # NOT directly_conditioned_ua > other_ua
                        #   => NOT indirectly_conditioned_zone
                        # zone has no interior parking, crawlspace, or attic
                        #   => zone_conditioning_category is "UNCONDITIONED"
                        {
                            "id": "zone_1_9",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_9_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_1_9_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_1_4",  # semi-heated
                                    "area": 10,  # m2
                                    "construction": "const_1_9_1",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_9_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 90,  # WALL
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_9_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "construction": "const_1_9_2",
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_9_2_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 90,  # WALL
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "volume": 1000,  # m3
                        },
                    ],
                },
                # lighting_building_area_type is specified but not one of the
                # residential types => building_segment_is_nonresidential
                {
                    "id": "bldg_seg_2",
                    "lighting_building_area_type": "FIRE_STATION",
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
                    ],
                    "zones": [
                        # hvac_2_1 => directly_conditioned_zone
                        # zone only has non-residential spaces
                        #   => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
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
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_2_1_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_2",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_1_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
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
                    ],
                },
                # lighting_building_area_type is not specified
                #   => building_segment is neither residential nor nonresidential
                {
                    "id": "bldg_seg_3",
                    "heating_ventilating_air_conditioning_systems": [
                        # User for directly conditioned zones
                        {
                            "id": "hvac_3_1",
                            "heating_system": {
                                "id": "hsys_3_1_1",
                                "design_capacity": SYSTEM_MIN_HEATING_OUTPUT
                                - POWER_DELTA,
                            },
                            "cooling_system": {
                                "id": "csys_3_1_1",
                                "design_sensible_cool_capacity": POWER_THRESHOLD_100
                                + POWER_DELTA,
                            },
                        },
                    ],
                    "zones": [
                        # hvac_3_1 => directly_conditioned_zone
                        # zone only has non-residential spaces
                        #   => zone_conditioning_category is "CONDITIONED NON-RESIDENTIAL"
                        {
                            "id": "zone_3_1",
                            "spaces": [
                                {
                                    "id": "space_3_1_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_1_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_2",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_1_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 90,  # wall
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
                    ],
                },
            ],
        }
    ],
    "constructions": [
        {
            "id": "const_1_4_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_4_2",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_4_3",
        },
        {
            "id": "const_1_5_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_5_2",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_6_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_6_2",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_7_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_7_2",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_8_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_8_2",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_9_1",
            "u_factor": 0.1,  # W/(m2 * K)
        },
        {
            "id": "const_1_9_2",
            "u_factor": 0.1,  # W/(m2 * K)
        },
    ],
    "type": "BASELINE_0",
}

TEST_RPD_12 = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMD],
    "metadata": {
        "schema_author": "ASHRAE SPC 229 Schema Working Group",
        "schema_name": "Ruleset Evaluation Schema",
        "schema_version": "0.1.3",
        "author": "author_example",
        "description": "description_example",
        "time_of_creation": "2024-02-12T09:00Z",
    },
}
TEST_RMD = quantify_rmd(TEST_RPD_12)["ruleset_model_descriptions"][0]
TEST_BUILDING = TEST_RMD["buildings"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_12)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zone_conditioning_category_dict():
    assert get_zone_conditioning_category_dict(
        CLIMATE_ZONE,
        TEST_BUILDING,
        constructions=find_all("$.constructions[*]", TEST_RMD),
    ) == {
        "zone_1_1": "CONDITIONED MIXED",
        "zone_1_2": "CONDITIONED NON-RESIDENTIAL",
        "zone_1_3": "CONDITIONED NON-RESIDENTIAL",
        "zone_1_4": "CONDITIONED RESIDENTIAL",
        "zone_1_5": "SEMI-HEATED",
        "zone_1_6": "UNENCLOSED",
        "zone_1_7": "UNENCLOSED",
        "zone_1_8": "UNENCLOSED",
        "zone_1_9": "UNCONDITIONED",
        "zone_2_1": "CONDITIONED NON-RESIDENTIAL",
        "zone_3_1": "CONDITIONED NON-RESIDENTIAL",
    }
