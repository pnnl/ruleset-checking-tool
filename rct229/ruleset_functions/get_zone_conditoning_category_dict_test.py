import pytest
from rct229.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    CAPACITY_THRESHOLD as CAPACITY_THRESHOLD_QUANTITY,
)
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    CRAWLSPACE_HEIGHT_THRESHOLD as CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY,
)
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.schema.config import ureg
from rct229.schema.validate import schema_validate_rmr
from rct229.schema.schema_utils import quantify_rmr

CLIMATE_ZONE = "CZ0A"
CAPACITY_DELTA = 1
SYSTEM_MIN_HEATING_OUTPUT_QUANTITY = table_3_2_lookup(CLIMATE_ZONE)[
    "system_min_heating_output"
]

# Convert pint quantities to match schema units
SYSTEM_MIN_HEATING_OUTPUT = SYSTEM_MIN_HEATING_OUTPUT_QUANTITY.to("W/m2").magnitude
CAPACITY_THRESHOLD = CAPACITY_THRESHOLD_QUANTITY.to("W/m2").magnitude
CRAWLSPACE_HEIGHT_THRESHOLD = CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY.to("m").magnitude

# This single RMR is intended to include all the cases handled by get_zone_conditioning_category_dict()
TEST_RMR = {
    "id": "test_rmr",
    "buildings": [
        {
            "id": "bldg_1",
            "building_open_schedule": "bldg_open_sched_1",
            "building_segments": [
                # lighting_building_area_type is one of the residential types
                # => building_segment_is _residential
                {
                    "id": "bdg_seg_1",
                    "lighting_building_area_type": "DORMITORY",
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_1_1",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT - CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD + CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_1_2",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_1_3",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_1_4",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT - CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                    ],
                    "zones": [
                        # hvac_1_1 => directly_conditioned_zone
                        # zone has a space with lighting_space_type one of the residential
                        #   types => zone_has_residential_spaces
                        # zone has no residential spaces but a space has a lighting_space_type
                        #   => zone_has_nonesidential_spaces
                        # zone zone_has_residential_spaces and zone_has_nonesidential_spaces
                        #  => zome_conditioning_category is "CONDITIONED MIXED"
                        {
                            "id": "zone_1_1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_1_1_1",
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                                {
                                    # Non-residential
                                    "id": "space_1_1_2",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_1"
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
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_2"
                            ],
                        },
                        # hvac_1_3 => semiheated_zone
                        # zone has no residential or non-residential spaces and
                        # building_segment_is_residential => zome_has_residential_spaces
                        {
                            "id": "zone_1_3",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_3_1",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_3"
                            ],
                        },
                        # hvac_1_4 => neither directly nor semi-heated zone
                        # Atrium => indirectly_conditioned_zone
                        {
                            "id": "zone_1_4",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_4_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_4"
                            ],
                        },
                        # hvac_1_4 => neither directly nor semi-heated zone
                        # Not directly_conditioned_ua > other_ua => Not indirectly conditioned
                        {
                            "id": "zone_1_5",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_5_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
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
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_4"
                            ],
                        },
                        # hvac_1_4 => neither directly nor semi-heated zone
                        # directly_conditioned_ua > other_ua => indirectly conditioned
                        {
                            "id": "zone_1_5",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_1_5_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
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
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_1_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_1_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_1_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_4"
                            ],
                        },
                    ],
                },
                # lighting_building_area_type is specified but not one of the
                # residential types => building_segment_is_nonresidential
                {
                    "id": "bdg_seg_2",
                    "lighting_building_area_type": "FIRE_STATION",
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_2_1",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT - CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD + CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_2_2",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_2_3",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_2_4",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT - CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                    ],
                    "zones": [
                        # hvac_1_1 => directly_conditioned_zone
                        # zone only has residential spaces => zone_conditioning_category
                        #   is "CONDITIONED RESIDENTIAL"
                        {
                            "id": "zone_2_1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_2_1_1",
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_1"
                            ],
                        },
                        # hvac_1_2 => directly_conditioned_zone
                        {
                            "id": "zone_2_2",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_2_2_1",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_2"
                            ],
                        },
                        # hvac_1_3 => semiheated_zone
                        # zone has no residential or non-residential spaces and
                        # building_segment_is_nonresidential => zome_has_nonresidential_spaces
                        {
                            "id": "zone_2_3",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_2_3_1",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_2_3"
                            ],
                        },
                        # hvac_1_4 => neither directly nor semi-heated zone
                        # Atrium => indirectly_conditioned_zone
                        {
                            "id": "zone_2_4",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_2_4_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_2_4"
                            ],
                        },
                        # hvac_1_4 => neither directly nor semi-heated zone
                        # Not directly_conditioned_ua > other_ua => Not indirectly conditioned
                        {
                            "id": "zone_2_5",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_2_5_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_2_5_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_2_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_2_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_2_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_2_4"
                            ],
                        },
                        # hvac_1_4 => neither directly nor semi-heated zone
                        # directly_conditioned_ua > other_ua => indirectly conditioned
                        {
                            "id": "zone_2_5",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_2_5_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_2_5_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_2_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_2_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_2_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_2_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_1_4"
                            ],
                        },
                    ],
                },
                # lighting_building_area_type is not specified
                #   => building_segment is neither residential nor nonresidential
                {
                    "id": "bdg_seg_3",
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_3_1",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT - CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD + CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_3_2",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_3_3",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                        {
                            "id": "hvac_3_4",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT - CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                        },
                    ],
                    "zones": [
                        # hvac_1_1 => directly_conditioned_zone
                        {
                            "id": "zone_3_1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_3_1_1",
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_1"
                            ],
                        },
                        # hvac_1_2 => directly_conditioned_zone
                        {
                            "id": "zone_3_2",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_3_2_1",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_2"
                            ],
                        },
                        # hvac_1_3 => semiheated_zone
                        # zone has no residential or non-residential spaces and
                        #   building segment is neither residential nor nonresidential
                        #   => zone_has_nonresidential_spaces
                        # zone semi-heated => zone_conditioning_category is "SEMI-HEATED"
                        {
                            "id": "zone_3_3",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_3_3_1",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_3"
                            ],
                        },
                        # hvac_1_4 => neither directly nor semi-heated zone
                        # Atrium => indirectly_conditioned_zone
                        {
                            "id": "zone_3_4",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_3_4_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_4"
                            ],
                        },
                        # hvac_3_4 => neither directly nor semi-heated zone
                        # Not directly_conditioned_ua > other_ua => Not indirectly conditioned
                        # zone not directly or indirectly conditione or semi-heated and
                        #   has a space with a lighting_space_type of "PARKING_AREA_INTERIOR"
                        #   => zone_conditioning_category is "UNENCLOSED"
                        {
                            "id": "zone_3_5",
                            "spaces": [
                                {
                                    "id": "space_3_5_1",
                                    "lighting_space_type": "PARKING_AREA_INTERIOR",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_3_5_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_3_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_3_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_4"
                            ],
                        },
                        # hvac_3_4 => neither directly nor semi-heated zone
                        # directly_conditioned_ua > other_ua => indirectly conditioned
                        {
                            "id": "zone_3_5",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_3_5_1",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_3_5_1",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_3_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_3_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_4"
                            ],
                        },
                        # hvac_3_4 => neither directly nor semi-heated zone
                        # Not directly_conditioned_ua > other_ua => Not indirectly conditioned
                        # zone not directly or indirectly conditioned or semi-heated
                        #   and has no interior parking spaces
                        #   and zone volumen / total space flooor area < CRAWLSPACE_HEIGHT_THRESHOLD
                        #   and it has a surface that is a floor adjacen to the ground
                        #   => zone_conditioning_category is "UNENCLOSED"
                        {
                            "id": "zone_3_6",
                            "spaces": [
                                {
                                    "id": "space_3_5_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_3_5_1",
                                    "adjacent_to": "GROUND",
                                    "adjacent_zone": "zone_3_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 180,  # degrees
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_3_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_4"
                            ],
                            "volume": 330,  # m3
                        },
                        # hvac_3_4 => neither directly nor semi-heated zone
                        # Not directly_conditioned_ua > other_ua => Not indirectly conditioned
                        # zone not directly or indirectly conditioned or semi-heated
                        #   and has no interior parking spaces
                        #   and is not an crawlspace
                        #   and it has a surface that is a ceiling adjacent to EXTERIOR
                        #   => zone_conditioning_category is "UNENCLOSED"
                        {
                            "id": "zone_3_6",
                            "spaces": [
                                {
                                    "id": "space_3_5_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_3_5_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_3_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 0,  # degrees, a ceiling
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_3_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_4"
                            ],
                            "volume": 330,  # m3
                        },
                        # hvac_3_4 => neither directly nor semi-heated zone
                        # Not directly_conditioned_ua > other_ua => Not indirectly conditioned
                        # zone not directly or indirectly conditioned or semi-heated
                        #   and has no interior parking spaces
                        #   and is not an crawlspace
                        #   and is not an attic
                        #   => zone_conditioning_category is "UNCONDITIONED"
                        {
                            "id": "zone_3_6",
                            "spaces": [
                                {
                                    "id": "space_3_5_1",
                                    "floor_area": 100,  # m2
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "surfaces": [
                                # Adds to zone_directly_conditioned_ua
                                {
                                    "id": "surface_3_5_1",
                                    "adjacent_to": "EXTERIOR",
                                    "adjacent_zone": "zone_3_1",  # directly conditioned
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 0,
                                            "opaque_area": 10,  # m2
                                            "u_factor": 0.5,  # W/(m2 * K)
                                        }
                                    ],
                                    "tilt": 0,  # degrees, a ceiling
                                },
                                # Adds to zone_other_ua
                                {
                                    "id": "surface_3_5_2",
                                    "adjacent_to": "INTERIOR",
                                    "adjacent_zone": "zone_3_4",  # semi-heated
                                    "area": 10,  # m2
                                    "subsurfaces": [
                                        {
                                            "id": "subsurface_3_5_1_1",
                                            "glazed_area": 10,  # m2
                                            "opaque_area": 0,
                                            "u_factor": 3,  # W/(m2 * K)
                                        }
                                    ],
                                },
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                            "served_by_heating_ventilation_air_conditioning_systems": [
                                "hvac_3_4"
                            ],
                            "volume": 330,  # m3
                        },
                    ],
                },
            ],
        }
    ],
}

TEST_BUILDING = quantify_rmr(TEST_RMR)["buildings"][0]


def test__TEST_RMR__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMR)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zone_conditioning_category_dict():
    assert get_zone_conditioning_category_dict(CLIMATE_ZONE, TEST_BUILDING) == {
        "1": "CONDITIONED RESIDENTIAL",
        "2": "CONDITIONED RESIDENTIAL",
        "3": "CONDITIONED RESIDENTIAL",
        "4": "CONDITIONED RESIDENTIAL",
        "5": "CONDITIONED RESIDENTIAL",
        "6": "CONDITIONED RESIDENTIAL",
    }
