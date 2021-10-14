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

CLIMATE_ZONE = "CZ0A"
CAPACITY_DELTA = 1
system_min_heating_output_quantity = table_3_2_lookup(CLIMATE_ZONE)[
    "system_min_heating_output"
]

# Convert pint quantities to match schema units
SYSTEM_MIN_HEATING_OUTPUT = system_min_heating_output_quantity.to("W/m2").magnitude
CAPACITY_THRESHOLD = CAPACITY_THRESHOLD_QUANTITY.to("W/m2").magnitude
CRAWLSPACE_HEIGHT_THRESHOLD = CRAWLSPACE_HEIGHT_THRESHOLD_QUANTITY.to("m").magnitude

# This single RMR is intended to include all the cases handled by get_zone_conditioning_category_dict()
TEST_RMR = {
    "id": "test_rmr",
    "buildings": [
        {
            "id": "1",
            "building_segments": [
                # Residential
                {
                    "lighting_building_area_type": "DORMITORY",
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_1",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT - CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD + CAPACITY_DELTA
                            ],
                            "zones_served": ["1", "2"],
                        }
                    ],
                    "zones": [
                        # Both directly conditioned
                        {
                            "id": "1",
                            "spaces": [
                                {
                                    # Residential
                                    "id": "space_1",
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                        {
                            "id": "2",
                            "spaces": [
                                {
                                    # Non-residential
                                    "id": "space_2",
                                    "lighting_space_type": "COMPUTER_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                        {
                            "id": "8",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_3",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                    ],
                },
                # Non-residential
                {
                    "lighting_building_area_type": "LIBRARY",
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_2",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                            "zones_served": ["3", "4"],
                        }
                    ],
                    "zones": [
                        # Both indirectly conditioned
                        {
                            "id": "3",
                            "spaces": [
                                # Residential
                                {
                                    "id": "space_4",
                                    "lighting_space_type": "GUEST_ROOM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                        {
                            "id": "4",
                            "spaces": [
                                # Non-residential
                                {
                                    "id": "space_5",
                                    "lighting_space_type": "BANKING_ACTIVITY_AREA",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                        {
                            "id": "9",
                            "spaces": [
                                # Non-residential
                                {
                                    "id": "space_6",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                    ],
                },
                {
                    "heating_ventilation_air_conditioning_systems": [
                        {
                            "id": "hvac_3",
                            "heat_capacity": [
                                SYSTEM_MIN_HEATING_OUTPUT + CAPACITY_DELTA
                            ],
                            "sensible_cool_capacity": [
                                CAPACITY_THRESHOLD - CAPACITY_DELTA
                            ],
                            "zones_served": ["5", "6"],
                        }
                    ],
                    "zones": [
                        {
                            # Indirectly conditioned
                            "id": "5",
                            "spaces": [
                                {
                                    "id": "space_7",
                                    "lighting_space_type": "ATRIUM_LOW_MEDIUM",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                        {
                            # Indirectly conditioned
                            "id": "6",
                            "spaces": [
                                {
                                    "id": "space_8",
                                    "lighting_space_type": "ATRIUM_HIGH",
                                    "occupant_multiplier_schedule": "om_sched_1",
                                }
                            ],
                            "thermostat_cooling_setpoint_schedule": "tcs_sched_1",
                            "thermostat_heating_setpoint_schedule": "ths_sched_1",
                        },
                    ],
                },
            ],
        }
    ],
}


def test__TEST_RMR__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMR)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


# def test__get_zone_conditioning_category_dict():
#     assert get_zone_conditioning_category_dict(CLIMATE_ZONE, TEST_BUILDING) == {
#         "1": "CONDITIONED RESIDENTIAL",
#         "2": "CONDITIONED RESIDENTIAL",
#         "3": "CONDITIONED RESIDENTIAL",
#         "4": "CONDITIONED RESIDENTIAL",
#         "5": "CONDITIONED RESIDENTIAL",
#         "6": "CONDITIONED RESIDENTIAL",
#     }
