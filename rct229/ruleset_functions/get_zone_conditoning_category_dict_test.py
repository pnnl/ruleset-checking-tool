import pytest
from rct229.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    CAPACITY_THRESHOLD,
    CRAWLSPACE_HEIGHT_THRESHOLD,
    get_zone_conditioning_category_dict,
)

CLIMATE_ZONE = "CZ0A"
SYSTEM_MIN_HEATING_OUTPUT = table_3_2_lookup(CLIMATE_ZONE)["system_min_heating_output"]
TEST_BUILDING = {
    "id": "1",
    "name": "building1",
    "building_segments": [
        # Residential
        {
            "lighting_building_area_type": "DORMITORY",
            "heating_ventilation_air_conditioning_systems": [
                {
                    "simulation_result_heat_capacity": SYSTEM_MIN_HEATING_OUTPUT - 1,
                    "simulation_result_sensible_cool_capacity": CAPACITY_THRESHOLD + 1,
                    "zones_served": ["1", "2"],
                }
            ],
            "thermal_blocks": [
                {
                    "zones": [
                        # Both directly conditioned
                        {
                            "id": "1",
                            "spaces": [
                                {
                                    # Residential
                                    "lighting_space_type": "DORMITORY_LIVING_QUARTERS"
                                }
                            ],
                        },
                        {
                            "id": "2",
                            "spaces": [
                                {
                                    # Non-residential
                                    "lighting_space_type": "COMPUTER_ROOM"
                                }
                            ],
                        },
                        {
                            "id": "8",
                            "spaces": [
                                # Residential
                                {}
                            ],
                        },
                    ]
                }
            ],
        },
        # Non-residential
        {
            "lighting_building_area_type": "LIBRARY",
            "heating_ventilation_air_conditioning_systems": [
                {
                    "simulation_result_heat_capacity": SYSTEM_MIN_HEATING_OUTPUT + 1,
                    "simulation_result_sensible_cool_capacity": CAPACITY_THRESHOLD - 1,
                    "zones_served": ["3", "4"],
                }
            ],
            "thermal_blocks": [
                {
                    "zones": [
                        # Both indirectly conditioned
                        {
                            "id": "3",
                            "spaces": [
                                # Residential
                                {"lighting_space_type": "GUEST_ROOM"}
                            ],
                        },
                        {
                            "id": "4",
                            "spaces": [
                                # Non-residential
                                {"lighting_space_type": "BANKING_ACTIVITY_AREA"}
                            ],
                        },
                        {
                            "id": "9",
                            "spaces": [
                                # Non-residential
                                {}
                            ],
                        },
                    ]
                }
            ],
        },
        {
            "heating_ventilation_air_conditioning_systems": [
                {
                    "simulation_result_heat_capacity": SYSTEM_MIN_HEATING_OUTPUT + 1,
                    "simulation_result_sensible_cool_capacity": CAPACITY_THRESHOLD - 1,
                    "zones_served": ["5", "6"],
                }
            ],
            "thermal_blocks": [
                {
                    "zones": [
                        {
                            # Indirectly conditioned
                            "id": "5",
                            "spaces": [{"lighting_space_type": "ATRIUM_LOW_MEDIUM"}],
                        },
                        {
                            # Indirectly conditioned
                            "id": "6",
                            "spaces": [{"lighting_space_type": "ATRIUM_HIGH"}],
                        },
                        # {
                        #     "id": "7",
                        #     "spaces": [
                        #         {"lighting_space_type": "BANKING_ACTIVITY_AREA"}
                        #     ],
                        #     "surfaces": [
                        #         {"adjacent_to": "INTERIOR", "adjacent_zone_id": "3"}
                        #     ]
                        # },
                    ]
                }
            ],
        },
    ],
}


def test__get_zone_conditioning_category_dict():
    assert get_zone_conditioning_category_dict(CLIMATE_ZONE, TEST_BUILDING) == {
        "1": "CONDITIONED RESIDENTIAL",
        "2": "CONDITIONED RESIDENTIAL",
        "3": "CONDITIONED RESIDENTIAL",
        "4": "CONDITIONED RESIDENTIAL",
        "5": "CONDITIONED RESIDENTIAL",
        "6": "CONDITIONED RESIDENTIAL",
    }
