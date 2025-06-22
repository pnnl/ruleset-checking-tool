from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "buildings": [
        {
            "id": "Building 1",
            "building_open_schedule": "Required Building Schedule 1",
            "building_segments": [
                {
                    "id": "Building Segment 1",
                    "service_water_heating_area_type": "LIBRARY",
                },
                {
                    "id": "Building Segment 2",
                    "zones": [
                        {
                            "id": "Zone 2",
                            "spaces": [
                                {
                                    "id": "Space 2_1",
                                    "service_water_heating_uses": [
                                        "service water heating uses 2_1",
                                    ],
                                },
                                {
                                    "id": "Space 2_2",
                                    "service_water_heating_uses": [
                                        "service water heating uses 2_2"
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "Building Segment 3",
                    "zones": [
                        {
                            "id": "Zone 3",
                            "spaces": [
                                {
                                    "id": "Space 3_1",
                                    "service_water_heating_uses": [
                                        "service water heating uses 3_1"
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "Building Segment 4",
                    "zones": [
                        {
                            "id": "Zone 4",
                            "spaces": [
                                {
                                    "id": "Space 4_1",
                                    "service_water_heating_area_type": "MUSEUM",
                                    "service_water_heating_uses": [
                                        "service water heating uses 4_1",
                                    ],
                                },
                                {
                                    "id": "Space 4_2",
                                    "service_water_heating_uses": [
                                        "service water heating uses 4_2",
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": "Building Segment 5",
                    "zones": [
                        {
                            "id": "Zone 5",
                            "spaces": [
                                {
                                    "id": "Space 5_1",
                                    "service_water_heating_area_type": "HOTEL",
                                    "service_water_heating_uses": [
                                        "service water heating uses 5_1",
                                    ],
                                },
                                {
                                    "id": "Space 5_2",
                                    "service_water_heating_area_type": "CONVENIENCE_STORE",
                                    "service_water_heating_uses": [
                                        "service water heating uses 5_2"
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
    "service_water_heating_uses": [
        {
            "id": "service water heating uses 5_1",
            "use": 400,
            "use_units": "POWER",
            "is_heat_recovered_by_drain": True,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "service water heating uses 2_1",
            "use": 10,
            "use_units": "VOLUME_PER_PERSON",
            "area_type": "OFFICE",
            "is_heat_recovered_by_drain": True,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "service water heating uses 2_2",
            "use": 100,
            "use_units": "POWER",
            "area_type": "CONVENIENCE_STORE",
            "is_heat_recovered_by_drain": True,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "service water heating uses 4_1",
            "use": 100,
            "use_units": "VOLUME_PER_PERSON",
            "is_heat_recovered_by_drain": True,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "service water heating uses 5_2",
            "use": 300,
            "use_units": "POWER",
            "is_heat_recovered_by_drain": True,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
        },
        {
            "id": "service water heating uses 3_1",
            "use": 5,
            "use_units": "OTHER",
            "served_by_distribution_system": "SWH Distribution 1",
        },
        {
            "id": "service water heating uses 4_2",
            "use": 300,
            "use_units": "POWER",
            "is_heat_recovered_by_drain": True,
            "served_by_distribution_system": "SWH Distribution 1",
            "use_multiplier_schedule": "SWH Schedule 1",
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
            "service_water_piping": {
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
        }
    ],
    "type": "BASELINE_0",
}

TEST_RPD_FULL = {
    "id": "229",
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

TEST_RMD = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__TEST_RPD__bldg_segment_swh_bat():
    assert get_building_segment_swh_bat(TEST_RMD, "Building Segment 1") == "LIBRARY"


def test__TEST_RPD__area_type():
    assert (
        get_building_segment_swh_bat(TEST_RMD, "Building Segment 2")
        == "CONVENIENCE_STORE"
    )


def test__TEST_RPD__other_use_unit():
    assert (
        get_building_segment_swh_bat(TEST_RMD, "Building Segment 3") == "UNDETERMINED"
    )


def test__TEST_RPD__two_spaces_one_undetermined():
    assert (
        get_building_segment_swh_bat(TEST_RMD, "Building Segment 4") == "UNDETERMINED"
    )


def test__TEST_RPD__two_spaces_none_undetermined():
    assert get_building_segment_swh_bat(TEST_RMD, "Building Segment 5") == "HOTEL"
