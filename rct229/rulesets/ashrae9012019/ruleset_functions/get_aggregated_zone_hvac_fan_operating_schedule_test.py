import pytest
from rct229.rulesets.ashrae9012019.ruleset_functions.get_aggregated_zone_hvac_fan_operating_schedule import (
    get_aggregated_zone_hvac_fan_operating_schedule,
)
from rct229.schema.validate import schema_validate_rmr
from rct229.utils.assertions import RCTFailureException

TEST_RMI = {
    "id": "test_rmi",
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "zones": [
                        {
                            "id": "zone 1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                            ],
                        },
                        {
                            "id": "zone 2",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 3",
                                },
                                {
                                    "id": "terminal_3",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 4",
                                },
                            ],
                        },
                    ],
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 1",
                            "fan_system": {
                                "id": "Fan System 1",
                            },
                        },
                        {
                            "id": "System 2",
                            "fan_system": {
                                "id": "Fan System 2",
                                "operating_schedule": "schedule 2",
                            },
                        },
                        {
                            "id": "System 3",
                            "fan_system": {
                                "id": "Fan System 3",
                                "operating_schedule": "schedule 3",
                            },
                        },
                        {
                            "id": "System 4",
                            "fan_system": {
                                "id": "Fan System 4",
                                "operating_schedule": "schedule 4",
                            },
                        },
                    ],
                }
            ],
        }
    ],
    "schedules": [
        {"id": "schedule 2", "hourly_values": [0] * 8760},
        {"id": "schedule 3", "hourly_values": [1.0] * 8760},
        {"id": "schedule 4", "hourly_values": [0.5] * 8760},
    ],
    "type": "BASELINE_0",
}

TEST_RMD = {
    "id": "229_01",
    "ruleset_model_descriptions": [TEST_RMI],
    "data_timestamp": "2024-02-12T09:00Z",
}


def test__TEST_RMD_FIXED_TYPE__is_valid():
    schema_validation_result = schema_validate_rmr(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_aggregated_zone_hvac_fan_operating_schedule__no_operating_schedule():
    assert (
        get_aggregated_zone_hvac_fan_operating_schedule(TEST_RMI, "zone 1")
        == [1] * 8760
    )


def test__get_aggregated_zone_hvac_fan_operating_schedule__correct_mapping():
    assert (
        get_aggregated_zone_hvac_fan_operating_schedule(TEST_RMI, "zone 2")
        == [0] * 8760
    )


def test__get_aggregated_zone_hvac_fan_operating_schedule__assertion():
    with pytest.raises(
        RCTFailureException,
        match="Please make sure the provided ZONE 'zone_id' is connected with at least one HVAC system",
    ):
        get_aggregated_zone_hvac_fan_operating_schedule(TEST_RMI, "zone_not_exist")
