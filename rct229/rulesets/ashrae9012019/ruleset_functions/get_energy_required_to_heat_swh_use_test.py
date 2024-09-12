from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rmd
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "zones": [
                        {
                            "id": "Thermal Zone 1",
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "service_water_heating_uses": [
                                        {
                                            "id": "SWH Use 1",
                                            "use": 100,
                                            "use_units": "POWER_PER_PERSON",
                                            "is_heat_recovered_by_drain": True,
                                            "served_by_distribution_system": "SWH Distribution 1",
                                            "use_multiplier_schedule": "SWH Schedule 1",
                                        },
                                        {
                                            "id": "SWH Use 2",
                                            "use": 100,
                                            "use_units": "POWER_PER_AREA",
                                            "served_by_distribution_system": "SWH Distribution 1",
                                            "use_multiplier_schedule": "SWH Schedule 1",
                                        },
                                    ],
                                    "number_of_occupants": 5,
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 2",
                                    "number_of_occupants": 5,
                                    "floor_area": 100,
                                },
                                {
                                    "id": "Space 3",
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "Building Segment 2",
                    "zones": [
                        {
                            "id": "Thermal Zone 2",
                            "spaces": [
                                {
                                    "id": "Space 3",
                                    "service_water_heating_uses": [
                                        {
                                            "id": "SWH Use 2",
                                            "served_by_distribution_system": "SWH Distribution 1",
                                            "use_multiplier_schedule": "SWH Schedule 1",
                                        }
                                    ],
                                },
                                {
                                    "id": "Space 4",
                                    "service_water_heating_uses": [
                                        {
                                            "id": "SWH Use 2",
                                            "served_by_distribution_system": "SWH Distribution 1",
                                        }
                                    ],
                                },
                            ],
                        }
                    ],
                },
            ],
        }
    ],
    "schedules": [
        {
            "id": "SWH Schedule 1",
            "hourly_values": [0.8] * 8760,
        },
        {
            "id": "SWH Entering Water Temp Schedule 1",
            "hourly_values": [50] * 8760,
        },
    ],
    "service_water_heating_distribution_systems": [
        {
            "id": "SWH Distribution 1",
            "design_supply_temperature": 60,
            "drain_heat_recovery_efficiency": 0.3,
            "entering_water_mains_temperature_schedule": "SWH Entering Water Temp Schedule 1",
            "tanks": [
                {
                    "id": "Tank 1",
                },
                {
                    "id": "Tank 2",
                },
            ],
            "service_water_piping": [
                {
                    "id": "SWH Piping 1",
                    "child": [
                        {
                            "id": "SWH Piping Child 1",
                            "child": [
                                {
                                    "id": "SWH Piping 1-a",
                                },
                                {
                                    "id": "SWH Piping 1-b",
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "SWH Piping 2",
                },
            ],
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
    "data_timestamp": "2024-02-12T09:00Z",
}

# TEST_SWH_USE_POWER_PER_PERSON = {
#     "service_water_heating_uses": [
#         {
#             "id": "SWH Use 1",
#             "use": 100,
#             "use_units": "POWER_PER_PERSON",
#             "is_heat_recovered_by_drain": 0.3,
#             "served_by_distribution_system": "SWH Distribution 1",
#             "use_multiplier_schedule": "SWH Schedule 1",
#         }
#     ]
# }

TEST_SWH_USE_POWER_PER_AREA = {
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 100,
            "use_units": "POWER_PER_AREA",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        }
    ]
}

TEST_SWH_USE_POWER = {
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 100,
            "use_units": "POWER",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        }
    ]
}

TEST_SWH_USE_VOLUME_PER_PERSON = {
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 100,
            "use_units": "VOLUME_PER_PERSON",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        }
    ]
}

TEST_SWH_USE_VOLUME_PER_AREA = {
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 100,
            "use_units": "VOLUME_PER_AREA",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        }
    ]
}

TEST_SWH_USE_VOLUME = {
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 100,
            "use_units": "VOLUME",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        }
    ]
}

TEST_SWH_USE_OTHER = {
    "service_water_heating_uses": [
        {
            "id": "SWH Use 1",
            "use": 100,
            "use_units": "OTHER",
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        }
    ]
}

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]

TEST_BUILDING_SEGMENT = find_exactly_one_with_field_value(
    "$.buildings[*].building_segments[*]",
    "id",
    "Building Segment 1",
    TEST_RMD,
)

TEST_BUILDING_SEGMENT_NO_SWH_USE = find_exactly_one_with_field_value(
    "$.buildings[*].building_segments[*]",
    "id",
    "Building Segment 2",
    TEST_RMD,
)

TEST_SWH_USE_POWER_PER_PERSON = find_exactly_one_with_field_value(
    "$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
    "id",
    "SWH Use 1",
    TEST_RMD,
)


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rmd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test_SWH_USE_POWER_PER_PERSON():
    res = get_energy_required_to_heat_swh_use(
        TEST_SWH_USE_POWER_PER_PERSON, TEST_RMD, TEST_BUILDING_SEGMENT
    )
    assert 0 == 0
    # assert get_energy_required_to_heat_swh_use(TEST_SWH_USE_POWER_PER_PERSON, TEST_BUILDING_SEGMENT, TEST_RPD_FULL) == {"Space 1": 100}
