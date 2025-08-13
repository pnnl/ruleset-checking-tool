from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zone_eflh import (
    get_zone_eflh,
)
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import schema_validate_rpd

TEST_RMD = {
    "id": "test_rmd",
    "schedules": [
        {
            "id": "Operation Schedule 1",
            "hourly_values": [1.0] * 8760,
            "hourly_heating_design_day": [1.0] * 24,
            "hourly_cooling_design_day": [1.0] * 24,
        },
        {
            "id": "Operation Schedule 2",
            "hourly_values": [0.0] * 8760,
        },
    ],
    "buildings": [
        {
            "id": "building_1",
            "building_segments": [
                {
                    "id": "building_segment_1",
                    "heating_ventilating_air_conditioning_systems": [
                        {
                            "id": "System 1",
                            "fan_system": {
                                "id": "Fan System 1",
                                "operating_schedule": "Operation Schedule 1",
                            },
                        },
                        {
                            "id": "System 2",
                            "fan_system": {
                                "id": "Fan System 2",
                                "operating_schedule": "Operation Schedule 2",
                            },
                        },
                        {
                            "id": "System 3",
                            "fan_system": {
                                "id": "Fan System 3",
                            },
                        },
                    ],
                    "zones": [
                        {
                            "id": "Zone 1",
                            "terminals": [
                                {
                                    "id": "terminal_1",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                                },
                                {
                                    "id": "terminal_2",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                            ],
                            "spaces": [
                                {
                                    "id": "Space 1",
                                    "occupant_multiplier_schedule": "Operation Schedule 1",
                                    "number_of_occupants": 5,
                                },
                                {
                                    "id": "Space 2",
                                    "occupant_multiplier_schedule": "Operation Schedule 1",
                                    "number_of_occupants": 5,
                                },
                                {
                                    "id": "Space 3",
                                    "number_of_occupants": 5,
                                },
                            ],
                        },
                        {
                            # this case, we miss the operation schedule in spaces
                            # so the occupants are 1.0 constant
                            "id": "Zone 2",
                            "terminals": [
                                {
                                    "id": "terminal_3",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 2",
                                },
                            ],
                            "spaces": [
                                {
                                    "id": "Space 4",
                                    "number_of_occupants": 5,
                                },
                            ],
                        },
                        {
                            # this case, we miss the operation schedule in HVAC
                            # so the HVAC is running constant 1.0
                            "id": "Zone 3",
                            "terminals": [
                                {
                                    "id": "terminal_4",
                                    "served_by_heating_ventilating_air_conditioning_system": "System 3",
                                },
                            ],
                            "spaces": [
                                {
                                    "id": "Space 5",
                                    "number_of_occupants": 5,
                                },
                            ],
                        },
                    ],
                }
            ],
        }
    ],
    "type": "BASELINE_0",
}


TEST_RPD_FULL = {
    "id": "229",
    "ruleset_model_descriptions": [TEST_RMD],
}

TEST_RMD_UNIT = quantify_rmd(TEST_RPD_FULL)["ruleset_model_descriptions"][0]


def test__TEST_RMD_FIXED_TYPE__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RPD_FULL)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


def test__get_zone_eflh_thermal_zone_1__success():
    assert get_zone_eflh(TEST_RMD_UNIT, "Zone 1") == 8760


def test__get_zone_eflh_thermal_zone_2__success():
    assert get_zone_eflh(TEST_RMD_UNIT, "Zone 2") == 0


def test__get_zone_eflh_thermal_zone_3__success():
    assert get_zone_eflh(TEST_RMD_UNIT, "Zone 3") == 8760
